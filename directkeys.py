# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:37:50 2020

@author: pang
"""

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

"""
CONST DIK_ESCAPE = 0x01
CONST DIK_1 = 0x02
CONST DIK_2 = 0x03
CONST DIK_3 = 0x04
CONST DIK_4 = 0x05
CONST DIK_5 = 0x06
CONST DIK_6 = 0x07
CONST DIK_7 = 0x08
CONST DIK_8 = 0x09
CONST DIK_9 = 0x0A
CONST DIK_0 = 0x0B
CONST DIK_MINUS = 0x0C /* - on main keyboard */
CONST DIK_EQUALS = 0x0D
CONST DIK_BACK = 0x0E /* backspace */
CONST DIK_TAB = 0x0F
CONST DIK_Q = 0x10
CONST DIK_W = 0x11
CONST DIK_E = 0x12
CONST DIK_R = 0x13
CONST DIK_T = 0x14
CONST DIK_Y = 0x15
CONST DIK_U = 0x16
CONST DIK_I = 0x17
CONST DIK_O = 0x18
CONST DIK_P = 0x19
CONST DIK_LBRACKET = 0x1A
CONST DIK_RBRACKET = 0x1B
CONST DIK_RETURN = 0x1C /* Enter on main keyboard */
CONST DIK_LCONTROL = 0x1D
CONST DIK_A = 0x1E
CONST DIK_S = 0x1F
CONST DIK_D = 0x20
CONST DIK_F = 0x21
CONST DIK_G = 0x22
CONST DIK_H = 0x23
CONST DIK_J = 0x24
CONST DIK_K = 0x25
CONST DIK_L = 0x26
CONST DIK_SEMICOLON = 0x27
CONST DIK_APOSTROPHE = 0x28
CONST DIK_GRAVE = 0x29 /* accent grave */
CONST DIK_LSHIFT = 0x2A
CONST DIK_BACKSLASH = 0x2B
CONST DIK_Z = 0x2C
CONST DIK_X = 0x2D
CONST DIK_C = 0x2E
CONST DIK_V = 0x2F
CONST DIK_B = 0x30
CONST DIK_N = 0x31
CONST DIK_M = 0x32
CONST DIK_COMMA = 0x33
CONST DIK_PERIOD = 0x34 /* . on main keyboard */
CONST DIK_SLASH = 0x35 /* / on main keyboard */
CONST DIK_RSHIFT = 0x36
CONST DIK_MULTIPLY = 0x37 /* * on numeric keypad */
CONST DIK_LMENU = 0x38 /* left Alt */
CONST DIK_SPACE = 0x39
CONST DIK_CAPITAL = 0x3A
CONST DIK_F1 = 0x3B
CONST DIK_F2 = 0x3C
CONST DIK_F3 = 0x3D
CONST DIK_F4 = 0x3E
CONST DIK_F5 = 0x3F
CONST DIK_F6 = 0x40
CONST DIK_F7 = 0x41
CONST DIK_F8 = 0x42
CONST DIK_F9 = 0x43
CONST DIK_F10 = 0x44
CONST DIK_NUMLOCK = 0x45
CONST DIK_SCROLL = 0x46 /* Scroll Lock */
CONST DIK_NUMPAD7 = 0x47
CONST DIK_NUMPAD8 = 0x48
CONST DIK_NUMPAD9 = 0x49
CONST DIK_SUBTRACT = 0x4A /* - on numeric keypad */
CONST DIK_NUMPAD4 = 0x4B
CONST DIK_NUMPAD5 = 0x4C
CONST DIK_NUMPAD6 = 0x4D
CONST DIK_ADD = 0x4E /* + on numeric keypad */
CONST DIK_NUMPAD1 = 0x4F
CONST DIK_NUMPAD2 = 0x50
CONST DIK_NUMPAD3 = 0x51
CONST DIK_NUMPAD0 = 0x52
CONST DIK_DECIMAL = 0x53 /* . on numeric keypad */
CONST DIK_OEM_102 = 0x56 /* < > | on UK/Germany keyboards */
CONST DIK_F11 = 0x57
CONST DIK_F12 = 0x58
CONST DIK_F13 = 0x64 /* (NEC PC98) */
CONST DIK_F14 = 0x65 /* (NEC PC98) */
CONST DIK_F15 = 0x66 /* (NEC PC98) */
CONST DIK_KANA = 0x70 /* (Japanese keyboard) */
CONST DIK_ABNT_C1 = 0x73 /* / ? on Portugese (Brazilian) keyboards */
CONST DIK_CONVERT = 0x79 /* (Japanese keyboard) */
CONST DIK_NOCONVERT = 0x7B /* (Japanese keyboard) */
CONST DIK_YEN = 0x7D /* (Japanese keyboard) */
CONST DIK_ABNT_C2 = 0x7E /* Numpad . on Portugese (Brazilian) keyboards */
CONST DIK_NUMPADEQUALS = 0x8D /* = on numeric keypad (NEC PC98) */
CONST DIK_PREVTRACK = 0x90 /* Previous Track (DIK_CIRCUMFLEX on Japanese keyboard) */
CONST DIK_AT = 0x91 /* (NEC PC98) */
CONST DIK_COLON = 0x92 /* (NEC PC98) */
CONST DIK_UNDERLINE = 0x93 /* (NEC PC98) */
CONST DIK_KANJI = 0x94 /* (Japanese keyboard) */
CONST DIK_STOP = 0x95 /* (NEC PC98) */
CONST DIK_AX = 0x96 /* (Japan AX) */
CONST DIK_UNLABELED = 0x97 /* (J3100) */
CONST DIK_NEXTTRACK = 0x99 /* Next Track */
CONST DIK_NUMPADENTER = 0x9C /* Enter on numeric keypad */
CONST DIK_RCONTROL = 0x9D
CONST DIK_MUTE = 0xA0 /* Mute */
CONST DIK_CALCULATOR = 0xA1 /* Calculator */
CONST DIK_PLAYPAUSE = 0xA2 /* Play / Pause */
CONST DIK_MEDIASTOP = 0xA4 /* Media Stop */
CONST DIK_VOLUMEDOWN = 0xAE /* Volume - */
CONST DIK_VOLUMEUP = 0xB0 /* Volume + */
CONST DIK_WEBHOME = 0xB2 /* Web home */
CONST DIK_NUMPADCOMMA = 0xB3 /* , on numeric keypad (NEC PC98) */
CONST DIK_DIVIDE = 0xB5 /* / on numeric keypad */
CONST DIK_SYSRQ = 0xB7
CONST DIK_RMENU = 0xB8 /* right Alt */
CONST DIK_PAUSE = 0xC5 /* Pause */
CONST DIK_HOME = 0xC7 /* Home on arrow keypad */
CONST DIK_UP = 0xC8 /* UpArrow on arrow keypad */
CONST DIK_PRIOR = 0xC9 /* PgUp on arrow keypad */
CONST DIK_LEFT = 0xCB /* LeftArrow on arrow keypad */
CONST DIK_RIGHT = 0xCD /* RightArrow on arrow keypad */
CONST DIK_END = 0xCF /* End on arrow keypad */
CONST DIK_DOWN = 0xD0 /* DownArrow on arrow keypad */
CONST DIK_NEXT = 0xD1 /* PgDn on arrow keypad */
CONST DIK_INSERT = 0xD2 /* Insert on arrow keypad */
CONST DIK_DELETE = 0xD3 /* Delete on arrow keypad */
CONST DIK_LWIN = 0xDB /* Left Windows key */
CONST DIK_RWIN = 0xDC /* Right Windows key */
CONST DIK_APPS = 0xDD /* AppMenu key */
CONST DIK_POWER = 0xDE /* System Power */
CONST DIK_SLEEP = 0xDF /* System Sleep */
CONST DIK_WAKE = 0xE3 /* System Wake */
CONST DIK_WEBSEARCH = 0xE5 /* Web Search */
CONST DIK_WEBFAVORITES = 0xE6 /* Web Favorites */
CONST DIK_WEBREFRESH = 0xE7 /* Web Refresh */
CONST DIK_WEBSTOP = 0xE8 /* Web Stop */
CONST DIK_WEBFORWARD = 0xE9 /* Web Forward */
CONST DIK_WEBBACK = 0xEA /* Web Back */
CONST DIK_MYCOMPUTER = 0xEB /* My Computer */
CONST DIK_MAIL = 0xEC /* Mail */
CONST DIK_MEDIASELECT = 0xED /* Media Select */ 作者：Hayashi-Lin https://www.bilibili.com/read/cv9217614 出处：bilibili
"""

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

T = 0x14 # Attack
Y = 0x15 # Defense
SPACE = 0x39
U = 0x16

M = 0x32
J = 0x24
K = 0x25
LSHIFT = 0x2A
R = 0x13#用R代替识破
V = 0x2F

Q = 0x10
I = 0x17
O = 0x18
P = 0x19
C = 0x2E
F = 0x21

up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD

esc = 0x01

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    
def defense():
    PressKey(Y)
    time.sleep(0.05)
    ReleaseKey(Y)
    #time.sleep(0.1)


def attack():
    PressKey(T)
    time.sleep(0.05)
    ReleaseKey(T)
    #time.sleep(0.1)
    
def go_forward():
    PressKey(W)
    time.sleep(0.4)
    ReleaseKey(W)
    
def go_back():
    PressKey(S)
    time.sleep(0.4)
    ReleaseKey(S)
    
def go_left():
    PressKey(A)
    time.sleep(0.4)
    ReleaseKey(A)
    
def go_right():
    PressKey(D)
    time.sleep(0.4)
    ReleaseKey(D)
    
def jump():
    PressKey(SPACE)
    time.sleep(0.1)
    ReleaseKey(SPACE)
    attack()
    time.sleep(0.1)
    attack()
    time.sleep(0.1)
    attack()
    #time.sleep(0.1)
    
def dodge():#闪避
    PressKey(LSHIFT)
    time.sleep(0.1)
    PressKey(D)
    ReleaseKey(D)
    ReleaseKey(LSHIFT)
    #time.sleep(0.1)
    
def lock_vision():
    PressKey(U)
    time.sleep(0.3)
    ReleaseKey(U)
    time.sleep(0.1)
    
def go_forward_QL(t):
    PressKey(W)
    time.sleep(t)
    ReleaseKey(W)
    
def turn_left(t):
    PressKey(left)
    time.sleep(t)
    ReleaseKey(left)
    
def turn_up(t):
    PressKey(up)
    time.sleep(t)
    ReleaseKey(up)
    
def turn_right(t):
    PressKey(right)
    time.sleep(t)
    ReleaseKey(right)
    
def F_go():
    PressKey(F)
    time.sleep(0.5)
    ReleaseKey(F)
    
def forward_jump(t):
    PressKey(W)
    time.sleep(t)
    PressKey(SPACE)
    ReleaseKey(W)
    ReleaseKey(SPACE)
    
def press_esc():
    PressKey(esc)
    time.sleep(0.3)
    ReleaseKey(esc)
    
def dead():
    PressKey(M)
    time.sleep(0.5)
    ReleaseKey(M)

if __name__ == '__main__':
    time.sleep(15)
    print('Action start')
    time1 = time.time()
    # while(True):
    #     if abs(time.time()-time1) > 5:
    #         break
    #     else:
    #         defense()
    #         time.sleep(0.2)
    #
    #
    # go_forward()
    # time.sleep(1)
    #
    # attack()
    # time.sleep(1)

    jump()
    time.sleep(1)
    dodge()