<template>
  <div class="sort-visualization">
    <div class="chart-container">
      <v-chart 
        class="chart" 
        :option="chartOption" 
        ref="chartRef"
        @click="onChartClick"
        @mousemove="onChartMouseMove"
        autoresize
      />
    </div>
    
    <!-- 控制面板已移除 -->
    
    <!-- 统计信息 -->
    <div class="stats-panel" v-if="currentStepData">
      <div class="stat-item">
        <span class="stat-label">比较次数:</span>
        <span class="stat-value">{{ currentStepData.data_snapshot?.performance?.comparisons || 0 }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">交换次数:</span>
        <span class="stat-value">{{ currentStepData.data_snapshot?.performance?.swaps || 0 }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">当前轮次:</span>
        <span class="stat-value">{{ currentStepData.data_snapshot?.current_pass || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import { storeToRefs } from 'pinia'
import { useAlgorithmStore } from '@/stores/algorithm'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent
])

// 状态管理
const algorithmStore = useAlgorithmStore()
const { currentStepData, currentAlgorithm } = storeToRefs(algorithmStore)

// 组件状态
const chartRef = ref()
const animationSpeed = ref(500)
const isDragging = ref(false)
const dragIndex = ref(-1)

// 图表配置
const chartOption = computed(() => {
  const stepData = currentStepData.value
  console.log('Computing chart option with step data:', stepData)
  
  if (!stepData || !stepData.data_snapshot) {
    console.log('No step data, returning default chart option')
    return getDefaultChartOption()
  }

  const { array, comparing, swapping, sorted } = stepData.data_snapshot
  console.log('Chart data:', { array, comparing, swapping, sorted })
  
  return {
    title: {
      text: '冒泡排序可视化',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const data = params[0]
        const index = data.dataIndex
        let status = '未排序'
        
        if (sorted?.includes(index)) {
          status = '已排序'
        } else if (comparing?.includes(index)) {
          status = '正在比较'
        } else if (swapping?.includes(index)) {
          status = '正在交换'
        }
        
        return `
          <div>
            <strong>位置 ${index}</strong><br/>
            值: ${data.value}<br/>
            状态: ${status}
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: array?.map((_: any, index: number) => `位置 ${index}`) || [],
      axisLabel: {
        rotate: 45,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      name: '数值',
      nameTextStyle: {
        fontSize: 14
      }
    },
    series: [
      {
        name: '数组元素',
        type: 'bar',
        data: array?.map((value: number, index: number) => ({
          value,
          itemStyle: {
            color: getBarColor(index, comparing, swapping, sorted)
          }
        })) || [],
        barWidth: '60%',
        animationDuration: animationSpeed.value,
        animationEasing: 'elasticOut',
        label: {
          show: true,
          position: 'top',
          fontSize: 14,
          fontWeight: 'bold'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ],
    toolbox: {
      feature: {
        saveAsImage: {
          title: '保存图片'
        },
        restore: {
          title: '重置'
        }
      },
      right: '2%'
    },
    animationDuration: animationSpeed.value,
    animationEasing: 'cubicOut'
  }
})

// 获取柱状图颜色
function getBarColor(index: number, comparing?: number[], swapping?: number[], sorted?: number[]) {
  if (sorted?.includes(index)) {
    return '#67c23a' // 绿色 - 已排序
  } else if (swapping?.includes(index)) {
    return '#f56c6c' // 红色 - 正在交换
  } else if (comparing?.includes(index)) {
    return '#e6a23c' // 橙色 - 正在比较
  } else {
    return '#409eff' // 蓝色 - 默认
  }
}

// 默认图表配置
function getDefaultChartOption() {
  return {
    title: {
      text: '等待算法执行...',
      left: 'center',
      textStyle: {
        fontSize: 18,
        color: '#999'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '20%'
    },
    xAxis: {
      type: 'category',
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: []
  }
}

// 图表点击事件
function onChartClick(params: any) {
  if (params.componentType === 'series') {
    console.log('点击了柱状图:', params)
    // 可以实现点击选择功能
  }
}

// 鼠标移动事件（用于拖拽）
function onChartMouseMove(params: any) {
  if (isDragging.value && params.componentType === 'series') {
    // 实现拖拽逻辑
    console.log('拖拽中:', params)
  }
}

// 生成随机数组
function generateRandomArray() {
  const length = Math.floor(Math.random() * 10) + 5 // 5-14个元素
  const array = Array.from({ length }, () => Math.floor(Math.random() * 100) + 1)
  
  // 触发算法执行
  algorithmStore.executeAlgorithm(
    { array },
    { 
      animation_speed: animationSpeed.value,
      show_comparisons: true,
      show_swaps: true
    }
  )
}

// 重置数组
function resetArray() {
  const defaultArray = [89, 34, 67, 23, 78, 45, 12, 56, 91, 38, 72, 15, 84, 29, 63]
  algorithmStore.executeAlgorithm(
    { array: defaultArray },
    { 
      animation_speed: animationSpeed.value,
      show_comparisons: true,
      show_swaps: true
    }
  )
}

// 更新动画速度
function updateAnimationSpeed(value: number) {
  animationSpeed.value = value
  // 更新图表动画速度
  if (chartRef.value) {
    const chart = chartRef.value.getChart()
    chart.setOption({
      animationDuration: value,
      series: [{
        animationDuration: value
      }]
    })
  }
}

// 调试图表
function debugChart() {
  console.log('=== Chart Debug Info ===')
  console.log('Chart ref:', chartRef.value)
  console.log('Current algorithm:', currentAlgorithm.value)
  console.log('Current step data:', currentStepData.value)
  console.log('Chart option:', chartOption.value)
  
  if (chartRef.value) {
    const chart = chartRef.value.getChart()
    console.log('ECharts instance:', chart)
    console.log('Chart DOM:', chart.getDom())
  } else {
    console.log('Chart ref is null!')
  }
}

// 监听算法变化，自动执行默认数据
watch(currentAlgorithm, (newAlgorithm) => {
  console.log('Algorithm changed:', newAlgorithm)
  if (newAlgorithm?.name === 'bubble_sort' && !currentStepData.value) {
    console.log('Auto-executing bubble sort with default data')
    nextTick(() => {
      resetArray()
    })
  }
}, { immediate: true })

// 调试数据变化
watch(currentStepData, (newData) => {
  console.log('Step data updated:', newData)
}, { deep: true })
</script>

<style scoped>
.sort-visualization {
  height: 100%;
  position: relative;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  overflow: hidden;
}

.chart-container {
  height: 85%;
  padding: 20px;
}

.chart {
  height: 100%;
  width: 100%;
}

/* 控制面板样式已移除 */

.stats-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  gap: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px 16px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .control-overlay {
    position: static;
    margin: 10px;
    flex-direction: row;
    justify-content: space-between;
  }
  
  .stats-panel {
    position: static;
    margin: 10px;
    justify-content: space-around;
  }
  
  .chart-container {
    height: 60%;
    padding: 10px;
  }
}
</style>