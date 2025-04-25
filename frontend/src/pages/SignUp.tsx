import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Eye, EyeOff, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';

const Signup = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [mobile, setMobile] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Password validation states
  const hasMinLength = password.length >= 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const passwordMatch = password === confirmPassword && password !== '';
  
  const getPasswordStrength = () => {
    const criteria = [hasMinLength, hasUpperCase, hasLowerCase, hasNumber];
    const metCriteria = criteria.filter(Boolean).length;
    
    if (metCriteria === 0) return { text: 'Very weak', color: 'bg-red-500', percentage: 25 };
    if (metCriteria === 1) return { text: 'Weak', color: 'bg-orange-500', percentage: 50 };
    if (metCriteria === 2) return { text: 'Medium', color: 'bg-yellow-500', percentage: 60 };
    if (metCriteria === 3) return { text: 'Strong', color: 'bg-green-400', percentage: 80 };
    return { text: 'Very strong', color: 'bg-green-500', percentage: 100 };
  };
  
  const passwordStrength = getPasswordStrength();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
        setLoading(true);
        await signup(email, password);
        toast({
            title: "Success!",
            description: "Account created successfully"
        });
        navigate('/login');
    } catch (error: any) {
        const errorMessage = error.response?.data?.error || "Failed to create account";
        setError(errorMessage);
        toast({
            variant: "destructive",
            title: "Error",
            description: errorMessage
        });
    } finally {
        setLoading(false);
    }
  };
  
  return (
    <div className="h-screen flex items-center justify-center bg-rentseva-gray-100 py-16">
      <div className="w-full max-w-lg px-4">
        <Card className="shadow-lg border-rentseva-gray-300">
          <CardHeader className="space-y-1">
            <div className="flex justify-center mb-2">
              <div className="h-12 w-12 bg-rentseva-blue-400 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">R</span>
              </div>
            </div>
            <CardTitle className="text-2xl font-bold text-center text-rentseva-blue-500">Create your account</CardTitle>
            <p className="text-rentseva-gray-500 text-center">Enter your details to sign up for RentSeva</p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input 
                  id="name" 
                  placeholder="Enter your full name" 
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  autoComplete="name"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="you@example.com" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="mobile">Mobile Number</Label>
                <Input 
                  id="mobile" 
                  placeholder="Your 10-digit mobile number" 
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value)}
                  autoComplete="tel"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input 
                    id="password" 
                    type={showPassword ? "text" : "password"} 
                    placeholder="Create a strong password" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                  />
                  <button 
                    type="button" 
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-rentseva-gray-500"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
                
                {/* Password strength indicator */}
                {password && (
                  <div className="mt-2 space-y-2">
                    <div className="w-full h-2 bg-rentseva-gray-200 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${passwordStrength.color}`} 
                        style={{ width: `${passwordStrength.percentage}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-rentseva-gray-600">
                      Password strength: <span className="font-medium">{passwordStrength.text}</span>
                    </p>
                    
                    <ul className="space-y-1 text-sm">
                      <li className="flex items-center gap-2">
                        {hasMinLength ? 
                          <CheckCircle size={16} className="text-green-500" /> : 
                          <XCircle size={16} className="text-red-500" />
                        }
                        <span className={hasMinLength ? "text-green-700" : "text-red-600"}>
                          At least 8 characters
                        </span>
                      </li>
                      <li className="flex items-center gap-2">
                        {hasUpperCase ? 
                          <CheckCircle size={16} className="text-green-500" /> : 
                          <XCircle size={16} className="text-red-500" />
                        }
                        <span className={hasUpperCase ? "text-green-700" : "text-red-600"}>
                          Uppercase letter
                        </span>
                      </li>
                      <li className="flex items-center gap-2">
                        {hasLowerCase ? 
                          <CheckCircle size={16} className="text-green-500" /> : 
                          <XCircle size={16} className="text-red-500" />
                        }
                        <span className={hasLowerCase ? "text-green-700" : "text-red-600"}>
                          Lowercase letter
                        </span>
                      </li>
                      <li className="flex items-center gap-2">
                        {hasNumber ? 
                          <CheckCircle size={16} className="text-green-500" /> : 
                          <XCircle size={16} className="text-red-500" />
                        }
                        <span className={hasNumber ? "text-green-700" : "text-red-600"}>
                          At least one number
                        </span>
                      </li>
                    </ul>
                  </div>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Input 
                    id="confirmPassword" 
                    type={showConfirmPassword ? "text" : "password"} 
                    placeholder="Confirm your password" 
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    autoComplete="new-password"
                  />
                  <button 
                    type="button" 
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-rentseva-gray-500"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
                {confirmPassword && (
                  <div className="flex items-center gap-2 mt-1">
                    {passwordMatch ? 
                      <CheckCircle size={16} className="text-green-500" /> : 
                      <XCircle size={16} className="text-red-500" />
                    }
                    <span className={passwordMatch ? "text-green-700 text-sm" : "text-red-600 text-sm"}>
                      {passwordMatch ? "Passwords match" : "Passwords don't match"}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox 
                  id="terms" 
                  checked={agreeToTerms}
                  onCheckedChange={(checked) => setAgreeToTerms(checked === true)}
                />
                <label
                  htmlFor="terms"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  I agree to the <Link to="#" className="text-rentseva-blue-400 hover:underline">Terms & Conditions</Link>
                </label>
              </div>
              
              <Button 
                type="submit" 
                className="w-full bg-rentseva-blue-400 hover:bg-rentseva-blue-500" 
                disabled={loading}
              >
                {loading ? "Creating Account..." : "Create Account"}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex justify-center">
            <p className="text-rentseva-gray-600">
              Already have an account?{" "}
              <Link to="/login" className="text-rentseva-blue-400 hover:underline font-medium">
                Sign In
              </Link>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Signup;
