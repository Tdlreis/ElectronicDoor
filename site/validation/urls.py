from django.urls import path
from . import views

urlpatterns = [
    path('validation/', views.validation, name='validation'),
    path('validate/<int:id>/', views.validate, name='validate'),
]
