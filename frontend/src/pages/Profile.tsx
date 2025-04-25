
import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { User, Mail, Phone, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';

const Profile = () => {
  const { user, isAuthenticated } = useAuth();
  const { toast } = useToast();
  
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [mobile, setMobile] = useState(user?.mobile || '');
  
  // Redirect if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };
  
  const handleSave = () => {
    // In a real app, this would call an API to update the user data
    setIsEditing(false);
    toast({
      title: "Profile updated",
      description: "Your profile has been updated successfully"
    });
  };
  
  return (
    <div className="section-container max-w-3xl pt-20 pb-16">
      <h1 className="text-3xl font-bold text-center mb-8 text-rentseva-gray-700">Your Profile</h1>
      
      <Card className="shadow-md">
        <CardHeader className="pb-6 pt-8 text-center">
          <div className="flex justify-center mb-6">
            <Avatar className="h-24 w-24 border-4 border-rentseva-blue-200">
              <AvatarImage src={user?.avatar} alt={user?.name} />
              <AvatarFallback className="bg-rentseva-blue-400 text-white text-xl">
                {user?.name ? getInitials(user.name) : "U"}
              </AvatarFallback>
            </Avatar>
          </div>
          
          <CardTitle className="text-2xl text-rentseva-gray-700 mb-1">
            {user?.name}
          </CardTitle>
          <p className="text-rentseva-gray-500">Member since April 2025</p>
        </CardHeader>
        <CardContent className="space-y-6 pb-8">
          {isEditing ? (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input 
                  id="name" 
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input 
                  id="email" 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="mobile">Mobile Number</Label>
                <Input 
                  id="mobile" 
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value)}
                />
              </div>
              
              <div className="flex space-x-3 pt-4">
                <Button 
                  onClick={handleSave} 
                  className="bg-rentseva-blue-400 hover:bg-rentseva-blue-500"
                >
                  Save Changes
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setIsEditing(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex flex-col space-y-4">
                <div className="flex items-center p-3 border border-rentseva-gray-200 rounded-md">
                  <User className="h-5 w-5 text-rentseva-blue-400 mr-3" />
                  <div>
                    <p className="text-sm text-rentseva-gray-500">Full Name</p>
                    <p className="font-medium text-rentseva-gray-700">{user?.name}</p>
                  </div>
                </div>
                
                <div className="flex items-center p-3 border border-rentseva-gray-200 rounded-md">
                  <Mail className="h-5 w-5 text-rentseva-blue-400 mr-3" />
                  <div>
                    <p className="text-sm text-rentseva-gray-500">Email Address</p>
                    <p className="font-medium text-rentseva-gray-700">{user?.email}</p>
                  </div>
                  <div className="ml-auto flex items-center text-rentseva-green-400">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    <span className="text-xs">Verified</span>
                  </div>
                </div>
                
                <div className="flex items-center p-3 border border-rentseva-gray-200 rounded-md">
                  <Phone className="h-5 w-5 text-rentseva-blue-400 mr-3" />
                  <div>
                    <p className="text-sm text-rentseva-gray-500">Mobile Number</p>
                    <p className="font-medium text-rentseva-gray-700">{user?.mobile}</p>
                  </div>
                </div>
              </div>
              
              <Button 
                onClick={() => setIsEditing(true)} 
                variant="outline" 
                className="border-rentseva-blue-300 text-rentseva-blue-500"
              >
                Edit Profile
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Profile;
