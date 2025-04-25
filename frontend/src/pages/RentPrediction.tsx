import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import predictionService, { VALID_LOCATIONS } from '@/services/predictionService';
import type { PredictionRequest } from '@/services/predictionService';

// Use the validated locations from the service
const locations = [...VALID_LOCATIONS].sort();

// Store normalized location map for case-insensitive matching
const locationMap = new Map(locations.map(loc => [loc.toLowerCase(), loc]));

export const RentPrediction = () => {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState<Omit<PredictionRequest, 'location'> & { location: typeof VALID_LOCATIONS[number] | null }>({
        location: null,
        bhk: 2,
        built_area_sqft: 1000,
        bathrooms: 1,
        lift: false,
        air_conditioner: false,
        parking: false,
        gym: false,
        security: false,
        water_supply: true,
        furnishing: 'unfurnished' // Default value for furnishing
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.location) {
            toast({
                variant: "destructive",
                title: "Validation Error",
                description: "Please select a location"
            });
            return;
        }

        if (formData.built_area_sqft < 400 || formData.built_area_sqft > 2000) {
            toast({
                variant: "destructive", 
                title: "Validation Error",
                description: "Area must be between 400 and 2000 sqft"
            });
            return;
        }

        if (!isAuthenticated) {
            toast({
                variant: "destructive",
                title: "Authentication Required",
                description: "Please login to get rent predictions"
            });
            navigate('/login');
            return;
        }

        setLoading(true);

        try {
            const response = await predictionService.predictRent({
                ...formData,
                location: locationMap.get(formData.location?.toLowerCase() || '') as typeof VALID_LOCATIONS[number], // Normalize and validate location
                bhk: Number(formData.bhk),
                built_area_sqft: Number(formData.built_area_sqft)
            });

            const rentData = {
                estimatedRent: response.predicted_rent,
                timestamp: response.timestamp,
                propertyDetails: { ...formData }
            };

            sessionStorage.setItem('rentData', JSON.stringify(rentData));
            
            toast({
                title: "Success",
                description: "Rent prediction calculated successfully!"
            });

            navigate('/results');
        } catch (error) {
            console.error('Prediction failed:', error);
            toast({
                variant: "destructive",
                title: "Prediction Failed",
                description: error instanceof Error 
                    ? error.message 
                    : "Failed to get rent prediction. Please try again."
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4 mt-20">
            <Card className="max-w-2xl mx-auto">
                <CardHeader>
                    <CardTitle>Predict Rent</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <Label htmlFor="location">Location</Label>
                            <Select
                                value={formData.location}
                                onValueChange={(value) => setFormData({ ...formData, location: value as typeof VALID_LOCATIONS[number] })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select location" />
                                </SelectTrigger>
                                <SelectContent>
                                    {locations.map((loc) => (
                                        <SelectItem key={loc} value={loc}>
                                            {loc}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="bhk">BHK</Label>
                                <Select
                                    value={formData.bhk.toString()}
                                    onValueChange={(value: string) => setFormData({ ...formData, bhk: Number(value) })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select BHK" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {[1, 2, 3].map((bhk) => (
                                            <SelectItem key={bhk} value={bhk.toString()}>
                                                {bhk} BHK
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="built_area_sqft">Area (sqft)</Label>
                                <Input
                                    id="built_area_sqft"
                                    type="number"
                                    value={formData.built_area_sqft}
                                    onChange={(e) => setFormData({ ...formData, built_area_sqft: parseInt(e.target.value) })}
                                    min="400"
                                    max="2000"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="lift"
                                    checked={formData.lift}
                                    onCheckedChange={(checked) => setFormData({ ...formData, lift: !!checked })}
                                />
                                <Label htmlFor="lift">Lift</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="ac"
                                    checked={formData.air_conditioner}
                                    onCheckedChange={(checked) => setFormData({ ...formData, air_conditioner: !!checked })}
                                />
                                <Label htmlFor="ac">AC</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="parking"
                                    checked={formData.parking}
                                    onCheckedChange={(checked) => setFormData({ ...formData, parking: !!checked })}
                                />
                                <Label htmlFor="parking">Parking</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="gym"
                                    checked={formData.gym}
                                    onCheckedChange={(checked) => setFormData({ ...formData, gym: !!checked })}
                                />
                                <Label htmlFor="gym">Gym</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="security"
                                    checked={formData.security}
                                    onCheckedChange={(checked) => setFormData({ ...formData, security: !!checked })}
                                />
                                <Label htmlFor="security">Security</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="water"
                                    checked={formData.water_supply}
                                    onCheckedChange={(checked) => setFormData({ ...formData, water_supply: !!checked })}
                                />
                                <Label htmlFor="water">Water Supply</Label>
                            </div>
                        </div>

                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? "Calculating..." : "Predict Rent"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
};

export default RentPrediction;