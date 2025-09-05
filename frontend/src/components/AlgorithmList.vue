<template>
  <div class="algorithm-list">
    <div class="list-header">
      <h3>可用算法</h3>
      <el-button 
        type="primary" 
        size="small" 
        @click="refreshList"
        :loading="loading"
      >
        刷新
      </el-button>
    </div>

    <div class="list-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-skeleton">
          <div v-for="i in 3" :key="i" class="skeleton-item">
            <div class="skeleton-header"></div>
            <div class="skeleton-lines">
              <div class="skeleton-line short"></div>
              <div class="skeleton-line long"></div>
              <div class="skeleton-line medium"></div>
            </div>
          </div>
        </div>
        <div class="loading-text">
          <span class="loading-icon">⏳</span>
          正在加载算法列表...
        </div>
      </div>
      
      <!-- 错误状态 -->
      <div v-else-if="error" class="error-state">
        <el-alert
          :title="error"
          type="error"
          show-icon
          effect="dark"
          @close="clearError"
        >
          <template #default>
            <p>无法加载算法列表，请检查网络连接或联系管理员。</p>
            <el-button type="primary" size="small" @click="refreshList">
              🔄 重试
            </el-button>
          </template>
        </el-alert>
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="algorithms.length === 0" class="empty-state">
        <el-empty description="暂无可用算法" image-size="120">
          <template #description>
            <p>目前还没有可用的算法</p>
            <p>请稍后再试或联系管理员添加算法</p>
          </template>
          <el-button type="primary" @click="refreshList">
            🔄 刷新列表
          </el-button>
        </el-empty>
      </div>
      
      <div v-else class="algorithm-items">
        <div
          v-for="algorithm in algorithms"
          :key="algorithm.name"
          class="algorithm-item"
          :class="{ active: currentAlgorithm?.name === algorithm.name }"
          @click="selectAlgorithm(algorithm)"
        >
          <div class="algorithm-info">
            <div class="algorithm-name">{{ algorithm.display_name }}</div>
            <div class="algorithm-category">{{ algorithm.category }}</div>
            <div class="algorithm-description">{{ algorithm.description }}</div>
            <div v-if="algorithm.complexity_time" class="algorithm-complexity">
              时间复杂度: {{ algorithm.complexity_time }}
            </div>
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
const { algorithms, currentAlgorithm, loading, error } = storeToRefs(algorithmStore)
const { fetchAlgorithms, selectAlgorithm, clearError } = algorithmStore

const refreshList = () => {
  fetchAlgorithms()
}
</script>

<style scoped>
.algorithm-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.list-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  backdrop-filter: blur(10px);
}

.list-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.list-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.algorithm-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.algorithm-item {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.algorithm-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.algorithm-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #409eff;
}

.algorithm-item:hover::before {
  transform: scaleX(1);
}

.algorithm-item.active {
  border-color: #409eff;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(64, 158, 255, 0.05) 100%);
  box-shadow: 0 4px 20px rgba(64, 158, 255, 0.2);
}

.algorithm-item.active::before {
  transform: scaleX(1);
}

.algorithm-name {
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  font-size: 16px;
  letter-spacing: 0.5px;
}

.algorithm-category {
  display: inline-block;
  font-size: 11px;
  color: white;
  background: linear-gradient(45deg, #409eff, #67c23a);
  text-transform: uppercase;
  padding: 4px 8px;
  border-radius: 12px;
  margin-bottom: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.algorithm-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  text-align: justify;
}

.algorithm-complexity {
  font-size: 12px;
  color: #909399;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 4px 8px;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

/* 加载状态样式 */
.loading-state {
  padding: 20px;
}

.loading-skeleton {
  margin-bottom: 20px;
}

.skeleton-item {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  backdrop-filter: blur(10px);
}

.skeleton-header {
  height: 20px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 12px;
  width: 60%;
}

.skeleton-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.skeleton-line.short {
  width: 40%;
}

.skeleton-line.medium {
  width: 70%;
}

.skeleton-line.long {
  width: 90%;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  padding: 16px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 错误状态样式 */
.error-state {
  padding: 20px;
}

.error-state .el-alert {
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.error-state .el-alert p {
  margin: 8px 0;
  color: #666;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.empty-state :deep(.el-empty) {
  padding: 40px 20px;
}

.empty-state :deep(.el-empty__description) {
  margin: 16px 0;
}

.empty-state :deep(.el-empty__description p) {
  margin: 4px 0;
  color: #666;
  line-height: 1.5;
}

/* 滚动条样式 */
.list-content::-webkit-scrollbar {
  width: 6px;
}

.list-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.list-content::-webkit-scrollbar-thumb {
  background: rgba(64, 158, 255, 0.3);
  border-radius: 3px;
}

.list-content::-webkit-scrollbar-thumb:hover {
  background: rgba(64, 158, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .list-header {
    padding: 16px;
  }
  
  .list-content {
    padding: 12px;
  }
  
  .algorithm-item {
    padding: 16px;
  }
  
  .algorithm-name {
    font-size: 15px;
  }
  
  .algorithm-description {
    font-size: 13px;
  }
}
</style>