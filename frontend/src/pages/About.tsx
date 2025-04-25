
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Check } from 'lucide-react';

const About = () => {
  return (
    <div className="pt-20 pb-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-rentseva-blue-100 to-rentseva-purple-100 py-12 sm:py-16">
        <div className="section-container">
          <div className="text-center">
            <h1 className="text-3xl sm:text-4xl font-bold mb-6 text-rentseva-gray-700">About RentSeva</h1>
            <p className="text-xl text-rentseva-gray-600 max-w-3xl mx-auto">
              RentSeva is a community-first platform designed to bring transparency to
              the rental housing market in India.
            </p>
          </div>
        </div>
      </section>
      
      {/* Mission Section */}
      <section className="py-12 bg-white">
        <div className="section-container">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold mb-6 text-rentseva-gray-700">Our Mission</h2>
              <p className="text-rentseva-gray-600 mb-6">
                RentSeva was created with a simple mission - to ensure that everyone, especially low and
                middle-income families, can find fair and affordable housing without overpaying or being exploited.
              </p>
              <p className="text-rentseva-gray-600 mb-6">
                We believe that access to fair housing information is a right, not a privilege. Our platform
                demystifies rental pricing and brings much-needed transparency to the Indian rental market.
              </p>
              <div className="space-y-3">
                <div className="flex items-start">
                  <Check className="h-5 w-5 text-rentseva-green-400 mr-2 mt-1" />
                  <p className="text-rentseva-gray-600">Promote transparency in rental pricing</p>
                </div>
                <div className="flex items-start">
                  <Check className="h-5 w-5 text-rentseva-green-400 mr-2 mt-1" />
                  <p className="text-rentseva-gray-600">Empower renters with accurate information</p>
                </div>
                <div className="flex items-start">
                  <Check className="h-5 w-5 text-rentseva-green-400 mr-2 mt-1" />
                  <p className="text-rentseva-gray-600">Make housing accessible through regional languages</p>
                </div>
                <div className="flex items-start">
                  <Check className="h-5 w-5 text-rentseva-green-400 mr-2 mt-1" />
                  <p className="text-rentseva-gray-600">Build community trust through reliable predictions</p>
                </div>
              </div>
            </div>
            <div className="flex justify-center">
              <img 
                src="https://images.unsplash.com/photo-1606761568499-6d2451b23c66?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=650&q=80"
                alt="Happy family in a home" 
                className="rounded-lg shadow-xl w-full max-w-md object-cover"
              />
            </div>
          </div>
        </div>
      </section>
      
      {/* How it Works Section */}
      <section className="py-12 bg-rentseva-gray-100">
        <div className="section-container">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold mb-4 text-rentseva-gray-700">How RentSeva Works</h2>
            <p className="text-rentseva-gray-600 max-w-3xl mx-auto">
              Our machine learning model is trained on thousands of actual rental listings to provide 
              the most accurate rent estimates possible.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="bg-rentseva-blue-100 h-12 w-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-rentseva-blue-500 text-xl font-bold">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Data Collection</h3>
              <p className="text-rentseva-gray-600">
                We collect and analyze real-time rental data from across India to ensure our estimates reflect 
                current market conditions.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="bg-rentseva-blue-100 h-12 w-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-rentseva-blue-500 text-xl font-bold">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Linear Regression Model</h3>
              <p className="text-rentseva-gray-600">
                Our ML algorithm uses linear regression to analyze property features and determine the most 
                significant factors affecting rent prices.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="bg-rentseva-blue-100 h-12 w-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-rentseva-blue-500 text-xl font-bold">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-rentseva-gray-700">Accurate Predictions</h3>
              <p className="text-rentseva-gray-600">
                By considering location, size, amenities, and other factors, we provide precise and 
                fair rent estimates for any property in India.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* FAQ Section */}
      <section className="py-12 bg-white">
        <div className="section-container">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold mb-4 text-rentseva-gray-700">Frequently Asked Questions</h2>
            <p className="text-rentseva-gray-600 max-w-3xl mx-auto">
              Get answers to common questions about RentSeva and our rent estimation process.
            </p>
          </div>
          
          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="space-y-4">
              <AccordionItem value="item-1" className="border rounded-lg p-1">
                <AccordionTrigger className="px-4 py-2 hover:no-underline">
                  <span className="text-left font-medium">How is the rent calculated?</span>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-4 pt-2 text-rentseva-gray-600">
                  RentSeva uses a machine learning model based on linear regression to analyze thousands of 
                  rental listings. We consider factors like location, property size, number of bedrooms and 
                  bathrooms, amenities, and current market trends to provide an accurate estimate.
                </AccordionContent>
              </AccordionItem>
              
              <AccordionItem value="item-2" className="border rounded-lg p-1">
                <AccordionTrigger className="px-4 py-2 hover:no-underline">
                  <span className="text-left font-medium">How accurate are RentSeva's estimates?</span>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-4 pt-2 text-rentseva-gray-600">
                  Our estimates are typically within 5-10% of actual market rates. The accuracy depends on 
                  the availability of data in your specific location and how common your property type is. 
                  Urban areas tend to have more accurate predictions due to more data points.
                </AccordionContent>
              </AccordionItem>
              
              <AccordionItem value="item-3" className="border rounded-lg p-1">
                <AccordionTrigger className="px-4 py-2 hover:no-underline">
                  <span className="text-left font-medium">Which cities does RentSeva cover?</span>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-4 pt-2 text-rentseva-gray-600">
                  RentSeva currently covers major metropolitan areas including Delhi NCR, Mumbai, Bangalore, 
                  Chennai, Hyderabad, Pune, Kolkata, and several tier-2 cities. We're constantly expanding 
                  our coverage to more locations across India.
                </AccordionContent>
              </AccordionItem>
              
              <AccordionItem value="item-4" className="border rounded-lg p-1">
                <AccordionTrigger className="px-4 py-2 hover:no-underline">
                  <span className="text-left font-medium">Can I use RentSeva if I'm a landlord?</span>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-4 pt-2 text-rentseva-gray-600">
                  Absolutely! Landlords can use RentSeva to ensure they're setting fair market rates for their 
                  properties. This helps attract quality tenants and reduces vacancy periods by pricing 
                  competitively.
                </AccordionContent>
              </AccordionItem>
              
              <AccordionItem value="item-5" className="border rounded-lg p-1">
                <AccordionTrigger className="px-4 py-2 hover:no-underline">
                  <span className="text-left font-medium">What languages does RentSeva support?</span>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-4 pt-2 text-rentseva-gray-600">
                  Currently, RentSeva is available in English, Hindi, Tamil, Telugu, and Bengali. We plan to 
                  add support for more regional languages to make our service accessible to all Indians 
                  regardless of language preference.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </div>
      </section>
      
      {/* Tech Stack Section */}
      <section className="py-12 bg-rentseva-blue-500 text-white">
        <div className="section-container">
          <div className="text-center">
            <h2 className="text-2xl sm:text-3xl font-bold mb-8">Powered By</h2>
            <div className="flex flex-wrap justify-center gap-6">
              <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
                <span className="font-medium text-lg">React</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
                <span className="font-medium text-lg">Python</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
                <span className="font-medium text-lg">Flask</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
                <span className="font-medium text-lg">Scikit-learn</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
                <span className="font-medium text-lg">TensorFlow</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
