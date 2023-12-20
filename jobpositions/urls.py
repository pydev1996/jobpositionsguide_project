# jobpositionsguide_project/jobpositions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.job_positions_list, name='job_positions_list'),
    path('', views.category_buttons, name='category_buttons'),
    path('institutions/', views.institutions, name='institutions'),
    path('institutor_signup/', views.institutor_signup, name='institutor_signup'),
    path('institutor_login', views.institutor_login, name='institutor_login'),
    path('institutorhomepage', views.institutorhomepage, name='institutorhomepage'),
    path('billing_detail/<int:billing_id>/', views.billing_detail, name='billing_detail'),
    path('add_billing/', views.add_billing, name='add_billing'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.job_positions_by_category, name='job_category'),
    # Add more URL patterns as needed
    path('job_positions/<int:job_position_id>/', views.job_position_detail, name='job_position_detail'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
