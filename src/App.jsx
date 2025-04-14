



import { useEffect } from 'react';
import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/pages/home/Header';
import About from './components/pages/About/About';
import Services from './components/pages/Services';
import Contact from './components/pages/Contact';
import Footer from './components/pages/Footer';
import BackToTopButton from './components/BackToTopButton';
import Chatbot from './components/Chatbot/src/Appchatbot';
import AboutDetails from './components/pages/About/AboutDetails'; // ← nouvelle page
import Loader from './components/Loader';

const App = () => {

    useEffect(() => {
      setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });    // smooth scroll au refresh 
      }, 50);
    }, []);


    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Simule un chargement (par exemple appel API ou animation d'intro)
      const timer = setTimeout(() => {
        setLoading(false);
      }, 3000); // 3 secondes
  
      return () => clearTimeout(timer);
    }, []);
  
    if (loading) {
      return <Loader />;
    }

  return (
    <div className='w-full overflow-hidden'>
      <Routes>
        <Route path="/" element={
          <>
            <BackToTopButton />
            <Header />
            <About />
            <Services />
            <Contact />
            <Chatbot />
          </>
        } />
        <Route path="/description-detaillee" element={<AboutDetails />} />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;


