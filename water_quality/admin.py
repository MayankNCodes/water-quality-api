from django.contrib import admin
from .models import WaterQualitySample

@admin.register(WaterQualitySample)
class WaterQualitySampleAdmin(admin.ModelAdmin):
    list_display = ['sample_id', 'sampling_date', 'latitude', 'longitude', 'hmpi', 'hpi', 'pli']
    list_filter = ['sampling_date', 'hmpi', 'hpi']
    search_fields = ['sample_id']
    readonly_fields = ['hmpi', 'hpi', 'hei', 'hci', 'cd', 'pi', 'pli', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sample_id', 'sampling_date', 'latitude', 'longitude', 'well_depth')
        }),
        ('Heavy Metal Concentrations (mg/L)', {
            'fields': ('lead', 'cadmium', 'chromium', 'arsenic', 'mercury', 'nickel', 
                      'copper', 'zinc', 'iron', 'manganese', 'cobalt')
        }),
        ('Calculated Indices', {
            'fields': ('hmpi', 'hpi', 'hei', 'hci', 'cd', 'pi', 'pli'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Example API Usage
"""
# 1. Create a new water quality sample
POST /api/water-quality/samples/
{
    "sample_id": "WQ001",
    "sampling_date": "2024-01-15",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "well_depth": 150.5,
    "lead": 0.02,
    "cadmium": 0.005,
    "chromium": 0.08,
    "arsenic": 0.015,
    "mercury": 0.001,
    "nickel": 0.03,
    "copper": 1.2,
    "zinc": 2.5,
    "iron": 0.45,
    "manganese": 0.25,
    "cobalt": 0.02
}

# 2. Get all samples
GET /api/water-quality/samples/

# 3. Get specific sample
GET /api/water-quality/samples/WQ001/

# 4. Generate PDF report for sample
GET /api/water-quality/samples/WQ001/pdf/

# 5. Get calculated indices only
GET /api/water-quality/samples/WQ001/indices/

# 6. Create sample and get PDF report in one request
POST /api/water-quality/create-and-report/
{
    "sample_id": "WQ002",
    "sampling_date": "2024-01-16",
    ...
}
"""
