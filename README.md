# Algorithm Visualization Platform

一个可扩展的算法可视化平台，让你可以轻松接入自己的算法并获得美观的动态可视化效果。

## 🚀 快速开始

### 🔥 全平台一键启动 (最简单)
```bash
python start.py
```
> 交互式选择启动后端、前端或两者

### 🎯 分别启动 (推荐)

#### 后端启动
```bash
cd backend
python start.py
```
> 自动创建虚拟环境、安装依赖并启动服务器

#### 前端启动 (需要Node.js)
```bash
cd frontend  
python start.py
```
> 自动清理、安装依赖并启动开发服务器

### 🧪 API测试
```bash
python test_api.py
```

## 📁 项目结构

```
fuck-you-algorithm/
├── backend/                     # Python后端
│   ├── app/
│   │   ├── main.py             # FastAPI应用入口
│   │   ├── api/                # API路由
│   │   ├── core/               # 核心框架
│   │   ├── algorithms/         # 算法实现
│   │   └── models/             # 数据模型
│   ├── requirements.txt
│   └── start.py                # 启动脚本
├── frontend/                    # Vue前端
│   ├── src/
│   │   ├── components/         # Vue组件
│   │   ├── stores/             # Pinia状态管理
│   │   ├── utils/              # 工具函数
│   │   └── types/              # TypeScript类型
│   ├── package.json
│   └── vite.config.ts
├── doc/                        # 文档
│   └── 设计方案.md
├── test_api.py                 # API测试脚本
└── README.md
```

## 🎯 核心特性

- **插件化算法接入** - 继承BaseAlgorithm即可快速接入新算法
- **动态可视化** - 实时步骤展示，支持播放/暂停/步进控制
- **现代化技术栈** - FastAPI + Vue3 + TypeScript + Element Plus
- **美观界面** - 响应式设计，动画效果，性能监控

## 📚 算法接入示例

```python
from app.core.base_algorithm import BaseAlgorithm
from app.core.registry import algorithm_register

@algorithm_register(
    name="my_algorithm",
    display_name="我的算法", 
    category="sorting",
    description="算法描述"
)
class MyAlgorithm(BaseAlgorithm):
    def get_config_schema(self):
        return {
            "param1": {"type": "number", "default": 10}
        }
    
    def execute(self, data, config):
        # 算法逻辑
        self.add_step("action", {"data": data}, [0], "描述")
        return {"result": "value"}
```

## 🔧 开发说明

- 后端服务运行在 `http://localhost:8000`
- 前端开发服务运行在 `http://localhost:5173`
- API文档访问 `http://localhost:8000/docs`

## 📖 更多文档

详细设计方案请查看 `doc/设计方案.md`