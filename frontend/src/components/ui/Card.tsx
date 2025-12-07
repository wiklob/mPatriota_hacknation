import { forwardRef } from 'react';
import type { HTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined' | 'interactive';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', padding = 'none', children, ...props }, ref) => {
    const variants = {
      default: cn(
        'bg-card text-card-foreground',
        'border border-border/50',
        'shadow-soft'
      ),
      elevated: cn(
        'bg-card text-card-foreground',
        'border-none',
        'shadow-soft-lg'
      ),
      outlined: cn(
        'bg-transparent',
        'border border-border',
        'shadow-none'
      ),
      interactive: cn(
        'bg-card text-card-foreground',
        'border border-border/50',
        'shadow-soft cursor-pointer',
        'hover:shadow-soft-lg hover:border-border',
        'active:scale-[0.99] transition-all duration-200'
      ),
    };

    const paddings = {
      none: '',
      sm: 'p-3',
      md: 'p-6',
      lg: 'p-8',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-xl',
          variants[variant],
          paddings[padding],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';
