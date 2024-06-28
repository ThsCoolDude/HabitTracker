from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('habits/', include('habits.urls')),
    path('', RedirectView.as_view(url='/habits/', permanent=True)),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    ]
