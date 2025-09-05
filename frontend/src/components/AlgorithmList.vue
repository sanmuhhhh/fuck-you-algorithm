<template>
  <div class="algorithm-list">
    <div class="list-header">
      <h3>可用算法</h3>
      <el-button 
        type="primary" 
        size="small" 
        @click="refreshList"
        :loading="loading"
        :icon="Refresh"
      >
        刷新
      </el-button>
    </div>

    <div class="list-content">
      <el-skeleton v-if="loading" :rows="5" animated />
      
      <el-alert
        v-else-if="error"
        :title="error"
        type="error"
        show-icon
        @close="clearError"
      />
      
      <div v-else-if="algorithms.length === 0" class="empty-state">
        <el-empty description="暂无可用算法" />
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
import { Refresh } from '@element-plus/icons-vue'
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
}

.list-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-header h3 {
  margin: 0;
  color: #333;
}

.list-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.algorithm-items {
  space-y: 8px;
}

.algorithm-item {
  padding: 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 8px;
}

.algorithm-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.algorithm-item.active {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.algorithm-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.algorithm-category {
  font-size: 12px;
  color: #409eff;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.algorithm-description {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  margin-bottom: 8px;
}

.algorithm-complexity {
  font-size: 12px;
  color: #909399;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}
</style>