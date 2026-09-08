from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/<slug:slug>/', views.ArtworkDetailView.as_view(), name='artwork_detail'),
    path('custom-order/', views.CommissionView.as_view(), name='commission'),
    path('classes/', views.ClassesView.as_view(), name='classes_list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
