# CLAUDE.md

本文件为Claude Code在此repository中工作时提供指导。

## 项目概览

这是一个名为"fuck-you-algorithm"的新Python项目，目前处于初始化阶段，只有基础文件。项目名称表明与algorithm问题或coding challenges相关。

## 开发命令

```bash
# 创建virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行tests
pytest
pytest tests/test_specific_file.py
pytest -v
pytest -k "test_function_name"

# Code formatting和linting
black .
flake8 .
isort .
mypy .

# 运行scripts
python main.py
python -m module_name
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