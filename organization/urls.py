from django.urls import path

from organization.views import AddPasswords, CreateOrganization, AddMembers, ViewOrgPassword, ViewAllOrgPassword

urlpatterns=[
    path('create/', CreateOrganization.as_view(), name='create_org'),
    path('add_members/', AddMembers.as_view(), name='add_members'),
    path('add_password/', AddPasswords.as_view(), name='add_password' ),
    path('view_password/<int:id>/',ViewOrgPassword.as_view(), name='view_org_pass'),
    path('viewall_org_passwords/<int:id>/',ViewAllOrgPassword.as_view(), name='viewall_org_password'),

]