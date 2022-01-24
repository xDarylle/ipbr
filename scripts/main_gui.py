from distutils import command
import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import Image, ImageTk
from matplotlib.image import thumbnail
from component_windows.settings_gui import Settings_GUI
from TkinterDnD2 import DND_FILES, TkinterDnD
import ipbr
import os

root = TkinterDnD.Tk()
root.title("Thesis Raph Design")
root.geometry("1280x720")
root.resizable(False, False)

#define variables
backgroundurl_array = []
image_array = []
input_folder_path = ""

def_size = (600, 900)
ipbr = ipbr.main()

#define functions
def helloWorld():
    print("Hello World")

def opensettingswindow():
    #Settings_GUI.settings_gui()
    for image_name in os.listdir(input_folder_path):
        image = Image.open(input_folder_path+ "/" +image_name)
        background = Image.open(backgroundurl_array[0])
        new_image = ipbr.process(image, background, def_size)
        new_image.show()

def selectBackgroundImage():
    global backgroundurl_array

    if(len(backgroundurl_array) < 6):
        imageURL = filedialog.askopenfilename(initialdir = "/Desktop", title = "Select Background Image", filetypes = (("image files",".jpg"),("image files",".png")))
        backgroundurl_array.append(imageURL)
        print(len(backgroundurl_array))

        for image in backgroundurl_array:
            print(image)
            background_view_image = Image.open(image)
            background_view_image.thumbnail((150, 150))
            background_view_image = ImageTk.PhotoImage(background_view_image)
            image_array.append(background_view_image)
            print(len(image_array))

            # background_view .configure(image = image_array[i])
            # background_view[i + 1].image = image_array[i]
            # background_view[i + 1].configure(width = 130, height = 110)

            # background_view2.configure(image = image_array[1])
            # background_view2.image = image_array[1]
            # background_view2.configure(width = 130, height = 110)

            # background_view3.configure(image = image_array[2])
            # background_view3.image = image_array[2]
            # background_view3.configure(width = 130, height = 110)

            # background_view4.configure(image = image_array[3])
            # background_view4.image = image_array[3]
            # background_view4.configure(width = 130, height = 110)

            # background_view5.configure(image = image_array[4])
            # background_view5.image = image_array[4]
            # background_view5.configure(width = 130, height = 110)

            # background_view6.configure(image = image_array[5])
            # background_view6.image = image_array[5]
            # background_view6.configure(width = 130, height = 110)

    else:
        error_background = tk.Toplevel(root)
        error_background.title("Error!")
        error_background.geometry("700x50")
        label = tk.Label(error_background, text = "Number of selected background reach its limit. (Only upto 6 images)", font = ("Tahoma", 12))
        label.pack()

def getInputPath():
    global input_folder_path
    input_folder_path = filedialog.askdirectory(initialdir= "/Desktop", title = "Select Input Folder")
    print(input_folder_path)

def drop_inside_list_box(event):
    global input_folder_path
    # foreground_input.insert("end", event.data)
    input_folder_path = event.data
    print(input_folder_path)
#inittialize widgets

#background / leftside panel
background_frame = tk.Frame(root, width = 322, height= 720, bg = "#3b3832")
background_button = tk.Button(background_frame, width = 30, height = 2,  text = "Select Background", fg = "#ffffff", bg="#3b3832", bd = 2, font = ("Arial", 12), borderwidth = 1, relief= "groove", command = selectBackgroundImage)
background_view1 = tk.Button(background_frame, width=17,  height= 7, bg = "#363636", command = helloWorld)
background_view2 = tk.Button(background_frame, width=17, height= 7, bg = "#363636", command = helloWorld)
background_view3 = tk.Button(background_frame, width=17, height= 7, bg = "#363636", command = helloWorld)
background_view4 = tk.Button(background_frame, width=17, height= 7, bg = "#363636", command = helloWorld)
background_view5 = tk.Button(background_frame, width=17, height= 7, bg = "#363636", command = helloWorld)
background_view6 = tk.Button(background_frame, width=17, height= 7, bg = "#363636", command = helloWorld)
preview_text1 = tk.Label(background_frame, text = "Click Background Preview", font = ("Arial", 12), fg = "white", bg="#3b3832")
preview_text2 = tk.Label(background_frame, text = "to Select Background", font = ("Arial", 12), fg = "white", bg="#3b3832")

#fpregrpund / rightside panel
foreground_pamel = tk.Frame(root, width=960, height=720, bg = "white")
setting_button = tk.Button(foreground_pamel, width = 8, height = 3, bg = "#F3F3F3", command = opensettingswindow)
foreground_input = tk.Listbox(foreground_pamel ,selectmode= tk.SINGLE, width = 135, height = 30, bg = "#e3e3e3", fg = "black")
foreground_input.drop_target_register(DND_FILES)
foreground_input.dnd_bind("<<Drop>>", drop_inside_list_box)
drag_drop_label = tk.Label(foreground_input , text = "Drag and Drop Input Folder Here", font = ("Tahoma", 15), fg = "black", bg = "#e3e3e3")
or_label = tk.Label(foreground_input, text = "Or", font = ("Tahoma", 15), fg = "black" ,bg = "#e3e3e3")
select_button = tk.Button(foreground_input, text = "Select Folder", font = ("Tahoma", 15), fg = "black", bg = '#e3e3e3', command= getInputPath)

#background / leftside panel
background_frame.place(relx=0, rely=0)
background_button.place(relx=0.05, rely=0.025)
background_view1.place(relx = 0.065, rely = 0.1)
background_view2.place(relx = 0.065, rely = 0.3)
background_view3.place(relx = 0.065, rely = 0.5)
background_view4.place(relx = 0.535, rely = 0.1)
background_view5.place(relx = 0.535, rely = 0.3)
background_view6.place(relx = 0.535, rely = 0.5)
preview_text1.place(relx = 0.2, rely = 0.7)
preview_text2.place(relx = 0.25, rely = 0.75)

#foreground / rightside panel
foreground_pamel.place(relx = 0.25, rely= 0)
setting_button.place(relx = 0.025, rely = 0.025)
foreground_input.place(relx = 0.075, rely = 0.15)
drag_drop_label.place(relx = 0.35, rely = 0.35)
or_label.place(relx = 0.49, rely = 0.45)
select_button.place(relx = 0.44, rely = 0.55)

root.mainloop()