from django.contrib import admin
from django.urls import path, include
from core.views import index, signup, login, logout, \
    setting, upload, like_post, profile_page, follow_user, search
from chat.views import new_chat
from comments.views import add_comment, view_comments
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('settings/', setting, name='settings'),
    path('upload', upload, name='upload'),
    path('search', search, name='search'),
    path('like-post/', like_post, name='like_post'),
    path('view_comments/<str:post_id>', view_comments, name='view_comments'),
    path('add_comment/<str:post_pk>', add_comment, name='add_comment'),
    path('inbox/', include('chat.urls')),
    path('<str:pk>/chat/', new_chat, name='new_chat'),
    path('profile/<str:pk>', profile_page, name='profile_page'),
    path('follow/', follow_user, name='follow'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('password-reset',
         auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'),
         name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_complete.html'),
         name='password_reset_done'),
    path('logout/', logout, name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
