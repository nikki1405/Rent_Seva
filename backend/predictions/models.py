from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import logging

logger = logging.getLogger(__name__)

class RentPrediction(models.Model):
    """
    Model to store rent predictions and associated property details.
    
    This model maintains a history of all rent predictions made by users,
    storing both the input parameters and the predicted rent value.
    Each prediction is associated with a user through their Firebase UID.
    """
    
    VALID_LOCATIONS = [
        'MVP Colony', 'Beach Road', 'Madhurawada', 'Gajuwaka',
        'Pendurthi', 'Seethammadhara', 'Rushikonda'
    ]
    
    user_id = models.CharField(
        max_length=128,
        help_text="Firebase UID of the user"
    )
    
    location = models.CharField(
        max_length=100,
        help_text="Location/area of the property",
        db_index=True,
        choices=[(loc, loc) for loc in VALID_LOCATIONS]
    )
    
    bhk = models.IntegerField(
        validators=[
            MinValueValidator(1, message="BHK must be at least 1"),
            MaxValueValidator(3, message="BHK cannot exceed 3")  # Updated for Vizag market
        ],
        help_text="Number of bedrooms (BHK)"
    )
    
    sqft = models.FloatField(
        validators=[
            MinValueValidator(400, message="Area must be at least 400 sqft"),
            MaxValueValidator(2000, message="Area cannot exceed 2000 sqft")  # Updated for Vizag market
        ],
        help_text="Built-up area in square feet"
    )
    
    predicted_rent = models.FloatField(
        validators=[MinValueValidator(4000, message="Rent must be at least ₹4,000")],
        help_text="Model-predicted monthly rent"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when prediction was made",
        db_index=True
    )
    
    # Additional fields for v1.1
    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi-furnished', 'Semi-Furnished'),
        ('fully-furnished', 'Fully Furnished')
    ]
    
    TENANT_CHOICES = [
        ('family', 'Family'),
        ('bachelors', 'Bachelors'),
        ('any', 'Any')
    ]
    
    furnishing_status = models.CharField(
        max_length=20,
        choices=FURNISHING_CHOICES,
        default='unfurnished',
        help_text="Property furnishing status"
    )
    
    preferred_tenants = models.CharField(
        max_length=20,
        choices=TENANT_CHOICES,
        default='any',
        help_text="Preferred tenant type"
    )
    
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ],
        help_text="Model's confidence score for the prediction"
    )
    
    api_version = models.CharField(
        max_length=10,
        default='1.1',
        help_text="API version used for prediction"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rent Prediction"
        verbose_name_plural = "Rent Predictions"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['location']),
            models.Index(fields=['furnishing_status']),
            models.Index(fields=['preferred_tenants']),
            models.Index(fields=['predicted_rent'])
        ]

    def __str__(self):
        """String representation of the prediction"""
        base_str = f"{self.location} - {self.bhk}BHK - ₹{self.predicted_rent:,.2f}"
        if self.api_version == '1.1':
            return f"{base_str} ({self.furnishing_status})"
        return base_str

    def clean(self):
        """
        Custom validation for the model.
        
        Ensures all numeric values are within reasonable ranges and
        required fields are properly formatted.
        """
        super().clean()
        
        # Location-specific rent validations
        location_ranges = {
            'MVP Colony': (8000, 30000),
            'Beach Road': (10000, 36000),
            'Madhurawada': (7000, 28000),
            'Gajuwaka': (5000, 20000),
            'Pendurthi': (4000, 16000),
            'Seethammadhara': (8000, 30000),
            'Rushikonda': (7000, 28000)
        }
        
        if self.location in location_ranges:
            min_rent, max_rent = location_ranges[self.location]
            
            # Adjust for BHK
            bhk_multiplier = {1: 1.0, 2: 1.5, 3: 2.0}.get(self.bhk, 1.0)
            min_rent = min_rent * bhk_multiplier
            max_rent = max_rent * bhk_multiplier
            
            if self.predicted_rent < min_rent or self.predicted_rent > max_rent:
                logger.warning(
                    f"Rent prediction ₹{self.predicted_rent:,.2f} outside expected range "
                    f"(₹{min_rent:,.2f} - ₹{max_rent:,.2f}) for {self.location}"
                )
        
        # Check price per sqft (should be between 5-35 for Vizag)
        price_per_sqft = self.predicted_rent / self.sqft
        if not (5 <= price_per_sqft <= 35):
            logger.warning(
                f"Price per sqft (₹{price_per_sqft:.2f}) outside normal range for Vizag"
            )

    def save(self, *args, **kwargs):
        """
        Custom save method with validation.
        
        Performs model validation before saving and ensures
        numeric fields are properly formatted.
        """
        self.full_clean()
        super().save(*args, **kwargs)
