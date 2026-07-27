"""
Views for the accounts app.

Handles registration, login, profile, and password management.
"""

import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/v1/accounts/register/

    Create a new user account and return JWT tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Send verification email (non-blocking, don't fail registration if email fails)
        try:
            from django.core.mail import send_mail

            from .tokens import generate_verification_token

            token = generate_verification_token(str(user.id))
            verification_url = f"http://localhost:5173/verify?token={token}"
            send_mail(
                subject="Verify your CodePilot AI account",
                message=f"Verify your email: {verification_url}",
                from_email="noreply@codepilot.ai",
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't block registration on email failure

        return Response(
            {
                "status": "success",
                "data": {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/v1/accounts/login/

    Authenticate user with email/password and return JWT tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower()
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Invalid credentials.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {
                    "status": "error",
                    "message": "Invalid credentials.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {
                    "status": "error",
                    "message": "Account is deactivated.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "success",
                "data": {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    POST /api/v1/accounts/logout/

    Blacklist the refresh token to log out.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"status": "error", "message": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"status": "success", "message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"status": "error", "message": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    """
    GET /api/v1/accounts/profile/
    PATCH /api/v1/accounts/profile/

    Retrieve or update the authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "status": "success",
                "data": UserSerializer(request.user).data,
            }
        )

    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "status": "success",
                "data": UserSerializer(request.user).data,
            }
        )


class ChangePasswordView(APIView):
    """
    POST /api/v1/accounts/password/change/

    Change the authenticated user's password.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"status": "error", "message": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"status": "success", "message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class SendVerificationEmailView(APIView):
    """
    POST /api/v1/accounts/auth/verify/send/

    Send a verification email to the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response(
                {"status": "success", "message": "Email already verified."}
            )

        from django.conf import settings
        from django.core.mail import send_mail

        from .tokens import generate_verification_token

        token = generate_verification_token(str(user.id))
        verification_url = f"{request.data.get('frontend_url', 'http://localhost:5173')}/verify?token={token}"

        try:
            send_mail(
                subject="Verify your CodePilot AI account",
                message=f"Click the link to verify your email: {verification_url}",
                html_message=f"""
                    <h2>Verify your email</h2>
                    <p>Click the button below to verify your CodePilot AI account:</p>
                    <a href="{verification_url}" style="background:#6366f1;color:white;padding:12px 24px;border-radius:6px;text-decoration:none;display:inline-block;">
                        Verify Email
                    </a>
                    <p style="margin-top:16px;color:#666;">This link expires in 24 hours.</p>
                """,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else "noreply@codepilot.ai",
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            return Response(
                {"status": "error", "message": "Failed to send email. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"status": "success", "message": "Verification email sent."}
        )


class VerifyEmailView(APIView):
    """
    POST /api/v1/accounts/auth/verify/

    Verify a user's email with the provided token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"status": "error", "message": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from .tokens import verify_token

        user_id = verify_token(token)
        if not user_id:
            return Response(
                {"status": "error", "message": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {"status": "success", "message": "Email already verified."}
            )

        user.is_verified = True
        user.save(update_fields=["is_verified", "updated_at"])

        return Response(
            {"status": "success", "message": "Email verified successfully."}
        )
