import { useEffect } from 'react'
import CustomCursor from './components/CustomCursor'
import Navigation from './components/Navigation'
import Hero from './components/Hero'
import Features from './components/Features'
import Analytics from './components/Analytics'

function App() {
  useEffect(() => {
    // Hide default cursor on mount
    document.body.style.cursor = 'none'
    
    return () => {
      document.body.style.cursor = 'auto'
    }
  }, [])

  return (
    <div className="App">
      <CustomCursor />
      <Navigation />
      <Hero />
      <Features />
      <Analytics />
      
      {/* Footer */}
      <footer id="contact" className="py-20 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <span className="text-white font-bold text-xl">BL</span>
                </div>
                <span className="text-2xl font-display font-bold text-gradient">
                  BridgeLens
                </span>
              </div>
              <p className="text-slate-400">
                Next-generation analytics platform for the modern enterprise.
              </p>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-slate-400">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#analytics" className="hover:text-white transition-colors">Analytics</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#contact" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
          </div>
          
          <div className="pt-8 border-t border-white/10 text-center text-slate-400">
            <p>&copy; 2025 BridgeLens. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

