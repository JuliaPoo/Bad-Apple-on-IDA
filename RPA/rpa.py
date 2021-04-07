import pyautogui as auto
import os, time

auto.hotkey("alt", "tab")
frame = 0

while True:

    reanalyse = None
    while not reanalyse:
        reanalyse = auto.locateOnScreen("anchors/Reanalysis_done.JPG", confidence=.9)

    auto.rightClick(*auto.center(reanalyse))
    time.sleep(.3)

    reanalyse = None
    while not reanalyse:
        reanalyse = auto.locateOnScreen("anchors/Reanalyze_button.JPG", confidence=.9)

    auto.moveTo(*auto.center(reanalyse))
    auto.click()
    auto.click()
    time.sleep(1)

    reanalyse = None
    while not reanalyse:
        reanalyse = auto.locateOnScreen("anchors/Reanalysis_done.JPG", confidence=.9)

    auto.press("w")
    time.sleep(1)

    auto.screenshot("out/frame%d.png"%frame)

    auto.press("F9")

    brkpt = None
    while not brkpt:
        brkpt = auto.locateOnScreen("anchors/Breakpoint.JPG", confidence=.9)

    auto.press("enter")

    brkpt = None
    while not brkpt:
        brkpt = auto.locateOnScreen("anchors/Breakpoint2.JPG", confidence=.9)

    auto.press("enter")

    frame += 1

