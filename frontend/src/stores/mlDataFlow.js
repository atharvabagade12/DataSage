// ✅ COMPLETE ML DATA FLOW STORE
import { defineStore } from 'pinia'

export const useMLDataFlowStore = defineStore('mlDataFlow', {
  state: () => ({
    backendConnected: false,
    backendStatus: null,
    currentDataset: null,
    registeredDatasets: new Map()
  }),
  
  actions: {
    async checkBackendConnection() {
      try {
        console.log('🔌 Checking backend connection...')
        
        const response = await fetch('http://localhost:8000/api/health', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        
        if (response.ok) {
          this.backendStatus = await response.json()
          this.backendConnected = true
          console.log('✅ Backend connected:', this.backendStatus.message)
          return true
        } else {
          throw new Error(`Backend returned ${response.status}`)
        }
      } catch (error) {
        console.error('❌ Backend connection failed:', error.message)
        this.backendConnected = false
        this.backendStatus = null
        return false
      }
    },
    
    async registerDataset(datasetInfo) {
      try {
        console.log('📝 Registering dataset:', datasetInfo.dataset_id)
        
        this.registeredDatasets.set(datasetInfo.dataset_id, {
          id: datasetInfo.dataset_id,
          filename: datasetInfo.filename,
          shape: datasetInfo.shape,
          columns: datasetInfo.columns,
          uploadTime: datasetInfo.upload_time,
          registered: new Date().toISOString()
        })
        
        this.currentDataset = datasetInfo.dataset_id
        console.log('✅ Dataset registered successfully')
        
      } catch (error) {
        console.error('❌ Failed to register dataset:', error)
      }
    },
    
    async verifyDatasetInBackend(datasetId = null) {
      if (!this.backendConnected) return false
      
      const targetId = datasetId || this.currentDataset
      if (!targetId) return false
      
      try {
        const response = await fetch(`http://localhost:8000/api/datasets/${targetId}`)
        return response.ok
      } catch (error) {
        console.error('Backend verification failed:', error)
        return false
      }
    }
  }
})
