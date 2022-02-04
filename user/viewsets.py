from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import get_user_model
import uuid
import json

from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.account.adapter import get_adapter
from dj_rest_auth.app_settings import (
    JWTSerializer, JWTSerializerWithExpiration, LoginSerializer,TokenSerializer,
    create_token,
)

from .models import UserProfile
from .utils import account_activation_token
from .serializers import UserSerializer, UserProfileSerializer, SocialLoginSerializer

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2',
    ),
)


def get_token_model():
    default_model = 'rest_framework.authtoken.models.Token'
    import_path = getattr(settings, 'REST_AUTH_TOKEN_MODEL', default_model)
    session_login = getattr(settings, 'REST_SESSION_LOGIN', True)
    use_jwt = getattr(settings, 'REST_USE_JWT', False)

    if not any((session_login, import_path, use_jwt)):
        raise ImproperlyConfigured(
            'No authentication is configured for rest auth. You must enable one or '
            'more of `REST_AUTH_TOKEN_MODEL`, `REST_USE_JWT` or `REST_SESSION_LOGIN`'
        )
    if (
        import_path == default_model
        and 'rest_framework.authtoken' not in settings.INSTALLED_APPS
    ):
        raise ImproperlyConfigured(
            'You must include `rest_framework.authtoken` in INSTALLED_APPS '
            'or set REST_AUTH_TOKEN_MODEL to None'
        )
    return import_string(import_path) if import_path else None


TokenModel = get_token_model()


class UserRegisterViewSet(viewsets.GenericViewSet, CreateModelMixin):
    def create(self, request):
        try:
            if UserProfile.objects.filter(user__email=request.data.get("email")).exists():
                return Response({"message": "Email is already registered"}, status=400)
            if UserProfile.objects.filter(user__username=request.data.get("username")).exists():
                return Response({"message": "Username is already registered"}, status=400)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save(is_active=False)
                user.set_password(serializer.validated_data["password"])
                user.save()
                return Response({"message": "User successfully registered. Please check your mail and verify your account"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": str(serializer.errors)}, status=400)
        except Exception as error:
            return Response({"message": str(error)}, status=400)

    def __str__(self):
        return "UserRegisterViewSet"


class UserSignIn(APIView):
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")
        if UserProfile.objects.filter(Q(user_name=username_or_email) | Q(email=username_or_email)).exists():
            profile = UserProfile.objects.filter(
                Q(user_name=username_or_email) | Q(email=username_or_email))
            user = profile[0].user
            if user.check_password(password):
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email,
                        'username': user.username})
                return Response({"message": "Unverified account .Please check your mail and verify your account."}, status=400)
        return Response({"message": "Invalid username  or password. Please enter a valid username or email or password"}, status=400)


def activate_user(request, uidb64, token):

    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # creating user profile
        profile = UserProfile.objects.create(
            user=user, email=user.email)
        first_name, last_name, email, middle_name = user.first_name, user.last_name, user.email, ''
        if first_name and last_name:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.middle_name = middle_name
            profile.email = email
            profile.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserProfileViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = UserProfile.objects.filter(user=request.user)
        serializer = UserProfileSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        profile = UserProfile.objects.get(pk=pk)
        area_of_interest = request.data.get('area_of_interest')
        bio = request.data.get('bio')
        if bio:
            bio_words_count = len(bio.split())

        if area_of_interest:
            interests = json.loads(area_of_interest)
            profile.area_of_interest.set(interests)
            request.data._mutable = True
            request.data.pop('area_of_interest', None)

        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True)

        if serializer.is_valid():
            if bio and bio_words_count > 100:
                return Response(status=403, data={'bio': [
                    "Ensure this field has no more than 100 words."
                ]})
            serializer.save()

            serializer = UserProfileSerializer(
                profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def __str__(self):
        return "UserProfileViewSet"


class RestPasswordConfirmEmail(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            if UserProfile.objects.filter(Q(email=email)).exists():
                profile = UserProfile.objects.filter(
                    Q(email=email))
                if profile[0].user.email == email:
                    uuid_code1 = uuid.uuid4()
                    uuid_code2 = uuid.uuid4()
                    uuid_code = str(uuid_code1)+str(uuid_code2)
                    profile = UserProfile.objects.get(user=profile[0].user)
                    profile.forget_password_token = uuid_code
                    profile.save()
                    subject = "Email Verification for password reset"
                    message = f'Click in the link to reset your password {settings.URL}/forgot-password/?token={uuid_code}'
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [email]
                    send_mail(subject, message, email_from, email_to)

                    return Response({"message": "A confirmation email confirmation link is send to you email please check it"}, status=status.HTTP_200_OK)
            return Response({"message": "Incorrect email or Email not found"}, status=400)
        except Exception as error:
            return Response({"message": str(error)}, status=400)


class ResetPassword(APIView):

    def post(self, request, *args, **kwargs):
        try:
            forgot_password_token = request.data.get("forgot_password_token")
            password1 = request.data.get("new_password1")
            password2 = request.data.get("new_password2")
            if password1 == password2:
                if UserProfile.objects.filter(forget_password_token=forgot_password_token).exists():
                    profile = UserProfile.objects.filter(
                        forget_password_token=forgot_password_token)
                    user = profile[0].user
                    user.set_password(password1)
                    user.save()
                    return Response({"message": "Password reset successfully. Please Login"}, status=status.HTTP_200_OK)
                return Response({"message": "Incorrect token "}, status=400)
            return Response({"message": "Password didnot match"}, status=400)
        except Exception as error:
            return Response({"message": str(error)}, status=400)



class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    throttle_scope = 'dj_rest_auth'

    user = None
    access_token = None
    token = None

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):

            if getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = JWTSerializer

        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        token_model = get_token_model()

        if getattr(settings, 'REST_USE_JWT', False):
            self.access_token, self.refresh_token = jwt_encode(self.user)
        elif token_model:
            self.token = create_token(token_model, self.user, self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(
                settings, 'JWT_AUTH_RETURN_EXPIRATION', False)

            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
            }

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from .jwt_auth import set_jwt_cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class SocialLoginView(LoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class CustomFacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CustomGoogleLoginView(SocialLoginView):

    # authentication_classes = [TokenAuthentication, ]
    adapter_class = GoogleOAuth2Adapter
