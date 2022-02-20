import tkinter as tk

error_icon = "resources/images/error.ico"
warning_icon = "resources/images/warning.ico"
done_icon = "resources/images/done.ico"

def error_handler(error, isError):
    error_window_width = 400
    error_window_height = 150
    error_window = tk.Toplevel()
    error_window.geometry(f"{error_window_width}x{error_window_height}+{int((error_window.winfo_screenwidth() / 2) - (error_window_width / 2))}+{int((error_window.winfo_screenheight() / 2) - (error_window_height - 2))}")
    if isError:
        error_window.iconbitmap(error_icon)
        error_window.title("ERROR!")
    else:
        error_window.title("WARNING!")
        error_window.iconbitmap(warning_icon)
    error_window.configure(bg = "#383737")

    label = tk.Label(error_window, text= error, font = ("Roboto", 15), fg = "#f0eee9", bg = "#383737", wraplength=300, justify="center")
    label.place(relx=0.5, rely=0.5, anchor='center')

def done_handler(text):
    error_window_width = 400
    error_window_height = 150
    error_window = tk.Toplevel()
    error_window.geometry(f"{error_window_width}x{error_window_height}+{int((error_window.winfo_screenwidth() / 2) - (error_window_width / 2))}+{int((error_window.winfo_screenheight() / 2) - (error_window_height - 2))}")
    error_window.title("Notification")
    error_window.iconbitmap(done_icon)
    error_window.configure(bg = "#383737")

    label = tk.Label(error_window, text= text, font = ("Roboto", 15), fg = "#f0eee9", bg = "#383737")
    label.place(relx=0.5, rely=0.5, anchor='center')

