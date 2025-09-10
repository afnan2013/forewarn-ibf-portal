import React from 'react';
import { Badge } from '@/components/ui/badge';

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

  const textSizes = {
    sm: 'text-lg',
    md: 'text-xl', 
    lg: 'text-2xl'
  };

  const subtextSizes = {
    sm: 'text-xs',
    md: 'text-xs',
    lg: 'text-sm'
  };

  return (
    <div className={`flex items-center ${className}`}>
      {/* Logo SVG - Warning/Alert themed for FOREWARN */}
      <div className="relative">
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
      </div>
      
      {/* Company Name with Shadcn/ui styling */}
      <div className="ml-3">
        <h1 className={`${textSizes[size]} font-bold text-foreground tracking-tight`}>
          FOREWARN IBF Portal
        </h1>
        <Badge variant="secondary" className={`${subtextSizes[size]} font-normal tracking-wider`}>
           Disaster Risk Information System
        </Badge>
      </div>
    </div>
  );
};

export default Logo;
