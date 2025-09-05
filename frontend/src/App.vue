<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 头部导航 -->
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">
            🚀 Algorithm Visualization Platform
          </h1>
          <div class="header-subtitle">可扩展的算法可视化平台</div>
        </div>
      </el-header>

      <!-- 主体内容 -->
      <el-container>
        <!-- 侧边栏 - 算法列表 -->
        <el-aside width="300px" class="sidebar">
          <AlgorithmList />
        </el-aside>

        <!-- 主要工作区 -->
        <el-main class="main-content">
          <AlgorithmWorkspace />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AlgorithmList from '@/components/AlgorithmList.vue'
import AlgorithmWorkspace from '@/components/AlgorithmWorkspace.vue'
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()

onMounted(() => {
  // 初始化时获取算法列表
  algorithmStore.fetchAlgorithms()
})
</script>

<style scoped>
.app-container {
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 100;
}

.header-content {
  width: 100%;
  padding: 0 20px;
}

.app-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.app-title .el-icon {
  font-size: 32px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.header-subtitle {
  font-size: 15px;
  opacity: 0.95;
  margin-top: 6px;
  font-weight: 400;
  letter-spacing: 0.5px;
}

.sidebar {
  background: rgba(255, 255, 255, 0.95);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  backdrop-filter: blur(10px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.main-content {
  background: rgba(255, 255, 255, 0.9);
  padding: 24px;
  backdrop-filter: blur(10px);
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-title {
    font-size: 22px;
  }
  
  .app-title .el-icon {
    font-size: 26px;
  }
  
  .header-subtitle {
    font-size: 13px;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style>