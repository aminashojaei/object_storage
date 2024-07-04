from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from storage import views as storage_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', user_views.register, name='register'),
    path('activate/<uid>/<token>/', user_views.activate, name='activate'),
    path('verify_account_sent/', user_views.verify_account_sent, name='verify_account_sent'),
    path('', include('storage.urls'))

]
