from django.urls import path
from . import views

urlpatterns = [
    path("",views.sign_up,name="signup"),
    path("login/",views.login_page,name="login"),
    path("home/",views.homepage,name="home"),
    path("logout/",views.logouts,name="logout"),
    path("create/", views.url_create, name="create"),
    path("retrieve/", views.url_read, name="retrieve"),
     path('search/',views.searchlist,name='searchs'),
    path('update/<int:id>/',views.url_update,name='update'),
    path('delete/<int:id>/',views.url_delete,name='delete'),
    
    
    
]
