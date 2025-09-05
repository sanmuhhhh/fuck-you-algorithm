<template>
  <div class="algorithm-visualization">
    <div class="visualization-header">
      <h4>算法可视化</h4>
    </div>
    
    <div class="visualization-content">
      <div v-if="!currentResult" class="empty-visualization">
        <el-empty description="请先执行算法以查看可视化效果" />
      </div>
      
      <div v-else class="visualization-display">
        <!-- Hello World 算法特定的可视化 -->
        <div v-if="currentAlgorithm?.name === 'hello_world'" class="hello-world-viz">
          <div class="calculation-display">
            <div class="numbers">
              <div 
                class="number-box"
                :class="{ highlighted: isHighlighted(0) }"
              >
                <div class="number-label">数字1</div>
                <div class="number-value">{{ currentStepData?.data_snapshot?.num1 || 0 }}</div>
              </div>
              
              <div class="operator">
                <div class="operator-symbol">+</div>
              </div>
              
              <div 
                class="number-box"
                :class="{ highlighted: isHighlighted(1) }"
              >
                <div class="number-label">数字2</div>
                <div class="number-value">{{ currentStepData?.data_snapshot?.num2 || 0 }}</div>
              </div>
              
              <div class="equals">
                <div class="equals-symbol">=</div>
              </div>
              
              <div 
                class="result-box"
                :class="{ 
                  highlighted: isHighlighted(2),
                  'has-result': currentStepData?.data_snapshot?.result !== null 
                }"
              >
                <div class="result-label">结果</div>
                <div class="result-value">
                  {{ currentStepData?.data_snapshot?.result || '?' }}
                </div>
              </div>
            </div>
            
            <div class="calculation-steps">
              <div class="current-action">
                <el-tag 
                  v-if="currentStepData"
                  :type="getActionType(currentStepData.action)"
                  size="large"
                >
                  {{ currentStepData.description }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 通用可视化 (为其他算法准备) -->
        <div v-else class="generic-visualization">
          <div class="data-snapshot">
            <h5>当前数据状态</h5>
            <pre>{{ JSON.stringify(currentStepData?.data_snapshot, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { currentResult, currentStepData, currentAlgorithm } = storeToRefs(algorithmStore)

const isHighlighted = (index: number) => {
  return currentStepData.value?.highlight?.includes(index) || false
}

const getActionType = (action: string) => {
  switch (action) {
    case 'initialize':
      return 'info'
    case 'calculate':
      return 'warning'
    case 'result':
      return 'success'
    default:
      return 'primary'
  }
}
</script>

<style scoped>
.algorithm-visualization {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.visualization-header {
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
}

.visualization-header h4 {
  margin: 0;
  color: #333;
}

.visualization-content {
  flex: 1;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-visualization {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.visualization-display {
  width: 100%;
  height: 100%;
}

/* Hello World 特定样式 */
.hello-world-viz {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.calculation-display {
  text-align: center;
}

.numbers {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
}

.number-box, .result-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  min-width: 80px;
  transition: all 0.3s ease;
  background: white;
}

.number-box.highlighted, .result-box.highlighted {
  border-color: #409eff;
  background: #f0f9ff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.result-box.has-result {
  border-color: #67c23a;
  background: #f0f9e8;
}

.number-label, .result-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.number-value, .result-value {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
}

.operator, .equals {
  display: flex;
  align-items: center;
  justify-content: center;
}

.operator-symbol, .equals-symbol {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  padding: 10px;
  border-radius: 50%;
  background: #f0f9ff;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calculation-steps {
  margin-top: 20px;
}

.current-action {
  font-size: 16px;
}

/* 通用可视化样式 */
.generic-visualization {
  width: 100%;
}

.data-snapshot {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
}

.data-snapshot h5 {
  margin: 0 0 12px 0;
  color: #333;
}

.data-snapshot pre {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 12px;
  margin: 0;
  overflow-x: auto;
  font-size: 14px;
}
</style>