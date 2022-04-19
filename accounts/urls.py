from django.urls import path
from accounts.views import Register

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
]