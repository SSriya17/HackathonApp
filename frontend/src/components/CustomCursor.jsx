import { useEffect, useState } from 'react'
import { motion, useMotionValue, useSpring } from 'framer-motion'

const CustomCursor = () => {
  const [isHovering, setIsHovering] = useState(false)
  const [isClicking, setIsClicking] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [cursorType, setCursorType] = useState('default')
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  const cursorX = useMotionValue(-100)
  const cursorY = useMotionValue(-100)
  const cursorScale = useMotionValue(1)

  const springConfig = { damping: 25, stiffness: 700 }
  const cursorXSpring = useSpring(cursorX, springConfig)
  const cursorYSpring = useSpring(cursorY, springConfig)
  const scaleSpring = useSpring(cursorScale, springConfig)

  useEffect(() => {
    const moveCursor = (e) => {
      cursorX.set(e.clientX - 16)
      cursorY.set(e.clientY - 16)
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    const handleMouseDown = () => {
      setIsClicking(true)
      cursorScale.set(0.8)
    }

    const handleMouseUp = () => {
      setIsClicking(false)
      cursorScale.set(1)
    }

    // Detect interactive elements
    const handleMouseEnter = (e) => {
      const target = e.target
      if (
        target.tagName === 'BUTTON' ||
        target.tagName === 'A' ||
        target.closest('button') ||
        target.closest('a') ||
        target.closest('[data-cursor="pointer"]')
      ) {
        setIsHovering(true)
        setCursorType('pointer')
        cursorScale.set(1.5)
      } else if (target.closest('[data-cursor="text"]')) {
        setIsHovering(true)
        setCursorType('text')
        cursorScale.set(1.2)
      } else if (target.closest('[data-cursor="drag"]')) {
        setIsHovering(true)
        setCursorType('drag')
        cursorScale.set(1.3)
      } else {
        setIsHovering(false)
        setCursorType('default')
        cursorScale.set(1)
      }
    }

    const handleMouseLeave = () => {
      setIsHovering(false)
      setCursorType('default')
      cursorScale.set(1)
    }

    const handleDragStart = () => {
      setIsDragging(true)
      cursorScale.set(1.2)
    }

    const handleDragEnd = () => {
      setIsDragging(false)
      cursorScale.set(1)
    }

    window.addEventListener('mousemove', moveCursor)
    window.addEventListener('mousedown', handleMouseDown)
    window.addEventListener('mouseup', handleMouseUp)
    document.addEventListener('mouseenter', handleMouseEnter, true)
    document.addEventListener('mouseleave', handleMouseLeave, true)
    document.addEventListener('dragstart', handleDragStart)
    document.addEventListener('dragend', handleDragEnd)

    return () => {
      window.removeEventListener('mousemove', moveCursor)
      window.removeEventListener('mousedown', handleMouseDown)
      window.removeEventListener('mouseup', handleMouseUp)
      document.removeEventListener('mouseenter', handleMouseEnter, true)
      document.removeEventListener('mouseleave', handleMouseLeave, true)
      document.removeEventListener('dragstart', handleDragStart)
      document.removeEventListener('dragend', handleDragEnd)
    }
  }, [cursorX, cursorY, cursorScale])

  return (
    <>
      {/* Main Cursor */}
      <motion.div
        className="fixed top-0 left-0 pointer-events-none z-[9999] mix-blend-difference"
        style={{
          x: cursorXSpring,
          y: cursorYSpring,
        }}
      >
        <motion.div
          className="relative"
          animate={{
            scale: scaleSpring,
          }}
          transition={{
            type: 'spring',
            stiffness: 500,
            damping: 28,
          }}
        >
          {/* Outer Ring */}
          <motion.div
            className="absolute -top-4 -left-4 w-8 h-8 rounded-full border-2 border-white"
            animate={{
              scale: isHovering ? 1.5 : 1,
              opacity: isHovering ? 0.6 : 0.4,
            }}
            transition={{ duration: 0.2 }}
          />
          
          {/* Main Cursor Dot */}
          <motion.div
            className={`w-4 h-4 rounded-full ${
              cursorType === 'pointer'
                ? 'bg-gradient-to-br from-blue-400 to-purple-500'
                : cursorType === 'text'
                ? 'bg-gradient-to-br from-pink-400 to-rose-500'
                : cursorType === 'drag'
                ? 'bg-gradient-to-br from-cyan-400 to-blue-500'
                : 'bg-white'
            }`}
            animate={{
              scale: isClicking ? 0.8 : 1,
            }}
            transition={{ duration: 0.1 }}
          />
          
          {/* Glow Effect */}
          <motion.div
            className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded-full ${
              cursorType === 'pointer'
                ? 'bg-blue-400'
                : cursorType === 'text'
                ? 'bg-pink-400'
                : cursorType === 'drag'
                ? 'bg-cyan-400'
                : 'bg-white'
            } opacity-30 blur-xl`}
            animate={{
              scale: isHovering ? 2 : isClicking ? 1.5 : 1,
              opacity: isHovering ? 0.4 : isClicking ? 0.2 : 0.1,
            }}
            transition={{ duration: 0.2 }}
          />
        </motion.div>
      </motion.div>

      {/* Cursor Trail */}
      <CursorTrail mousePosition={mousePosition} isHovering={isHovering} />
    </>
  )
}

const CursorTrail = ({ mousePosition, isHovering }) => {
  const [trail, setTrail] = useState([])

  useEffect(() => {
    const interval = setInterval(() => {
      setTrail((prev) => {
        const newTrail = [
          { x: mousePosition.x, y: mousePosition.y, id: Date.now() },
          ...prev.slice(0, 4),
        ]
        return newTrail
      })
    }, 50)

    return () => clearInterval(interval)
  }, [mousePosition])

  return (
    <div className="fixed top-0 left-0 pointer-events-none z-[9998]">
      {trail.map((point, index) => (
        <motion.div
          key={point.id}
          className="absolute w-2 h-2 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20"
          style={{
            left: point.x - 4,
            top: point.y - 4,
          }}
          initial={{ opacity: 0.8, scale: 1 }}
          animate={{
            opacity: 0,
            scale: 0,
          }}
          transition={{
            duration: 0.5,
            delay: index * 0.1,
          }}
        />
      ))}
    </div>
  )
}

export default CustomCursor

