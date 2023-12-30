from django.urls import path
from . import views
urlpatterns=[
    # path('',views.welcome,name="welcome"),
    path('',views.home,name="home"),
    path('leaderboard',views.leader_view,name="leaderboard"),
    path('dashboard',views.dashboard_view,name="dashboard"),
    path('about',views.about_view,name="about"),
    path('blogs',views.blogs_view,name="blogs"),
    path('blogs/<str:blog_id>',views.blog_view,name="blog"),
    path('contact',views.contact_view,name="contact"),
    path('term_conditions',views.term_conditions_view,name="term_conditions"),
    path('downloads',views.downloads_view,name="downloads"),
    path('message/<str:id>',views.message_view,name="message"),
    path('search/users',views.search_view,name="search_users"),
    
]