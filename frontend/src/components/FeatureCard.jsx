import { motion } from 'framer-motion'

const FeatureCard = ({ icon, title, description, delay = 0 }) => {
  return (
    <motion.div
      className="glass rounded-2xl p-8 hover-lift glow-effect group"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.6 }}
      whileHover={{ scale: 1.02 }}
      data-cursor="pointer"
    >
      <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-2xl font-display font-bold text-white mb-4">
        {title}
      </h3>
      <p className="text-slate-300 leading-relaxed">{description}</p>
    </motion.div>
  )
}

export default FeatureCard

