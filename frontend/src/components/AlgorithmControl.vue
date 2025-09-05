<template>
  <div class="algorithm-control">
    <div class="control-section">
      <h4>参数配置</h4>
      <div class="config-form">
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
      
      <div class="action-buttons">
        <el-button 
          type="primary" 
          @click="executeAlgorithm"
          :loading="loading"
          :icon="Play"
        >
          执行算法
        </el-button>
        <el-button @click="resetConfig" :icon="Refresh">
          重置参数
        </el-button>
      </div>
    </div>

    <div v-if="currentResult" class="control-section">
      <h4>播放控制</h4>
      <div class="playback-controls">
        <el-button-group>
          <el-button 
            @click="reset" 
            :icon="RefreshLeft"
            :disabled="totalSteps === 0"
          >
            重置
          </el-button>
          <el-button 
            @click="prevStep" 
            :icon="ArrowLeft"
            :disabled="!hasPrevStep"
          >
            上一步
          </el-button>
          <el-button 
            @click="isPlaying ? pause() : play()" 
            :icon="isPlaying ? VideoPause : VideoPlay"
            type="primary"
            :disabled="totalSteps === 0"
          >
            {{ isPlaying ? '暂停' : '播放' }}
          </el-button>
          <el-button 
            @click="nextStep" 
            :icon="ArrowRight"
            :disabled="!hasNextStep"
          >
            下一步
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { 
  Play, 
  Refresh, 
  RefreshLeft, 
  ArrowLeft, 
  ArrowRight,
  VideoPlay,
  VideoPause
} from '@element-plus/icons-vue'
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { 
  currentResult, 
  currentStep, 
  totalSteps,
  hasNextStep,
  hasPrevStep,
  isPlaying,
  loading 
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

// 配置表单
const configForm = reactive({
  num1: 1,
  num2: 1,
  show_steps: true
})

const executeAlgorithm = async () => {
  await storeExecuteAlgorithm(
    { num1: configForm.num1, num2: configForm.num2 },
    { 
      num1: configForm.num1, 
      num2: configForm.num2,
      show_steps: configForm.show_steps 
    }
  )
}

const resetConfig = () => {
  configForm.num1 = 1
  configForm.num2 = 1
  configForm.show_steps = true
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
</style>