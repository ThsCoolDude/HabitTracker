from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('<int:habit_id>/', views.habit_detail, name='habit_detail'),
    path('add/', views.add_habit, name='add_habit'),
    path('<int:habit_id>/record/', views.record_habit, name='record_habit'),
    path('<int:habit_id>/delete/', views.delete_habit, name='delete_habit'),
    path('logout/', logout_view.as_view(), name='logout'),
]
