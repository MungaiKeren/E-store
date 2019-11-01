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
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search_results, name='search')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
