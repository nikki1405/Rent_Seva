
import { useState } from 'react';
import { Mail, Phone, MapPin, Send, Loader2 } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

const Contact = () => {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.name || !formData.email || !formData.message) {
      toast({
        title: "Please fill all fields",
        description: "All fields are required to submit the form",
        variant: "destructive"
      });
      return;
    }
    
    // Simulate form submission
    setIsSubmitting(true);
    
    setTimeout(() => {
      setIsSubmitting(false);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        message: ''
      });
      
      // Show success toast
      toast({
        title: "Message sent successfully!",
        description: "We'll get back to you as soon as possible.",
        variant: "default"
      });
    }, 1500);
  };

  return (
    <div className="pt-20 pb-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-rentseva-blue-100 to-rentseva-purple-100 py-12 sm:py-16">
        <div className="section-container">
          <div className="text-center">
            <h1 className="text-3xl sm:text-4xl font-bold mb-6 text-rentseva-gray-700">Contact Us</h1>
            <p className="text-xl text-rentseva-gray-600 max-w-3xl mx-auto">
              Have questions or feedback? We'd love to hear from you.
            </p>
          </div>
        </div>
      </section>
      
      {/* Contact Details and Form Section */}
      <section className="py-12 bg-white">
        <div className="section-container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div className="order-2 lg:order-1">
              <h2 className="text-2xl font-bold mb-6 text-rentseva-gray-700">Send us a message</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-rentseva-gray-700 font-medium mb-2">
                    Your Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="John Doe"
                    className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
                  />
                </div>
                
                <div>
                  <label htmlFor="email" className="block text-rentseva-gray-700 font-medium mb-2">
                    Email Address
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="john@example.com"
                    className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
                  />
                </div>
                
                <div>
                  <label htmlFor="message" className="block text-rentseva-gray-700 font-medium mb-2">
                    Your Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    rows={6}
                    placeholder="How can we help you?"
                    className="w-full px-4 py-3 rounded-lg border border-rentseva-gray-300 focus:outline-none focus:ring-2 focus:ring-rentseva-blue-400"
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary flex items-center justify-center py-3 px-8 disabled:opacity-70"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="mr-2 h-5 w-5" />
                      Send Message
                    </>
                  )}
                </button>
              </form>
            </div>
            
            {/* Contact Info */}
            <div className="order-1 lg:order-2">
              <h2 className="text-2xl font-bold mb-6 text-rentseva-gray-700">Get in touch</h2>
              <p className="text-rentseva-gray-600 mb-8">
                Have questions about RentSeva or need assistance with your rent estimation? 
                Our team is here to help!
              </p>
              
              <div className="space-y-6">
                <div className="flex items-start">
                  <div className="bg-rentseva-blue-100 p-3 rounded-full mr-4">
                    <Mail className="h-6 w-6 text-rentseva-blue-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-rentseva-gray-700 mb-1">Email Us</h3>
                    <p className="text-rentseva-gray-600">help@rentseva.in</p>
                    <p className="text-rentseva-gray-600 mt-1">support@rentseva.in</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="bg-rentseva-purple-100 p-3 rounded-full mr-4">
                    <Phone className="h-6 w-6 text-rentseva-purple-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-rentseva-gray-700 mb-1">Call Us</h3>
                    <p className="text-rentseva-gray-600">+91 98765 43210</p>
                    <p className="text-rentseva-gray-600 mt-1">Monday to Friday, 9am to 6pm IST</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="bg-rentseva-green-100 p-3 rounded-full mr-4">
                    <MapPin className="h-6 w-6 text-rentseva-green-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-rentseva-gray-700 mb-1">Visit Us</h3>
                    <p className="text-rentseva-gray-600">
                      RentSeva Office, 
                      <br />
                      123 Tech Park, Sector 5,
                      <br />
                      Koramangala, Bangalore - 560034
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="mt-10 p-5 bg-rentseva-gray-100 rounded-lg">
                <h3 className="text-lg font-medium text-rentseva-gray-700 mb-3">RentSeva Help Desk</h3>
                <p className="text-rentseva-gray-600 mb-3">
                  For urgent assistance or technical support:
                </p>
                <p className="flex items-center text-rentseva-gray-600">
                  <Phone className="h-4 w-4 mr-2" />
                  Toll-free: 1800-123-4567
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Map Section */}
      <section className="py-0 h-80 bg-rentseva-gray-200">
        <div className="h-full">
          {/* Replace with an actual map integration if needed */}
          <div className="h-full w-full bg-rentseva-gray-300 flex items-center justify-center">
            <p className="text-rentseva-gray-600 text-lg">Map placeholder - Add Google Maps integration here</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
