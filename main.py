# 流程
# 1 搞蒙版
# 2 截头像
# 3 叠头像
# 4 嵌字
# 5 改分辨率
#1 优化算法 尽量不出现两个重复表情在一块
#2 优化代码 md0.2s的时间太长了
#3 把原代码重做 他def的函数我看不懂 只能打印一次文本吗我靠
#4 增加多种表情包选择
#5 把选择的地方做的更明显一些
#6 加阴影
#7 新增：快捷键切换角色功能
#8 新增：限制生成图片大小功能

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import random
import time
import keyboard
import pyperclip
import io
from PIL import Image, ImageTk
import win32clipboard
import os
import re
import shutil
import threading
import win32gui
import win32process
import psutil
from text_fit_draw import draw_text_auto
from image_fit_paste import paste_image_auto
import getpass

# ===== PyInstaller 资源路径处理函数 =====
def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包后的环境"""
    try:
        # PyInstaller 创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境中使用当前文件所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# 全局变量
i = -1
value_1 = -1
expression = 1  # 默认表情为1
backgroundNum = 1  # 默认背景为1

#前台窗口白名单
windowwhitelist=["TIM.exe","WeChat.exe","Weixin.exe","WeChatApp.exe","QQ.exe"]
enablewhitelist=True

# 角色配置字典
mahoshojo = {
    "ema": {"emotion_count": 8, "font": "font3.ttf", "name": "樱羽艾玛"},     # 樱羽艾玛
    "hiro": {"emotion_count": 6, "font": "font3.ttf", "name": "二阶堂希罗"},    # 二阶堂希罗
    "sherri": {"emotion_count": 7, "font": "font3.ttf", "name": "橘雪莉"},  # 橘雪莉
    "hanna": {"emotion_count": 5, "font": "font3.ttf", "name": "远野汉娜"},   # 远野汉娜
    "anan": {"emotion_count": 9, "font": "font3.ttf", "name": "夏目安安"},    # 夏目安安
    "yuki" : {"emotion_count": 18, "font": "font3.ttf", "name": "月代雪"},
    "meruru": {"emotion_count": 6, "font": "font3.ttf", "name": "冰上梅露露"},   # 冰上梅露露
    "noa": {"emotion_count": 6, "font": "font3.ttf", "name": "城崎诺亚"},     # 城崎诺亚
    "reia": {"emotion_count": 7, "font": "font3.ttf", "name": "莲见蕾雅"},    # 莲见蕾雅
    "miria": {"emotion_count": 4, "font": "font3.ttf", "name": "佐伯米莉亚"},   # 佐伯米莉亚
    "nanoka": {"emotion_count": 5, "font": "font3.ttf", "name": "黑部奈叶香"},  # 黑部奈叶香
    "mago": {"emotion_count": 5, "font": "font3.ttf", "name": "宝生玛格"},   # 宝生玛格
    "alisa": {"emotion_count": 6, "font": "font3.ttf", "name": "紫藤亚里沙"},   # 紫藤亚里沙
    "coco": {"emotion_count": 5, "font": "font3.ttf", "name": "泽渡可可"}
}

# 角色文字配置字典 - 每个角色对应4个文字配置
text_configs_dict = {
    "nanoka": [  # 黑部奈叶香
        {"text":"黑","position":(759,63),"font_color":(131,143,147),"font_size":196},
        {"text":"部","position":(955,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"奈","position":(1053,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"叶香","position":(1197,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "hiro": [  # 二阶堂希罗
        {"text":"二","position":(759,63),"font_color":(239,79,84),"font_size":196},
        {"text":"阶堂","position":(955,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"希","position":(1143,110),"font_color":(255, 255, 255),"font_size":147},
        {"text":"罗","position":(1283,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "ema": [  # 樱羽艾玛
        {"text":"樱","position":(759,73),"font_color":(253,145,175),"font_size":186},
        {"text":"羽","position":(949,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"艾","position":(1039,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"玛","position":(1183,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "sherri": [  # 橘雪莉
        {"text":"橘","position":(759,73),"font_color":(137,177,251),"font_size":186},
        {"text":"雪","position":(943,110),"font_color":(255, 255, 255),"font_size":147},
        {"text":"莉","position":(1093,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"","position":(0,0),"font_color":(255, 255, 255),"font_size":1}  # 占位符
    ],
    "anan": [  # 夏目安安
        {"text":"夏","position":(759,73),"font_color":(159,145,251),"font_size":186},
        {"text":"目","position":(949,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"安","position":(1039,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"安","position":(1183,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "noa": [  # 城崎诺亚
        {"text":"城","position":(759,73),"font_color":(104,223,231),"font_size":186},
        {"text":"崎","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"诺","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"亚","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "coco": [  # 泽渡可可
        {"text":"泽","position":(759,73),"font_color":(251,114,78),"font_size":186},
        {"text":"渡","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"可","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"可","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "alisa": [  # 紫藤亚里沙
        {"text":"紫","position":(759,73),"font_color":(235,75,60),"font_size":186},
        {"text":"藤","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"亚","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"里沙","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "reia": [  # 莲见蕾雅
        {"text":"莲","position":(759,73),"font_color":(253,177,88),"font_size":186},
        {"text":"见","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"蕾","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"雅","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "mago": [  # 宝生玛格
        {"text":"宝","position":(759,73),"font_color":(185,124,235),"font_size":186},
        {"text":"生","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"玛","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"格","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "hanna": [  # 远野汉娜
        {"text":"远","position":(759,73),"font_color":(169,199,30),"font_size":186},
        {"text":"野","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"汉","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"娜","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "meruru": [  # 冰上梅露露
        {"text":"冰","position":(759,73),"font_color":(227,185,175),"font_size":186},
        {"text":"上","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"梅","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"露露","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}
    ],
    "miria": [  # 佐伯米莉亚
        {"text":"佐","position":(759,73),"font_color":(235,207,139),"font_size":186},
        {"text":"伯","position":(945,175),"font_color":(255, 255, 255),"font_size":92},
        {"text":"米","position":(1042,117),"font_color":(255, 255, 255),"font_size":147},
        {"text":"莉亚","position":(1186,175),"font_color":(255, 255, 255),"font_size":92}   
    ],
    "yuki": [  #月代雪
    {"text":"月","position":(759,63),"font_color":(195,209,231),"font_size":196},
    {"text":"代","position":(948,175),"font_color":(255, 255, 255),"font_size":92},
    {"text":"雪","position":(1053,117),"font_color":(255, 255, 255),"font_size":147} ,   
    {"text":"","position":(0,0),"font_color":(255, 255, 255),"font_size":1}
        ]
}

# 获取当前用户名
username = getpass.getuser()

# 构建用户文档路径
if os.name == 'nt':  # Windows系统
    user_documents = os.path.join('C:\\', 'Users', username, 'Documents')
else:  # 其他系统
    user_documents = os.path.expanduser('~/Documents')

# 构建"魔裁"文件夹路径
magic_cut_folder = os.path.join(user_documents, '魔裁')

# 创建"魔裁"文件夹（如果不存在）
os.makedirs(magic_cut_folder, exist_ok=True)

# 角色列表（按顺序对应1-14的角色）
character_list = list(mahoshojo.keys())

# 角色配置
current_character_index = 3  # 初始角色为橘雪莉（索引从1开始）
mahoshojo_postion = [728,355] #文本范围起始位置
mahoshojo_over = [2339,800]   #文本范围右下角位置

# 获取当前角色信息
def get_current_character():
    return character_list[current_character_index-1]

def get_current_font():
    # 使用 get_resource_path 获取字体文件路径
    return get_resource_path(mahoshojo[get_current_character()]["font"])

def get_current_emotion_count():
    return mahoshojo[get_current_character()]["emotion_count"]

def delate(folder_path, quality=85):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg'):
            os.remove(folder_path+"\\"+filename)
         

def generate_and_save_images(character_name):
    # 获取当前角色的表情数量
    emotion_count = mahoshojo[character_name]["emotion_count"]

    for filename in os.listdir(magic_cut_folder):
        if filename.startswith(character_name):
            return
    print("正在加载")
    for i in range(16):     
        for j in range(emotion_count):
            # 使用 get_resource_path 获取资源路径
            background_path = get_resource_path(os.path.join("background", f"c{i+1}.png"))
            overlay_path = get_resource_path(os.path.join(character_name, f"{character_name} ({j+1}).png"))
                
            background = Image.open(background_path).convert("RGBA")
            overlay = Image.open(overlay_path).convert("RGBA")
                
            img_num = j * 16 + i + 1
            result = background.copy()
            result.paste(overlay, (0, 134), overlay)
                
            # 使用绝对路径保存生成的图片
            save_path = os.path.join(magic_cut_folder, f"{character_name} ({img_num}).jpg")
            result.convert("RGB").save(save_path)
    print("加载完成")


def switch_character(new_index):
    global current_character_index
    if 0 <= new_index < len(character_list):
        current_character_index = new_index
        character_name = get_current_character()
        print(f"已切换到角色: {character_name}")
        
        # 生成并保存图片
        generate_and_save_images(character_name)
        
        return True
    return False

# 显示当前角色信息
def show_current_character():
    character_name = get_current_character()
    print(f"当前角色: {character_name}")


# 显示当前角色信息
show_current_character()

# 测试：生成当前角色的图片
generate_and_save_images(get_current_character())

def get_expression(i):
    global expression
    character_name = get_current_character()
    if i <= mahoshojo[character_name]["emotion_count"]:
        print(f"已切换至第{i}个表情")
        expression = i


HOTKEY= "enter"

# 全选快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SELECT_ALL_HOTKEY= "ctrl+a"

# 剪切快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
CUT_HOTKEY= "ctrl+x"

# 黏贴快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
PASTE_HOTKEY= "ctrl+v"

# 发送消息快捷键, 此按键并不会监听,  而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SEND_HOTKEY= "enter"

# 是否阻塞按键, 如果热键设置为阻塞模式, 则按下热键时不会将该按键传递给前台应用
# 如果生成热键和发送热键相同, 则强制阻塞, 防止误触发发送消息
# 此值为布尔值, True 或 False
BLOCK_HOTKEY= False

# 操作的间隔, 如果失效可以适当增大此数值
# 此值为数字, 单位为秒
DELAY= 0.1

# 是否自动黏贴生成的图片(如果为否则保留图片在剪贴板, 可以手动黏贴)
# 此值为布尔值, True 或 False
AUTO_PASTE_IMAGE= True

# 生成图片后是否自动发送(模拟回车键输入), 只有开启自动黏贴才生效
# 此值为布尔值, True 或 False
AUTO_SEND_IMAGE= True



def copy_png_bytes_to_clipboard(png_bytes: bytes):
    # 打开 PNG 字节为 Image
    image = Image.open(io.BytesIO(png_bytes))
    # 转换成 BMP 字节流（去掉 BMP 文件头的前 14 个字节）
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]
    # 打开剪贴板并写入 DIB 格式
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    win32clipboard.CloseClipboard()

#判断窗口名
def get_window_exe_name():
    try:
        hwnd=win32gui.GetForegroundWindow()
        _,pid=win32process.GetWindowThreadProcessId(hwnd)
        process=psutil.Process(pid)
        exe_path=process.exe()
        return os.path.basename(exe_path)
    except Exception as e:
        print(f"获取文件名时发生错误：{e}")
        return None

def cut_all_and_get_text() -> str:
    """
    #模拟 Ctrl+A / Ctrl+X 剪切全部文本，并返回剪切得到的内容。
    #delay: 每步之间的延时（秒），默认0.1秒。
    """
    # 备份原剪贴板
    old_clip = pyperclip.paste()

    # 清空剪贴板，防止读到旧数据
    pyperclip.copy("")

    # 发送 Ctrl+A 和 Ctrl+X
    keyboard.send(SELECT_ALL_HOTKEY)
    keyboard.send(CUT_HOTKEY)
    time.sleep(DELAY)

    # 获取剪切后的内容
    new_clip = pyperclip.paste()

    return new_clip

def try_get_image() -> Image.Image | None:
    """
    尝试从剪贴板获取图像，如果没有图像则返回 None。
    仅支持 Windows。
    """
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            if data:
                # 将 DIB 数据转换为字节流，供 Pillow 打开
                bmp_data = data
                # DIB 格式缺少 BMP 文件头，需要手动加上
                # BMP 文件头是 14 字节，包含 "BM" 标识和文件大小信息
                header = b'BM' + (len(bmp_data) + 14).to_bytes(4, 'little') + b'\x00\x00\x00\x00\x36\x00\x00\x00'
                image = Image.open(io.BytesIO(header + bmp_data))
                return image
    except Exception as e:
        print("无法从剪贴板获取图像：", e)
    finally:
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
    return None

def perform_keyboard_actions(png_bytes):
    """在主线程中执行所有键盘操作"""
    if png_bytes is None:
        print("Generate image failed!")
        return
    
    copy_png_bytes_to_clipboard(png_bytes)
    
    if AUTO_PASTE_IMAGE:
        # 使用 call_later 确保 send 在 keyboard 自己的线程中运行
        keyboard.call_later(lambda: keyboard.send(PASTE_HOTKEY), delay=0.1)

        if AUTO_SEND_IMAGE:
            keyboard.call_later(lambda: keyboard.send(SEND_HOTKEY), delay=0.4) # 增加延迟以确保粘贴完成

def Start():
    print("Start generate...")
    
    character_name = get_current_character()
    # 不再使用get_random_value()函数，直接使用expression和backgroundNum构建路径
    address = os.path.join(magic_cut_folder, f"{get_current_character()} ({(expression-1)*16+backgroundNum})"+".jpg")
    BASEIMAGE_FILE = address
    # 修改print语句
    print(character_name,str(expression),"背景",str(backgroundNum))



# 文本框左上角坐标 (x, y), 同时适用于图片框
# 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
    TEXT_BOX_TOPLEFT= (mahoshojo_postion[0], mahoshojo_postion[1])
# 文本框右下角坐标 (x, y), 同时适用于图片框
# 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
    IMAGE_BOX_BOTTOMRIGHT= (mahoshojo_over[0], mahoshojo_over[1])
    
    text = pyperclip.paste() # 暂时从剪贴板获取，而不是模拟按键
    image=try_get_image()

    if text == "" and image is None:
        print("no text or image")
        # 即使没有文本/图像，也调用回调以确保线程安全
        keyboard.call_later(perform_keyboard_actions, args=[None])
        return
    
    png_bytes=None

    if image is not None:
        try:
            print("Get image")
            png_bytes = paste_image_auto(
                image_source=BASEIMAGE_FILE,
                image_overlay=None,
                top_left=TEXT_BOX_TOPLEFT,
                bottom_right=IMAGE_BOX_BOTTOMRIGHT,
                content_image=image,
                align="center",
                valign="middle",
                padding=12,
                allow_upscale=True, 
                keep_alpha=True,      # 使用内容图 alpha 作为蒙版 
                role_name=character_name,  # 传递角色名称
                text_configs_dict=text_configs_dict,  # 传递文字配置字典
                )
        except Exception as e:
            print("Generate image failed:", e)
            keyboard.call_later(perform_keyboard_actions, args=[None])
            return
    
    elif text != "":
        print("Get text: "+text)
# ==================== 新增功能开始 ====================
        # 定义高亮规则变量，默认为 None
        highlight_args = {}
        
        # 如果当前角色是夏目安安 (anan)
        if character_name == "anan":
            # 使用正则表达式匹配中文方括号及内容
            # 颜色采用安安的主题紫色 (参考自你的 text_configs_dict)
            highlight_args = {
                "bracket_color": (159, 145, 251)  # 安安的紫色
            }
        # ==================== 新增功能结束 ====================
        try:
            png_bytes = draw_text_auto(
                image_source=BASEIMAGE_FILE,
                image_overlay=None,
                top_left=TEXT_BOX_TOPLEFT,
                bottom_right=IMAGE_BOX_BOTTOMRIGHT,
                text=text,
                align="left",
                valign='top' ,
                color=(255, 255, 255), 
                max_font_height=145,        # 例如限制最大字号高度为 145 像素
                font_path=get_current_font(),
                role_name=character_name,  # 传递角色名称
                text_configs_dict=text_configs_dict,  # 传递文字配置字典
                **highlight_args
                )

        except Exception as e:
            print("Generate image failed:", e)
            keyboard.call_later(perform_keyboard_actions, args=[None])
            return
        
    # 将 png_bytes 传递给主线程的 perform_keyboard_actions
    keyboard.call_later(perform_keyboard_actions, args=[png_bytes])


def run_start_in_thread():
    if enablewhitelist and get_window_exe_name() not in windowwhitelist:
        print("当前窗口不在白名单内")
        keyboard.send(HOTKEY)
        return
    # 1. 在主线程（keyboard线程）中安全地剪切文本
    text = cut_all_and_get_text()
    
    # 2. 在后台线程中运行耗时的图像处理
    # 将获取的文本作为参数传递给 Start 函数（需要修改Start函数以接受它）
    # 但为了简化，我们依赖于剪贴板，因为 cut_all_and_get_text 已经更新了它
    threading.Thread(target=Start).start()

# GUI界面类
class MagicCutGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("魔法少女的魔裁工具")
        self.root.geometry("800x880")
        
        # 创建滚动文本框
        self.create_intro_text()
        # 创建选择区域
        self.create_selection_area()
        # 创建预览区域
        self.create_preview_area()
        
        # 初始化预览
        self.update_preview()
    
    def create_intro_text(self):
        """创建开头说明文本区域"""
        intro_frame = ttk.Frame(self.root)
        intro_frame.pack(fill=tk.X, padx=10, pady=5)
        
        intro_label = ttk.Label(intro_frame, text="程序说明：", font=("Arial", 12, "bold"))
        intro_label.pack(anchor=tk.W)
        
        intro_text = """角色说明:
1为樱羽艾玛，2为二阶堂希罗，3为橘雪莉，4为远野汉娜
5为夏目安安，6为月代雪，7为冰上梅露露，8为城崎诺亚，9为莲见蕾雅，10为佐伯米莉亚
11为黑部奈叶香，12为宝生玛格，13为紫藤亚里沙，14为泽渡可可

快捷键说明:
Ctrl+1 到 Ctrl+9: 切换角色1-9
Ctrl+q: 切换角色10
Ctrl+e: 切换角色11
Ctrl+r: 切换角色12
Ctrl+t: 切换角色13
Ctrl+y: 切换角色14
Ctrl+0: 显示当前角色
Alt+1-9: 切换表情1-9(部分角色表情较少 望大家谅解)
Enter: 生成图片
Esc: 退出程序
Ctrl+Tab: 清除图片

程序说明：
这个版本的程序占用体积较小，但是需要预加载，初次更换角色后需要等待数秒才能正常使用，望周知（
按Tab可清除生成图片，降低占用空间，但清除图片后需重启才能正常使用
感谢各位的支持

改动说明：
默认启用窗口白名单，只在微信和QQ等聊天窗口前台时才响应热键，避免误触发"""
        
        text_widget = tk.Text(intro_frame, height=15, wrap=tk.WORD, font=("Arial", 9))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, intro_text)
        text_widget.config(state=tk.DISABLED)  # 设置为只读
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(intro_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    
    def create_selection_area(self):
        """创建选择区域"""
        selection_frame = ttk.LabelFrame(self.root, text="角色选择", padding=10)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 角色选择下拉框
        ttk.Label(selection_frame, text="角色:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # 创建角色名称列表用于下拉框
        character_names = []
        for i, key in enumerate(character_list):
            character_names.append(f"{i+1}. {mahoshojo[key]['name']}")
        
        self.character_var = tk.StringVar()
        self.character_combo = ttk.Combobox(selection_frame, textvariable=self.character_var, values=character_names, state="readonly")
        self.character_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.character_combo.set(f"{current_character_index}. {mahoshojo[get_current_character()]['name']}")
        self.character_combo.bind('<<ComboboxSelected>>', self.on_character_change)
        
        # 表情选择区域
        ttk.Label(selection_frame, text="表情:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        expression_frame = ttk.Frame(selection_frame)
        expression_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.expression_var = tk.StringVar(value=str(expression))
        expression_entry = ttk.Entry(expression_frame, textvariable=self.expression_var, width=10)
        expression_entry.pack(side=tk.LEFT)
        expression_entry.bind('<KeyRelease>', self.on_expression_change)
        
        # 表情上下箭头按钮
        expression_buttons_frame = ttk.Frame(expression_frame)
        expression_buttons_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        expression_up_btn = ttk.Button(expression_buttons_frame, text="▲", width=2, 
                                      command=lambda: self.increment_expression(1))
        expression_up_btn.pack(side=tk.TOP)
        
        expression_down_btn = ttk.Button(expression_buttons_frame, text="▼", width=2,
                                        command=lambda: self.increment_expression(-1))
        expression_down_btn.pack(side=tk.TOP)
        
        # 背景选择区域
        ttk.Label(selection_frame, text="背景:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        background_frame = ttk.Frame(selection_frame)
        background_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.background_var = tk.StringVar(value=str(backgroundNum))
        background_entry = ttk.Entry(background_frame, textvariable=self.background_var, width=10)
        background_entry.pack(side=tk.LEFT)
        background_entry.bind('<KeyRelease>', self.on_background_change)
        
        # 背景上下箭头按钮
        background_buttons_frame = ttk.Frame(background_frame)
        background_buttons_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        background_up_btn = ttk.Button(background_buttons_frame, text="▲", width=2,
                                      command=lambda: self.increment_background(1))
        background_up_btn.pack(side=tk.TOP)
        
        background_down_btn = ttk.Button(background_buttons_frame, text="▼", width=2,
                                        command=lambda: self.increment_background(-1))
        background_down_btn.pack(side=tk.TOP)
        
        # 设置列权重使下拉框可以扩展
        selection_frame.columnconfigure(1, weight=1)
    
    def create_preview_area(self):
        """创建预览区域"""
        preview_frame = ttk.LabelFrame(self.root, text="预览", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 预览图像
        self.preview_label = ttk.Label(preview_frame, text="选择有误！", font=("Arial", 16))
        self.preview_label.pack(expand=True)
    
    def on_character_change(self, event):
        """角色选择改变事件"""
        global current_character_index
        selected = self.character_combo.get()
        if selected:
            # 提取角色索引（第一个字符）
            try:
                new_index = int(selected.split('.')[0])
                if 1 <= new_index <= len(character_list):
                    current_character_index = new_index
                    print(f"已切换到角色: {get_current_character()}")
                    # 生成并保存图片
                    generate_and_save_images(get_current_character())
                    self.update_preview()
            except ValueError:
                pass
    
    def on_expression_change(self, event):
        """表情输入改变事件"""
        global expression
        try:
            new_expression = int(self.expression_var.get())
            character_name = get_current_character()
            max_expression = mahoshojo[character_name]["emotion_count"]
            if 1 <= new_expression <= max_expression:
                expression = new_expression
                print(f"已切换至第{expression}个表情")
                self.update_preview()
            else:
                self.preview_label.config(text=f"表情范围: 1-{max_expression}")
        except ValueError:
            self.preview_label.config(text="请输入有效数字")
    
    def on_background_change(self, event):
        """背景输入改变事件"""
        global backgroundNum
        try:
            new_background = int(self.background_var.get())
            if 1 <= new_background <= 16:
                backgroundNum = new_background
                print(f"已切换至第{backgroundNum}个背景")
                self.update_preview()
            else:
                self.preview_label.config(text="背景范围: 1-16")
        except ValueError:
            self.preview_label.config(text="请输入有效数字")
    
    def increment_expression(self, step):
        """表情增减方法"""
        global expression
        try:
            character_name = get_current_character()
            max_expression = mahoshojo[character_name]["emotion_count"]
            new_expression = expression + step
            
            if 1 <= new_expression <= max_expression:
                expression = new_expression
                self.expression_var.set(str(expression))
                print(f"已切换至第{expression}个表情")
                self.update_preview()
            else:
                self.preview_label.config(text=f"表情范围: 1-{max_expression}")
        except Exception as e:
            self.preview_label.config(text="表情调整错误")
    
    def increment_background(self, step):
        """背景增减方法"""
        global backgroundNum
        try:
            new_background = backgroundNum + step
            
            if 1 <= new_background <= 16:
                backgroundNum = new_background
                self.background_var.set(str(backgroundNum))
                print(f"已切换至第{backgroundNum}个背景")
                self.update_preview()
            else:
                self.preview_label.config(text="背景范围: 1-16")
        except Exception as e:
            self.preview_label.config(text="背景调整错误")
    
    def update_preview(self):
        """更新预览图像"""
        try:
            character_name = get_current_character()
            image_path = os.path.join(magic_cut_folder, f"{get_current_character()} ({(expression-1)*16+backgroundNum})"+".jpg")
            
            if os.path.exists(image_path):
                # 加载并显示图像
                image = Image.open(image_path)
                # 调整图像大小以适应预览区域
                image.thumbnail((800, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo  # 保持引用
            else:
                self.preview_label.config(image="", text="选择有误！")
        except Exception as e:
            self.preview_label.config(image="", text=f"预览错误: {str(e)}")

# 主函数
def main():
    # 创建GUI
    root = tk.Tk()
    app = MagicCutGUI(root)
    
    # 角色切换快捷键绑定
    # 按Ctrl+1 到 Ctrl+9: 切换角色1-9
    for i in range(1,10):
        keyboard.add_hotkey(f'ctrl+{i}', lambda idx=i: switch_character(idx))
    
    # 角色10-14使用特殊快捷键
    keyboard.add_hotkey('ctrl+q', lambda: switch_character(10))   # 角色10
    keyboard.add_hotkey('ctrl+e', lambda: switch_character(11))  # 角色11
    keyboard.add_hotkey('ctrl+r', lambda: switch_character(12))  # 角色12
    keyboard.add_hotkey('ctrl+t', lambda: switch_character(13))  # 角色13
    keyboard.add_hotkey('ctrl+y', lambda: switch_character(0))   # 角色14
    keyboard.add_hotkey('ctrl+Tab', lambda: delate(magic_cut_folder))
    
    for i in range(1,10):
        keyboard.add_hotkey(f'alt+{i}', lambda idx=i: get_expression(idx))
    
    # 绑定 Ctrl+Alt+H 作为全局热键
    ok=keyboard.add_hotkey(HOTKEY,run_start_in_thread, suppress=BLOCK_HOTKEY or HOTKEY==SEND_HOTKEY)
    
    # 绑定Ctrl+0显示当前角色
    keyboard.add_hotkey('ctrl+0', show_current_character)
    
    def on_closing():
        # 移除所有热键
        keyboard.unhook_all()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动GUI主循环
    root.mainloop()

if __name__ == "__main__":
    main()
