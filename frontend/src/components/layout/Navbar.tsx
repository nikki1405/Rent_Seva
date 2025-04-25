import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, Lock } from 'lucide-react';
import { cn } from '@/lib/utils';
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useToast } from '@/components/ui/use-toast';

interface User {
  email: string;
}

export interface AuthContextType {
  user: User | null;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const location = useLocation();
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const navLinks = [
    { name: 'Home', path: '/' },
    {
      name: 'Estimate',
      path: isAuthenticated ? '/rent-form' : '#',
      onClick: isAuthenticated ? undefined : () => setShowAuthModal(true),
      requiresAuth: true
    },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' }
  ];

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const handleLogout = async () => {
    try {
      await logout();
      toast({
        title: "Success",
        description: "Logged out successfully"
      });
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to logout"
      });
    }
  };

  return (
    <>
      <nav className="bg-white py-4 shadow-sm fixed w-full top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="h-9 w-9 bg-rentseva-blue-400 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">R</span>
              </div>
              <span className="text-xl font-bold font-heading text-rentseva-blue-500">RentSeva</span>
            </Link>

            <div className="hidden md:flex items-center space-x-8">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  to={link.path}
                  onClick={link.onClick}
                  className={cn(
                    "font-medium text-rentseva-gray-600 hover:text-rentseva-blue-400 transition-colors flex items-center gap-1",
                    location.pathname === link.path && "text-rentseva-blue-400 font-semibold",
                    link.requiresAuth && !isAuthenticated && "cursor-pointer opacity-85"
                  )}
                >
                  {link.name}
                  {link.requiresAuth && !isAuthenticated && (
                    <Lock className="h-3 w-3 text-rentseva-gray-500" />
                  )}
                </Link>
              ))}

              {user ? (
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="flex items-center">
                      <span className="mr-2">{user.email}</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-56">
                    <DropdownMenuItem onClick={() => navigate('/profile')}>
                      Profile
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/history')}>
                      Estimates History
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={handleLogout}>
                      Logout
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              ) : (
                <Button 
                  variant="ghost" 
                  className="text-rentseva-gray-600 hover:text-rentseva-blue-400 font-medium"
                  onClick={() => navigate('/login')}
                >
                  Login
                </Button>
              )}
            </div>

            <div className="md:hidden flex items-center">
              <button
                onClick={toggleMenu}
                className="text-rentseva-gray-600 hover:text-rentseva-blue-400 focus:outline-none"
              >
                {isMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </button>
            </div>
          </div>

          {isMenuOpen && (
            <div className="md:hidden pt-4 pb-2 animate-fade-in">
              <div className="flex flex-col space-y-3">
                {navLinks.map((link) => (
                  <Link
                    key={link.name}
                    to={link.path}
                    onClick={(e) => {
                      if (link.onClick) {
                        e.preventDefault();
                        link.onClick();
                      }
                      setIsMenuOpen(false);
                    }}
                    className={cn(
                      "py-2 px-3 rounded-md font-medium hover:bg-rentseva-blue-100 transition-colors flex items-center justify-between",
                      location.pathname === link.path
                        ? "bg-rentseva-blue-100 text-rentseva-blue-500"
                        : "text-rentseva-gray-600",
                      link.requiresAuth && !isAuthenticated && "cursor-pointer opacity-85"
                    )}
                  >
                    {link.name}
                    {link.requiresAuth && !isAuthenticated && (
                      <Lock className="h-4 w-4 text-rentseva-gray-500" />
                    )}
                  </Link>
                ))}

                <div className="pt-2 border-t border-rentseva-gray-200 mt-2">
                  <div className="py-2 px-3">
                    {user ? (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="flex items-center">
                            <span className="mr-2">{user.email}</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-56">
                          <DropdownMenuItem onClick={() => navigate('/profile')}>
                            Profile
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => navigate('/history')}>
                            Estimates History
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={handleLogout}>
                            Logout
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    ) : (
                      <Button 
                        variant="ghost" 
                        className="text-rentseva-gray-600 hover:text-rentseva-blue-400 font-medium"
                        onClick={() => navigate('/login')}
                      >
                        Login
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </nav>

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
    </>
  );
};

export default Navbar;
