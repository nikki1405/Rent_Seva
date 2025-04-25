
import { ArrowRight, BarChart3, Users, MessageSquare, Lock } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { 
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

const Landing = () => {
  const { isAuthenticated } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-rentseva-blue-100 to-rentseva-purple-100 py-16 sm:py-24">
        <div className="section-container">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="text-center md:text-left">
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold leading-tight mb-6 text-rentseva-gray-700">
                <span className="text-rentseva-blue-500">RentSeva</span> - Your Trusted Guide to Fair Rent
              </h1>
              <p className="text-lg text-rentseva-gray-600 mb-8">
                Get accurate rent estimates for homes across India. No more overpaying. 
                Know the fair price powered by machine learning technology.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                {isAuthenticated ? (
                  <Link to="/rent-form" className="btn-primary flex items-center justify-center gap-2">
                    Check My Rent 
                    <ArrowRight size={18} />
                  </Link>
                ) : (
                  <button 
                    onClick={() => setShowAuthModal(true)}
                    className="btn-primary flex items-center justify-center gap-2 relative group"
                  >
                    <span className="flex items-center gap-2">
                      Check My Rent
                      <Lock size={16} className="text-white" />
                    </span>
                    <ArrowRight size={18} />
                  </button>
                )}
                <Link to="/about" className="btn-outline flex items-center justify-center gap-2">
                  Learn More
                </Link>
              </div>
            </div>
            <div className="flex justify-center md:justify-end">
              <img 
                src="https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=500&q=80" 
                alt="Indian apartment buildings" 
                className="rounded-lg shadow-xl w-full max-w-md object-cover h-80"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Feature Card Section */}
      <section className="py-16 bg-white">
        <div className="section-container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4 text-rentseva-gray-700">How RentSeva Helps You</h2>
            <p className="text-rentseva-gray-600 max-w-2xl mx-auto">
              Our platform gives you the tools to make informed rental decisions, saving you money and time.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Card 1 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow card-shadow">
              <div className="bg-rentseva-blue-100 p-3 rounded-full inline-flex mb-4">
                <BarChart3 className="h-8 w-8 text-rentseva-blue-500" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Accurate Price Prediction</h3>
              <p className="text-rentseva-gray-600">
                Our ML algorithm analyzes thousands of rental listings to provide you the most accurate rent estimate.
              </p>
            </div>
            
            {/* Card 2 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow card-shadow">
              <div className="bg-rentseva-purple-100 p-3 rounded-full inline-flex mb-4">
                <Users className="h-8 w-8 text-rentseva-purple-500" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Community-First Service</h3>
              <p className="text-rentseva-gray-600">
                Built for low and middle-income families to ensure fair rent prices and prevent exploitation.
              </p>
            </div>
            
            {/* Card 3 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow card-shadow">
              <div className="bg-rentseva-green-100 p-3 rounded-full inline-flex mb-4">
                <MessageSquare className="h-8 w-8 text-rentseva-green-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Available in Regional Languages</h3>
              <p className="text-rentseva-gray-600">
                Access RentSeva in Hindi, Tamil, Telugu, Bengali and more languages for easier understanding.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section */}
      <section className="py-16 bg-rentseva-gray-100">
        <div className="section-container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4 text-rentseva-gray-700">What Our Users Say</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Testimonial 1 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-rentseva-blue-200 flex items-center justify-center text-rentseva-blue-500 font-bold text-xl">
                  R
                </div>
                <div className="ml-4">
                  <h4 className="font-semibold">Rahul Sharma</h4>
                  <p className="text-sm text-rentseva-gray-500">Delhi NCR</p>
                </div>
              </div>
              <p className="text-rentseva-gray-600">
                "RentSeva saved me ₹3,000 per month! I was about to pay much more than the fair price for my 2BHK in Noida."
              </p>
            </div>
            
            {/* Testimonial 2 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-rentseva-purple-200 flex items-center justify-center text-rentseva-purple-500 font-bold text-xl">
                  P
                </div>
                <div className="ml-4">
                  <h4 className="font-semibold">Priya Patel</h4>
                  <p className="text-sm text-rentseva-gray-500">Bangalore</p>
                </div>
              </div>
              <p className="text-rentseva-gray-600">
                "As a student, finding affordable housing was a nightmare until I found RentSeva. Their estimate helped me negotiate better."
              </p>
            </div>
            
            {/* Testimonial 3 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-rentseva-green-200 flex items-center justify-center text-rentseva-green-400 font-bold text-xl">
                  S
                </div>
                <div className="ml-4">
                  <h4 className="font-semibold">Suresh Kumar</h4>
                  <p className="text-sm text-rentseva-gray-500">Chennai</p>
                </div>
              </div>
              <p className="text-rentseva-gray-600">
                "Using the app in Tamil made it so easy for my parents to understand the rental process. Great service!"
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-rentseva-blue-500 text-white">
        <div className="section-container">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold mb-6">Ready to Find Your Fair Rent?</h2>
            <p className="text-xl mb-8 text-rentseva-blue-100">
              Join thousands of Indian families who are paying the right price for their homes.
            </p>
            {isAuthenticated ? (
              <Link to="/rent-form" className="bg-white text-rentseva-blue-500 hover:bg-rentseva-blue-100 px-8 py-4 rounded-lg text-lg font-medium inline-flex items-center gap-2 transition-colors">
                Get Started Now
                <ArrowRight size={20} />
              </Link>
            ) : (
              <button
                onClick={() => setShowAuthModal(true)}
                className="bg-white text-rentseva-blue-500 hover:bg-rentseva-blue-100 px-8 py-4 rounded-lg text-lg font-medium inline-flex items-center gap-2 transition-colors"
              >
                Get Started Now
                <Lock size={18} className="ml-1" />
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Auth Required Modal */}
      <Dialog open={showAuthModal} onOpenChange={setShowAuthModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5 text-rentseva-blue-500" />
              Sign in required
            </DialogTitle>
            <DialogDescription>
              Please sign in to use the rent estimation feature.
            </DialogDescription>
          </DialogHeader>
          <div className="flex flex-col gap-4 py-4">
            <p className="text-rentseva-gray-600">
              Create an account or sign in to get accurate rent estimates and save your search history.
            </p>
          </div>
          <DialogFooter className="flex flex-col sm:flex-row gap-2 sm:gap-0">
            <Button variant="outline" asChild>
              <Link to="/signup" onClick={() => setShowAuthModal(false)}>
                Create Account
              </Link>
            </Button>
            <Button asChild className="bg-rentseva-blue-500 hover:bg-rentseva-blue-600">
              <Link to="/login" onClick={() => setShowAuthModal(false)}>
                Sign In
              </Link>
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Landing;
