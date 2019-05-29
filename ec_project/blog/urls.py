from django.urls import path
from . import views



urlpatterns = [
    path('',views.landing, name="blog-landing"),
    path('home/',views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('contact/', views.contact, name="blog-contact"),

]
