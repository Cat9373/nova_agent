import '../styles/background.css';

export const DarkRayField = () => (
  <div className="nova-bg-container dark-mode">
    <div className="nova-bg-layer nova-breathe">
      <div className="nova-light nova-light-left-blue"></div>
      <div className="nova-light nova-light-center-magenta"></div>
      <div className="nova-light nova-light-right-orange"></div>
      <div className="nova-rays"></div>
    </div>
  </div>
);

export const DarkAtmosphere = () => (
  <div className="nova-bg-container dark-mode">
    <div className="nova-bg-layer nova-breathe">
      <div className="nova-light nova-light-center-vertical"></div>
    </div>
  </div>
);

export const LightAtmosphere = () => (
  <div className="nova-bg-container light-mode">
    <div className="nova-bg-layer nova-breathe">
      <div className="nova-light nova-light-top-lavender"></div>
      <div className="nova-light nova-light-bottom-blue"></div>
    </div>
  </div>
);

export const WaveAtmosphere = () => (
  <div className="nova-bg-container light-mode">
    <div className="nova-bg-layer nova-breathe">
      <div className="nova-light nova-light-top-lavender"></div>
      <svg className="nova-waves" viewBox="0 0 1000 300" preserveAspectRatio="none">
        <defs>
          <linearGradient id="wave-grad-1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#2563EB" stopOpacity="0.8" />
            <stop offset="33%" stopColor="#8B5CF6" stopOpacity="0.8" />
            <stop offset="66%" stopColor="#EC4899" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#FB923C" stopOpacity="0.8" />
          </linearGradient>
          <linearGradient id="wave-grad-2" x1="0%" y1="0%" x2="100%" y2="0%">
             <stop offset="0%" stopColor="#7C3AED" stopOpacity="0.6" />
             <stop offset="50%" stopColor="#C026D3" stopOpacity="0.6" />
             <stop offset="100%" stopColor="#F97316" stopOpacity="0.6" />
          </linearGradient>
        </defs>
        <path d="M 0 150 C 200 100, 300 200, 500 150 C 700 100, 800 200, 1000 150" fill="none" stroke="url(#wave-grad-1)" strokeWidth="1.5" className="nova-wave-path nova-wave-1" />
        <path d="M 0 160 C 250 210, 250 90, 500 140 C 750 190, 750 90, 1000 160" fill="none" stroke="url(#wave-grad-2)" strokeWidth="2.5" className="nova-wave-path nova-wave-2" />
        <path d="M 0 140 C 150 200, 350 100, 500 160 C 650 220, 850 120, 1000 140" fill="none" stroke="url(#wave-grad-1)" strokeWidth="1" className="nova-wave-path nova-wave-3" />
      </svg>
    </div>
  </div>
);
