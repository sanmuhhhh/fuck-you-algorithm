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
            <!-- 进度指示器 -->
            <div class="progress-indicator">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: progressPercentage + '%' }"
                ></div>
              </div>
              <div class="progress-text">
                执行进度: {{ Math.round(progressPercentage) }}%
              </div>
            </div>
            
            <div class="numbers">
              <div 
                class="number-box"
                :class="{ 
                  highlighted: isHighlighted(0),
                  processing: isProcessing(0),
                  completed: isCompleted(0)
                }"
              >
                <div class="number-label">数字1</div>
                <div class="number-value">{{ currentStepData?.data_snapshot?.num1 || 0 }}</div>
                <div v-if="isHighlighted(0)" class="highlight-effect"></div>
              </div>
              
              <div class="operator" :class="{ active: isCalculating }">
                <div class="operator-symbol">+</div>
                <div v-if="isCalculating" class="calculation-ripple"></div>
              </div>
              
              <div 
                class="number-box"
                :class="{ 
                  highlighted: isHighlighted(1),
                  processing: isProcessing(1),
                  completed: isCompleted(1)
                }"
              >
                <div class="number-label">数字2</div>
                <div class="number-value">{{ currentStepData?.data_snapshot?.num2 || 0 }}</div>
                <div v-if="isHighlighted(1)" class="highlight-effect"></div>
              </div>
              
              <div class="equals" :class="{ active: isCalculating }">
                <div class="equals-symbol">=</div>
              </div>
              
              <div 
                class="result-box"
                :class="{ 
                  highlighted: isHighlighted(2),
                  'has-result': currentStepData?.data_snapshot?.result !== null,
                  processing: isProcessing(2),
                  completed: isCompleted(2)
                }"
              >
                <div class="result-label">结果</div>
                <div class="result-value">
                  <transition name="result-fade" mode="out-in">
                    <span :key="currentStepData?.data_snapshot?.result">
                      {{ currentStepData?.data_snapshot?.result || '?' }}
                    </span>
                  </transition>
                </div>
                <div v-if="isHighlighted(2)" class="highlight-effect success"></div>
              </div>
            </div>
            
            <div class="calculation-steps">
              <div class="current-action">
                <transition name="action-slide" mode="out-in">
                  <el-tag 
                    v-if="currentStepData"
                    :key="currentStepData.step_id"
                    :type="getActionType(currentStepData.action)"
                    size="large"
                    effect="dark"
                  >
                    <span v-if="currentStepData.action === 'calculate'">⚡</span>
                    <span v-else-if="currentStepData.action === 'result'">✅</span>
                    <span v-else>ℹ️</span>
                    {{ currentStepData.description }}
                  </el-tag>
                </transition>
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
// 不再使用图标导入
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { currentResult, currentStepData, currentAlgorithm, currentStep, totalSteps } = storeToRefs(algorithmStore)

const isHighlighted = (index: number) => {
  return currentStepData.value?.highlight?.includes(index) || false
}

const isProcessing = (index: number) => {
  return currentStepData.value?.action === 'calculate' && isHighlighted(index)
}

const isCompleted = (index: number) => {
  return currentStepData.value?.action === 'result' && currentStepData.value?.data_snapshot?.result !== null
}

const isCalculating = computed(() => {
  return currentStepData.value?.action === 'calculate'
})

const progressPercentage = computed(() => {
  if (!totalSteps.value || totalSteps.value === 0) return 0
  return ((currentStep.value + 1) / totalSteps.value) * 100
})

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
  padding: 20px;
}

.calculation-display {
  text-align: center;
  width: 100%;
  max-width: 800px;
}

/* 进度指示器样式 */
.progress-indicator {
  margin-bottom: 40px;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff 0%, #67c23a 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-text {
  font-size: 14px;
  color: #666;
  font-weight: 600;
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
  position: relative;
  overflow: hidden;
}

.number-box.highlighted, .result-box.highlighted {
  border-color: #409eff;
  background: #f0f9ff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  transform: scale(1.05);
}

.number-box.processing, .result-box.processing {
  border-color: #e6a23c;
  background: #fdf6ec;
  animation: pulse-border 1s infinite;
}

.number-box.completed, .result-box.completed {
  border-color: #67c23a;
  background: #f0f9e8;
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
}

.result-box.has-result {
  border-color: #67c23a;
  background: #f0f9e8;
}

@keyframes pulse-border {
  0%, 100% { border-color: #e6a23c; }
  50% { border-color: #f56c6c; }
}

/* 高亮效果 */
.highlight-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.2) 0%, transparent 70%);
  animation: highlight-pulse 1.5s infinite;
  pointer-events: none;
}

.highlight-effect.success {
  background: radial-gradient(circle, rgba(103, 194, 58, 0.2) 0%, transparent 70%);
}

@keyframes highlight-pulse {
  0%, 100% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1); }
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
  position: relative;
  transition: all 0.3s ease;
}

.operator.active, .equals.active {
  transform: scale(1.1);
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
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.operator.active .operator-symbol,
.equals.active .equals-symbol {
  background: linear-gradient(45deg, #409eff, #67c23a);
  color: white;
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.4);
}

/* 计算涟漪效果 */
.calculation-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  background: rgba(64, 158, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ripple 1s infinite;
}

@keyframes ripple {
  0% {
    width: 20px;
    height: 20px;
    opacity: 1;
  }
  100% {
    width: 100px;
    height: 100px;
    opacity: 0;
  }
}

/* 过渡动画 */
.result-fade-enter-active,
.result-fade-leave-active {
  transition: all 0.5s ease;
}

.result-fade-enter-from {
  opacity: 0;
  transform: scale(0.8) rotateY(90deg);
}

.result-fade-leave-to {
  opacity: 0;
  transform: scale(1.2) rotateY(-90deg);
}

.action-slide-enter-active,
.action-slide-leave-active {
  transition: all 0.4s ease;
}

.action-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.action-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(1.1);
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