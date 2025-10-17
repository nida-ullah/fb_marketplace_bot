import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "destructive" | "purple";
  size?: "sm" | "md" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "md", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";

    const variants = {
      default:
        "bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-600",
      outline:
        "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus-visible:ring-gray-600",
      ghost: "text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-600",
      destructive:
        "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-600",
      purple:
        "bg-purple-600 text-white hover:bg-purple-700 focus-visible:ring-purple-600",
    };

    const sizes = {
      sm: "h-9 px-3 text-sm",
      md: "h-10 px-4 text-sm",
      lg: "h-11 px-8 text-base",
    };

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button };
