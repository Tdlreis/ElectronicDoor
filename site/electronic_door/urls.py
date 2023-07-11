from django.contrib import admin
from django.urls import path, include
from door_user import views

urlpatterns = [
    path('', views.index, name='index'),  # Specify the root URL pattern directly to the "index" view
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('door_user.urls')),  # Move this line below the root URL pattern
    path('', include('hours.urls')),  # Move this line below the root URL pattern
    path('', include('validation.urls')),  # Move this line below the root URL pattern
]

handler404 = 'door_user.views.handler404'
handler500 = 'door_user.views.handler500'