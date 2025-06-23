import pyautogui
import time
import pyscreeze
import winsound
import sys


from sys import exit

# 配置参数
BUTTON_IMAGES = ['button1.png', 'button2.png', 'button3.png', 'button4.png']  # 按钮截图列表
MAX_RETRIES = 200             # 总循环次数
TIMEOUT = 120                 # 单次按钮等待超时（秒）
CONFIDENCE = 0.8              # 图像识别置信度（需OpenCV）
PAUSE = 1                     # 操作间隔时间（防失控）

# 设置PyAutoGUI安全参数
pyautogui.PAUSE = PAUSE

def long_beep():
    """持续5秒的蜂鸣声（Windows）"""
    try:
        duration = 5000   # 持续5秒（5000毫秒）
        frequency = 1000  # 1000Hz高频警报音
        winsound.Beep(frequency, duration)
    except Exception as e:
        print(f"蜂鸣失败: {e}")

def wait_and_click(image_path):
    """等待按钮出现并点击，超时则退出"""
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE)
            if pos:
                pyautogui.click(pos)
                # print(f"[成功] 点击按钮: {image_path}")
                return True
        except Exception as e:
            # print(f"识别 {image_path} 时出错: {str(e)}")
            time.sleep(0.5)
            # pass  # 显式忽略错误，避免空代码块
    print(f"[超时] 未找到按钮: {image_path}")
    return False

def single_cycle(cycle_num):
    """单次循环：依次点击4个按钮"""
    print(f"\n=== 开始第 {cycle_num} 次循环 ===")
    for button in BUTTON_IMAGES:
        if not wait_and_click(button):
            print(f"退出本次循环，重新加载初始网页")             
            pyautogui.hotkey('ctrl', 'r')    # 重新加载每次循环的初始网页            
            long_beep()     # 调用蜂鸣告警5秒
            time.sleep(5)   # 初始网页加载较慢，等待5秒       
            return True  # 点击按钮失败则退出本次循环
        time.sleep(1)    # 点击后等待下一个页面加载
    return True

def main():
    print(f"=== 开始自动化流程（共 {MAX_RETRIES} 次循环）===")
    for i in range(1, MAX_RETRIES + 1):
        if not single_cycle(i):
            exit(1)  # 任意一次失败则退出
    print("所有循环完成！")

if __name__ == "__main__":
    main()
