##########################
# Program: MouseRecorder #
# Code Version: 1.3      #
# Code by BolliSoft      #
# (c) by Nico Bollhalder #
##########################

import pyautogui
import keyboard
import time
from pynput import mouse, keyboard as pynput_keyboard
import tkinter as tk
from tkinter import filedialog

def record_position():
    x, y = pyautogui.position()
    with open(filename, "a") as f:
        f.write(f"Position: {x},{y}\n")

def on_click(x, y, button, pressed):
    if pressed:
        with open(filename, "a") as f:
            f.write("Click\n")

def on_press(key):
    try:
        with open(filename, "a") as f:
            f.write(f"Key: {key.char}\n") 
    except AttributeError:
        with open(filename, "a") as f:
            f.write(f"Key: {key}\n") 

def record_delay():
    try:
        delay = float(10.0)  # Default delay of 1 second
        with open(filename, "a") as f:
            f.write(f"Delay: {delay}\n")
    except ValueError:
        print("Invalid input. Please enter a number.") 

def start_recording(wert1,wert2):
    global filename
    filename = filedialog.asksaveasfilename(initialdir="./Konfig/Recorder/", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not filename:
        return  # User cancelled

    # Mouse clicks and keyboard inputs are detected automatically
    with mouse.Listener(on_click=on_click) as mouse_listener, \
         pynput_keyboard.Listener(on_press=on_press) as keyboard_listener:

        print("Recording program started.\n\nKey: F3 (Add delay)\n\nMouse clicks and keyboard inputs are recorded automatically.\n\nPress 'F4' to stop.\n\nCode by BolliSoft (Nico Bollhalder) (c)")

        while True:
            record_position()
            time.sleep(0.1) 
            if keyboard.is_pressed(wert2):
                mouse_listener.stop()
                keyboard_listener.stop()
                break

        mouse_listener.stop()
        keyboard_listener.stop()
    print("Recording stopped. Data saved to:", filename)

#start_recording()
##keyboard.press("o")
