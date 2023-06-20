from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form),
    path('create/', views.create, name='create'),
    path('detail/<int:user_id>/', views.detail, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),

]
