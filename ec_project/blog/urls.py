from django.urls import path
from . import views



urlpatterns = [
    path('',views.landing, name="blog-landing"),
    path('notes/',views.notes, name="blog-notes"),
    path('homeworks/', views.homeworks, name="blog-homeworks"),
    path('learning/', views.learning, name="blog-learning"),

]
