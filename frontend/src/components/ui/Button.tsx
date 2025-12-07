import { forwardRef } from 'react';
import type { ButtonHTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, disabled, children, ...props }, ref) => {
    const baseStyles = cn(
      'relative font-medium transition-all duration-200',
      'flex items-center justify-center gap-2',
      'active:scale-[0.97] disabled:active:scale-100',
      'disabled:opacity-50 disabled:cursor-not-allowed'
    );

    const variants = {
      primary: cn(
        'bg-primary text-primary-foreground',
        'shadow-soft hover:shadow-soft-lg',
        'hover:bg-primary/90',
        'active:scale-[0.98]'
      ),
      secondary: cn(
        'bg-secondary text-secondary-foreground',
        'hover:bg-secondary/80',
        'shadow-sm'
      ),
      ghost: cn(
        'text-muted-foreground hover:text-foreground',
        'hover:bg-accent hover:text-accent-foreground'
      ),
      outline: cn(
        'border border-input bg-transparent shadow-sm',
        'hover:bg-accent hover:text-accent-foreground'
      ),
    };

    const sizes = {
      sm: 'h-9 rounded-md px-3 text-xs',
      md: 'h-11 rounded-lg px-8 text-sm',
      lg: 'h-14 rounded-xl px-8 text-base',
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
