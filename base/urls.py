from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.home_sec, name="home_sec"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-book/', views.addBook, name="create-book"),
    path('book/<str:pk>/', views.book, name="book"),
    path('book/<str:pk>/edit', views.updateBook, name="update-book"),

    path('update-user/', views.updateUser, name="update-user"),
    path('loans/<str:pk>/', views.loansUser, name="loans-user"),
]