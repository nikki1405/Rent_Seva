import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { RefreshCw, Share, Check, MapPin, Home, Square, Bed, Bath } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

interface RentData {
  estimatedRent: number;
  areaAverage: number;
  propertyDetails: {
    location: string;
    builtArea: string;
    bhk: string;
    bathrooms: string;
    amenities: {
      lift: boolean;
      parking: boolean;
      ac: boolean;
      gym: boolean;
      security: boolean;
      water_supply: boolean;  // Changed from waterSupply to water_supply
    };
  };
}

const Results = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [rentData, setRentData] = useState<RentData | null>(null);
  const [showSuccess, setShowSuccess] = useState(false);
  
  useEffect(() => {
    // Retrieve data from sessionStorage
    const storedData = sessionStorage.getItem('rentData');
    
    if (!storedData) {
      // If no data, redirect to form
      navigate('/rent-form');
      return;
    }
    
    try {
      const parsedData = JSON.parse(storedData);
      setRentData(parsedData);
    } catch (error) {
      console.error('Error parsing rent data:', error);
      navigate('/rent-form');
    }
  }, [navigate]);
  
  const handleShareClick = () => {
    if (!rentData) return;
    
    const message = `My estimated rent by RentSeva for a ${rentData.propertyDetails.bhk} BHK in ${rentData.propertyDetails.location} is ₹${rentData.estimatedRent}. Check your fair rent at rentseva.in`;
    
    // Check if Web Share API is available
    if (navigator.share) {
      navigator.share({
        title: 'My RentSeva Estimate',
        text: message,
        url: window.location.href,
      })
      .catch((error) => console.log('Error sharing', error));
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(message)
        .then(() => {
          setShowSuccess(true);
          toast({
            title: "Copied to clipboard!",
            description: "You can now paste it in WhatsApp or any other app.",
          });
          
          setTimeout(() => setShowSuccess(false), 2000);
        })
        .catch((error) => console.error('Error copying to clipboard:', error));
    }
  };
  
  // Prepare chart data
  const chartData = rentData ? [
    {
      name: 'RentSeva Estimate',
      value: rentData.estimatedRent,
      fill: '#4A90E2'
    },
    {
      name: 'Area Average',
      value: rentData.areaAverage,
      fill: '#B8C4D6'
    }
  ] : [];
  
  // Get active amenities
  const getActiveAmenities = (amenities: RentData['propertyDetails']['amenities']) => {
    const active: string[] = [];
    if (amenities.lift) active.push('Lift');
    if (amenities.parking) active.push('Parking');
    if (amenities.ac) active.push('AC');
    if (amenities.gym) active.push('Gym');
    if (amenities.security) active.push('Security');
    if (amenities.water_supply) active.push('24/7 Water Supply');  // Changed from waterSupply to water_supply
    
    return active;
  };
  
  if (!rentData) {
    return (
      <div className="pt-20 pb-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Loading...</h2>
          <p>Please wait while we fetch your results.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-20 pb-16 min-h-screen bg-gradient-to-br from-rentseva-blue-100 to-rentseva-purple-100">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-3xl font-bold text-rentseva-gray-700 mb-2">Your Estimated Rent</h1>
          <p className="text-rentseva-gray-600">Based on the property details you provided</p>
        </div>
        
        {/* Estimated Rent Card */}
        <Card className="mb-6 shadow-lg border-0 animate-fade-in">
          <CardContent className="p-8 text-center">
            <h2 className="text-2xl text-rentseva-gray-600 mb-4">Your Fair Rent Price</h2>
            <div className="text-5xl font-bold text-rentseva-blue-500 mb-2">
              ₹{rentData.estimatedRent.toLocaleString('en-IN')}
            </div>
            <p className="text-rentseva-gray-500">per month</p>
          </CardContent>
        </Card>
        
        {/* Property Details Card */}
        <Card className="mb-6 shadow-lg border-0 animate-fade-in">
          <CardHeader>
            <CardTitle className="text-xl text-rentseva-gray-700">Property Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex items-start">
                <MapPin className="h-5 w-5 mr-2 text-rentseva-blue-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-rentseva-gray-700">Location</h3>
                  <p className="text-rentseva-gray-600">{rentData.propertyDetails.location}</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <Square className="h-5 w-5 mr-2 text-rentseva-blue-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-rentseva-gray-700">Built Area</h3>
                  <p className="text-rentseva-gray-600">{rentData.propertyDetails.builtArea} sq. ft.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <Bed className="h-5 w-5 mr-2 text-rentseva-blue-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-rentseva-gray-700">BHK</h3>
                  <p className="text-rentseva-gray-600">{rentData.propertyDetails.bhk} BHK</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <Bath className="h-5 w-5 mr-2 text-rentseva-blue-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-rentseva-gray-700">Bathrooms</h3>
                  <p className="text-rentseva-gray-600">{rentData.propertyDetails.bathrooms}</p>
                </div>
              </div>
              
              <div className="flex items-start sm:col-span-2">
                <Home className="h-5 w-5 mr-2 text-rentseva-blue-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-rentseva-gray-700">Amenities</h3>
                  <p className="text-rentseva-gray-600">
                    {getActiveAmenities(rentData.propertyDetails.amenities).length > 0 
                      ? getActiveAmenities(rentData.propertyDetails.amenities).join(', ')
                      : 'No amenities selected'}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        {/* Comparison Chart */}
        <Card className="mb-6 shadow-lg border-0 animate-fade-in">
          <CardHeader>
            <CardTitle className="text-xl text-rentseva-gray-700">Rent Comparison</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" tickFormatter={(value) => `₹${value}`} />
                  <YAxis dataKey="name" type="category" />
                  <Tooltip formatter={(value) => [`₹${value}`, 'Amount']} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <div className="mt-4 text-sm text-rentseva-gray-600">
              <p>Your estimate is {rentData.estimatedRent < rentData.areaAverage ? 'lower' : 'higher'} than the area average by {Math.abs(rentData.estimatedRent - rentData.areaAverage).toLocaleString('en-IN')} rupees.</p>
            </div>
          </CardContent>
        </Card>
        
        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 animate-fade-in">
          <Link 
            to="/rent-form" 
            className="btn-outline flex-1 flex items-center justify-center gap-2"
          >
            <RefreshCw className="h-5 w-5" />
            Estimate Again
          </Link>
          
          <button
            onClick={handleShareClick}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {showSuccess ? (
              <>
                <Check className="h-5 w-5" />
                Copied to Clipboard
              </>
            ) : (
              <>
                <Share className="h-5 w-5" />
                Share with WhatsApp
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;
