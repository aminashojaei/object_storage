from django.urls import path
from .views import ObjectListView
from storage import views as storage_views
from . import views

urlpatterns = [
    # path('', storage_views.index, name='index'),
    path('', ObjectListView.as_view(), name='index'),
    path('add/', storage_views.upload_file_view, name="add"),
    # path('query/', storage_views.objects_list_view, name="query"),
    path('object/<str:pk>/update/', views.update_permissions, name='update_permissions'),
    path('object/<str:pk>/delete/', storage_views.delete_object, name='delete_object'),

    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
