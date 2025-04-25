
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Landing from './Landing';

// This component simply redirects to the Landing page
const Index = () => {
  const navigate = useNavigate();

  useEffect(() => {
    navigate('/', { replace: true });
  }, [navigate]);

  // Render Landing as fallback while redirecting
  return <Landing />;
};

export default Index;
