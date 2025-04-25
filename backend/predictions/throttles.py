from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class BurstPredictionRateThrottle(UserRateThrottle):
    """
    Throttle for burst prediction requests.
    
    Limits how many predictions a user can make in quick succession.
    This prevents abuse while allowing reasonable burst usage.
    """
    rate = settings.PREDICTION_RATE_LIMIT['BURST_RATE']
    scope = 'prediction_burst'

    def allow_request(self, request, view):
        """
        Check if request should be allowed.
        
        Args:
            request: The incoming request
            view: The view handling the request
            
        Returns:
            bool: Whether the request should be allowed
        """
        allowed = super().allow_request(request, view)
        if not allowed:
            logger.warning(
                "Burst rate limit exceeded for user %s: %s requests/min",
                request.user.uid,
                self.rate
            )
        return allowed

class SustainedPredictionRateThrottle(UserRateThrottle):
    """
    Throttle for sustained prediction usage.
    
    Implements a daily limit on predictions to ensure fair usage
    of the service over longer periods.
    """
    rate = settings.PREDICTION_RATE_LIMIT['SUSTAINED_RATE']
    scope = 'prediction_sustained'

    def allow_request(self, request, view):
        """
        Check if request should be allowed.
        
        Args:
            request: The incoming request
            view: The view handling the request
            
        Returns:
            bool: Whether the request should be allowed
        """
        allowed = super().allow_request(request, view)
        if not allowed:
            logger.warning(
                "Daily rate limit exceeded for user %s: %s predictions/day",
                request.user.uid,
                self.rate
            )
        return allowed

class StrictIPRateThrottle(AnonRateThrottle):
    """
    Strict IP-based throttling for anonymous users.
    
    Implements stricter rate limiting for anonymous requests
    to protect the API from potential abuse.
    """
    rate = '3/hour'  # Stricter limit for anonymous users
    
    def get_cache_key(self, request, view):
        """
        Generate cache key for rate limiting.
        
        Uses a combination of IP address and path to track limits.
        
        Args:
            request: The incoming request
            view: The view handling the request
            
        Returns:
            str: Cache key for rate tracking
        """
        ident = self.get_ident(request)
        return f"strict_ip_throttle_{ident}"