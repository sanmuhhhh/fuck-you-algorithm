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
            🔄 刷新算法列表
          </el-button>
        </template>
      </el-result>
    </div>

    <div v-else class="workspace-content">
      <!-- 算法信息头部 - 紧凑版 -->
      <div class="algorithm-header">
        <div class="algorithm-title">
          <h2>{{ currentAlgorithm.display_name }}</h2>
          <el-tag type="primary">{{ currentAlgorithm.category }}</el-tag>
        </div>
        <div class="algorithm-meta">
          <span class="algorithm-desc">{{ currentAlgorithm.description }}</span>
          <div v-if="currentAlgorithm.complexity_time" class="complexity-info">
            <span>{{ currentAlgorithm.complexity_time }}</span>
            <span v-if="currentAlgorithm.complexity_space">{{ currentAlgorithm.complexity_space }}</span>
          </div>
        </div>
      </div>

      <!-- 主工作区 - 网格布局 -->
      <div class="main-workspace">
        <!-- 左侧：控制面板 -->
        <div class="control-panel">
          <AlgorithmControl />
        </div>

        <!-- 右侧：可视化区域 -->
        <div class="visualization-area">
          <AlgorithmVisualization />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
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
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  margin: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.workspace-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.algorithm-header {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.algorithm-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.algorithm-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.algorithm-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.algorithm-title h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.algorithm-desc {
  color: #666;
  margin: 0;
  line-height: 1.5;
  font-size: 14px;
  flex: 1;
}

.complexity-info {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 6px 12px;
  border-radius: 6px;
  border-left: 3px solid #409eff;
  white-space: nowrap;
}

/* 主工作区网格布局 */
.main-workspace {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-template-rows: 1fr;
  gap: 16px;
  min-height: 0;
}

.control-panel {
  grid-column: 1;
  grid-row: 1;
  background: rgba(255, 255, 255, 0.95);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow-y: auto;
}

.visualization-area {
  grid-column: 2;
  grid-row: 1;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  transition: all 0.3s ease;
  min-height: 400px;
}

.visualization-area:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

/* .step-info 样式已移除，执行信息已整合到控制面板 */

.ml-4 {
  margin-left: 16px;
}

/* Element Plus组件样式覆盖 */
:deep(.el-result) {
  background: transparent;
  padding: 40px 20px;
}

:deep(.el-result__title) {
  color: #333;
  font-weight: 600;
}

:deep(.el-result__subtitle) {
  color: #666;
  margin-top: 8px;
}

:deep(.el-tag) {
  background: linear-gradient(45deg, #409eff, #67c23a);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-workspace {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    gap: 12px;
  }
  
  .control-panel {
    grid-column: 1;
    grid-row: 1;
    max-height: none;
  }
  
  .visualization-area {
    grid-column: 1;
    grid-row: 2;
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .workspace-content {
    gap: 12px;
  }
  
  .algorithm-header {
    padding: 12px 16px;
  }
  
  .algorithm-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .algorithm-title h2 {
    font-size: 18px;
  }
  
  .algorithm-desc {
    font-size: 13px;
  }
  
  .complexity-info {
    flex-direction: column;
    gap: 6px;
    font-size: 11px;
  }
  
  .control-panel {
    padding: 12px;
  }
  
  .visualization-area {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .welcome-state {
    margin: 10px;
  }
  
  .algorithm-title {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>