<template>
  <div class="algorithm-workspace">
    <div v-if="!currentAlgorithm" class="welcome-state">
      <el-result
        icon="info"
        title="欢迎使用算法可视化平台"
        sub-title="请从左侧选择一个算法开始体验"
      >
        <template #extra>
          <el-button type="primary" @click="refreshAlgorithms">
            <el-icon><Refresh /></el-icon>
            刷新算法列表
          </el-button>
        </template>
      </el-result>
    </div>

    <div v-else class="workspace-content">
      <!-- 算法信息头部 -->
      <div class="algorithm-header">
        <div class="algorithm-title">
          <h2>{{ currentAlgorithm.display_name }}</h2>
          <el-tag type="primary">{{ currentAlgorithm.category }}</el-tag>
        </div>
        <p class="algorithm-desc">{{ currentAlgorithm.description }}</p>
        <div v-if="currentAlgorithm.complexity_time" class="complexity-info">
          <span>时间复杂度: {{ currentAlgorithm.complexity_time }}</span>
          <span v-if="currentAlgorithm.complexity_space" class="ml-4">
            空间复杂度: {{ currentAlgorithm.complexity_space }}
          </span>
        </div>
      </div>

      <!-- 控制面板 -->
      <div class="control-panel">
        <AlgorithmControl />
      </div>

      <!-- 可视化区域 -->
      <div class="visualization-area">
        <AlgorithmVisualization />
      </div>

      <!-- 步骤信息 -->
      <div class="step-info">
        <StepInfo />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { Refresh } from '@element-plus/icons-vue'
import { useAlgorithmStore } from '@/stores/algorithm'
import AlgorithmControl from './AlgorithmControl.vue'
import AlgorithmVisualization from './AlgorithmVisualization.vue'
import StepInfo from './StepInfo.vue'

const algorithmStore = useAlgorithmStore()
const { currentAlgorithm } = storeToRefs(algorithmStore)
const { fetchAlgorithms } = algorithmStore

const refreshAlgorithms = () => {
  fetchAlgorithms()
}
</script>

<style scoped>
.algorithm-workspace {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.welcome-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.workspace-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.algorithm-header {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.algorithm-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.algorithm-title h2 {
  margin: 0;
  color: #333;
}

.algorithm-desc {
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.complexity-info {
  font-size: 14px;
  color: #909399;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
}

.control-panel {
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.visualization-area {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-height: 400px;
}

.step-info {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ml-4 {
  margin-left: 16px;
}
</style>