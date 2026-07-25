"""
Tests for the chat app — conversations and messages with RAG.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.ai.services.llm_provider import MockProvider
from apps.ai.services.prompt_builder import PromptBuilder
from apps.ai.services.rag_pipeline import RAGPipeline
from apps.chat.models import Conversation, Message
from apps.repositories.models import Repository

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="other@example.com",
        email="other@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def repository(user):
    return Repository.objects.create(
        owner=user,
        name="my-project",
        source_type="upload",
        status="ready",
    )


@pytest.fixture
def conversation(user, repository):
    return Conversation.objects.create(
        user=user,
        repository=repository,
        title="Test Conversation",
    )


@pytest.fixture
def conversation_with_messages(conversation):
    Message.objects.create(conversation=conversation, role="user", content="How does auth work?")
    Message.objects.create(
        conversation=conversation,
        role="assistant",
        content="The auth system uses JWT tokens.",
        context_chunks=[{"file_path": "src/auth.py", "start_line": 1, "end_line": 10}],
    )
    return conversation


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


class TestPromptBuilder:
    """Tests for the prompt builder."""

    def test_build_basic_messages(self):
        builder = PromptBuilder()
        messages = builder.build_messages(user_query="How does auth work?")
        assert len(messages) == 2  # system + user
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "How does auth work?"

    def test_build_with_context(self):
        builder = PromptBuilder()
        chunks = [
            {
                "file_path": "src/auth.py",
                "start_line": 1,
                "end_line": 10,
                "language": "python",
                "content": "def authenticate(user): pass",
                "relevance_score": 0.92,
            }
        ]
        messages = builder.build_messages(
            user_query="How does auth work?",
            context_chunks=chunks,
        )
        assert len(messages) == 3  # system + context + user
        assert "src/auth.py" in messages[1]["content"]

    def test_build_with_history(self):
        builder = PromptBuilder()
        history = [
            {"role": "user", "content": "What is this project?"},
            {"role": "assistant", "content": "It's a web app."},
        ]
        messages = builder.build_messages(
            user_query="Tell me more",
            conversation_history=history,
        )
        assert len(messages) == 4  # system + 2 history + user

    def test_build_with_repo_name(self):
        builder = PromptBuilder()
        messages = builder.build_messages(
            user_query="test",
            repository_name="my-project",
        )
        assert "my-project" in messages[0]["content"]

    def test_history_trimming(self):
        builder = PromptBuilder()
        # Create long history
        history = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(20)
        ]
        messages = builder.build_messages(
            user_query="latest question",
            conversation_history=history,
        )
        # Should trim to max_messages (6) + system + user
        assert len(messages) <= 9


class TestMockProvider:
    """Tests for the mock LLM provider."""

    def test_generate(self):
        provider = MockProvider(response="Test response")
        result = provider.generate([{"role": "user", "content": "hello"}])
        assert result == "Test response"

    def test_generate_stream(self):
        provider = MockProvider(response="Hello world")
        tokens = list(provider.generate_stream([{"role": "user", "content": "hi"}]))
        assert len(tokens) > 0
        assert "".join(tokens).strip() == "Hello world"


@pytest.mark.django_db
class TestRAGPipeline:
    """Tests for the RAG pipeline."""

    def test_generate_response(self):
        import uuid
        mock_llm = MockProvider(response="The auth uses JWT tokens.")
        pipeline = RAGPipeline(llm_provider=mock_llm)

        response = pipeline.generate_response(
            query="How does auth work?",
            repository_id=str(uuid.uuid4()),
            repository_name="my-project",
        )

        assert response.content == "The auth uses JWT tokens."
        assert isinstance(response.sources, list)

    def test_generate_stream(self):
        import uuid
        mock_llm = MockProvider(response="Streaming response here")
        pipeline = RAGPipeline(llm_provider=mock_llm)

        events = list(pipeline.generate_response_stream(
            query="test",
            repository_id=str(uuid.uuid4()),
        ))

        # Should have chunk events + sources + done
        chunk_events = [e for e in events if e["type"] == "chunk"]
        assert len(chunk_events) > 0

        done_events = [e for e in events if e["type"] == "done"]
        assert len(done_events) == 1


@pytest.mark.django_db
class TestConversationAPI:
    """Tests for conversation CRUD endpoints."""

    def test_list_conversations(self, authenticated_client, conversation):
        response = authenticated_client.get("/api/v1/chat/conversations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Test Conversation"

    def test_list_only_own_conversations(self, authenticated_client, conversation, other_user, repository):
        # Create conversation for other user
        Conversation.objects.create(user=other_user, repository=repository, title="Other")
        response = authenticated_client.get("/api/v1/chat/conversations/")
        assert len(response.json()["data"]) == 1

    def test_create_conversation(self, authenticated_client, repository):
        response = authenticated_client.post(
            "/api/v1/chat/conversations/",
            {"repository_id": str(repository.id), "title": "New Chat"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["data"]["title"] == "New Chat"

    def test_create_conversation_invalid_repo(self, authenticated_client):
        import uuid
        response = authenticated_client.post(
            "/api/v1/chat/conversations/",
            {"repository_id": str(uuid.uuid4())},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_conversation_detail(self, authenticated_client, conversation_with_messages):
        url = f"/api/v1/chat/conversations/{conversation_with_messages.id}/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["messages"]) == 2

    def test_get_conversation_not_owner(self, api_client, conversation, other_user):
        api_client.force_authenticate(user=other_user)
        url = f"/api/v1/chat/conversations/{conversation.id}/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_archive_conversation(self, authenticated_client, conversation):
        url = f"/api/v1/chat/conversations/{conversation.id}/"
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        conversation.refresh_from_db()
        assert conversation.is_archived is True

    def test_archived_not_in_list(self, authenticated_client, conversation):
        conversation.is_archived = True
        conversation.save()
        response = authenticated_client.get("/api/v1/chat/conversations/")
        assert len(response.json()["data"]) == 0


@pytest.mark.django_db
class TestSendMessage:
    """Tests for the message sending endpoint."""

    def test_send_message(self, authenticated_client, conversation):
        url = f"/api/v1/chat/conversations/{conversation.id}/messages/"
        response = authenticated_client.post(
            url,
            {"content": "How does the login system work?"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["user_message"]["role"] == "user"
        assert data["user_message"]["content"] == "How does the login system work?"
        assert data["assistant_message"]["role"] == "assistant"
        assert len(data["assistant_message"]["content"]) > 0

    def test_send_empty_message(self, authenticated_client, conversation):
        url = f"/api/v1/chat/conversations/{conversation.id}/messages/"
        response = authenticated_client.post(url, {"content": "   "}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_send_message_updates_title(self, authenticated_client, repository):
        # Create a new conversation
        conv = Conversation.objects.create(
            user=authenticated_client.handler._force_user,
            repository=repository,
            title="New Conversation",
        )
        url = f"/api/v1/chat/conversations/{conv.id}/messages/"
        authenticated_client.post(
            url, {"content": "Explain the auth middleware"}, format="json"
        )
        conv.refresh_from_db()
        assert conv.title != "New Conversation"

    def test_send_message_unauthenticated(self, api_client, conversation):
        url = f"/api/v1/chat/conversations/{conversation.id}/messages/"
        response = api_client.post(url, {"content": "test"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_message_history_maintained(self, authenticated_client, conversation):
        url = f"/api/v1/chat/conversations/{conversation.id}/messages/"
        # Send multiple messages
        authenticated_client.post(url, {"content": "First question"}, format="json")
        authenticated_client.post(url, {"content": "Follow-up"}, format="json")

        # Check messages stored
        messages = Message.objects.filter(conversation=conversation)
        assert messages.count() == 4  # 2 user + 2 assistant
