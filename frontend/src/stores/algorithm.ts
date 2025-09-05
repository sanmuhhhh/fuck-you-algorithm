import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AlgorithmMetadata, AlgorithmResult, AlgorithmStep } from '@/types/algorithm'
import { algorithmApi } from '@/utils/api'

export const useAlgorithmStore = defineStore('algorithm', () => {
  // 状态
  const algorithms = ref<AlgorithmMetadata[]>([])
  const currentAlgorithm = ref<AlgorithmMetadata | null>(null)
  const currentResult = ref<AlgorithmResult | null>(null)
  const currentStep = ref(0)
  const isPlaying = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const steps = computed(() => currentResult.value?.steps || [])
  const totalSteps = computed(() => steps.value.length)
  const currentStepData = computed(() => steps.value[currentStep.value] || null)
  const hasNextStep = computed(() => currentStep.value < totalSteps.value - 1)
  const hasPrevStep = computed(() => currentStep.value > 0)

  // 动作
  const fetchAlgorithms = async () => {
    try {
      loading.value = true
      error.value = null
      const response = await algorithmApi.getAlgorithms()
      algorithms.value = response.algorithms
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取算法列表失败'
    } finally {
      loading.value = false
    }
  }

  const selectAlgorithm = (algorithm: AlgorithmMetadata) => {
    currentAlgorithm.value = algorithm
    currentResult.value = null
    currentStep.value = 0
    isPlaying.value = false
  }

  const executeAlgorithm = async (data: Record<string, any>, config: Record<string, any> = {}) => {
    if (!currentAlgorithm.value) return

    try {
      loading.value = true
      error.value = null
      
      const result = await algorithmApi.executeAlgorithm(
        currentAlgorithm.value.name,
        { data, config }
      )
      
      currentResult.value = result
      currentStep.value = 0
      isPlaying.value = false
    } catch (err) {
      error.value = err instanceof Error ? err.message : '算法执行失败'
    } finally {
      loading.value = false
    }
  }

  const nextStep = () => {
    if (hasNextStep.value) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (hasPrevStep.value) {
      currentStep.value--
    }
  }

  const goToStep = (stepIndex: number) => {
    if (stepIndex >= 0 && stepIndex < totalSteps.value) {
      currentStep.value = stepIndex
    }
  }

  const play = () => {
    isPlaying.value = true
    const timer = setInterval(() => {
      if (hasNextStep.value) {
        nextStep()
      } else {
        isPlaying.value = false
        clearInterval(timer)
      }
    }, 200) // 每200毫秒一步，更快的播放速度
  }

  const pause = () => {
    isPlaying.value = false
  }

  const reset = () => {
    currentStep.value = 0
    isPlaying.value = false
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // 状态
    algorithms,
    currentAlgorithm,
    currentResult,
    currentStep,
    isPlaying,
    loading,
    error,
    
    // 计算属性
    steps,
    totalSteps,
    currentStepData,
    hasNextStep,
    hasPrevStep,
    
    // 动作
    fetchAlgorithms,
    selectAlgorithm,
    executeAlgorithm,
    nextStep,
    prevStep,
    goToStep,
    play,
    pause,
    reset,
    clearError,
  }
})