export interface AlgorithmStep {
  step_id: number
  action: string
  data_snapshot: Record<string, any>
  highlight: number[]
  description: string
  timestamp: number
}

export interface AlgorithmMetadata {
  name: string
  display_name: string
  category: string
  description: string
  complexity_time?: string
  complexity_space?: string
  author?: string
}

export interface AlgorithmResult {
  algorithm_name: string
  steps: AlgorithmStep[]
  final_result: any
  performance_metrics: Record<string, any>
  execution_time: number
  created_at: string
}

export interface AlgorithmConfig {
  name: string
  schema: Record<string, any>
}

export interface AlgorithmExecuteRequest {
  data: Record<string, any>
  config: Record<string, any>
}