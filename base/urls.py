from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.homeSec, name="home_sec"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/', views.userProfile, name="user-profile"),
    path('create-book/', views.addBook, name="create-book"),
    path('book/<str:pk>/', views.book, name="book"),
    path('book/<str:pk>/edit', views.updateBook, name="update-book"),
    path('update-user/', views.updateUser, name="update-user"),
    path('password/', views.PasswordsChangeView.as_view(
        template_name='base/change-password.html'), name="update-password"),
    path('check-outs/', views.loansUser, name="loans-user"),
]
