from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ItemDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('register/', views.register, name='register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
