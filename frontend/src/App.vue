<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 头部导航 -->
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">
            <el-icon><Cpu /></el-icon>
            Algorithm Visualization Platform
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
import { Cpu } from '@element-plus/icons-vue'
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
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  width: 100%;
}

.app-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
}

.sidebar {
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
}

.main-content {
  background: white;
  padding: 20px;
}
</style>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app {
  height: 100vh;
}
</style>