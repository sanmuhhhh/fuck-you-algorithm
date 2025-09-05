<template>
  <div class="step-info">
    <div class="info-header">
      <h4>执行信息</h4>
    </div>
    
    <div v-if="!currentResult" class="no-execution">
      <el-empty description="暂无执行信息" size="small" />
    </div>
    
    <div v-else class="info-content">
      <!-- 执行结果摘要 -->
      <div class="result-summary">
        <div class="summary-item">
          <span class="label">算法:</span>
          <span class="value">{{ currentResult.algorithm_name }}</span>
        </div>
        <div class="summary-item">
          <span class="label">执行时间:</span>
          <span class="value">{{ (currentResult.execution_time * 1000).toFixed(2) }}ms</span>
        </div>
        <div class="summary-item">
          <span class="label">步骤数:</span>
          <span class="value">{{ totalSteps }}</span>
        </div>
      </div>

      <!-- 最终结果 -->
      <div class="final-result">
        <h5>最终结果</h5>
        <div class="result-content">
          <el-descriptions :column="2" size="small" border>
            <el-descriptions-item 
              v-for="(value, key) in currentResult.final_result" 
              :key="key"
              :label="formatLabel(key)"
            >
              {{ value }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>

      <!-- 当前步骤详情 -->
      <div v-if="currentStepData" class="current-step">
        <h5>当前步骤详情</h5>
        <div class="step-details">
          <el-descriptions :column="1" size="small" border>
            <el-descriptions-item label="步骤ID">
              {{ currentStepData.step_id + 1 }}
            </el-descriptions-item>
            <el-descriptions-item label="动作">
              <el-tag :type="getActionType(currentStepData.action)">
                {{ currentStepData.action }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="描述">
              {{ currentStepData.description }}
            </el-descriptions-item>
            <el-descriptions-item label="时间戳">
              {{ (currentStepData.timestamp * 1000).toFixed(2) }}ms
            </el-descriptions-item>
            <el-descriptions-item label="高亮索引">
              {{ currentStepData.highlight.join(', ') || '无' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>

      <!-- 性能指标 -->
      <div class="performance-metrics">
        <h5>性能指标</h5>
        <div class="metrics-grid">
          <div 
            v-for="(value, key) in currentResult.performance_metrics" 
            :key="key"
            class="metric-item"
          >
            <div class="metric-label">{{ formatLabel(key) }}</div>
            <div class="metric-value">{{ formatMetricValue(key, value) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { currentResult, currentStepData, totalSteps } = storeToRefs(algorithmStore)

const formatLabel = (key: string) => {
  const labelMap: Record<string, string> = {
    'num1': '数字1',
    'num2': '数字2',
    'result': '结果',
    'operation': '运算',
    'execution_time': '执行时间',
    'step_count': '步骤数量',
    'memory_usage': '内存使用'
  }
  return labelMap[key] || key
}

const formatMetricValue = (key: string, value: any) => {
  if (key === 'execution_time') {
    return `${(value * 1000).toFixed(2)}ms`
  }
  return value
}

const getActionType = (action: string) => {
  switch (action) {
    case 'initialize':
      return 'info'
    case 'calculate':
      return 'warning'
    case 'result':
      return 'success'
    case 'compare':
      return 'warning'
    case 'swap':
      return 'danger'
    default:
      return 'primary'
  }
}
</script>

<style scoped>
.step-info {
  border-top: 1px solid #e9ecef;
}

.info-header {
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
}

.info-header h4 {
  margin: 0;
  color: #333;
}

.no-execution {
  padding: 20px;
  text-align: center;
}

.info-content {
  padding: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.result-summary {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-item .label {
  font-size: 12px;
  color: #666;
}

.summary-item .value {
  font-weight: bold;
  color: #333;
}

.final-result,
.current-step,
.performance-metrics {
  margin-bottom: 20px;
}

.final-result h5,
.current-step h5,
.performance-metrics h5 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.metric-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  text-align: center;
}

.metric-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.metric-value {
  font-weight: bold;
  color: #333;
}
</style>