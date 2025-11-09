import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

const Analytics = () => {
  const [stats, setStats] = useState([
    { label: 'Data Points Processed', value: 0, target: 2500000, suffix: 'M' },
    { label: 'Active Users', value: 0, target: 12500, suffix: 'K' },
    { label: 'Queries Per Second', value: 0, target: 45000, suffix: '' },
    { label: 'Uptime', value: 0, target: 99.9, suffix: '%' },
  ])

  useEffect(() => {
    const intervals = stats.map((stat, index) => {
      const duration = 2000
      const steps = 60
      const increment = stat.target / steps
      let current = 0

      return setInterval(() => {
        current += increment
        if (current >= stat.target) {
          current = stat.target
          clearInterval(intervals[index])
        }
        setStats((prev) => {
          const newStats = [...prev]
          newStats[index].value = Math.floor(current)
          return newStats
        })
      }, duration / steps)
    })

    return () => intervals.forEach(clearInterval)
  }, [])

  return (
    <section id="analytics" className="py-32 relative">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-5xl md:text-6xl font-display font-bold mb-6">
            <span className="text-gradient">Analytics at Scale</span>
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Real-time metrics that matter
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              className="glass rounded-2xl p-8 text-center"
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              whileHover={{ scale: 1.05, y: -5 }}
            >
              <div className="text-4xl md:text-5xl font-display font-bold text-gradient mb-2">
                {stat.value.toLocaleString()}
                {stat.suffix}
              </div>
              <div className="text-slate-400 font-medium">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Chart Visualization */}
        <motion.div
          className="glass rounded-2xl p-8"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-2xl font-display font-bold text-white mb-6">
            Performance Metrics
          </h3>
          <div className="h-64 flex items-end justify-between gap-4">
            {[65, 80, 45, 90, 70, 85, 60, 75, 55, 95].map((height, index) => (
              <motion.div
                key={index}
                className="flex-1 bg-gradient-to-t from-blue-500 to-purple-600 rounded-t-lg relative group"
                initial={{ height: 0 }}
                whileInView={{ height: `${height}%` }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.8 }}
                whileHover={{ scale: 1.1 }}
              >
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity text-xs font-semibold text-white bg-slate-800 px-2 py-1 rounded">
                  {height}%
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default Analytics

