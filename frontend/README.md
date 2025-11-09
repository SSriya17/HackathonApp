# BridgeLens 

## 🚀 Live App
Check it out here: [BridgeLens App](https://bridgelens.streamlit.app/)

An ultra-modern, visually impressive React frontend featuring a custom animated cursor and cutting-edge UI design. Built with React, Vite, Framer Motion, and Tailwind CSS.

## ✨ Features

### Custom Animated Cursor
- **Precision Tracking**: Smooth, responsive cursor that follows mouse movements with spring physics
- **Dynamic Morphing**: Cursor shape transforms based on interaction context (default, pointer, text, drag)
- **Glow Effects**: Subtle glow that intensifies on hover and click
- **Trail Effects**: Beautiful particle trail that follows cursor movement
- **Interactive Feedback**: Visual feedback for all user interactions

### Modern UI Design
- **Minimalist Aesthetics**: Clean, uncluttered interface with bold accent colors
- **Smooth Gradients**: Beautiful gradient backgrounds and text effects
- **Glass Morphism**: Modern glassmorphic design elements
- **Micro-interactions**: Every element responds to user interaction
- **Responsive Design**: Flawless experience across all devices

### Components
- **Navigation**: Sticky navigation with smooth scroll effects
- **Hero Section**: Eye-catching hero with animated background
- **Feature Cards**: Interactive cards with hover effects
- **Analytics Dashboard**: Real-time metrics with animated charts
- **Responsive Layout**: Mobile-first design approach

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn/pnpm

### Installation

1. **Navigate to the project directory:**
```bash
cd bridgelens-frontend
```

2. **Install dependencies:**
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. **Start the development server:**
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. **Open your browser:**
The app will automatically open at `http://localhost:3000`

### Build for Production

```bash
npm run build
# or
yarn build
# or
pnpm build
```

The production build will be in the `dist` folder.

### Preview Production Build

```bash
npm run preview
# or
yarn preview
# or
pnpm preview
```

## 🎨 Customization

### Cursor Behavior
Edit `src/components/CustomCursor.jsx` to customize:
- Cursor size and colors
- Trail particle count and behavior
- Hover state transformations
- Click animations

### Styling
- **Global Styles**: `src/index.css`
- **Tailwind Config**: `tailwind.config.js`
- **Component Styles**: Inline Tailwind classes in components

### Colors
Modify the gradient colors in:
- `tailwind.config.js` - Theme colors
- Component files - Gradient classes

## 📁 Project Structure

```
bridgelens-frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── CustomCursor.jsx    # Custom animated cursor
│   │   ├── Navigation.jsx      # Navigation bar
│   │   ├── Hero.jsx            # Hero section
│   │   ├── Features.jsx        # Features section
│   │   ├── FeatureCard.jsx     # Feature card component
│   │   └── Analytics.jsx       # Analytics dashboard
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🛠️ Technologies

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Framer Motion** - Animation library
- **Tailwind CSS** - Utility-first CSS framework
- **PostCSS** - CSS processing

## 🎯 Key Features Explained

### Custom Cursor System
The custom cursor uses Framer Motion's `useMotionValue` and `useSpring` for smooth, physics-based animations. It detects interactive elements and morphs accordingly.

### Responsive Design
All components are built mobile-first with Tailwind's responsive utilities. The layout adapts seamlessly from mobile to desktop.

### Performance
- Optimized animations using Framer Motion
- CSS-based animations where possible
- Lazy loading and code splitting ready

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🔧 Development

### Adding New Components
1. Create component in `src/components/`
2. Import and use in `App.jsx`
3. Style with Tailwind classes
4. Add animations with Framer Motion

### Cursor Integration
To make elements interactive with the custom cursor:
- Add `data-cursor="pointer"` for clickable elements
- Add `data-cursor="text"` for text inputs
- Add `data-cursor="drag"` for draggable elements

## 📝 License

This project is open source and available for use in your projects.


---

**Built with precision and innovation** 🚀

