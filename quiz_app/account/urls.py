from django.urls import path
from . import views
urlpatterns=[
    path('submit',views.submit,name='submit'),
    path('user_profiles/<str:username>',views.user_profiles,name="user_profile"),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name="edit"),
    path('delete',views.delete,name="delete")


]