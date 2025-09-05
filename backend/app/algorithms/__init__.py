# -*- coding: utf-8 -*-
"""
算法模块初始化
自动导入所有算法模块，让装饰器注册生效
"""

# 导入所有算法模块，让装饰器注册生效
from . import hello_world
from . import bubble_sort

# 这个文件的主要目的是确保所有算法模块被导入
# 实际的算法注册通过装饰器完成