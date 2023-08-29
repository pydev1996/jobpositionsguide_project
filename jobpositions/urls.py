# jobpositionsguide_project/jobpositions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.job_positions_list, name='job_positions_list'),
    path('', views.category_buttons, name='category_buttons'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('category/<str:category>/', views.job_positions_by_category, name='job_category'),
    # Add more URL patterns as needed
    path('job_positions/<int:job_position_id>/', views.job_position_detail, name='job_position_detail'),
]
