import pygetwindow as gw
import pyautogui
import pyperclip
import time
import get_API
import get_API_img
from windows_pet_v2_yun import event
import win32clipboard
import win32con
from PIL import Image
import io
import threading


def resize_wechat_window():  # 调整窗口大小
    window_titles = gw.getAllTitles()  # 获取所有打开的窗口
    wechat_window = None
    for title in window_titles:  # 判断是否存在标题包含“微信”的窗口
        if "微信" in title:
            wechat_window = gw.getWindowsWithTitle(title)[0]
            break
    if wechat_window:
        wechat_window.restore()  # 还原窗口
        wechat_window.activate()  # 激活窗口显示在前台
        wechat_window.resizeTo(700, 500)
        autowx()
    else:
        print("微信窗口未找到")

is_function_running_text = False
def autowx():
    global is_function_running_text
    red = r'icon\red.png'  # 消息来了的红图标
    name = r'icon\name.png'  # 接收人的图标
    while True:
        if event.is_set():
            break
        else:
            try:
                location_red = pyautogui.locateCenterOnScreen(red, confidence=0.90)
                location_name = pyautogui.locateCenterOnScreen(name, confidence=0.90)
                if location_red and location_name:
                    if 0 < location_name[0] - location_red[0] < 50:
                        if 0 < location_name[1] - location_red[1] < 20:
                            is_function_running_text = True
                            pyautogui.click(location_red)
                            text = find_txt()
                else:
                    time.sleep(1)
            except:
                time.sleep(5)
                continue

num = 0
is_function_running_img = False
is_img_running = False
def find_txt():
    global num, is_img_running
    pos3 = r'icon\pos3.png'  # 聊天窗口
    while True:
        locations_pos3 = pyautogui.locateAllOnScreen(pos3, confidence=0.98)  # 所有坐标
        if locations_pos3:
            break
        else:
            print("没有收到窗口消息,1秒后重试")
            time.sleep(1)
    time.sleep(0.1)
    list_text = list(locations_pos3)
    if list_text != []:
        pos = sorted(list_text, key=lambda x:x[1], reverse=True)[0]  # lambda x:x[1]元组的第二个元素从小到大排序的顺 # reverse降序
        pyautogui.doubleClick(x = pos[0] + 15 + pos[2] / 2,y = pos[1] + pos[3] / 2)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        text = pyperclip.paste()
    t1 = threading.Thread(target=get_API.getchat,args=(text,))
    t1.start()
    if is_img_running == False:
        num = num + 1
        if num % 2 == 0:
            is_img_running = True
            t2 = threading.Thread(target=get_API_img.get_img_memory,args=(text,))
            t2.start()


def givechat(text):
    global is_function_running_text
    pos1 = r'icon\pos1.png'  # 笑脸图标
    send = r'icon\send.png'  # 发送图标
    while True:
        location_pos1 = pyautogui.locateCenterOnScreen(pos1, confidence=0.90)
        location_send = pyautogui.locateCenterOnScreen(send, confidence=0.90)
        if location_pos1 and location_send and is_function_running_img == False:
            break
        else:
            print("没有收到gpt消息,1秒后重试")
            time.sleep(1)
    pyautogui.click(location_pos1[0], location_pos1[1] + 30)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.click(location_send)
    is_function_running_text = False


def givechat_img(img_data):
    global is_function_running_img, is_img_running
    pos1 = r'icon\pos1.png'  # 笑脸图标
    send = r'icon\send.png'  # 发送图标
    while True:
        location_pos1 = pyautogui.locateCenterOnScreen(pos1, confidence=0.90)
        location_send = pyautogui.locateCenterOnScreen(send, confidence=0.90)
        if location_pos1 and location_send and is_function_running_text == False:
            break
        else:
            print("没有收到gpt消息,1秒后重试")
            time.sleep(1)
    is_function_running_img = True
    img_path = io.BytesIO(img_data)
    img = Image.open(img_path)  # 使用 PIL 的 Image 模块从二进制数据打开图像
    output = io.BytesIO()
    img.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()  # 打开剪贴板
    win32clipboard.EmptyClipboard()  # 清空剪贴板
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)  # 将 PNG 数据设置为剪贴板内容
    win32clipboard.CloseClipboard()  # 关闭剪贴板
    pyautogui.click(location_pos1[0], location_pos1[1] + 30)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.click(location_send)
    is_function_running_img = False
    is_img_running = False



# if __name__ == '__main__':
    # resize_wechat_window()








