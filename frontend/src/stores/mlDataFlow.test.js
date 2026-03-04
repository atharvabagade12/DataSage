import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMLDataFlowStore } from './mlDataFlow'

describe('mlDataFlow Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with default state', () => {
    const store = useMLDataFlowStore()
    expect(store.dataset).toEqual([])
    expect(store.currentStep).toBe('upload')
    expect(store.isDirty).toBe(false)
  })

  it('sets dataset correctly', () => {
    const store = useMLDataFlowStore()
    const mockData = [{ col1: 1, col2: 'A' }, { col1: 2, col2: 'B' }]
    store.setDataset(mockData, 'test.csv', 'ds_123')

    expect(store.dataset).toEqual(mockData)
    expect(store.fileName).toBe('test.csv')
    expect(store.datasetId).toBe('ds_123')
    expect(store.columns.length).toBe(2)
  })

  it('detects column types correctly', () => {
    const store = useMLDataFlowStore()
    
    const numericValues = [1, 2, 3, 4, 5]
    const categoricalValues = ['A', 'B', 'C', 'A', 'B']
    
    expect(store.detectColumnType(numericValues)).toBe('numerical')
    expect(store.detectColumnType(categoricalValues)).toBe('categorical')
  })

  it('updates dataset after preprocessing', () => {
    const store = useMLDataFlowStore()
    const initialData = [{ a: 1 }]
    store.setDataset(initialData, 'old.csv', 'id1')
    
    const newData = [{ a: 1, b: 2 }]
    store.updateDataset(newData)
    
    expect(store.dataset).toEqual(newData)
    expect(store.preprocessed).toBe(true)
    expect(store.isDirty).toBe(true)
  })

  it('resets state correctly', () => {
    const store = useMLDataFlowStore()
    store.setDataset([{ a: 1 }], 'test.csv', 'id1')
    store.reset()
    
    expect(store.dataset).toEqual([])
    expect(store.datasetId).toBe('')
    expect(store.currentStep).toBe('upload')
  })
})
