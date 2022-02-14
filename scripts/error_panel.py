import tkinter as tk

def error_handler(error):
    error_window_width = 400
    error_window_height = 150
    error_window = tk.Toplevel()
    error_window.geometry(f"{error_window_width}x{error_window_height}+{int((error_window.winfo_screenwidth() / 2) - (error_window_width / 2))}+{int((error_window.winfo_screenheight() / 2) - (error_window_height - 2))}")
    error_window.title("ERROR!")
    error_window.configure(bg = "#383737")

    label = tk.Label(error_window, text= error, font = ("Roboto", 15), fg = "#ffffff", bg = "#383737")
    label.place(relx=0.5, rely=0.5, anchor='center')


