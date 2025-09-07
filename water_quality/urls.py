from django.urls import path
from . import views

urlpatterns = [
    path('samples/', views.WaterQualitySampleListCreateView.as_view(), name='sample-list-create'),
    path('samples/<str:sample_id>/', views.WaterQualitySampleDetailView.as_view(), name='sample-detail'),
    path('samples/<str:sample_id>/pdf/', views.generate_pdf_report, name='generate-pdf'),
    path('samples/<str:sample_id>/indices/', views.get_sample_indices, name='sample-indices'),
    path('create-and-report/', views.create_sample_and_generate_report, name='create-and-report'),
