# tests/test_gui.py
import tkinter as tk
from gui.app import App

def test_gui_init():
    app = App()
    assert app.title() == "Network Server GUI"
    app.destroy()