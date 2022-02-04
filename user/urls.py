from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from user.viewsets import UserRegisterViewSet, UserProfileViewSet, UserSignIn, \
    change_password, forgot_password, CustomGoogleLoginView, CustomFacebookLoginView, \
    activate_user, reset_passoword
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register(r"sign-up", UserRegisterViewSet, basename="users")
router.register(r"user-profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("", include(router.urls)),
    path("sign-in/", UserSignIn.as_view()),
    path('email-verification/<str:uidb64>/<str:token>/',
         activate_user, name='email_activate'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password,
         name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/',
         reset_passoword, name='reset_password'),

    # remove these urls and respective views, serializers if you don't need social login
    path('facebook-sign-in/', CustomFacebookLoginView.as_view(), name='fb_sign_in'),
    path('google-sign-in/', CustomGoogleLoginView.as_view(), name='google_sign_in'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
