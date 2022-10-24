"""Acme_Support URL Configuration

this url configaration is used for connecting admin app 
all urls of the ADMIN are listed below which was connected to main project urls

the main connection of urls is setup in setting.py which we assigned to ROOT_URLCONF 
and in  settings.urls we included acme_admin app urls


"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',SignInView.as_view(),name='signin'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('index',IndexView.as_view(),name='index_url'),
    path('users/',include([
        path('',ListUsersView.as_view(),name='list_users'),
        path('add-users',CreateUsersView.as_view(),name='add_users'),
        path('assign-department/<int:pk>',AssignDepartmentView.as_view(),name='asign_department'),

    ])),
    path('departments/',include([
        path('',ListDepartmentView.as_view(),name='list_departments'),
        path('add-departments',CreateDepartmentsView.as_view(),name='add_departments'),
        path('update-departments/<int:slug>',UpdateDepartmentsView.as_view(),name='update_departments'),
        path('delete-departments/<int:slug>',DeleteDepartmentsView.as_view(),name='delete_departments'),
        path('assign-department/<int:pk>',AssignDepartmentView.as_view(),name='asign_department'),

    ])),
    path('roles/',include([
        path('',ListRolesView.as_view(),name='list_roles'),
        path('add-roles',CreateRolesView.as_view(),name='add_roles'),
        path('set-permissions/<int:slug>',SetPermissionsView.as_view(),name='set_permissions'),

    ]))
    

]
