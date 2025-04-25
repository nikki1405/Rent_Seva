
import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { User, LogOut, History } from 'lucide-react';

const UserAvatar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  const handleLogout = () => {
    logout();
    setIsOpen(false);
    navigate('/');
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!isAuthenticated) {
    return (
      <div className="flex items-center space-x-4">
        <Link to="/login" className="text-rentseva-gray-600 hover:text-rentseva-blue-400 font-medium">
          Log In
        </Link>
        <Link to="/signup" className="btn-primary">
          Sign Up
        </Link>
      </div>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <div className="hidden md:block">
          <p className="text-rentseva-gray-600 text-sm">Welcome,</p>
          <p className="font-medium text-rentseva-blue-500">{user?.name}</p>
        </div>
        <Avatar className="h-9 w-9 border-2 border-rentseva-blue-300 cursor-pointer hover:border-rentseva-blue-400 transition-colors">
          <AvatarImage src={user?.avatar} alt={user?.name} />
          <AvatarFallback className="bg-rentseva-blue-400 text-white">
            {user?.name ? getInitials(user.name) : "U"}
          </AvatarFallback>
        </Avatar>
      </div>
      
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg overflow-hidden z-50 border border-rentseva-gray-300 animate-fade-in">
          <div className="py-2">
            <div className="px-4 py-3 border-b border-gray-200">
              <p className="text-sm text-rentseva-gray-500">Signed in as</p>
              <p className="font-medium truncate">{user?.email}</p>
            </div>
            
            <Link
              to="/profile"
              className="flex items-center px-4 py-2 text-sm text-rentseva-gray-700 hover:bg-rentseva-blue-100 hover:text-rentseva-blue-500"
              onClick={() => setIsOpen(false)}
            >
              <User size={16} className="mr-2" />
              Your Profile
            </Link>
            
            <Link
              to="/estimates"
              className="flex items-center px-4 py-2 text-sm text-rentseva-gray-700 hover:bg-rentseva-blue-100 hover:text-rentseva-blue-500"
              onClick={() => setIsOpen(false)}
            >
              <History size={16} className="mr-2" />
              My Estimates
            </Link>
            
            <button
              onClick={handleLogout}
              className="flex items-center w-full text-left px-4 py-2 text-sm text-rentseva-gray-700 hover:bg-rentseva-blue-100 hover:text-rentseva-blue-500"
            >
              <LogOut size={16} className="mr-2" />
              Log out
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserAvatar;
