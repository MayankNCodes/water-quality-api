from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import math

class WaterQualitySample(models.Model):
    sample_id = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Unique identifier for the water sample"
    )
    sampling_date = models.DateField(help_text="Date when the sample was collected")
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate (-90 to 90)"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate (-180 to 180)"
    )
    well_depth = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Depth of the well in meters"
    )
    
    # Heavy metal concentrations (mg/L)
    lead = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Lead concentration (mg/L)"
    )
    cadmium = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Cadmium concentration (mg/L)"
    )
    chromium = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Chromium concentration (mg/L)"
    )
    arsenic = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Arsenic concentration (mg/L)"
    )
    mercury = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Mercury concentration (mg/L)"
    )
    nickel = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Nickel concentration (mg/L)"
    )
    copper = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Copper concentration (mg/L)"
    )
    zinc = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Zinc concentration (mg/L)"
    )
    iron = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Iron concentration (mg/L)"
    )
    manganese = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Manganese concentration (mg/L)"
    )
    cobalt = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Cobalt concentration (mg/L)"
    )
    
    # Calculated indices (auto-calculated)
    hmpi = models.FloatField(null=True, blank=True, help_text="Heavy Metal Pollution Index")
    hpi = models.FloatField(null=True, blank=True, help_text="Health Risk Index")
    hei = models.FloatField(null=True, blank=True, help_text="Heavy Metal Evaluation Index")
    hci = models.FloatField(null=True, blank=True, help_text="Heavy Metal Contamination Index")
    cd = models.FloatField(null=True, blank=True, help_text="Contamination Degree")
    pi = models.FloatField(null=True, blank=True, help_text="Pollution Index")
    pli = models.FloatField(null=True, blank=True, help_text="Pollution Load Index")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-sampling_date', '-created_at']
        verbose_name = "Water Quality Sample"
        verbose_name_plural = "Water Quality Samples"
    
    def __str__(self):
        return f"Sample {self.sample_id} - {self.sampling_date}"
    
    def get_absolute_url(self):
        return reverse('sample-detail', kwargs={'sample_id': self.sample_id})
    
    def calculate_indices(self):
        """Calculate all water quality indices based on WHO/EPA standards"""
        # WHO/EPA standards for heavy metals (mg/L)
        standards = {
            'lead': 0.01,       # WHO guideline
            'cadmium': 0.003,   # WHO guideline  
            'chromium': 0.05,   # WHO guideline
            'arsenic': 0.01,    # WHO guideline
            'mercury': 0.006,   # WHO guideline
            'nickel': 0.07,     # WHO guideline
            'copper': 2.0,      # WHO guideline
            'zinc': 3.0,        # WHO guideline (aesthetic)
            'iron': 0.3,        # WHO guideline (aesthetic)
            'manganese': 0.4,   # WHO guideline (aesthetic)
            'cobalt': 0.05      # WHO/EPA estimate
        }
        
        metals = {
            'lead': self.lead,
            'cadmium': self.cadmium,
            'chromium': self.chromium,
            'arsenic': self.arsenic,
            'mercury': self.mercury,
            'nickel': self.nickel,
            'copper': self.copper,
            'zinc': self.zinc,
            'iron': self.iron,
            'manganese': self.manganese,
            'cobalt': self.cobalt
        }
        
        # Heavy Metal Pollution Index (HMPI)
        hmpi_sum = 0
        for metal, value in metals.items():
            if standards[metal] > 0:
                hmpi_sum += (value / standards[metal]) * 100
        self.hmpi = round(hmpi_sum / len(metals), 2)
        
        # Heavy Metal Evaluation Index (HEI)
        hei_sum = sum(value / standards[metal] for metal, value in metals.items() if standards[metal] > 0)
        self.hei = round(hei_sum, 2)
        
        # Heavy metal Contamination Index (HCI)
        self.hci = round(sum(value / standards[metal] for metal, value in metals.items() if standards[metal] > 0), 2)
        
        # Contamination Degree (Cd)
        self.cd = round(sum(value / standards[metal] for metal, value in metals.items() if standards[metal] > 0), 2)
        
        # Pollution Index (PI) - maximum contamination factor
        pi_values = []
        for metal, value in metals.items():
            if standards[metal] > 0:
                pi_values.append(value / standards[metal])
        self.pi = round(max(pi_values) if pi_values else 0, 2)
        
        # Pollution Load Index (PLI) - geometric mean of contamination factors
        pli_product = 1
        valid_metals = 0
        for metal, value in metals.items():
            if standards[metal] > 0:
                cf = value / standards[metal]
                pli_product *= cf
                valid_metals += 1
        
        if valid_metals > 0:
            self.pli = round(pli_product ** (1/valid_metals), 2)
        else:
            self.pli = 0
        
        # Health Risk Index (HPI) - weighted approach
        hpi_sum = 0
        total_weight = 0
        
        # Weights based on health significance
        weights = {
            'arsenic': 0.5,   # Highly toxic
            'lead': 0.4,      # Highly toxic
            'cadmium': 0.4,   # Highly toxic
            'mercury': 0.5,   # Highly toxic
            'chromium': 0.3,  # Moderately toxic
            'nickel': 0.2,    # Moderately toxic
            'copper': 0.2,    # Less toxic (essential element)
            'zinc': 0.1,      # Less toxic (essential element)
            'iron': 0.1,      # Less toxic (essential element)
            'manganese': 0.1, # Less toxic (essential element)
            'cobalt': 0.2     # Moderately toxic
        }
        
        for metal, value in metals.items():
            weight = weights.get(metal, 0.1)
            if standards[metal] > 0:
                # Quality rating (Qi) = (Ci/Si) × 100
                qi = (value / standards[metal]) * 100
                hpi_sum += weight * qi
                total_weight += weight
        
        self.hpi = round(hpi_sum / total_weight if total_weight > 0 else 0, 2)
        
        # Save the updated values
        self.save(update_fields=['hmpi', 'hpi', 'hei', 'hci', 'cd', 'pi', 'pli'])
    
    def get_pollution_status(self):
        """Get overall pollution status based on calculated indices"""
        if not all([self.hmpi, self.hpi, self.pli]):
            return "Not calculated"
        
        # Classification based on multiple indices
        high_pollution_count = 0
        
        if self.hmpi > 200:
            high_pollution_count += 1
        if self.hpi > 300:
            high_pollution_count += 1
        if self.pli > 2:
            high_pollution_count += 1
        
        if high_pollution_count >= 2:
            return "High Pollution"
        elif self.hmpi > 100 or self.hpi > 100 or self.pli > 1:
            return "Moderate Pollution"
        else:
            return "Low Pollution"
