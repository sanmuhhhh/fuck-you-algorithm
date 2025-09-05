<template>
  <div class="algorithm-control">
    <div class="control-section">
      <h4>参数配置</h4>
      <!-- Hello World 配置 -->
      <div v-if="currentAlgorithm?.name === 'hello_world'" class="config-form">
        <el-form :model="configForm" label-width="80px" size="small">
          <el-form-item label="数字1">
            <el-input-number 
              v-model="configForm.num1" 
              :min="0" 
              :max="100" 
              :step="1"
            />
          </el-form-item>
          <el-form-item label="数字2">
            <el-input-number 
              v-model="configForm.num2" 
              :min="0" 
              :max="100" 
              :step="1"
            />
          </el-form-item>
          <el-form-item label="显示步骤">
            <el-switch v-model="configForm.show_steps" />
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 冒泡排序配置 -->
      <div v-else-if="currentAlgorithm?.name === 'bubble_sort'" class="config-form">
        <el-form :model="sortConfigForm" label-width="80px" size="small">
          <el-form-item label="数组">
            <el-input 
              v-model="arrayInput" 
              placeholder="输入数字，用逗号分隔"
              @blur="updateArrayFromInput"
            />
          </el-form-item>
          <el-form-item label="数组长度">
            <el-input-number 
              v-model="arrayLength" 
              :min="5" 
              :max="30" 
              @change="generateRandomArray"
            />
          </el-form-item>
          <el-form-item label="动画速度">
            <el-slider
              v-model="sortConfigForm.animation_speed"
              :min="100"
              :max="2000"
              :step="100"
              show-input
              input-size="small"
            />
          </el-form-item>
          <el-form-item label="显示比较">
            <el-switch v-model="sortConfigForm.show_comparisons" />
          </el-form-item>
          <el-form-item label="显示交换">
            <el-switch v-model="sortConfigForm.show_swaps" />
          </el-form-item>
        </el-form>
      </div>
      
      <div class="action-buttons">
        <el-button 
          type="primary" 
          @click="executeAlgorithm"
          :loading="loading"
        >
          ▶️ 执行算法
        </el-button>
        <el-button @click="resetConfig">
          🔄 重置参数
        </el-button>
      </div>
    </div>

    <div v-if="currentResult" class="control-section">
      <h4>播放控制</h4>
      <div class="playback-controls">
        <el-button-group>
          <el-button 
            @click="reset" 
            :disabled="totalSteps === 0"
          >
            🔄 重置
          </el-button>
          <el-button 
            @click="prevStep" 
            :disabled="!hasPrevStep"
          >
            ⬅️ 上一步
          </el-button>
          <el-button 
            @click="isPlaying ? pause() : play()" 
            type="primary"
            :disabled="totalSteps === 0"
          >
            {{ isPlaying ? '⏸️ 暂停' : '▶️ 播放' }}
          </el-button>
          <el-button 
            @click="nextStep" 
            :disabled="!hasNextStep"
          >
            ➡️ 下一步
          </el-button>
        </el-button-group>
      </div>
      
      <div class="step-slider">
        <el-slider
          v-model="currentStep"
          :min="0"
          :max="Math.max(0, totalSteps - 1)"
          :step="1"
          :disabled="totalSteps === 0"
          @change="goToStep"
          show-stops
        />
        <div class="step-info-text">
          步骤: {{ currentStep + 1 }} / {{ totalSteps }}
        </div>
      </div>
      
      <!-- 执行信息 -->
      <div class="execution-info">
        <h5>📊 执行统计</h5>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">执行时间:</span>
            <span class="stat-value">{{ currentResult?.execution_time?.toFixed(2) || 0 }}ms</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总步骤:</span>
            <span class="stat-value">{{ totalSteps }}</span>
          </div>
          <template v-if="currentStepData?.data_snapshot">
            <div class="stat-item">
              <span class="stat-label">比较次数:</span>
              <span class="stat-value">{{ currentStepData.data_snapshot.performance?.comparisons || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">交换次数:</span>
              <span class="stat-value">{{ currentStepData.data_snapshot.performance?.swaps || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">当前轮次:</span>
              <span class="stat-value">{{ currentStepData.data_snapshot.current_pass || 0 }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { storeToRefs } from 'pinia'
// 不再使用图标导入
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { 
  currentResult, 
  currentStep, 
  currentStepData,
  totalSteps,
  hasNextStep,
  hasPrevStep,
  isPlaying,
  loading,
  currentAlgorithm
} = storeToRefs(algorithmStore)

const { 
  executeAlgorithm: storeExecuteAlgorithm,
  nextStep,
  prevStep,
  goToStep,
  play,
  pause,
  reset
} = algorithmStore

// Hello World 配置表单
const configForm = reactive({
  num1: 1,
  num2: 1,
  show_steps: true
})

// 冒泡排序配置表单
const sortConfigForm = reactive({
  array: [89, 34, 67, 23, 78, 45, 12, 56, 91, 38, 72, 15, 84, 29, 63],
  animation_speed: 300,
  show_comparisons: true,
  show_swaps: true
})

// 数组输入和长度控制
const arrayInput = ref('89, 34, 67, 23, 78, 45, 12, 56, 91, 38, 72, 15, 84, 29, 63')
const arrayLength = ref(15)

// 从输入更新数组
const updateArrayFromInput = () => {
  try {
    const numbers = arrayInput.value
      .split(',')
      .map(s => parseInt(s.trim()))
      .filter(n => !isNaN(n))
    
    if (numbers.length >= 2) {
      sortConfigForm.array = numbers
      arrayLength.value = numbers.length
    }
  } catch (error) {
    console.error('Invalid array input:', error)
  }
}

// 生成随机数组
const generateRandomArray = () => {
  const length = arrayLength.value
  const array = Array.from({ length }, () => Math.floor(Math.random() * 100) + 1)
  sortConfigForm.array = array
  arrayInput.value = array.join(', ')
}

// 执行算法
const executeAlgorithm = async () => {
  if (currentAlgorithm.value?.name === 'hello_world') {
    await storeExecuteAlgorithm(
      { num1: configForm.num1, num2: configForm.num2 },
      { 
        num1: configForm.num1, 
        num2: configForm.num2,
        show_steps: configForm.show_steps 
      }
    )
  } else if (currentAlgorithm.value?.name === 'bubble_sort') {
    await storeExecuteAlgorithm(
      { array: sortConfigForm.array },
      {
        animation_speed: sortConfigForm.animation_speed,
        show_comparisons: sortConfigForm.show_comparisons,
        show_swaps: sortConfigForm.show_swaps
      }
    )
  }
}

// 重置配置
const resetConfig = () => {
  if (currentAlgorithm.value?.name === 'hello_world') {
    configForm.num1 = 1
    configForm.num2 = 1
    configForm.show_steps = true
  } else if (currentAlgorithm.value?.name === 'bubble_sort') {
    sortConfigForm.array = [64, 34, 25, 12, 22, 11, 90]
    sortConfigForm.animation_speed = 500
    sortConfigForm.show_comparisons = true
    sortConfigForm.show_swaps = true
    arrayInput.value = '64, 34, 25, 12, 22, 11, 90'
    arrayLength.value = 7
  }
}
</script>

<style scoped>
.algorithm-control {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-section {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 16px;
}

.control-section h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
}

.config-form {
  margin-bottom: 16px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.playback-controls {
  margin-bottom: 16px;
}

.step-slider {
  margin-top: 16px;
}

.step-info-text {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 8px;
}

.execution-info {
  margin-top: 20px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.execution-info h5 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 6px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #f0f0f0;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.stat-value {
  font-size: 12px;
  color: #409eff;
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}
</style>