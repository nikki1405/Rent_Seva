import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Info, Home, MapPin, Square, Bed, Bath, Check, Loader2, Facebook, Twitter, Instagram } from 'lucide-react';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/context/AuthContext";
import predictionService from "@/services/predictionService";
import { Label } from "@/components/ui/label";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

// Update the FormData interface to match PredictionRequest
interface FormData {
  location: "MVP Colony" | "Beach Road" | "Madhurawada" | "Gajuwaka" | "Pendurthi" | "Seethammadhara" | "Rushikonda";
  bhk: string;
  built_area_sqft: string;
  bathrooms: string;
  furnishing: 'unfurnished' | 'semi-furnished' | 'fully-furnished';
  amenities: {
    lift: boolean;
    parking: boolean;
    ac: boolean;
    gym: boolean;
    security: boolean;
    water_supply: boolean;  // Changed from waterSupply to water_supply
  };
}

const RentForm = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { isAuthenticated } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Predefined locations
  const locations = [
    "MVP Colony",
    "Beach Road", 
    "Madhurawada",
    "Gajuwaka",
    "Pendurthi",
    "Seethammadhara",
    "Rushikonda"
  ];
  
  const [formData, setFormData] = useState<FormData>({
    location: "MVP Colony",
    bhk: '',
    built_area_sqft: '',
    bathrooms: '1', // Default value
    furnishing: 'unfurnished', // Default to unfurnished
    amenities: {
      lift: false,
      parking: false,
      ac: false,
      gym: false,
      security: false,
      water_supply: true // Changed from waterSupply to water_supply
    }
  });
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    if (name === 'location') {
      // Type assertion for location field
      const locationValue = value as FormData['location'];
      setFormData(prev => ({
        ...prev,
        location: locationValue
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };
  
  const handleAmenityChange = (amenity: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      amenities: {
        ...prev.amenities,
        [amenity]: checked
      }
    }));
  };
  
  // Update the handleSubmit function
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!isAuthenticated) {
      toast({
        variant: "destructive",
        title: "Authentication Required",
        description: "Please login to get rent predictions"
      });
      navigate('/login');
      return;
    }

    // Validate form data
    if (!formData.location || !formData.bhk || !formData.built_area_sqft) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please fill in all required fields"
      });
      return;
    }

    setIsSubmitting(true);
    
    try {
      const response = await predictionService.predictRent({
        location: formData.location,
        bhk: Number(formData.bhk),
        built_area_sqft: Number(formData.built_area_sqft),
        bathrooms: Number(formData.bathrooms),
        furnishing: formData.furnishing,
        lift: formData.amenities.lift,
        air_conditioner: formData.amenities.ac,
        parking: formData.amenities.parking,
        gym: formData.amenities.gym,
        security: formData.amenities.security,
        water_supply: formData.amenities.water_supply
      });

      const rentData = {
        estimatedRent: response.predicted_rent,
        timestamp: response.timestamp,
        confidence_score: response.confidence_score,
        propertyDetails: {
          location: formData.location,
          bhk: Number(formData.bhk),
          built_area_sqft: Number(formData.built_area_sqft),
          bathrooms: Number(formData.bathrooms),
          furnishing: formData.furnishing,
          amenities: formData.amenities
        }
      };
      
      sessionStorage.setItem('rentData', JSON.stringify(rentData));
      
      toast({
        title: "Success",
        description: "Rent prediction calculated successfully!"
      });
      
      navigate('/results');
    } catch (error) {
      console.error('Prediction error:', error);
      toast({
        variant: "destructive",
        title: "Prediction Failed",
        description: error instanceof Error ? error.message : "Failed to get rent prediction. Please try again."
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="pt-28 pb-16 bg-gradient-to-br from-rentseva-blue-100 to-rentseva-purple-100 min-h-screen">
      <div className="max-w-2xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-rentseva-gray-700 mb-3">Enter Property Details</h1>
          <p className="text-rentseva-gray-600">Fill in your property information to get an accurate rent estimate</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6 sm:p-8 animate-fade-in">
          <form onSubmit={handleSubmit}>
            {/* Location Field */}
            <div className="mb-6">
              <label className="flex items-center text-rentseva-gray-700 font-medium mb-2">
                <MapPin className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                Location *
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span className="ml-2 cursor-help">
                        <Info className="h-4 w-4 text-rentseva-gray-400" />
                      </span>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p className="w-60">Select your area from the available options</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </label>
              <select
                name="location"
                value={formData.location}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
              >
                <option value="">Select Area</option>
                {locations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Built Area Field */}
            <div className="mb-6">
              <label className="flex items-center text-rentseva-gray-700 font-medium mb-2">
                <Square className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                Built Area (sq. ft.) *
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span className="ml-2 cursor-help">
                        <Info className="h-4 w-4 text-rentseva-gray-400" />
                      </span>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p className="w-60">The total built-up area of your property in square feet</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </label>
              <input
                type="number"
                name="built_area_sqft"
                value={formData.built_area_sqft}
                onChange={handleChange}
                placeholder="e.g. 850"
                className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
              />
            </div>
            
            {/* BHK and Bathrooms in a grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
              {/* BHK Field */}
              <div>
                <label className="flex items-center text-rentseva-gray-700 font-medium mb-2">
                  <Bed className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                  BHK *
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <span className="ml-2 cursor-help">
                          <Info className="h-4 w-4 text-rentseva-gray-400" />
                        </span>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="w-60">BHK stands for Bedroom, Hall, Kitchen. Select the number of bedrooms.</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </label>
                <select
                  name="bhk"
                  value={formData.bhk}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
                >
                  <option value="">Select BHK</option>
                  <option value="1">1 BHK</option>
                  <option value="2">2 BHK</option>
                  <option value="3">3 BHK</option>
                  <option value="4">4 BHK</option>
                  <option value="5+">5+ BHK</option>
                </select>
              </div>
              
              {/* Bathrooms Field */}
              <div>
                <label className="flex items-center text-rentseva-gray-700 font-medium mb-2">
                  <Bath className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                  Bathrooms *
                </label>
                <Select
                  value={formData.bathrooms}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, bathrooms: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select bathrooms" />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4].map((num) => (
                      <SelectItem key={num} value={num.toString()}>
                        {num} {num === 1 ? 'Bathroom' : 'Bathrooms'}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            {/* Furnishing Status Field */}
            <div className="mb-6">
              <label className="flex items-center text-rentseva-gray-700 font-medium mb-2">
                <Home className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                Furnishing Status *
              </label>
              <Select
                value={formData.furnishing}
                onValueChange={(value) => setFormData(prev => ({ 
                  ...prev, 
                  furnishing: value as 'unfurnished' | 'semi-furnished' | 'fully-furnished' 
                }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select furnishing status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="unfurnished">Unfurnished</SelectItem>
                  <SelectItem value="semi-furnished">Semi-Furnished</SelectItem>
                  <SelectItem value="fully-furnished">Fully Furnished</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Amenities Section */}
            <div className="mb-8">
              <label className="flex items-center text-rentseva-gray-700 font-medium mb-4">
                <Home className="h-5 w-5 mr-2 text-rentseva-blue-400" />
                Amenities
              </label>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="lift" 
                    checked={formData.amenities.lift}
                    onCheckedChange={(checked) => handleAmenityChange('lift', checked as boolean)}
                  />
                  <label htmlFor="lift" className="text-rentseva-gray-600 cursor-pointer">Lift Available</label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="parking" 
                    checked={formData.amenities.parking}
                    onCheckedChange={(checked) => handleAmenityChange('parking', checked as boolean)}
                  />
                  <label htmlFor="parking" className="text-rentseva-gray-600 cursor-pointer">Parking Space</label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="ac" 
                    checked={formData.amenities.ac}
                    onCheckedChange={(checked) => handleAmenityChange('ac', checked as boolean)}
                  />
                  <label htmlFor="ac" className="text-rentseva-gray-600 cursor-pointer">Air Conditioning</label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="gym" 
                    checked={formData.amenities.gym}
                    onCheckedChange={(checked) => handleAmenityChange('gym', checked as boolean)}
                  />
                  <label htmlFor="gym" className="text-rentseva-gray-600 cursor-pointer">Gym Facility</label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="security" 
                    checked={formData.amenities.security}
                    onCheckedChange={(checked) => handleAmenityChange('security', checked as boolean)}
                  />
                  <label htmlFor="security" className="text-rentseva-gray-600 cursor-pointer">Security</label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="water_supply" 
                    checked={formData.amenities.water_supply}
                    onCheckedChange={(checked) => handleAmenityChange('water_supply', checked as boolean)}
                  />
                  <label htmlFor="water_supply" className="text-rentseva-gray-600 cursor-pointer">24/7 Water Supply</label>
                </div>
              </div>
            </div>
            
            {/* Submit Button */}
            <Button
              type="submit"
              disabled={isSubmitting}
              className="w-full btn-primary flex items-center justify-center py-4 text-lg disabled:opacity-70 mb-6"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Estimating Rent...
                </>
              ) : (
                <>
                  <Check className="mr-2 h-5 w-5" />
                  Estimate Rent
                </>
              )}
            </Button>

            {/* Social Media Links */}
            <div className="flex justify-center space-x-6 mt-4 border-t pt-6">
              <a
                href="https://instagram.com/rentseva"
                target="_blank"
                rel="noopener noreferrer"
                className="text-rentseva-gray-600 hover:text-pink-600 transition-colors"
                aria-label="Follow us on Instagram"
              >
                <Instagram className="h-6 w-6" />
              </a>
              <a
                href="https://twitter.com/rentseva"
                target="_blank"
                rel="noopener noreferrer"
                className="text-rentseva-gray-600 hover:text-blue-400 transition-colors"
                aria-label="Follow us on Twitter"
              >
                <Twitter className="h-6 w-6" />
              </a>
              <a
                href="https://facebook.com/rentseva"
                target="_blank"
                rel="noopener noreferrer"
                className="text-rentseva-gray-600 hover:text-blue-600 transition-colors"
                aria-label="Follow us on Facebook"
              >
                <Facebook className="h-6 w-6" />
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RentForm;
