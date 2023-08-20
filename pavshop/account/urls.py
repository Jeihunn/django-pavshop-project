from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from . import views
 
urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('register/', views.register_view, name="register_view"),
    path('user-profile/', views.user_profile_view, name="user_profile_view"),

    # Cities
    path('load-cities/', views.load_cities_view, name='load_cities_view'),

    # Social Auth
    path('social-auth/', include('social_django.urls', namespace="social")),

    # Activation User
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,33})/$', views.activate_view, name='activate_view'),
    path('request-new-token/', views.request_new_token_view, name='request_new_token_view'),

    # Forgot Password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name="account/password_reset_email.html",
        template_name="account/password_reset.html",
        form_class=CustomPasswordResetForm
        ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html",
        ), name='password_reset_done'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html",
        form_class=CustomSetPasswordForm
        ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/password_reset_complete.html",
        ), name='password_reset_complete'),

    # Change Password
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name="account/change_password.html",
        form_class=CustomPasswordChangeForm
        ), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="account/change_password_done.html"
        ), name='password_change_done'),
]
