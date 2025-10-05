// src/composables/useCharts.js
export const useChart = () => {
  const loadChart = async () => {
    try {
      console.log('🔄 Attempting to import Chart.js...')
      
      // Import Chart.js
      const ChartJS = await import('chart.js')
      console.log('✅ Chart.js module imported:', ChartJS)
      
      // Get the Chart constructor and registerables
      const { Chart, registerables } = ChartJS
      console.log('✅ Chart constructor:', Chart)
      console.log('✅ Registerables:', registerables)
      
      // Register all components
      Chart.register(...registerables)
      console.log('✅ Chart.js components registered')
      
      // Return the Chart constructor (not an instance)
      return Chart
      
    } catch (error) {
      console.error('❌ Failed to load Chart.js:', error)
      throw error
    }
  }
  
  return {
    loadChart
  }
}
