import { useState, useEffect } from 'react';
import { 
  DarkRayField, 
  DarkAtmosphere, 
  LightAtmosphere, 
  WaveAtmosphere 
} from './components/BackgroundSystem';

function App() {
  const [variantIndex, setVariantIndex] = useState(0);

  // For preview purposes, we cycle through the background variants every 15 seconds.
  // In a real application, you would render the specific variant based on the current route/section.
  useEffect(() => {
    const interval = setInterval(() => {
      setVariantIndex((prev) => (prev + 1) % 4);
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {variantIndex === 0 && <DarkRayField />}
      {variantIndex === 1 && <DarkAtmosphere />}
      {variantIndex === 2 && <LightAtmosphere />}
      {variantIndex === 3 && <WaveAtmosphere />}
    </>
  );
}

export default App;
