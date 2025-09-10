import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const Logo: React.FC<LogoProps> = ({ className = '', size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12'
  };

  return (
    <div className={`flex items-center ${className}`}>
      {/* Logo SVG - Warning/Alert themed for FOREWARN */}
      <svg
        className={`${sizeClasses[size]} text-blue-600`}
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z"
        />
      </svg>
      
      {/* Company Name */}
      <div className="ml-3">
        <h1 className="text-xl font-bold text-gray-900 tracking-tight">
          FOREWARN
        </h1>
        <p className="text-xs text-gray-500 uppercase tracking-wider">
          IBF Portal
        </p>
      </div>
    </div>
  );
};

export default Logo;
