from django.urls import path
from passwords.views import CreatePassword, SinglePassword, PasswordView, ViewPasswordOnly, EditPasswordOnly, SharedViewSinglePassword, SharedEditSinglePassword

urlpatterns = [
    path('create/', CreatePassword.as_view(), name='create'),
    path('view/<int:id>/', SinglePassword.as_view(),name='single_view'),
    path('view/', PasswordView.as_view(), name='view'),
    path('share_view/<int:id>/', ViewPasswordOnly.as_view(), name='view_password'),
    path('share_edit/<int:id>/', EditPasswordOnly.as_view(), name='share_password'),
    path('sharedview/<int:id>/', SharedViewSinglePassword.as_view(),name='shared_view'),
    path('sharededit/<int:id>/', SharedEditSinglePassword.as_view(),name='shared_edit'),



]
