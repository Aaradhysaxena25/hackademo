"""
Views for the chat app.

Handles conversations and message sending with RAG pipeline.
"""

import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.services.llm_provider import get_llm_provider
from apps.ai.services.rag_pipeline import RAGPipeline
from apps.repositories.models import Repository

from .models import Conversation, Message
from .serializers import (
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
    SendMessageSerializer,
)

logger = logging.getLogger(__name__)


class ConversationListView(APIView):
    """
    GET  /api/v1/chat/conversations/         — List conversations
    POST /api/v1/chat/conversations/         — Create conversation
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Conversation.objects.filter(
            user=request.user, is_archived=False
        ).select_related("repository")

        # Filter by repository
        repo_id = request.query_params.get("repository_id")
        if repo_id:
            queryset = queryset.filter(repository_id=repo_id)

        serializer = ConversationListSerializer(queryset[:50], many=True)
        return Response(
            {"status": "success", "data": serializer.data}
        )

    def post(self, request):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo_id = serializer.validated_data["repository_id"]

        # Verify user owns the repository
        repo = get_object_or_404(Repository, id=repo_id, owner=request.user)

        conversation = Conversation.objects.create(
            user=request.user,
            repository=repo,
            title=serializer.validated_data.get("title") or "New Conversation",
        )

        return Response(
            {
                "status": "success",
                "data": ConversationDetailSerializer(conversation).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ConversationDetailView(APIView):
    """
    GET    /api/v1/chat/conversations/{id}/  — Get conversation with messages
    DELETE /api/v1/chat/conversations/{id}/  — Delete/archive conversation
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        conversation = get_object_or_404(
            Conversation, pk=pk, user=request.user
        )
        serializer = ConversationDetailSerializer(conversation)
        return Response({"status": "success", "data": serializer.data})

    def delete(self, request, pk):
        conversation = get_object_or_404(
            Conversation, pk=pk, user=request.user
        )
        conversation.is_archived = True
        conversation.save(update_fields=["is_archived", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendMessageView(APIView):
    """
    POST /api/v1/chat/conversations/{id}/messages/  — Send a message

    Triggers the RAG pipeline: retrieves relevant code → generates AI response.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        conversation = get_object_or_404(
            Conversation, pk=pk, user=request.user
        )

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_content = serializer.validated_data["content"]

        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_content,
        )

        # Get conversation history for context
        history_messages = Message.objects.filter(
            conversation=conversation
        ).exclude(id=user_message.id).order_by("-created_at")[:6]

        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(list(history_messages))
        ]

        # Run RAG pipeline
        try:
            # Use mock provider if no API key configured
            from django.conf import settings
            if settings.OPENAI_API_KEY:
                provider = get_llm_provider("openai")
            else:
                provider = get_llm_provider("mock", response=self._generate_mock_response(user_content, conversation))

            pipeline = RAGPipeline(llm_provider=provider)

            repository_name = conversation.repository.name if conversation.repository else ""
            repository_id = str(conversation.repository_id) if conversation.repository_id else ""

            rag_response = pipeline.generate_response(
                query=user_content,
                repository_id=repository_id,
                conversation_history=conversation_history,
                repository_name=repository_name,
            )

            # Save assistant message
            assistant_message = Message.objects.create(
                conversation=conversation,
                role="assistant",
                content=rag_response.content,
                context_chunks=rag_response.sources,
                token_count=rag_response.token_count,
                model_used=rag_response.model_used,
            )

            # Update conversation title if it's the first message
            if conversation.title == "New Conversation" and user_content:
                conversation.title = user_content[:50]
                conversation.save(update_fields=["title", "updated_at"])

        except Exception as e:
            logger.error(f"RAG pipeline error: {e}")
            assistant_message = Message.objects.create(
                conversation=conversation,
                role="assistant",
                content="I'm sorry, I encountered an error while processing your question. Please try again.",
                context_chunks=[],
            )

        return Response(
            {
                "status": "success",
                "data": {
                    "user_message": MessageSerializer(user_message).data,
                    "assistant_message": MessageSerializer(assistant_message).data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def _generate_mock_response(self, query: str, conversation: Conversation) -> str:
        """Generate a mock response when no LLM API key is configured."""
        repo_name = conversation.repository.name if conversation.repository else "your repository"
        return (
            f"Based on my analysis of **{repo_name}**, here's what I found regarding your question:\n\n"
            f"Your question: \"{query[:100]}\"\n\n"
            "I would search through the codebase to find relevant code and provide a detailed answer. "
            "To enable real AI responses, please configure your OpenAI API key in the environment variables.\n\n"
            "**Note:** This is a mock response. Configure `OPENAI_API_KEY` for real AI-powered answers."
        )


class MessageListView(APIView):
    """
    GET /api/v1/chat/conversations/{id}/messages/  — List messages
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        conversation = get_object_or_404(
            Conversation, pk=pk, user=request.user
        )
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({"status": "success", "data": serializer.data})


class StreamMessageView(APIView):
    """
    POST /api/v1/chat/conversations/{id}/messages/stream/

    Send a message and receive the AI response via Server-Sent Events (SSE).
    Returns a streaming response with chunked tokens.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        import json
        from django.http import StreamingHttpResponse

        conversation = get_object_or_404(Conversation, pk=pk, user=request.user)

        content = request.data.get("content", "").strip()
        if not content:
            return Response(
                {"status": "error", "message": "Message cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            role="user",
            content=content,
        )

        # Get conversation history
        history_messages = Message.objects.filter(
            conversation=conversation
        ).exclude(id=user_message.id).order_by("-created_at")[:6]

        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(list(history_messages))
        ]

        # Set up RAG pipeline
        from django.conf import settings as django_settings
        if django_settings.OPENAI_API_KEY:
            provider = get_llm_provider("openai")
        else:
            provider = get_llm_provider("mock", response="This is a streaming mock response. Configure OPENAI_API_KEY for real AI responses.")

        pipeline = RAGPipeline(llm_provider=provider)

        repository_name = conversation.repository.name if conversation.repository else ""
        repository_id = str(conversation.repository_id) if conversation.repository_id else ""

        def event_stream():
            full_content = ""
            sources = []

            try:
                for event in pipeline.generate_response_stream(
                    query=content,
                    repository_id=repository_id,
                    conversation_history=conversation_history,
                    repository_name=repository_name,
                ):
                    if event["type"] == "chunk":
                        full_content += event["content"]
                        yield f"data: {json.dumps(event)}\n\n"
                    elif event["type"] == "sources":
                        sources = event["sources"]
                        yield f"data: {json.dumps(event)}\n\n"
                    elif event["type"] == "done":
                        # Save assistant message
                        Message.objects.create(
                            conversation=conversation,
                            role="assistant",
                            content=full_content,
                            context_chunks=sources,
                            token_count=event.get("token_count", 0),
                            model_used=event.get("model_used", ""),
                        )
                        # Update title if first message
                        if conversation.title == "New Conversation":
                            conversation.title = content[:50]
                            conversation.save(update_fields=["title", "updated_at"])

                        yield f"data: {json.dumps(event)}\n\n"

            except Exception as e:
                logger.error(f"SSE stream error: {e}")
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
