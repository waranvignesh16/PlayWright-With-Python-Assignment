import pyautogui
import time
#Mouse Operation
"""
pyautogui.click(100,100)
#time.sleep(2)
#pyautogui.rightClick(100,100)
time.sleep(4)

pyautogui.click(1150,576)

pyautogui.doubleClick(100,100)

#pyautogui.dragTo(100,100,200,200)

#pyautogui.scrollDown(500)

"""

#Keyboard Operation
"""
time.sleep(2)

pyautogui.click(661, 333)

#time.sleep(1)

#pyautogui.typewrite("Socialeagle.ai")

#pyautogui.press("enter")

pyautogui.hotkey('command','a')
"""

#Image Operation

locaiton = pyautogui.locateOnScreen("copilot.png",confidence=0.7)
print(locaiton)

time.sleep(2)

pyautogui.click(pyautogui.center(locaiton))

#print(pyautogui.size())

#ss = pyautogui.screenshot()

#s.save("demo.png")