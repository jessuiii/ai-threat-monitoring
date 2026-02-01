export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        cyan: {
          50: '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
          950: '#083344',
        },
        violet: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        dark: {
          50: '#f9fafb',   // gray-50
          100: '#f3f4f6',  // gray-100
          200: '#e5e7eb',  // gray-200
          300: '#d1d5db',  // gray-300
          400: '#9ca3af',  // gray-400
          500: '#6b7280',  // gray-500
          600: '#4b5563',  // gray-600
          700: '#374151',  // gray-700
          800: '#1f2937',  // gray-800
          900: '#111827',  // gray-900
          950: '#030712',  // gray-950
          bg: '#050505',
          surface: '#0a0a0a',
          border: '#1f1f1f'
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    }
  },
  plugins: []
};
