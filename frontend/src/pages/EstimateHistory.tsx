import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import authService from '@/services/authService';

interface EstimateRecord {
  id: number;
  location: string;
  bhk: number;
  sqft: number;
  predicted_rent: number;
  created_at: string;
  furnishing_status?: string;
  confidence_score?: number;
}

export const EstimateHistory = () => {
  const [history, setHistory] = useState<EstimateRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const data = await authService.getEstimatesHistory();
        setHistory(data);
      } catch (error) {
        console.error('Error fetching history:', error);
        let errorMessage = 'Unable to connect to server. Please try again later.';
        
        if (error instanceof Error) {
          if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Network error. Please check your internet connection.';
          } else if (error.message.includes('401')) {
            errorMessage = 'Your session has expired. Please log in again.';
          } else {
            errorMessage = error.message;
          }
        }
        
        toast({
          variant: "destructive",
          title: "Error Loading History",
          description: errorMessage
        });
        setHistory([]);
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchHistory();
    }
  }, [isAuthenticated, toast]);

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto p-4 mt-20">
        <h2 className="text-2xl font-bold mb-6">Estimate History</h2>
        <p className="text-gray-500">Please log in to view your estimate history.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container mx-auto p-4 mt-20">
        <h2 className="text-2xl font-bold mb-6">Estimate History</h2>
        <div className="animate-pulse">
          <div className="h-24 bg-gray-200 rounded-lg mb-4"></div>
          <div className="h-24 bg-gray-200 rounded-lg mb-4"></div>
          <div className="h-24 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 mt-20">
      <h2 className="text-2xl font-bold mb-6">Estimate History</h2>
      {history.length === 0 ? (
        <p className="text-gray-500">No estimates found. Try making a new estimate!</p>
      ) : (
        <div className="grid gap-6">
          {history.map((record) => (
            <Card key={record.id} className="shadow-md hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Location</p>
                    <p className="font-medium text-gray-900">{record.location}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 mb-1">BHK</p>
                    <p className="font-medium text-gray-900">{record.bhk}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Area (sqft)</p>
                    <p className="font-medium text-gray-900">{record.sqft}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Predicted Rent</p>
                    <p className="font-medium text-gray-900">₹{record.predicted_rent.toLocaleString()}</p>
                  </div>
                  {record.furnishing_status && (
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Furnishing</p>
                      <p className="font-medium text-gray-900">
                        {record.furnishing_status.charAt(0).toUpperCase() + record.furnishing_status.slice(1)}
                      </p>
                    </div>
                  )}
                  {record.confidence_score !== undefined && (
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Confidence Score</p>
                      <p className="font-medium text-gray-900">{(record.confidence_score * 100).toFixed(1)}%</p>
                    </div>
                  )}
                </div>
                <div className="mt-4 border-t pt-4">
                  <p className="text-xs text-gray-400">
                    Estimated on: {new Date(record.created_at).toLocaleDateString()}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default EstimateHistory;
