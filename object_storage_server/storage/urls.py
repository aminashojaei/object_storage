from django.urls import path
from .views import ObjectListView
from storage import views as storage_views
from . import views

urlpatterns = [
    path('', storage_views.index, name='index'),
    # path('', ObjectListView.as_view(), name='index'),
]
