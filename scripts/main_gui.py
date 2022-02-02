from argparse import FileType
from distutils import command
from multiprocessing.sharedctypes import Value
import tkinter as tk
from tkinter import BooleanVar, StringVar, font
from turtle import width
from tkinter import PhotoImage, filedialog
from typing_extensions import IntVar
from PIL import Image, ImageTk
from TkinterDnD2 import DND_FILES, TkinterDnD
import os, os.path
import imghdr
import ipbr

import config

# class MainWindow():
    
#     def main_gui_design(self):
def background_panel_gui():

    #access variables
    global add_background_icon
    global backgrounds_array
    global yindex
    #refresh the yindex value every time the this function is called
    yindex = 0.1

    #create main panel
    background_panel = tk.Frame(mainwindow, height= 720, width=350, relief="groove", bg = "#161010")
    background_panel.place(relx= 0.72, rely= 0)
    #create button widgets
    tk.Button(background_panel, height = 20, width = 20,bd = 0, image = add_background_icon, cursor="hand2", command = lambda: add_background(background_panel)).place(relx= 0.05, rely= 0.025)
    tk.Button(background_panel, height = 0, width = 0, bd = 0, text = "Add Background", font = ("Roboto", 15), fg = "#CDC9C9", bg = "#383d3a", cursor="hand2", command = (lambda: add_background(background_panel))).place(relx= 0.15, rely= 0.015)
    tk.Button(background_panel, height = 0, width = 0, bd = 1, text = "Done",font = ("Roboto", 15), fg = "#CDC9C9", bg = "#383d3a", cursor="hand2", command= background_panel.destroy).place(relx= 0.75, rely= 0.015)

    #recreate the image gallery with current image and panel as paramenter
    for img in backgrounds_array:
        create_background_gallery(img, background_panel)
    
    return background_panel

def add_background(panel):    
    global backgrounds_array
    print(len(backgrounds_array))
    if len(backgrounds_array) <= 2:
        image_url = filedialog.askopenfilename(initialdir="/Desktop", filetypes=(("image files",".jpg"),("image files",".png")))
        create_background_gallery(image_url, panel)
        backgrounds_array.append(image_url)
        conf.set_array_backgrounds(backgrounds_array)
        conf.write()
    else:
        print("Exceeded Number of Backgrounds")

def create_background_gallery(image_url, panel):
    #acces y index
    global yindex
    global im_index

    img = Image.open(image_url)
    img.thumbnail((250, 250))
    img = ImageTk.PhotoImage(img)
    #create the image in image gallery, I used button for command attribute
    image_view = tk.Button(panel,name = str(im_index), height= 175, width = 275 , image = img, bg = "#383d3a", cursor = "hand2", command = lambda: choosebackground(img, image_url))
    image_view.place(relx = 0.1, rely = (yindex))
    #create a delete button
    tk.Button(image_view, height = "1", width = "2", bg = "white", cursor="hand2", command = lambda: (image_view.destroy(), panel.destroy(), deletebackground(image_url))).place(relx = 0.95, rely = 0.00)
    im_index += 1
    #increase yindex for proper margin of suceeding image
    yindex += 0.3

def deletebackground(image_url):
    global backgrounds_array
    print(len(backgrounds_array))
    backgrounds_array.remove(image_url)
    conf.set_array_backgrounds(backgrounds_array)
    conf.write()
    print(len(backgrounds_array))

    background_panel_gui()

def choosebackground(bgimg, image_url):
    #access essential variable background image
    global background_image
    print("here")
    #assign it with the argument variable image
    background_image = image_url
    conf.set_background(background_image)
    conf.write()
    background_preview.configure(height = 160, width = 310, image = bgimg)

def open_settings():
    #access temporary variables
    global temp_output_loc
    global height_temp
    global width_temp

    #create variable for checkbox  with bollean as datatype
    ifcheck_var = BooleanVar()
  
    setting_panel = tk.Frame(mainwindow, height= 720, bd = 2, width=350, relief="groove", bg = "#161010")
    setting_panel.place(relx= 0.72, rely= 0)
    tk.Button(setting_panel, height = 2, width = 10, text = "Cancel", font = ("Roboto", 11), fg = "white", bg = "#ba6032", cursor = "hand2", command = setting_panel.destroy).place(relx = 0.65, rely = 0.025)
    tk.Button(setting_panel, height = 2, width = 25, text = "Apply Changes", font = ("Roboto", 11), fg = "white", bg = "#127DF4", cursor = "hand2" , command = lambda : [save_settings(setting_panel,height_error_label,width_error_label)]).place(relx = 0.175, rely = 0.75)
    tk.Label(setting_panel, text = "Settings", font = ("Roboto", 20), fg = "#127DF4", bg = "#161010").place(relx= 0.05, rely= 0.025)
    tk.Label(setting_panel, text = "Output Location", font = ("Roboto", 14), fg = "#D6D2D2", bg = "#161010").place(relx= 0.05, rely= 0.1)
    output_loc_entry = tk.Label(setting_panel, width = 25, font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 2, relief= "groove")
    output_loc_entry.place(relx = 0.05, rely = 0.15, height =40)
    tk.Button(setting_panel, height= 0,  width= 3, text = "...", font = ("Roboto", 15), fg = "#D6D2D2", bg = "#161010", bd = 2, relief= "groove", command= lambda : [output_loc_entry.destroy(), get_output_loc(setting_panel)]).place(relx= 0.7, rely = 0.15)
    tk.Label(setting_panel, text = "Use Custom Resolution", font = ("Roboto", 13), fg = "#D6D2D2", bg = "#161010").place(relx = 0.05, rely = 0.25)
    tk.Checkbutton(setting_panel, variable = ifcheck_var, font = ("Roboto", 12), bg = "#161010", command=lambda: [height_entry.destroy(), width_entry.destroy(), checkbox(ifcheck_var.get(), setting_panel)]).place(relx= 0.60, rely = 0.248)
    tk.Label(setting_panel, text = "Height (Pixels): ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010").place(relx= 0.05, rely = 0.3)
    height_entry = tk.Entry(setting_panel, state = 'disabled', width = 5, font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
    height_entry.place(relx= 0.4, rely = 0.3)
    tk.Label(setting_panel, text = "Width (Pixels): ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010").place(relx= 0.05, rely = 0.35)
    width_entry = tk.Entry(setting_panel,  state = 'disabled', width = 5, font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
    width_entry.place(relx= 0.4, rely = 0.35)
    height_error_label = tk.Label(setting_panel, font = ("Roboto", 10), fg = "#ff7045", bg = "#161010")
    height_error_label.place(relx= 0.575, rely = 0.305)
    width_error_label = tk.Label(setting_panel, font = ("Roboto", 10), fg = "#ff7045", bg = "#161010")
    width_error_label.place(relx= 0.575, rely = 0.355)

    return height_error_label, width_error_label, setting_panel


def checkbox(ifcheck_var, element):
    #access temporary width and hieght holder variables
    global height_temp
    global width_temp

    #check if checkbox is checked or not
    if ifcheck_var == True:
        #if yet create entry widget with state == normal since I can't entry.configure it when I pass it as parameter
        height_entry = tk.Entry(element, width = 5, textvariable= height_temp, state = "normal", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
        height_entry.place(relx= 0.4, rely = 0.3)
        width_entry = tk.Entry(element, width = 5, textvariable= width_temp, state = "normal", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
        width_entry.place(relx= 0.4, rely = 0.35)
        #if not recreate the entry with state == disabled
    else:
        height_entry = tk.Entry(element, width = 5, state = "readonly", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
        height_entry.place(relx= 0.4, rely = 0.3)
        width_entry = tk.Entry(element, width = 5, state = "readonly", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 3)
        width_entry.place(relx= 0.4, rely = 0.35)
        
    print(ifcheck_var)

def get_output_loc(element):
    #access temporary location variables as holedr
    global temp_output_loc

    #assign it with value <str> path from filedialog.askdirectory fpr folder path only
    temp_output_loc = filedialog.askdirectory(initialdir= "/Desktop")
    output_loc_entry = tk.Label(element, text = temp_output_loc ,width = 25, font = ("Roboto", 12), fg = "#D6D2D2", bg = "#161010", bd = 2, relief= "groove")
    output_loc_entry.place(relx = 0.05, rely = 0.15, height =40)

def save_settings(setting_panel,height_error_label,width_error_label):
    #access temporary variables
    global temp_output_loc
    global height_temp
    global width_temp

    #access permanent variables
    global output_loc
    global height_var
    global width_var

    try: 
        height_holder = int(height_temp.get())
        height_error_label.configure(text = "")
        height_error = False
        # check if height input is 512 or higher
        if height_holder < 512:
            height_error_label.configure(text = "(512 MINIMUM)")
            height_error = True
        else:
            height_error = False

    except ValueError:
        height_error_label.configure(text = "Numbers Only (Integers)")
        height_error = True
    try: 
        width_holder = int(width_temp.get())
        width_error_label.configure(text = "")
        width_error = False
                # check if height input is 512 or higher
        if width_holder < 512:
            width_error_label.configure(text = "(512 MINIMUM)")
            width_error = True
        else:
            width_error = False
    except ValueError:
        width_error_label.configure(text = "Numbers Only (Integers)")
        width_error = True

    # print(output_loc)
    # print(height_error)
    # print(width_error)

    # if all conditions are good and no errors then pass all data to corresponding permanent variables
    if height_error == False and width_error == False and temp_output_loc != "":
        #assign permanent variables when saving settings
        output_loc = temp_output_loc
        height_var = height_holder
        width_var = width_holder

        conf.set_output_path(str(output_loc))
        conf.set_width(str(width_var))
        conf.set_height(str(height_var))
        conf.write()

        setting_panel.destroy()
    else:
        tk.Label(setting_panel, text = "Please check all fields inputs!", font = ("Roboto", 15), fg = "#ff7045", bg = "#161010").place(relx= 0.125, rely = 0.7)

def start_process():

    #access permanent variables
    global background_image
    global input_folder_path
    global width_var
    global height_var
    global output_loc

    print(background_image)
    print(input_folder_path)
    print(width_var)
    print(height_var)
    print(output_loc)

    #check if all needed variables are populated
    if(background_image != None and input_folder_path != "" and width_var != 0 and width_var != 0 and output_loc != ""):
        print("Ok!")
        background_image = Image.open(background_image)
        im_names = os.listdir(input_folder_path)
        for im in im_names:
            print("Processing: " + im)
            img = Image.open(os.path.join(input_folder_path, im))
            name = im.split('.')[0] + '.png'
            img = main.process(img, background_image, (width_var, height_var)).save(os.path.join(output_loc, name))
        print("DONE!")

    else:
        print("Some Needed Parameters are not defined!")

def drop_inside_list_box(event):
    #access essential variable
    global input_folder_path
    #assign it with data from event
    input_folder_path = event.data
    #configure the label widget to display path text in the gui
    input_folder_label.configure(text = input_folder_path)
    #call counter function and pass the path
    file_counter_handler(input_folder_path)

def get_input_handler():
    #access essential variable
    global input_folder_path
    #assign it with data from event
    input_folder_path = filedialog.askdirectory(initialdir = "/Desktop",title = "Select Input Path")
    #configure the label widget to display path text in the gui
    input_folder_label.configure(text = input_folder_path)
    #call counter function and pass the path
    file_counter_handler(input_folder_path)

def file_counter_handler(filepath):
    #initialise a counter variable
    i = 0
    #looping every file inside the path
    for name in os.listdir(filepath):
        #check if file is an image or not
        if imghdr.what(os.path.join(filepath, name)) == "jpeg" or imghdr.what(os.path.join(filepath, name)) == "jpg" or imghdr.what(os.path.join(filepath, name)) == "png":
            #if file is an image increase counter var by 1
            i += 1
    #configure label widget to display file count to gui
    input_counter_label.configure(text = i)


# start of main gui creationg with TkinterDnD wrapper
mainwindow = TkinterDnD.Tk()

# initialize ipbr
main = ipbr.main()

# load config
conf = config.conf()
output_loc, background_image, width_var, height_var = conf.get_conf()

#global variables
#temporary holder variables
height_temp = StringVar()
width_temp = StringVar()  
temp_output_loc = ""

input_count = 0
yindex = 0.1
backgrounds_array = []
im_index = 0

#create and assign icons image
add_background_icon = tk.PhotoImage(file = "../resources/images/add_background_icon.png")
icon = tk.PhotoImage(file = "../resources/images/add_background_icon.png")

#configure mainwindow / root
mainwindow.iconphoto(False, icon)
mainwindow.geometry("1280x720")
mainwindow.title("Main Window")
mainwindow.configure(bg = "#2C2B2B")
mainwindow.resizable(False, False)

#create main window widgets
tk.Label(mainwindow, text = "Input Path: ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.02, rely=0.02)
input_folder_label = tk.Label(mainwindow,  font = ("Rboto", 12), fg = "#D6D2D2", bg = "#2C2B2B")
input_folder_label.place(relx= 0.085, rely= 0.02)
tk.Label(mainwindow, text = "Input Count", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.4, rely= 0.02)
input_counter_label = tk.Label(mainwindow,  font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B")
input_counter_label.place(relx= 0.475, rely= 0.02)
foreground_input_list_box = tk.Listbox(mainwindow, selectmode= tk.SINGLE, width = 155, height = 31, bg = "#2C2B2B", bd = 1, relief = "groove")
foreground_input_list_box.drop_target_register(DND_FILES)
foreground_input_list_box.dnd_bind("<<Drop>>", drop_inside_list_box)
foreground_input_list_box.place(relx= 0, rely=0.3)
tk.Label(foreground_input_list_box, text= "Drop Input Folder Here", font = ("Roboto", 14), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.40, rely = 0.35)
tk.Label(foreground_input_list_box, text= "or", font = ("Roboto", 14), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.50, rely = 0.45)
tk.Button(foreground_input_list_box, text = "Browse", height = 1, width=10, font = ("Roboto", 14),  fg = "#D6D2D2", bg = "#2C2B2B", cursor = "hand2", command= get_input_handler).place(relx= 0.45, rely = 0.55)

#create menu frame widget
menu_frame = tk.Frame(mainwindow, height= 720, width=350, relief="groove", bg = "#2C2B2B")
menu_frame.place(relx= 0.72, rely= 0)
tk.Label(menu_frame, text = "Chosen Background Image Preview: ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.05, rely = 0.02)
background_preview = tk.Button(menu_frame, height = 10, width = 43, bg = "#2C2B2B", bd =2, relief = "groove")
background_preview.place(relx = 0.05, rely = 0.05)
tk.Button(menu_frame, height = 2, width = 34, text = "Change Background", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2", command=background_panel_gui).place(relx= 0.05, rely= 0.30)
tk.Button(menu_frame, height = 2, width = 34, text = "Settings", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2", command = open_settings).place(relx= 0.05, rely= 0.45)
tk.Button(menu_frame, height = 4, width = 34, text = "Start Process", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2", command = start_process).place(relx= 0.05, rely= 0.85)

#make main window display in loop
mainwindow.mainloop()
