from rest_framework import serializers
from .models import WaterQualitySample

class WaterQualitySampleSerializer(serializers.ModelSerializer):
    pollution_status = serializers.SerializerMethodField()
    
    class Meta:
        model = WaterQualitySample
        fields = '__all__'
        read_only_fields = (
            'hmpi', 'hpi', 'hei', 'hci', 'cd', 'pi', 'pli', 
            'created_at', 'updated_at', 'pollution_status'
        )
    
    def get_pollution_status(self, obj):
        return obj.get_pollution_status()
    
    def create(self, validated_data):
        sample = super().create(validated_data)
        sample.calculate_indices()
        return sample
    
    def update(self, instance, validated_data):
        sample = super().update(instance, validated_data)
        sample.calculate_indices()
        return sample

class WaterQualityReportSerializer(serializers.ModelSerializer):
    pollution_status = serializers.SerializerMethodField()
    
    class Meta:
        model = WaterQualitySample
        fields = [
            'sample_id', 'sampling_date', 'latitude', 'longitude', 'well_depth',
            'lead', 'cadmium', 'chromium', 'arsenic', 'mercury', 'nickel', 
            'copper', 'zinc', 'iron', 'manganese', 'cobalt',
            'hmpi', 'hpi', 'hei', 'hci', 'cd', 'pi', 'pli', 'pollution_status'
        ]
    
    def get_pollution_status(self, obj):
        return obj.get_pollution_status()
