from django.urls import path
from . import views


app_name = 'loginapp'
urlpatterns = [
    path('', views.login),
    path('index/', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('add_staff/add/', views.add_staff_add, name = 'add_staff_add'),
    path('add_staff/update/<int:id>', views.add_staff_update, name = 'add_staff_update'),
    path('add_staff/del/<int:id>', views.add_staff_del, name = 'add_staff_del'),
]