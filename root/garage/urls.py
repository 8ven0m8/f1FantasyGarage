from django.urls import path
from . import views

urlpatterns = [
    path('', views.garage_home, name='garage_home'),
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('chat/', views.chat, name="chat"),
    path('create/', views.create_post, name="create"),
    path('post/<int:post_id>/vote/<str:vote_type>/', views.vote_post, name='vote_post'),
    path('register/', views.register, name="register"),
    path('edit/<int:post_id>/', views.post_edit, name="edit"),
    path('delete/<int:post_id>/', views.post_delete, name="delete"),
    path('profile/', views.profile, name="profile"),
    path('comment/<int:post_id>/', views.comments, name="comment"),
    path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('profile/update-image/', views.update_profile_image, name='update_profile_image'),
    path('editcomment/<int:post_id>/<int:comment_id>/', views.edit_comments, name="edit_comment"),
    path('editreply/<int:post_id>/<int:comment_id>/', views.edit_reply_to_comment, name="edit_reply"),
    path('deletecomment/<int:post_id>/<int:comment_id>/', views.delete_comment, name="delete_comment"),
    path('deletereply/<int:post_id>/<int:comment_id>/', views.delete_reply_to_comment, name="delete_reply"),
    path('search/', views.search_view, name='search'),
]