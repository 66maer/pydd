# pydd

> [中文](README.md) | English

A Python wrapper for the DD driver, providing an easy-to-use interface for mouse and keyboard automation.

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)


## Overview

pydd is a simplified Python wrapper for the DD driver that provides developers with a clean, intuitive API for automating mouse and keyboard interactions. Built with type hints and comprehensive error handling, it's designed to make automation tasks more accessible and reliable.

## Acknowledgments

Special thanks to the DD driver developers at [ddxoft/master](https://github.com/ddxoft/master) for creating the underlying DD driver that makes this wrapper possible.

## Features

- **Complete Mouse Control**: Left, right, middle, and side button support with precise positioning
- **Comprehensive Keyboard Input**: Full keyboard support with string-based key names
- **Text Input Methods**: Both direct text input via `DD_str` and keyboard simulation
- **Relative Mouse Movement**: Move mouse cursor relative to current position
- **Type-Safe API**: Full type hints for better IDE support and error prevention
- **Error Handling**: Custom exception types for better debugging
- **Convenient Shortcuts**: Common operations like copy/paste, window switching

## Key Improvements Over Raw DD Driver

- **Correct Button Codes**: Proper press/release code pairs (e.g., left down=1, left up=2)
- **String-Based Keys**: Use intuitive names like `"a"`, `"enter"`, `"ctrl"` instead of numeric codes
- **Enhanced Text Input**: Choose between direct text input or keyboard simulation
- **Pythonic API**: Clean, readable method names and parameters
- **Comprehensive Key Mapping**: Complete keyboard layout support including numpad and function keys

## Installation

1. Download the DD driver DLL file (e.g., `dd.54900.dll`) from the [official DD driver repository](https://github.com/ddxoft/master)
2. Place the DLL file in your project directory
3. Copy `pydd.py` to your project or install as a module

## Quick Start

```python
from pydd import PyDD, DDError

try:
    # Initialize DD driver
    dd = PyDD("./dd.54900.dll")
    
    # Mouse operations
    dd.mouse_move(100, 100)           # Move to absolute coordinates
    dd.mouse_move_relative(50, 50)    # Move relative to current position
    dd.mouse_click("left")            # Left click
    dd.mouse_click("right", 200, 200) # Right click at (200,200)
    dd.mouse_double_click("left")     # Double click
    dd.mouse_scroll(1)                # Scroll up
    
    # Keyboard operations
    dd.key_press("a")                 # Press 'A' key
    dd.key_press("enter")             # Press Enter
    dd.key_combination("ctrl", "c")   # Ctrl+C combination
    
    # Text input
    dd.type_text("Hello World! @#$")  # Direct text input
    
    # Convenience methods
    dd.click_at(300, 400)             # Click at position
    dd.right_click_at(300, 400)       # Right click at position
    dd.ctrl_c()                       # Copy shortcut
    dd.ctrl_v()                       # Paste shortcut
    
except DDError as e:
    print(f"DD driver error: {e}")
```

## Requirements

- Python 3.7+
- Windows operating system
- DD driver DLL file
- Administrator privileges (may be required in some environments)

## Supported Mouse Buttons

| Button String | Description |
|---------------|-------------|
| `"left"`      | Left mouse button |
| `"right"`     | Right mouse button |
| `"middle"`    | Middle mouse button (scroll wheel) |
| `"x4"`        | Side button 4 |
| `"x5"`        | Side button 5 |

## Supported Keyboard Keys

### Letter Keys
`"a"` through `"z"`

### Number Keys
`"1"` through `"0"`, plus symbols like `"`"`, `"-"`, `"+"`, `"\\"`, etc.

### Function Keys
`"f1"` through `"f12"`, `"esc"`

### Special Keys
| Key String | Description |
|------------|-------------|
| `"enter"` | Enter key |
| `"space"` | Space bar |
| `"tab"` | Tab key |
| `"shift"` | Shift key |
| `"ctrl"` | Control key |
| `"alt"` | Alt key |
| `"backspace"` | Backspace key |
| `"delete"` | Delete key |

### Arrow Keys
`"up"`, `"down"`, `"left"`, `"right"`

### Numpad Keys
`"num0"` through `"num9"`, `"num+"`, `"num-"`, `"num*"`, `"num/"`, `"numenter"`, `"num."`

## Usage Examples

### Basic Mouse Control
```python
from pydd import PyDD

dd = PyDD("./dd.54900.dll")

# Move and click
dd.mouse_move(100, 100)
dd.mouse_click("left")

# Drag operation
dd.mouse_down("left")
dd.mouse_move_relative(100, 50)
dd.mouse_up("left")

# Scroll
dd.mouse_scroll(3)  # Scroll up 3 times
dd.mouse_scroll(-2) # Scroll down 2 times
```

### Keyboard Automation
```python
# Type text with special characters
dd.type_text("Hello World! @#$%^&*()")

# Keyboard shortcuts
dd.key_combination("ctrl", "shift", "t")  # Open new tab
dd.key_combination("alt", "f4")           # Close window

# Sequential key presses
dd.key_press("tab")
dd.key_press("tab")
dd.key_press("enter")
```
### Advanced Text Input
```python
# Direct text input (using DD_str, slower but more stable)
dd.type_text("Fast text input", use_dd_str=True)

# Keyboard simulation (custom implementation, faster with 0.05s interval)
dd.type_text("Simulated keyboard input", use_dd_str=False)
```

### Automation Workflows
```python
# Copy-paste workflow
dd.key_combination("ctrl", "a")  # Select all
dd.ctrl_c()                      # Copy
dd.mouse_click("right", 300, 300) # Right click elsewhere
dd.ctrl_v()                      # Paste

# Window switching
dd.alt_tab()                     # Switch window
dd.key_press("enter")           # Confirm selection
```

## Error Handling

pydd uses custom exceptions for better error handling:

```python
from pydd import PyDD, DDError

try:
    dd = PyDD("./nonexistent.dll")
except DDError as e:
    print(f"Driver error: {e}")
    # Handle driver initialization failure

try:
    dd.mouse_click("invalid_button")
except DDError as e:
    print(f"Invalid operation: {e}")
    # Handle invalid parameters
```

## Important Notes

1. **DLL Path**: Make sure the DD driver DLL file path is correct.
2. **Permissions**: The DD driver requires administrator privileges.
3. **Error Handling**: Always wrap DD operations in try-catch blocks for robust applications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

