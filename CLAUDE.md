# CLAUDE.md

本文件为Claude Code在此repository中工作时提供指导。

## 项目概览

这是一个名为"fuck-you-algorithm"的新Python项目，目前处于初始化阶段，只有基础文件。项目名称表明与algorithm问题或coding challenges相关。

## 开发命令

### 一键启动服务
```bash
# 全平台启动 (交互式选择)
python start.py

# 仅启动后端
cd backend && python start.py

# 仅启动前端  
cd frontend && python start.py
```

### 开发环境
```bash
# 后端测试
python test_api.py

# 前端依赖管理 (自动处理)
cd frontend && python start.py

# 手动前端操作 (如需要)
cd frontend
npm install
npm run dev
npm run build
```

### 代码质量 (后端)
```bash
# 在虚拟环境中运行
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# 代码检查
black .
flake8 .
isort .
mypy .

# 测试
pytest
pytest tests/test_specific_file.py -v
```

## 项目结构

当前结构：
- `README.md` - 项目标题
- `LICENSE` - MIT许可证
- `.gitignore` - Python配置

预期未来结构：
```
/
├── algorithms/          # 算法实现
├── data_structures/     # 数据结构实现
├── problems/           # 题解
├── tests/              # 测试文件
├── utils/              # 工具函数
└── requirements.txt    # 依赖项
```

## 开发备注

- 专注于algorithm/coding challenge的项目
- 目前为空，尚未建立架构
- 已准备好初始开发setup