import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from TkinterDnD2 import DND_FILES, TkinterDnD
import os, os.path
import ipbr
import config

def background_panel_gui():
    # access variables
    global add_background_icon
    global backgrounds_array
    global yindex
    # refresh the yindex value every time the this function is called
    yindex = 0.1

    # create main panel
    background_panel = tk.Frame(mainwindow, height=720, width=350, relief="groove", bg="#161010")
    background_panel.place(relx=0.72, rely=0)
    # create button widgets
    tk.Button(background_panel, height=20, width=20, bd=0, image=add_background_icon, cursor="hand2",
              command=lambda: add_background(background_panel)).place(relx=0.05, rely=0.025)
    tk.Button(background_panel, height = 2, width = 10, text = "Close", font = ("Roboto", 12), cursor = "hand2", fg="white", bg="#ba6032", command = background_panel.destroy).place(relx = 0.70, rely = 0.015)
    # recreate the image gallery with current image and panel as paramenter
    for img in backgrounds_array:
        create_background_gallery(img, background_panel)

    return background_panel

def add_background(panel):
    global backgrounds_array
    if len(backgrounds_array) <= 2:
        image_url = filedialog.askopenfilename(initialdir="/Desktop",
                                               filetypes=(("image files", ".jpg"), ("image files", ".png")))
        create_background_gallery(image_url, panel)
        backgrounds_array.append(image_url)

        conf.set_array_backgrounds(backgrounds_array)
        conf.write()
    else:
        print("Exceeded Number of Backgrounds")

def create_background_gallery(image_url, panel):
    # acces y index
    global yindex
    global im_index
    print(image_url)
    img = Image.open(image_url)
    img.thumbnail((250, 250))
    img = ImageTk.PhotoImage(img)
    # create the image in image gallery, I used button for command attribute
    image_view = tk.Button(panel, name=str(im_index), height=175, width=275, image=img, bg="#383d3a", cursor="hand2",
                           command=lambda: choosebackground(img,image_url, panel))
    image_view.place(relx=0.1, rely=(yindex))
    # create a delete button
    tk.Button(image_view, height="1", width="2", bg="white", cursor="hand2",
              command=lambda: (image_view.destroy(), panel.destroy(), deletebackground(image_url))).place(relx=0.95,
                                                                                                          rely=0.00)
    im_index += 1
    # increase yindex for proper margin of suceeding image
    yindex += 0.3

    return panel

def deletebackground(image_url):
    global backgrounds_array
    print(len(backgrounds_array))
    backgrounds_array.remove(image_url)
    print(len(backgrounds_array))
    conf.set_array_backgrounds(backgrounds_array)
    conf.write()
    background_panel_gui()

def choosebackground(bgimg,image_url, panel):
    #access essential variable background image
    global background_path
    global background_image
    #assign it with the argument variable image
    background_image = bgimg
    background_path = image_url
    background_preview.configure(height=160, width=310, image=background_image)
    conf.set_background(background_path)
    conf.write()
    panel.destroy()

def open_settings():
    # access temporary variables
    global output_loc
    global height_entry_var
    global width_entry_var
    global ifcheck_var
    global ch
    global temp

    temp = tk.BooleanVar()
    temp.set(ifcheck_var)

    height_entry_var.set(str(height_var))
    width_entry_var.set(str(width_var))

    setting_panel = tk.Frame(mainwindow, height=720, width=350, bg="#161010")
    setting_panel.place(relx=0.72, rely=0)
    tk.Button(setting_panel, height=2, width=10, text="Cancel", font=("Roboto", 11), fg="white", bg="#ba6032",
              cursor="hand2", command=setting_panel.destroy).place(relx = 0.70, rely=0.015)
    tk.Button(setting_panel, height=2, width=25, text="Apply Changes", font=("Roboto", 11), fg="white", bg="#127DF4",
              cursor="hand2", command=lambda: [
            save_settings(height_error_label, width_error_label, output_error_label, setting_panel,  ifcheck_var)]).place(
        relx=0.175, rely=0.75)
    tk.Label(setting_panel, text="Settings", font=("Roboto", 20), fg="#127DF4", bg="#161010").place(relx=0.05,
                                                                                                    rely=0.025)
    tk.Label(setting_panel, text="Output Location", font=("Roboto", 14), fg="#D6D2D2", bg="#161010").place(relx=0.05,
                                                                                                           rely=0.1)
    output_loc_entry = tk.Label(setting_panel, width=25, font=("Roboto", 12), fg="#D6D2D2", bg="#161010", bd=2,
                                relief="groove")
    output_loc_entry.configure(text = output_loc)
    output_loc_entry.place(relx=0.05, rely=0.15, height=40)

    output_error_label = tk.Label(setting_panel, font=("Roboto", 10), fg="#ff7045", bg="#161010")
    output_error_label.place(relx=0.25, rely=0.215)

    tk.Button(setting_panel, height=0, width=3, text="...", font=("Roboto", 15), fg="#D6D2D2", bg="#161010", bd=2,
              relief="groove", command=lambda: [get_output_loc(output_loc_entry)]).place(relx=0.7, rely=0.15)

    tk.Label(setting_panel, text="Use Custom Resolution", font=("Roboto", 13), fg="#D6D2D2", bg="#161010").place(
        relx=0.05, rely=0.25)

    tk.Checkbutton(setting_panel, variable= temp, font=("Roboto", 12), bg="#161010",
                   command=lambda: [checkbox(height_entry, width_entry)]).place(relx=0.60, rely=0.248)

    tk.Label(setting_panel, text="Height (Pixels): ", font=("Roboto", 12), fg="#D6D2D2", bg="#161010").place(relx=0.05,
                                                                                                             rely=0.3)
    height_entry = tk.Entry(setting_panel, state='readonly',  textvariable=height_entry_var, width=5,
                            font=("Roboto", 12), fg="#D6D2D2", bg="#161010", bd=3)

    height_entry.place(relx=0.4, rely=0.3)

    tk.Label(setting_panel, text="Width (Pixels): ", font=("Roboto", 12), fg="#D6D2D2", bg="#161010").place(relx=0.05,rely=0.35)

    width_entry = tk.Entry(setting_panel, state='readonly', textvariable=width_entry_var, width=5, font=("Roboto", 12),
                           fg="#D6D2D2", bg="#161010", bd=3)

    width_entry.place(relx=0.4, rely=0.35)
    height_error_label = tk.Label(setting_panel, font=("Roboto", 10), fg="#ff7045", bg="#161010")
    height_error_label.place(relx=0.575, rely=0.305)
    width_error_label = tk.Label(setting_panel, font=("Roboto", 10), fg="#ff7045", bg="#161010")
    width_error_label.place(relx=0.575, rely=0.355)
    checkbox(height_entry, width_entry)

    return height_error_label, width_error_label, output_error_label, output_loc_entry, setting_panel

def checkbox(height_entry, width_entry):
    # check if checkbox is checked or not
    global ifcheck_var
    if temp.get() is True:
        height_entry.configure(state="normal")
        width_entry.configure(state="normal")

    else:
        height_entry.configure(state="readonly")
        width_entry.configure(state="readonly")
        print("false")

    ifcheck_var = temp.get()

def get_output_loc(output_loc_entry):
    #access temporary location variables as holedr
    global temp_output_loc
    global output_loc
    #assign it with value <str> path from filedialog.askdirectory fpr folder path only
    temp_output_loc = filedialog.askdirectory(initialdir= "/Desktop" if temp_output_loc is None else temp_output_loc)

    if not temp_output_loc:
        temp_output_loc = output_loc

    output_loc_entry.configure(text = temp_output_loc)

def save_settings(height_error_label, width_error_label, output_error_label , setting_panel ,ifcheck_var):
    # access permanent variables
    global height_entry_var
    global width_entry_var
    global temp_output_loc
    global output_loc
    global height_var
    global width_var

    height_error = False
    width_error = False

    if ifcheck_var is True:
        try:
            height_var = int(height_entry_var.get())
            height_error_label.configure(text="")
            height_error = False
            # check if height input is 512 or higher
            if height_var < 512:
                height_error_label.configure(text="(512 MINIMUM)")
                height_error = True
            elif height_var == "":
                height_error_label.configure(text="Invalid Input")
                height_error = True
            else:
                height_error = False
        except ValueError:
            height_error_label.configure(text="Numbers Only (Integers)")
            height_error = True
        try:
            width_var = int(width_entry_var.get())
            width_error_label.configure(text="")
            width_error = False
            # check if height input is 512 or higher
            if width_var < 512:
                width_error_label.configure(text="(512 MINIMUM)")
                width_error = True
            elif width_var == "":
                width_error_label.configure(text="(Invalid Input)")
                width_error = True
            else:
                width_error = False
        except ValueError:
            width_error_label.configure(text="Numbers Only (Integers)")
            width_error = True
    else:
        height_var = 900
        width_var = 600

    if height_error is False and width_error is False and os.path.exists(temp_output_loc) is True:
        # pass temporary output location to permanent output location
        output_loc = temp_output_loc
        conf.set_output_path(output_loc)
        conf.set_width(width_var)
        conf.set_height(height_var)
        conf.set_checkbox_state(1 if ifcheck_var is True else 0)
        conf.write()
        setting_panel.destroy()
    else:
        output_error_label.configure(text="Path Not Found!")

def start_process():
    #access permanent variables
    global background_path
    global input_folder_path
    global width_var
    global height_var
    global output_loc

    print(background_path)
    print(input_folder_path)
    print(width_var)
    print(height_var)
    print(output_loc)

    #check if all needed variables are populated
    if(background_path != None and input_folder_path != "" and width_var != 0 and width_var != 0 and output_loc != ""):
        print("Ok!")
        background_path = Image.open(background_path)
        im_names = os.listdir(input_folder_path)
        for im in im_names:
            if im.endswith(".png") or im.endswith(".jpg") or im.endswith(".jpeg"):
                print("Processing: " + im)
                try:
                    img = Image.open(os.path.join(input_folder_path, im))
                    name = im.split('.')[0] + '.png'
                    img = main.process(img, background_path, (width_var, height_var)).save(os.path.join(output_loc, name))
                except:
                    print("Cannot Process: ", im)
        print("DONE!")

    else:
        print("Some Needed Parameters are not defined!")

def drop_inside_list_box(event):
    #access essential variable
    global input_folder_path
    #assign it with data from event
    input_folder_path = event.data

def get_input_handler():
    #access essential variable
    global input_folder_path
    #assign it with data from event
    input_folder_path = filedialog.askdirectory(initialdir = "/Desktop" if input_folder_path is None else input_folder_path,title = "Select Input Path")

    if input_folder_path:
        input_path_validity_handler(input_folder_path)

def input_path_validity_handler(input_folder_path):
    if os.path.exists(input_folder_path):
        input_gallery_gui(input_folder_path)
        view_input_error.configure(text="")
    else:
        view_input_error.configure(text = "No Path Folder Found! Please Intert Inout Folder")

def clear():
    global foreground_input_list_box

    for widgets in foreground_input_list_box.winfo_children():
        widgets.destroy()

    tk.Label(foreground_input_list_box, text="Drop image folder here", font=("Roboto", 20), fg="#D6D2D2",
             bg="#2C2B2B").place(relx=0.25, rely=0.35)
    tk.Label(foreground_input_list_box, text="or", font=("Roboto", 20), fg="#D6D2D2", bg="#2C2B2B").place(relx=0.35,
                                                                                                          rely=0.41)
    tk.Button(foreground_input_list_box, text="Browse", height=1, width=20, font=("Roboto", 17), fg="white",
              bg="#127DF4", cursor="hand2", borderwidth=0, highlightthickness=0, command=get_input_handler).place(
        relx=0.255, rely=0.50)

def input_gallery_gui(input_folder_path):
    global images
    global view_frame
    global foreground_input_list_box
    images = []

    def on_configure(event):
        display_canvas.configure(scrollregion=display_canvas.bbox('all'))

    display_frame = tk.Frame(foreground_input_list_box, height=720, width=927, bg="#2C2B2B")
    display_frame.place(relx=0, rely=0)
    display_canvas = tk.Canvas(display_frame, bg="#2C2B2B", height=720, width=927, borderwidth=0, highlightthickness=0)
    display_canvas.place(relx=0, rely=0)
    view_frame = tk.Frame(display_canvas, bg="#2C2B2B")
    view_frame.bind('<Configure>', on_configure)
    display_canvas.create_window(0, 0, window=view_frame)
    scrollbar = ttk.Scrollbar(display_frame, command=display_canvas.yview, orient= "vertical")
    scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
    display_canvas.configure(yscrollcommand=scrollbar.set)

    row_dimension = 0
    column_cimension = 0
    for file in os.listdir(input_folder_path):
        # validate if file is a valid image file using imghdr.what() module
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            # if file is an image then create an image widget
            try:
                image = Image.open(input_folder_path + "/" + file)
                image.thumbnail((200, 220), resample=4)
                image = ImageTk.PhotoImage(image)
                images.append(image)

                if column_cimension < 4:
                    image_frame = tk.Frame(view_frame, height=200, width=220, bg="#2C2B2B", bd=0, relief="groove")
                    image_frame.grid(row=row_dimension, column=column_cimension)
                    # change the h and w of tk.Button when trying display the image
                    tk.Label(image_frame, image=image, borderwidth= 0).place(relx=0.15, rely=0.1)
                    column_cimension += 1
                else:
                    row_dimension += 1
                    column_cimension = 0
            except:

                if column_cimension < 4:
                    image_frame = tk.Frame(view_frame, height=200, width=220, bg="#2C2B2B", bd=0, relief="groove")
                    image_frame.grid(row=row_dimension, column=column_cimension)
                    # change the h and w of tk.Button when trying display the image
                    tk.Label(image_frame, text= "CORRUPTED IMAGE", bg="BLACK", fg= "#FFFFFF", width=20, height=10 ).place(relx=0.15, rely=0.1)
                    column_cimension += 1
                else:
                    row_dimension += 1
                    column_cimension = 0

    check_gallery()

# delete this line
from threading import Timer

col_d = 0
row_d = 0

def check_gallery():
    global col_d
    global row_d
    global view_frame

    if col_d == 4:
        row_d += 1
        col_d = 0

    if col_d == 0 and row_d != 0:
        label = tk.Label(view_frame, text = " Finish! ", font = ("Roboto", 24), fg = "orange", bg = "black")
        label.grid(row = row_d - 1, column = 3)

    if col_d == 0:
        label = tk.Label(view_frame, text = "Current!", font = ("Roboto", 24), fg = "orange", bg = "black")
        label.grid(row = row_d, column = col_d)
    else:
        label = tk.Label(view_frame, text = "Current!", font = ("Roboto", 24), fg = "orange",bg = "black")
        label.grid(row = row_d, column = col_d)
        label = tk.Label(view_frame, text = " Finish! ", font = ("Roboto", 24), fg = "orange",bg = "black")
        label.grid(row = row_d, column = col_d - 1)
    col_d +=1
    print(row_d)
    print(col_d)
    print("")

    # delete this line as well
    Timer(1, check_gallery).start()



# start of main gui creationg with TkinterDnD wrapper
mainwindow = TkinterDnD.Tk()

# initialize ipbr
main = ipbr.main()

# load config
conf = config.conf()
output_loc, background_path, ifcheck_var, width_var, height_var, backgrounds_array = conf.get_conf()

# convert str to int
width_var = int(width_var)
height_var = int(height_var)

# convert int to bool
ifcheck_var = bool(ifcheck_var)

# set default background preview
try:
    background_image = Image.open(background_path)
    background_image.thumbnail((250, 250))
    background_image = ImageTk.PhotoImage(background_image)
except:
    background_image = None

#global variables
height_entry_var = tk.StringVar()
width_entry_var = tk.StringVar()
temp_output_loc = output_loc
yindex = 0.1
im_index = 0
view_frame = None
input_folder_path = ""

#create and assign icons image
add_background_icon = tk.PhotoImage(file = "../resources/images/add_background_icon.png")
icon2 = ("../resources/images/logo.ico")

#configure mainwindow / root
mainwindow.iconbitmap(icon2)
mainwindow.geometry("1280x720")
mainwindow.title("Intelligent Portrait Background Replacement")
mainwindow.configure(bg = "#323232")
mainwindow.resizable(False, False)

#create main window widgets
frame1 = tk.Frame(mainwindow, height= 50, width = 900, bg = "#323232").place(x=0,y=0)
tk.Button(frame1, height = 1, width = 10, text = "Clear",font = ("Roboto", 14), fg = "white", bg = "#127DF4", cursor = "hand2", borderwidth= 0, highlightthickness= 0,command = lambda: clear()).place(relx = 0.640, rely = 0.035)

foreground_input_list_box = tk.Listbox(mainwindow, selectmode= tk.SINGLE, width = 200, height = 40, bg = "#2C2B2B", bd = 1, relief = "groove", borderwidth= 0, highlightthickness=0 )
foreground_input_list_box.drop_target_register(DND_FILES)
foreground_input_list_box.dnd_bind("<<Drop>>", drop_inside_list_box)
foreground_input_list_box.place(relx= 0.005, rely=0.1)
view_input_error = tk.Label(foreground_input_list_box, font = ("Roboto", 11), fg = "#f7ad8f", bg = "#2C2B2B")
view_input_error.place(relx = 0.65, rely = 0.05)
tk.Label(foreground_input_list_box, text= "Drop image folder here", font = ("Roboto", 20), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.25, rely = 0.35)
tk.Label(foreground_input_list_box, text= "or", font = ("Roboto", 20), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.35, rely = 0.41)
tk.Button(foreground_input_list_box, text = "Browse", height = 1, width=20, font = ("Roboto", 17),  fg = "white", bg = "#127DF4", cursor = "hand2", borderwidth= 0, highlightthickness= 0,command= get_input_handler).place(relx= 0.255, rely = 0.50)

#create menu frame widget
menu_frame = tk.Frame(mainwindow, height= 720, width=350, relief="groove", bg = "#323232")
menu_frame.place(relx= 0.73, rely= 0)
#tk.Label(menu_frame, text = "Chosen Background Image Preview: ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.05, rely = 0.02)
background_preview = tk.Button(menu_frame, height = 10, width = 43, bg = "#2C2B2B", bd =2, relief = "groove", borderwidth= 0, highlightthickness=0)
background_preview.place(relx = 0.05, rely = 0.03)
background_preview.configure(height = 160, width = 310, image = background_image)
tk.Button(menu_frame, height = 2, width = 34, text = "Change Background", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2",borderwidth= 0, highlightthickness= 0, command=background_panel_gui).place(relx= 0.05, rely= 0.30)
tk.Button(menu_frame, height = 2, width = 34, text = "Settings", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2",borderwidth= 0, highlightthickness= 0,command = open_settings).place(relx= 0.05, rely= 0.38)
tk.Button(menu_frame, height = 4, width = 34, text = "Start Process", font = ("Roboto", 12), fg = "white", bg = "#127DF4", cursor ="hand2",borderwidth= 0, highlightthickness= 0, command = start_process).place(relx= 0.05, rely= 0.85)

#make main window display in loop
mainwindow.mainloop()
