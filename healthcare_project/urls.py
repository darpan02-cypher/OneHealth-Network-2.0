from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Accounts App URLs
    path('accounts/', include('accounts.urls')),

    # Home Page
    path('', views.index, name='index'),

    # Static Pages
    path('about/', views.about, name='about'),
    path('contributors/', views.contributors, name='contributors'),
]

# Only for development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
