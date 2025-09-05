import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入 Vue-ECharts
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'

// 导入自定义样式
import '@/assets/styles/global.css'
import '@/assets/styles/theme.css'

import App from './App.vue'

const app = createApp(App)

// 注册 Vue-ECharts 全局组件
app.component('v-chart', ECharts)

app.use(createPinia())
app.use(ElementPlus)

app.mount('#app')