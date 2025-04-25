import { Link } from 'react-router-dom';
import { Facebook, Twitter, Instagram, Mail, Phone, Linkedin, Youtube } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const Footer = () => {
  return (
    <footer className="bg-rentseva-gray-800 text-black pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Brand Section */}
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-6">
              <div className="h-10 w-10 bg-white rounded-lg flex items-center justify-center">
                <span className="text-rentseva-blue-500 font-bold text-2xl">R</span>
              </div>
              <span className="text-2xl font-bold">RentSeva</span>
            </div>
            <p className="text-black mb-6">
              Your trusted guide to fair rent pricing in India. We help families find affordable housing with confidence.
            </p>
            <div className="flex space-x-4">
              <a 
                href="https://facebook.com/rentseva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="bg-rentseva-gray-700 p-2 rounded-full hover:bg-rentseva-blue-500 transition-colors"
                aria-label="Follow us on Facebook"
              >
                <Facebook size={20} />
              </a>
              <a 
                href="https://twitter.com/rentseva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="bg-rentseva-gray-700 p-2 rounded-full hover:bg-rentseva-blue-400 transition-colors"
                aria-label="Follow us on Twitter"
              >
                <Twitter size={20} />
              </a>
              <a 
                href="https://instagram.com/rentseva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="bg-rentseva-gray-700 p-2 rounded-full hover:bg-pink-600 transition-colors"
                aria-label="Follow us on Instagram"
              >
                <Instagram size={20} />
              </a>
              <a 
                href="https://linkedin.com/company/rentseva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="bg-rentseva-gray-700 p-2 rounded-full hover:bg-blue-700 transition-colors"
                aria-label="Follow us on LinkedIn"
              >
                <Linkedin size={20} />
              </a>
              <a 
                href="https://youtube.com/@rentseva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="bg-rentseva-gray-700 p-2 rounded-full hover:bg-red-600 transition-colors"
                aria-label="Subscribe to our YouTube channel"
              >
                <Youtube size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-6 text-black">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-black hover:text-gray-600 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/rent-form" className="text-black hover:text-gray-600 transition-colors">
                  Estimate Rent
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-black hover:text-gray-600 transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-black hover:text-gray-600 transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-6 text-black">Contact Us</h3>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-rentseva-blue-400" />
                <span className="text-black">+91 98765 43210</span>
              </li>
              <li className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-rentseva-blue-400" />
                <a href="mailto:contact@rentseva.in" className="text-black hover:text-gray-600 transition-colors">
                  contact@rentseva.in
                </a>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-6 text-black">Stay Updated</h3>
            <p className="text-sm text-black mb-4">
              Subscribe to our newsletter for the latest updates and insights about rental markets.
            </p>
            <form onSubmit={(e) => e.preventDefault()} className="space-y-2">
              <Input 
                type="email"
                placeholder="Your email address"
                className="bg-rentseva-gray-700 border-rentseva-gray-600 text-white placeholder:text-rentseva-gray-400"
              />
              <Button type="submit" className="w-full bg-rentseva-blue-500 hover:bg-rentseva-blue-600">
                Subscribe
              </Button>
            </form>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-16 pt-8 border-t border-rentseva-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-black">
              © {new Date().getFullYear()} RentSeva. All rights reserved.
            </p>
            <div className="flex space-x-6">
              <Link to="/privacy" className="text-sm text-black hover:text-gray-600 transition-colors">
                Privacy Policy
              </Link>
              <Link to="/terms" className="text-sm text-black hover:text-gray-600 transition-colors">
                Terms of Service
              </Link>
              <Link to="/sitemap" className="text-sm text-black hover:text-gray-600 transition-colors">
                Sitemap
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
