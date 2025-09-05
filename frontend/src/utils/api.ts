import axios from 'axios'
import type { 
  AlgorithmMetadata, 
  AlgorithmResult, 
  AlgorithmConfig,
  AlgorithmExecuteRequest 
} from '@/types/algorithm'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const algorithmApi = {
  // 获取算法列表
  getAlgorithms: (): Promise<{ algorithms: AlgorithmMetadata[], total: number }> => {
    return api.get('/algorithms')
  },

  // 获取算法配置
  getAlgorithmConfig: (name: string): Promise<AlgorithmConfig> => {
    return api.get(`/algorithms/${name}/config`)
  },

  // 执行算法
  executeAlgorithm: (name: string, request: AlgorithmExecuteRequest): Promise<AlgorithmResult> => {
    return api.post(`/algorithms/${name}/execute`, request)
  },

  // 获取算法元数据
  getAlgorithmMetadata: (name: string): Promise<AlgorithmMetadata> => {
    return api.get(`/algorithms/${name}/metadata`)
  },
}

export default api