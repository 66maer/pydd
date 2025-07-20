# pydd

> [English](README_EN.md) | 中文

DD驱动的Python包装器，提供了易于使用的鼠标和键盘操作接口。

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

## 项目简介

pydd是一个简化的DD驱动Python包装器，为开发者提供了清晰、直观的API来实现鼠标和键盘交互自动化。具备类型提示和完整的错误处理机制，旨在让自动化任务更加便于实现和可靠。

## 致谢

特别感谢DD驱动开发者 [ddxoft/master](https://github.com/ddxoft/master) 创建了底层DD驱动，使得这个包装器的实现成为可能。

## 功能特性

- **完整的鼠标控制**：支持左键、右键、中键和侧键，精确定位
- **全面的键盘输入**：完整的键盘支持，使用字符串形式的按键名称
- **多种文本输入方式**：支持通过`DD_str`直接输入文本和键盘模拟两种方式
- **鼠标相对移动**：支持相对于当前位置移动鼠标光标
- **类型安全的API**：完整的类型提示，提供更好的IDE支持和错误预防
- **错误处理**：自定义异常类型，便于调试
- **便捷快捷方式**：常用操作如复制/粘贴、窗口切换等

## 相比原始DD驱动的改进

- **正确的按键代码**：使用正确的按下/释放代码对（如：左键按下=1，释放=2）
- **字符串形式按键**：使用直观的名称如`"a"`、`"enter"`、`"ctrl"`而非数字代码
- **增强的文本输入**：可选择直接文本输入或键盘模拟方式
- **Python风格的API**：清晰、可读的方法名称和参数
- **完整的按键映射**：完整的键盘布局支持，包括小键盘和功能键

## 安装说明

1. 从[DD驱动官方仓库](https://github.com/ddxoft/master)下载DD驱动DLL文件（如：`dd.54900.dll`）
2. 将DLL文件放置到你的项目目录中
3. 将`pydd.py`复制到你的项目中或作为模块安装

## 快速开始

```python
from pydd import PyDD, DDError

try:
    # 初始化DD驱动
    dd = PyDD("./dd.54900.dll")
    
    # 鼠标操作
    dd.mouse_move(100, 100)           # 移动到绝对坐标
    dd.mouse_move_relative(50, 50)    # 相对当前位置移动
    dd.mouse_click("left")            # 左键点击
    dd.mouse_click("right", 200, 200) # 在(200,200)右键点击
    dd.mouse_double_click("left")     # 双击
    dd.mouse_scroll(1)                # 向上滚动
    
    # 键盘操作
    dd.key_press("a")                 # 按下'A'键
    dd.key_press("enter")             # 按下回车键
    dd.key_combination("ctrl", "c")   # Ctrl+C组合键
    
    # 文本输入
    dd.type_text("Hello World! @#$")  # 直接文本输入
    
    # 便捷方法
    dd.click_at(300, 400)             # 在指定位置点击
    dd.right_click_at(300, 400)       # 在指定位置右键点击
    dd.ctrl_c()                       # 复制快捷键
    dd.ctrl_v()                       # 粘贴快捷键
    
except DDError as e:
    print(f"DD驱动错误: {e}")
```

## 系统要求

- Windows操作系统
- DD驱动DLL文件
- 管理员权限（某些环境下可能需要）

## 支持的鼠标按键

| 按键字符串 | 描述 |
|------------|------|
| `"left"`   | 鼠标左键 |
| `"right"`  | 鼠标右键 |
| `"middle"` | 鼠标中键（滚轮） |
| `"x4"`     | 侧键4 |
| `"x5"`     | 侧键5 |

## 支持的键盘按键

### 字母键
`"a"` 到 `"z"`

### 数字键
`"1"` 到 `"0"`，以及符号如 `"`"`, `"-"`, `"+"`, `"\\"` 等

### 功能键
`"f1"` 到 `"f12"`, `"esc"`

### 特殊键
| 按键字符串 | 描述 |
|------------|------|
| `"enter"` | 回车键 |
| `"space"` | 空格键 |
| `"tab"` | Tab键 |
| `"shift"` | Shift键 |
| `"ctrl"` | Ctrl键 |
| `"alt"` | Alt键 |
| `"backspace"` | 退格键 |
| `"delete"` | 删除键 |

### 方向键
`"up"`, `"down"`, `"left"`, `"right"`

### 小键盘
`"num0"` 到 `"num9"`, `"num+"`, `"num-"`, `"num*"`, `"num/"`, `"numenter"`, `"num."`

## 使用示例

### 基础鼠标控制
```python
from DDWrapper import DDWrapper

dd = DDWrapper("./dd.54900.dll")

# 移动和点击
dd.mouse_move(100, 100)
dd.mouse_click("left")

# 拖拽操作
dd.mouse_down("left")
dd.mouse_move_relative(100, 50)
dd.mouse_up("left")

# 滚轮操作
dd.mouse_scroll(3)  # 向上滚动3次
dd.mouse_scroll(-2) # 向下滚动2次
```

### 键盘自动化
```python
# 输入带特殊字符的文本
dd.type_text("Hello World! @#$%^&*()")

# 键盘快捷键
dd.key_combination("ctrl", "shift", "t")  # 打开新标签页
dd.key_combination("alt", "f4")           # 关闭窗口

# 连续按键
dd.key_press("tab")
dd.key_press("tab")
dd.key_press("enter")
```

### 高级文本输入
```python
# 直接文本输入（使用dd_str接口，速度较慢，但应该比较稳定）
dd.type_text("快速文本输入", use_dd_str=True)

# 键盘模拟输入（自己写的模拟，速度快 0.05s 间隔）
dd.type_text("模拟键盘输入", use_dd_str=False)
```

### 自动化工作流
```python
# 复制粘贴工作流
dd.key_combination("ctrl", "a")  # 全选
dd.ctrl_c()                      # 复制
dd.mouse_click("right", 300, 300) # 在其他地方右键点击
dd.ctrl_v()                      # 粘贴

# 窗口切换
dd.alt_tab()                     # 切换窗口
dd.key_press("enter")           # 确认选择
```

## 错误处理

DDWrapper使用自定义异常进行更好的错误处理：

```python
from DDWrapper import DDWrapper, DDError

try:
    dd = DDWrapper("./nonexistent.dll")
except DDError as e:
    print(f"驱动错误: {e}")
    # 处理驱动初始化失败

try:
    dd.mouse_click("invalid_button")
except DDError as e:
    print(f"无效操作: {e}")
    # 处理无效参数
```

## 重要说明

1. **DLL路径**: 确保DD驱动DLL文件路径正确
2. **权限**: DD驱动要求使用管理员权限
3. **错误处理**: 在健壮的应用程序中，始终将DD操作包装在try-catch块中

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

