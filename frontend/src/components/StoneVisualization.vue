<template>
  <div class="stone-visualization">
    <div class="grid-container">
      <!-- 格子网格 -->
      <div 
        class="grid-layout"
        :style="{ 
          gridTemplateColumns: `repeat(${gridCols}, 1fr)`,
          gridTemplateRows: `repeat(${gridRows}, 1fr)`
        }"
      >
        <div
          v-for="(stones, index) in currentBoxes"
          :key="index"
          class="box"
          :class="{
            'highlighted': isHighlighted(index),
            'source': isSource(index),
            'target': isTarget(index),
            'goal': isGoalBox(index)
          }"
        >
          <div class="box-header">
            <span class="box-index">{{ index }}</span>
            <span class="stone-count">{{ stones }}</span>
          </div>
          
          <!-- 石头可视化 -->
          <div class="stones-area">
            <div 
              v-for="i in Math.min(stones, 20)" 
              :key="i"
              class="stone"
              :style="{ 
                animationDelay: `${i * 50}ms`,
                opacity: stones > 20 ? 0.7 : 1
              }"
            >
              🪨
            </div>
            <div v-if="stones > 20" class="overflow-indicator">
              +{{ stones - 20 }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 操作信息 -->
    <div class="operation-info" v-if="currentStepData">
      <div class="current-operation">
        <h4>当前操作</h4>
        <div class="operation-details">
          <span class="operation-description">{{ currentStepData.description }}</span>
          <div v-if="currentStepData.data_snapshot?.action_type" class="operation-visual">
            <div class="operation-arrow">
              格子{{ currentStepData.data_snapshot.from_box }} 
              <span class="arrow">→</span> 
              格子{{ currentStepData.data_snapshot.to_box }}
            </div>
            <div class="operation-amount">
              {{ currentStepData.data_snapshot.action_type === 'half' ? '移动一半' : '移动全部' }}
              ({{ currentStepData.data_snapshot.amount || 0 }}个石头)
            </div>
          </div>
        </div>
      </div>
      
      <!-- 目标状态对比 -->
      <div class="target-comparison">
        <h4>目标状态</h4>
        <div class="target-boxes">
          <div 
            v-for="(target, index) in targetState" 
            :key="index"
            class="target-box"
            :class="{ 'achieved': currentBoxes[index] === target && target > 0 }"
          >
            <span class="target-index">{{ index }}</span>
            <span class="target-count">{{ target }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAlgorithmStore } from '@/stores/algorithm'

const algorithmStore = useAlgorithmStore()
const { currentStepData, currentAlgorithm } = storeToRefs(algorithmStore)

// 计算当前状态的格子布局
const currentBoxes = computed(() => {
  const stepData = currentStepData.value
  if (!stepData || !stepData.data_snapshot) {
    return []
  }
  return stepData.data_snapshot.current_state || []
})

const targetState = computed(() => {
  const stepData = currentStepData.value
  if (!stepData || !stepData.data_snapshot) {
    return []
  }
  return stepData.data_snapshot.target_state || []
})

// 网格布局计算
const gridCols = computed(() => {
  const boxCount = currentBoxes.value.length
  if (boxCount <= 9) return 3
  if (boxCount <= 16) return 4
  return 5
})

const gridRows = computed(() => {
  const boxCount = currentBoxes.value.length
  return Math.ceil(boxCount / gridCols.value)
})

// 高亮状态判断
const isHighlighted = (index: number) => {
  return currentStepData.value?.highlight?.includes(index) || false
}

const isSource = (index: number) => {
  return currentStepData.value?.data_snapshot?.from_box === index
}

const isTarget = (index: number) => {
  return currentStepData.value?.data_snapshot?.to_box === index
}

const isGoalBox = (index: number) => {
  const target = targetState.value[index]
  return target > 0
}
</script>

<style scoped>
.stone-visualization {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
  border-radius: 12px;
  overflow: hidden;
}

.grid-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.grid-layout {
  display: grid;
  gap: 16px;
  max-width: 600px;
  width: 100%;
}

.box {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
  transition: all 0.3s ease;
  min-height: 120px;
  position: relative;
  overflow: hidden;
}

.box.highlighted {
  border-color: #3b82f6;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
  transform: scale(1.05);
}

.box.source {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.box.target {
  border-color: #10b981;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.box.goal {
  border-color: #8b5cf6;
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 600;
}

.box-index {
  font-size: 14px;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 6px;
}

.stone-count {
  font-size: 18px;
  color: #1e293b;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}

.stones-area {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
  min-height: 60px;
  position: relative;
}

.stone {
  font-size: 16px;
  animation: stoneAppear 0.3s ease-out;
  transition: all 0.2s ease;
}

.stone:hover {
  transform: scale(1.1);
}

@keyframes stoneAppear {
  from {
    opacity: 0;
    transform: scale(0) rotate(180deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.overflow-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: #64748b;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.operation-info {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.current-operation h4,
.target-comparison h4 {
  margin: 0 0 12px 0;
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
}

.operation-description {
  color: #475569;
  font-weight: 500;
  display: block;
  margin-bottom: 8px;
}

.operation-visual {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.operation-arrow {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #1e293b;
  font-weight: 600;
}

.arrow {
  color: #3b82f6;
  font-size: 18px;
  font-weight: bold;
}

.operation-amount {
  font-size: 12px;
  color: #64748b;
  font-style: italic;
}

.target-boxes {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.target-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  min-width: 40px;
  transition: all 0.3s ease;
}

.target-box.achieved {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-color: #10b981;
}

.target-index {
  font-size: 10px;
  color: #64748b;
  font-weight: 500;
}

.target-count {
  font-size: 14px;
  color: #1e293b;
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stone-visualization {
    padding: 12px;
    gap: 16px;
  }
  
  .grid-layout {
    gap: 12px;
  }
  
  .box {
    min-height: 100px;
    padding: 8px;
  }
  
  .stone {
    font-size: 14px;
  }
  
  .operation-info {
    padding: 12px;
  }
}
</style>