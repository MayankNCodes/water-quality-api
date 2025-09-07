from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import WaterQualitySample
from .serializers import WaterQualitySampleSerializer, WaterQualityReportSerializer
from .pdf_generator import WaterQualityPDFGenerator

class WaterQualitySampleListCreateView(generics.ListCreateAPIView):
    queryset = WaterQualitySample.objects.all()
    serializer_class = WaterQualitySampleSerializer

class WaterQualitySampleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterQualitySample.objects.all()
    serializer_class = WaterQualitySampleSerializer
    lookup_field = 'sample_id'

@api_view(['GET'])
def generate_pdf_report(request, sample_id):
    """Generate PDF report for a specific water quality sample"""
    try:
        sample = get_object_or_404(WaterQualitySample, sample_id=sample_id)
        serializer = WaterQualityReportSerializer(sample)
        
        # Generate PDF
        pdf_generator = WaterQualityPDFGenerator()
        pdf_buffer = pdf_generator.generate_report(serializer.data)
        
        # Create HTTP response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="water_quality_report_{sample_id}.pdf"'
        
        return response
    
    except Exception as e:
        return Response(
            {'error': f'Error generating PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def create_sample_and_generate_report(request):
    """Create a new sample and immediately generate PDF report"""
    serializer = WaterQualitySampleSerializer(data=request.data)
    
    if serializer.is_valid():
        sample = serializer.save()
        
        try:
            # Generate PDF report
            pdf_generator = WaterQualityPDFGenerator()
            report_serializer = WaterQualityReportSerializer(sample)
            pdf_buffer = pdf_generator.generate_report(report_serializer.data)
            
            # Return PDF as response
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="water_quality_report_{sample.sample_id}.pdf"'
            
            return response
        
        except Exception as e:
            return Response(
                {'error': f'Sample created but PDF generation failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_sample_indices(request, sample_id):
    """Get calculated indices for a specific sample"""
    sample = get_object_or_404(WaterQualitySample, sample_id=sample_id)
    serializer = WaterQualityReportSerializer(sample)
    return Response(serializer.data)
