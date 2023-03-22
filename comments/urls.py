from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('view_comments/<str:post_id>', views.view_comments, name='view_comments'),
    path('add_comment/<str:post_pk>', views.add_comment, name='add_comment')
]