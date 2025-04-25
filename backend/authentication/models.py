from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class EstimateHistory(models.Model):
    """
    Model to store user's rent estimate history.
    
    This model maintains a complete history of rent estimates made by users,
    allowing them to track their previous searches and predictions. Each
    estimate is tied to a specific user through their Firebase UID.
    
    The model includes essential property details and the predicted rent,
    with proper validation on all numeric fields to ensure data integrity.
    
    Attributes:
        user_id (str): Firebase UID of the user who made the estimate
        location (str): Location/area of the property
        bhk (int): Number of bedrooms (BHK - Bedroom, Hall, Kitchen)
        sqft (float): Built-up area in square feet
        predicted_rent (float): Model-predicted monthly rent
        created_at (datetime): Timestamp when estimate was made
    
    Meta:
        ordering: Orders estimates by creation date, newest first
        indexes: Optimizes queries by user_id and creation date
    """
    user_id = models.CharField(
        max_length=128,
        help_text="Firebase UID of the user"
    )
    location = models.CharField(
        max_length=100,
        help_text="Location/area of the property"
    )
    bhk = models.IntegerField(
        validators=[
            MinValueValidator(1, message="BHK must be at least 1"),
            MaxValueValidator(6, message="BHK cannot exceed 6")
        ],
        help_text="Number of bedrooms (BHK)"
    )
    sqft = models.FloatField(
        validators=[
            MinValueValidator(100, message="Area must be at least 100 sqft"),
            MaxValueValidator(10000, message="Area cannot exceed 10000 sqft")
        ],
        help_text="Built-up area in square feet"
    )
    predicted_rent = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Model-predicted monthly rent"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when estimate was made"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Estimate History"
        verbose_name_plural = "Estimate Histories"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user_id', '-created_at'])
        ]

    def __str__(self):
        """String representation of the estimate"""
        return f"{self.location} - {self.bhk}BHK - ₹{self.predicted_rent:,.2f}"

    def clean(self):
        """
        Custom validation for the model.
        
        Ensures all numeric values are within reasonable ranges and
        required fields are properly formatted.
        """
        super().clean()

    def save(self, *args, **kwargs):
        """
        Custom save method with validation.
        
        Performs model validation before saving and ensures
        numeric fields are properly formatted.
        """
        self.full_clean()
        super().save(*args, **kwargs)


class FirebaseUser:
    """
    Custom user class for Firebase authentication.
    
    This class implements the minimum interface required by Django's
    authentication system while using Firebase as the authentication
    backend. It provides basic user functionality without requiring
    a database table.
    
    Attributes:
        uid (str): Firebase User ID
        email (str, optional): User's email address
        is_authenticated (bool): Always True for valid users
        user_id (str): Alias for uid, maintained for compatibility
    """
    
    def __init__(self, uid, email=None):
        """
        Initialize a FirebaseUser instance.
        
        Args:
            uid (str): Firebase User ID
            email (str, optional): User's email address
        """
        self.uid = uid
        self.email = email
        self.is_authenticated = True
        self.user_id = uid  # Compatibility with Django's auth system

    @property
    def id(self):
        """
        Get the user's ID.
        
        Returns:
            str: The Firebase UID
        """
        return self.uid

    def __str__(self):
        """String representation of the user"""
        return self.email or self.uid
