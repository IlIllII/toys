# Auto Antilock

Auto Antilock is a Python script that prevents your computer screen from locking automatically by toggling the scroll lock key at a specified interval. It's perfect for situations where you need to step away from your computer but don't want to change your screen lock settings.

To use the script, simply navigate to the directory containing it in your terminal and run the following command:

## Instructions

Navigate your terminal to the directory containing this script and type:

```bash
py antilock.py
```

The script will run indefinitely until you stop it by interrupting the program or closing your terminal. You'll know it's working when you see the scroll lock button blinking or when your screen remains unlocked.

By default, the script toggles the scroll lock key every 10 minutes. If you need to toggle it more frequently, you can specify the desired toggle frequency by passing the number of minutes as an argument:

```bash
py antilock.py 5
```

This command will toggle the scroll lock key every 5 minutes.

Please note that the script uses the pyautogui module to toggle the button. If you don't have this module installed, you can install it by typing:

```bash
pip install pyautogui
```

With Auto Antilock, you can step away from your computer with peace of mind, knowing that your screen will stay unlocked until you return.