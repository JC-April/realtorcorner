from django.urls import path
from . import views


urlpatterns = [
    path('properties/', views.property_list, name="properties"),
    path('properties/create/', views.create_property, name="create_property"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('properties/<slug:slug>/', views.property_detail, name="property_detail"),
    path('properties/<slug:slug>/edit/', views.property_edit, name="property_edit"),
]