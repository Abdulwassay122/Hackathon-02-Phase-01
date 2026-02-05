"use client"

import { useEffect, useState } from 'react';
import { Toaster, toast, ToastOptions } from 'react-hot-toast';

interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration: number;
}

interface ToastComponentProps {
  position?: 'top-left' | 'top-right' | 'top-center' | 'bottom-left' | 'bottom-right' | 'bottom-center';
}

const ToastComponent = ({ position = 'top-right' }: ToastComponentProps) => {
  // Global toast configuration
  const toastOptions: ToastOptions = {
    position: position,
    duration: 4000, // Default duration for info messages
    style: {
      borderRadius: '8px',
      padding: '12px 16px',
      fontSize: '14px',
    },
    success: {
      style: {
        background: '#d1fae5', // light green background
        color: '#065f46',      // dark green text
      },
      iconTheme: {
        primary: '#065f46',
        secondary: '#d1fae5',
      },
    },
    error: {
      style: {
        background: '#fee2e2', // light red background
        color: '#991b1b',      // dark red text
      },
      iconTheme: {
        primary: '#991b1b',
        secondary: '#fee2e2',
      },
    },
  };

  return <Toaster {...toastOptions} />;
};

// Export utility functions for different toast types
export const showToast = {
  success: (message: string, duration?: number) => {
    toast.success(message, {
      duration: duration || 3000, // 3 seconds for success
    });
  },
  error: (message: string, duration?: number) => {
    toast.error(message, {
      duration: duration || 5000, // 5 seconds for error
    });
  },
  info: (message: string, duration?: number) => {
    toast(message, {
      duration: duration || 4000, // 4 seconds for info
    });
  },
  warning: (message: string, duration?: number) => {
    toast(message, {
      icon: '⚠️',
      duration: duration || 4000, // 4 seconds for warning
    });
  },
};

export default ToastComponent;