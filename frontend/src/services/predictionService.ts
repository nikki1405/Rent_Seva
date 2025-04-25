import axiosInstance from './axiosConfig';

export const VALID_LOCATIONS = [
    'MVP Colony', 'Beach Road', 'Madhurawada', 'Gajuwaka',
    'Pendurthi', 'Seethammadhara', 'Rushikonda'
] as const;

export interface PredictionRequest {
    location: typeof VALID_LOCATIONS[number];
    bhk: number;
    built_area_sqft: number;
    bathrooms: number;
    furnishing: 'unfurnished' | 'semi-furnished' | 'fully-furnished';
    lift: boolean;
    air_conditioner: boolean;
    parking: boolean;
    gym: boolean;
    security: boolean;
    water_supply: boolean;
}

interface PredictionResponse {
    id: number;
    predicted_rent: number;
    confidence_score: number;
    timestamp: string;
}

const predictionService = {
    async predictRent(data: PredictionRequest): Promise<PredictionResponse> {
        // Validate required fields
        const requiredFields: (keyof PredictionRequest)[] = [
            'location', 'bhk', 'built_area_sqft', 'bathrooms',
            'lift', 'air_conditioner', 'parking', 'gym', 'security', 'water_supply'
        ];

        const missingFields = requiredFields.filter(field => data[field] === undefined);
        if (missingFields.length > 0) {
            throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
        }

        // Validate location
        if (!VALID_LOCATIONS.includes(data.location)) {
            throw new Error(`Invalid location: ${data.location}. Must be one of: ${VALID_LOCATIONS.join(', ')}`);
        }

        // Validate numeric ranges
        if (![1, 2, 3].includes(data.bhk)) {
            throw new Error('BHK must be 1, 2, or 3');
        }

        if (data.built_area_sqft < 400 || data.built_area_sqft > 2000) {
            throw new Error('Built-up area must be between 400 and 2000 square feet');
        }

        if (data.bathrooms < 1 || data.bathrooms > 4) {
            throw new Error('Number of bathrooms must be between 1 and 4');
        }

        // Convert boolean amenities to numbers for the API
        const requestData = {
            ...data,
            lift: Number(data.lift),
            air_conditioner: Number(data.air_conditioner),
            parking: Number(data.parking),
            gym: Number(data.gym),
            security: Number(data.security),
            water_supply: Number(data.water_supply)
        };

        try {
            const response = await axiosInstance.post<PredictionResponse>('/api/predict/', requestData);
            return response.data;
        } catch (error: any) {
            if (error.response?.data?.error) {
                throw new Error(error.response.data.error);
            }
            throw new Error('Failed to get rent prediction. Please try again.');
        }
    }
};

export default predictionService;