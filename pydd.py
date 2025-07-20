"""
pydd - DD驱动Python包装器

为DD驱动提供简化的Python接口，用于鼠标和键盘自动化操作。

作者: 66maer
版本: 1.0.0
许可证: MIT
仓库: https://github.com/66maer/pydd

依赖项:
    - Windows操作系统
    - DD驱动DLL文件

使用方法:
    from pydd import PyDD, DDError

    dd = PyDD("./dd.54900.dll")
    dd.mouse_click("left", 100, 100)
    dd.type_text("Hello World!")
"""

__version__ = "1.0.0"
__author__ = "66maer"
__license__ = "MIT"

import time
from ctypes import windll, c_int, c_char_p
from typing import Union, Optional
from enum import IntEnum


class DDError(Exception):
    """DD驱动操作基础异常"""

    pass


class DDInitializationError(DDError):
    """DD驱动初始化失败时抛出"""

    pass


class DDInvalidParameterError(DDError):
    """传入无效参数时抛出"""

    pass


class MouseButton(IntEnum):
    """鼠标按键枚举"""

    LEFT_DOWN = 1
    LEFT_UP = 2
    RIGHT_DOWN = 4
    RIGHT_UP = 8
    MIDDLE_DOWN = 16
    MIDDLE_UP = 32
    X4_DOWN = 64
    X4_UP = 128
    X5_DOWN = 256
    X5_UP = 512


class KeyCode(IntEnum):
    """DD驱动按键代码映射"""

    # 功能键区
    ESC = 100
    F1 = 101
    F2 = 102
    F3 = 103
    F4 = 104
    F5 = 105
    F6 = 106
    F7 = 107
    F8 = 108
    F9 = 109
    F10 = 110
    F11 = 111
    F12 = 112

    # 数字键区
    BACKTICK = 200  # `
    NUM_1 = 201
    NUM_2 = 202
    NUM_3 = 203
    NUM_4 = 204
    NUM_5 = 205
    NUM_6 = 206
    NUM_7 = 207
    NUM_8 = 208
    NUM_9 = 209
    NUM_0 = 210
    MINUS = 211  # -
    PLUS = 212  # +
    BACKSLASH = 213  # \
    BACKSPACE = 214

    # 字母键区第一行
    TAB = 300
    Q = 301
    W = 302
    E = 303
    R = 304
    T = 305
    Y = 306
    U = 307
    I = 308
    O = 309
    P = 310
    LEFT_BRACKET = 311  # [
    RIGHT_BRACKET = 312  # ]
    ENTER = 313

    # 字母键区第二行
    CAPS_LOCK = 400
    A = 401
    S = 402
    D = 403
    F = 404
    G = 405
    H = 406
    J = 407
    K = 408
    L = 409
    SEMICOLON = 410  # ;
    QUOTE = 411  # '

    # 字母键区第三行
    SHIFT = 500
    Z = 501
    X = 502
    C = 503
    V = 504
    B = 505
    N = 506
    M = 507
    COMMA = 508  # ,
    PERIOD = 509  # .
    SLASH = 510  # /

    # 底部功能键
    CTRL = 600
    WIN = 601
    ALT = 602
    SPACE = 603

    # 方向键
    ARROW_UP = 709
    ARROW_LEFT = 710
    ARROW_DOWN = 711
    ARROW_RIGHT = 712

    # 小键盘
    NUMPAD_0 = 800
    NUMPAD_1 = 801
    NUMPAD_2 = 802
    NUMPAD_3 = 803
    NUMPAD_4 = 804
    NUMPAD_5 = 805
    NUMPAD_6 = 806
    NUMPAD_7 = 807
    NUMPAD_8 = 808
    NUMPAD_9 = 809
    NUMPAD_LOCK = 810
    NUMPAD_DIVIDE = 811  # /
    NUMPAD_MULTIPLY = 812  # *
    NUMPAD_MINUS = 813  # -
    NUMPAD_PLUS = 814  # +
    NUMPAD_ENTER = 815
    NUMPAD_PERIOD = 816  # .

    # 删除键
    DELETE = 706


class PyDD:
    """
    DD驱动Python包装器

    为DD驱动鼠标和键盘操作提供清晰、类型安全的接口。
    """

    # 按键映射常量，避免代码重复
    _BUTTON_DOWN_MAP = {
        "left": MouseButton.LEFT_DOWN,
        "right": MouseButton.RIGHT_DOWN,
        "middle": MouseButton.MIDDLE_DOWN,
        "x4": MouseButton.X4_DOWN,
        "x5": MouseButton.X5_DOWN,
    }

    _BUTTON_UP_MAP = {
        "left": MouseButton.LEFT_UP,
        "right": MouseButton.RIGHT_UP,
        "middle": MouseButton.MIDDLE_UP,
        "x4": MouseButton.X4_UP,
        "x5": MouseButton.X5_UP,
    }

    def __init__(self, dll_path: str = "./dd.54900.dll"):
        """
        初始化DD驱动包装器。

        Args:
            dll_path: DD驱动DLL文件路径

        Raises:
            DDInitializationError: 当DLL无法加载或驱动初始化失败时抛出
        """
        try:
            self.dd_dll = windll.LoadLibrary(dll_path)
            # 设置DD_str函数参数类型以确保正确的ctypes处理
            self.dd_dll.DD_str.argtypes = [c_char_p]
            self.dd_dll.DD_str.restype = c_int
        except (OSError, FileNotFoundError) as e:
            raise DDInitializationError(f"加载DD驱动DLL失败: {e}")
        except Exception as e:
            raise DDInitializationError(f"加载DD驱动时发生意外错误: {e}")

        # 初始化驱动
        if not self._init_driver():
            raise DDInitializationError("DD驱动初始化失败")

    def _init_driver(self) -> bool:
        """
        初始化DD驱动。

        Returns:
            如果初始化成功返回True，否则返回False
        """
        try:
            result = self.dd_dll.DD_btn(0)
            return result == 1
        except Exception:
            return False

    # 鼠标操作
    def mouse_move(self, x: int, y: int) -> None:
        """
        将鼠标光标移动到绝对屏幕坐标。

        Args:
            x: 屏幕X坐标
            y: 屏幕Y坐标
        """
        self.dd_dll.DD_mov(x, y)

    def mouse_move_relative(self, dx: int, dy: int) -> None:
        """
        相对于当前位置移动鼠标光标。

        Args:
            dx: X轴相对移动距离
            dy: Y轴相对移动距离
        """
        self.dd_dll.DD_movR(dx, dy)

    def mouse_click(
        self,
        button: str = "left",
        x: Optional[int] = None,
        y: Optional[int] = None,
        duration: float = 0.0,
    ) -> None:
        """
        执行鼠标点击操作。

        Args:
            button: 要点击的鼠标按键 ("left", "right", "middle", "x4", "x5")
            x: X坐标（可选，不指定则在当前位置点击）
            y: Y坐标（可选，不指定则在当前位置点击）
            duration: 按键持续时间（秒）

        Raises:
            DDInvalidParameterError: 当按键类型不支持时抛出
        """
        if x is not None and y is not None:
            self.mouse_move(x, y)

        # 按键映射获取按下/释放代码
        button_lower = button.lower()
        if button_lower not in self._BUTTON_DOWN_MAP:
            raise DDInvalidParameterError(f"不支持的鼠标按键: {button}")

        down_code = self._BUTTON_DOWN_MAP[button_lower]
        up_code = self._BUTTON_UP_MAP[button_lower]

        # 按下按键
        self.dd_dll.DD_btn(down_code)

        if duration > 0:
            time.sleep(duration)

        # 释放按键
        self.dd_dll.DD_btn(up_code)

    def mouse_down(self, button: str = "left") -> None:
        """
        按下并保持鼠标按键。

        Args:
            button: 要按下的鼠标按键 ("left", "right", "middle", "x4", "x5")

        Raises:
            DDInvalidParameterError: 当按键类型不支持时抛出
        """
        button_lower = button.lower()
        if button_lower not in self._BUTTON_DOWN_MAP:
            raise DDInvalidParameterError(f"不支持的鼠标按键: {button}")

        self.dd_dll.DD_btn(self._BUTTON_DOWN_MAP[button_lower])

    def mouse_up(self, button: str = "left") -> None:
        """
        释放鼠标按键。

        Args:
            button: 要释放的鼠标按键 ("left", "right", "middle", "x4", "x5")

        Raises:
            DDInvalidParameterError: 当按键类型不支持时抛出
        """
        button_lower = button.lower()
        if button_lower not in self._BUTTON_UP_MAP:
            raise DDInvalidParameterError(f"不支持的鼠标按键: {button}")

        self.dd_dll.DD_btn(self._BUTTON_UP_MAP[button_lower])

    def mouse_double_click(
        self,
        button: str = "left",
        x: Optional[int] = None,
        y: Optional[int] = None,
        interval: float = 0.05,
    ) -> None:
        """
        执行双击操作。

        Args:
            button: 要双击的鼠标按键 ("left", "right", "middle", "x4", "x5")
            x: X坐标（可选）
            y: Y坐标（可选）
            interval: 两次点击之间的时间间隔（秒）
        """
        self.mouse_click(button, x, y)
        time.sleep(interval)
        self.mouse_click(button, x, y)

    def mouse_scroll(self, direction: int = 1, interval: float = 0.1) -> None:
        """
        滚动鼠标滚轮。

        Args:
            direction: 滚动方向和次数（正数向上滚动，负数向下滚动，绝对值表示滚动次数）
            interval: 每次滚动之间的时间间隔（秒）
        """
        if direction == 0:
            return

        count = abs(direction)
        scroll_code = 1 if direction > 0 else 2

        for i in range(count):
            self.dd_dll.DD_whl(scroll_code)
            if interval > 0 and i < count - 1:  # 最后一次滚动后不需要等待
                time.sleep(interval)

    # 键盘操作
    def key_press(self, key: Union[str, int, KeyCode], duration: float = 0.0) -> None:
        """
        按下并释放按键。

        Args:
            key: 要按下的按键（字符串名称、键码或KeyCode枚举）
            duration: 按键持续时间（秒）

        Raises:
            DDInvalidParameterError: 当按键不支持时抛出
        """
        key_code = self._get_key_code(key)

        # 按下按键
        self.dd_dll.DD_key(key_code, 1)

        if duration > 0:
            time.sleep(duration)

        # 释放按键
        self.dd_dll.DD_key(key_code, 2)

    def key_down(self, key: Union[str, int, KeyCode]) -> None:
        """
        按下并保持按键。

        Args:
            key: 要按下的按键

        Raises:
            DDInvalidParameterError: 当按键不支持时抛出
        """
        key_code = self._get_key_code(key)
        self.dd_dll.DD_key(key_code, 1)

    def key_up(self, key: Union[str, int, KeyCode]) -> None:
        """
        释放按键。

        Args:
            key: 要释放的按键

        Raises:
            DDInvalidParameterError: 当按键不支持时抛出
        """
        key_code = self._get_key_code(key)
        self.dd_dll.DD_key(key_code, 2)

    def key_combination(
        self, *keys: Union[str, int, KeyCode], duration: float = 0.05
    ) -> None:
        """
        同时按下多个按键（键盘快捷键）。

        Args:
            keys: 要同时按下的按键
            duration: 按键持续时间（秒）

        Raises:
            DDInvalidParameterError: 当任何按键不支持时抛出
        """
        # 按顺序按下所有按键
        for key in keys:
            self.key_down(key)

        if duration > 0:
            time.sleep(duration)

        # 以相反顺序释放所有按键
        for key in reversed(keys):
            self.key_up(key)

    def type_text(self, text: str, use_dd_str: bool = True) -> None:
        """
        使用DD驱动输入文本。

        Args:
            text: 要输入的文本
            use_dd_str: 使用DD_str直接输入（推荐）或键盘模拟

        Note:
            DD_str方法仅支持ASCII字符。对于非ASCII字符，
            请考虑使用输入法切换或设置use_dd_str=False。
        """
        if not text:
            return

        if use_dd_str:
            # 使用DD_str直接输入文本（支持可见字符和空格）
            text_bytes = text.encode("ascii", errors="ignore")
            if text_bytes:  # 仅在有有效ASCII字符时调用
                self.dd_dll.DD_str(text_bytes)
        else:
            # 使用键盘模拟方法
            self._type_text_by_key(text)

    def _type_text_by_key(self, text: str, interval: float = 0.05) -> None:
        """
        使用键盘模拟输入文本。

        Args:
            text: 要输入的文本
            interval: 字符输入间隔时间（秒）
        """
        for char in text:
            try:
                if char == " ":
                    self.key_press("space")
                elif char.isalpha():
                    # 处理大小写
                    if char.isupper():
                        self.key_combination("shift", char.lower())
                    else:
                        self.key_press(char.lower())
                elif char.isdigit():
                    self.key_press(char)
                else:
                    # 对特殊字符使用DD_str
                    char_bytes = char.encode("ascii", errors="ignore")
                    if char_bytes:
                        self.dd_dll.DD_str(char_bytes)
            except DDInvalidParameterError:
                # 跳过不支持的字符
                continue

            if interval > 0:
                time.sleep(interval)

    def _get_key_code(self, key: Union[str, int, KeyCode]) -> int:
        """
        获取指定按键的键码。

        Args:
            key: 按键标识符（字符串名称、整数代码或KeyCode枚举）

        Returns:
            DD驱动键码

        Raises:
            DDInvalidParameterError: 当按键不支持时抛出
        """
        if isinstance(key, (int, KeyCode)):
            return int(key)
        elif isinstance(key, str):
            # 字符串按键名称映射
            key_name_map = {
                # 功能键
                "esc": KeyCode.ESC,
                "f1": KeyCode.F1,
                "f2": KeyCode.F2,
                "f3": KeyCode.F3,
                "f4": KeyCode.F4,
                "f5": KeyCode.F5,
                "f6": KeyCode.F6,
                "f7": KeyCode.F7,
                "f8": KeyCode.F8,
                "f9": KeyCode.F9,
                "f10": KeyCode.F10,
                "f11": KeyCode.F11,
                "f12": KeyCode.F12,
                # 数字行按键
                "`": KeyCode.BACKTICK,
                "1": KeyCode.NUM_1,
                "2": KeyCode.NUM_2,
                "3": KeyCode.NUM_3,
                "4": KeyCode.NUM_4,
                "5": KeyCode.NUM_5,
                "6": KeyCode.NUM_6,
                "7": KeyCode.NUM_7,
                "8": KeyCode.NUM_8,
                "9": KeyCode.NUM_9,
                "0": KeyCode.NUM_0,
                "-": KeyCode.MINUS,
                "+": KeyCode.PLUS,
                "\\": KeyCode.BACKSLASH,
                "backspace": KeyCode.BACKSPACE,
                # 字母键
                "tab": KeyCode.TAB,
                "q": KeyCode.Q,
                "w": KeyCode.W,
                "e": KeyCode.E,
                "r": KeyCode.R,
                "t": KeyCode.T,
                "y": KeyCode.Y,
                "u": KeyCode.U,
                "i": KeyCode.I,
                "o": KeyCode.O,
                "p": KeyCode.P,
                "[": KeyCode.LEFT_BRACKET,
                "]": KeyCode.RIGHT_BRACKET,
                "enter": KeyCode.ENTER,
                "caps": KeyCode.CAPS_LOCK,
                "capslock": KeyCode.CAPS_LOCK,
                "a": KeyCode.A,
                "s": KeyCode.S,
                "d": KeyCode.D,
                "f": KeyCode.F,
                "g": KeyCode.G,
                "h": KeyCode.H,
                "j": KeyCode.J,
                "k": KeyCode.K,
                "l": KeyCode.L,
                ";": KeyCode.SEMICOLON,
                "'": KeyCode.QUOTE,
                "shift": KeyCode.SHIFT,
                "z": KeyCode.Z,
                "x": KeyCode.X,
                "c": KeyCode.C,
                "v": KeyCode.V,
                "b": KeyCode.B,
                "n": KeyCode.N,
                "m": KeyCode.M,
                ",": KeyCode.COMMA,
                ".": KeyCode.PERIOD,
                "/": KeyCode.SLASH,
                # 修饰键和特殊键
                "ctrl": KeyCode.CTRL,
                "win": KeyCode.WIN,
                "alt": KeyCode.ALT,
                "space": KeyCode.SPACE,
                # 方向键
                "up": KeyCode.ARROW_UP,
                "down": KeyCode.ARROW_DOWN,
                "left": KeyCode.ARROW_LEFT,
                "right": KeyCode.ARROW_RIGHT,
                # 小键盘
                "num0": KeyCode.NUMPAD_0,
                "num1": KeyCode.NUMPAD_1,
                "num2": KeyCode.NUMPAD_2,
                "num3": KeyCode.NUMPAD_3,
                "num4": KeyCode.NUMPAD_4,
                "num5": KeyCode.NUMPAD_5,
                "num6": KeyCode.NUMPAD_6,
                "num7": KeyCode.NUMPAD_7,
                "num8": KeyCode.NUMPAD_8,
                "num9": KeyCode.NUMPAD_9,
                "num/": KeyCode.NUMPAD_DIVIDE,
                "num*": KeyCode.NUMPAD_MULTIPLY,
                "num-": KeyCode.NUMPAD_MINUS,
                "num+": KeyCode.NUMPAD_PLUS,
                "numenter": KeyCode.NUMPAD_ENTER,
                "num.": KeyCode.NUMPAD_PERIOD,
                "delete": KeyCode.DELETE,
                "del": KeyCode.DELETE,
            }

            key_lower = key.lower()
            if key_lower in key_name_map:
                return key_name_map[key_lower]
            else:
                raise DDInvalidParameterError(f"不支持的按键名称: {key}")
        else:
            raise DDInvalidParameterError(f"不支持的按键类型: {type(key)}")

    # 便捷方法
    def click_at(self, x: int, y: int, button: str = "left") -> None:
        """在指定坐标点击。"""
        self.mouse_click(button, x, y)

    def right_click_at(self, x: int, y: int) -> None:
        """在指定坐标右键点击。"""
        self.mouse_click("right", x, y)

    def double_click_at(self, x: int, y: int) -> None:
        """在指定坐标双击。"""
        self.mouse_double_click("left", x, y)

    def ctrl_c(self) -> None:
        """复制 (Ctrl+C)。"""
        self.key_combination("ctrl", "c")

    def ctrl_v(self) -> None:
        """粘贴 (Ctrl+V)。"""
        self.key_combination("ctrl", "v")

    def ctrl_x(self) -> None:
        """剪切 (Ctrl+X)。"""
        self.key_combination("ctrl", "x")

    def ctrl_z(self) -> None:
        """撤销 (Ctrl+Z)。"""
        self.key_combination("ctrl", "z")

    def alt_tab(self) -> None:
        """切换窗口 (Alt+Tab)。"""
        self.key_combination("alt", "tab")


# 使用示例
if __name__ == "__main__":
    try:
        # 初始化DD驱动
        dd = PyDD("./dd.54900.dll")
        print("DD驱动初始化成功")

        # 鼠标操作示例
        print("移动鼠标到 (100, 100)")
        dd.mouse_move(100, 100)

        print("左键点击")
        dd.mouse_click()

        print("在 (200, 200) 右键点击")
        dd.right_click_at(200, 200)

        print("鼠标相对移动")
        dd.mouse_move_relative(50, 50)

        print("鼠标向上滚动")
        dd.mouse_scroll(1)

        # 键盘操作示例
        print("按下A键")
        dd.key_press("a")

        print("按下回车键")
        dd.key_press("enter")

        print("Ctrl+C组合键")
        dd.ctrl_c()

        print("输入文本（使用DD_str）")
        dd.type_text("Hello World! @#$%")

        print("输入文本（使用键盘模拟）")
        dd.type_text("Hello", use_dd_str=False)

        print("所有操作完成")

    except DDError as e:
        print(f"DD驱动错误: {e}")
    except Exception as e:
        print(f"意外错误: {e}")
