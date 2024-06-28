from django.urls import path
from .views import ObjectListView
from . import views

urlpatterns = [
    path('', ObjectListView.as_view(), name='index'),
]
