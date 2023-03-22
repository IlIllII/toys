import sys
import time
import pyautogui

MINUTE = 60
sleep_duration = 10 * MINUTE


if __name__ == "__main__":
    args = sys.argv[1:]

    for arg in args:
        try:
            sleep_duration = int(arg) * MINUTE
        except:
            print("Usage: antilock.py [antilock frequency in minutes]")
            exit(0)

    if sleep_duration < 0:
        print("frequency must be a postitive number.")
        exit(0)

    while True:
        pyautogui.press("scrolllock")
        time.sleep(sleep_duration)