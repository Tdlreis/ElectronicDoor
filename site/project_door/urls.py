from django.contrib import admin
from django.urls import path, include
from hours_app import views

urlpatterns = [
    path('', views.index, name='index'),  # Specify the root URL pattern directly to the "index" view
    path('admin/', admin.site.urls),
    path('projects/<int:user_id>/punch_in/', views.punch_in, name='punch_in'),
    path('projects/<int:user_id>/punch_out/', views.punch_out, name='punch_out'),
    path('', include('hours_app.urls')),  # Move this line below the root URL pattern
]
