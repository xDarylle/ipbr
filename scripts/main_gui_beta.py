import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from TkinterDnD2 import DND_FILES, TkinterDnD
import os, os.path
import sys
from threading import *
import cv2
from pygrabber.dshow_graph import FilterGraph
import time
import numpy as np

sys.path.append('scripts')
import ipbr
import config
import cam_modnet
from error_panel import error_handler, done_handler

if __name__ == "__main__":
    def background_panel_gui():
        # access variables
        global add_background_icon
        global backgrounds_array
        global yindex
        # refresh the yindex value every time the this function is called
        yindex = 0.1

        # create main panel
        background_panel = tk.Frame(mainwindow, height=720, width=360, relief="groove", bg="#161010")
        background_panel.place(relx=0.72, rely=0)
        # create button widgets
        tk.Button(background_panel, height=20, width=20, bd=0, image=add_background_icon, cursor="hand2",
                  command=lambda: add_background(background_panel)).place(relx=0.05, rely=0.025)
        tk.Button(background_panel, height = 1, width = 15, text = "Add Background", font = ("Roboto", 12), fg = "#ffffff", bg = "#161010", activebackground = "#858585", cursor = "hand2", borderwidth=0, highlightthickness=0,command=lambda: add_background(background_panel)).place(relx=0.15, rely=0.02)
        tk.Button(background_panel, height = 1, width = 8, text = "Close", font = ("Roboto", 12),borderwidth=0, highlightthickness=0, cursor = "hand2", fg="white", bg="#303E8C", command = background_panel.destroy).place(relx = 0.7, rely = 0.02)
        # recreate the image gallery with current image and panel as paramenter
        for img in backgrounds_array:
            create_background_gallery(img, background_panel)

        return background_panel

    def add_background(panel):
        global backgrounds_array
        if len(backgrounds_array) <= 2:
            image_url = filedialog.askopenfilename(initialdir="/Desktop" if len(backgrounds_array) == 0 else  os.path.dirname(backgrounds_array[-1]),
                                                   filetypes=(("image files", ".jpg"), ("image files", ".png")))
            if image_url:
                create_background_gallery(image_url, panel)
                backgrounds_array.append(image_url)

                conf.set_array_backgrounds(backgrounds_array)
                conf.write()
        else:
            text = "Exceeded Number of Backgrounds"
            error_handler(text, True)

    def create_background_gallery(image_url, panel):
        # acces y index
        global yindex
        global im_index
        global isPortraitBackground
        global height_prev_bg

        if os.path.exists(image_url):
            img = Image.open(image_url)
            img.thumbnail((250, 250))
            img = ImageTk.PhotoImage(img)

            # create the image in image gallery, I used button for command attribute
            image_panel = tk.Frame(panel, height = 180, width = img.width(), bg = "#161010")
            mainwindow.update()
            x = ((panel.winfo_width() - img.width()) / 2) / panel.winfo_width()
            image_panel.place(relx=x, rely=(yindex))
            image_view = tk.Button(image_panel, text="view", height=img.height(), width=img.width(), image=img, bg="#383d3a", cursor="hand2", borderwidth=0, highlightthickness=0,
                                   command=lambda: choosebackground(img,image_url, panel))
            image_view.place(relx=0,rely=0)

            # create a delete button
            mainwindow.update()
            bx = (image_view.winfo_width() - 25)/image_view.winfo_width()
            delete = tk.Button(image_panel, image = trash_image, height="20", width="20", bg="#161010", cursor="hand2",
                      command=lambda: (deletebackground(image_url, image_view, panel)))
            delete.place(relx=bx, rely=0.00)

            im_index += 1
            # increase yindex for proper margin of succeeding images
            yindex += 0.285
        else:
            text = "Background Image Not Found\n" + image_url
            error_handler(text, True)
            backgrounds_array.remove(image_url)
            conf.set_array_backgrounds(backgrounds_array)
            conf.write()

        return panel

    def deletebackground(image_url, image_view, panel):
        global backgrounds_array
        global background_path

        image_view.destroy()
        panel.destroy()

        backgrounds_array.remove(image_url)
        if len(backgrounds_array) == 0:
            background_preview.configure(height=160, width=310, image = "")
            background_path = ""
            conf.set_background("")
            conf.set_array_backgrounds(backgrounds_array)
            conf.write()

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
        global inputsize_checkbox
        global isSaveTransparent

        temp.set(ifcheck_var)

        height_entry_var.set(str(height_var))
        width_entry_var.set(str(width_var))

        setting_panel = tk.Frame(mainwindow, height=720, width=350, bg="#161010")
        setting_panel.place(relx=0.730, rely=0)
        tk.Label(setting_panel, text="Settings", font=("Roboto", 20), fg="#4369D9", bg="#161010").place(relx=0.05,
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

        tk.Label(setting_panel, text = "Use Input Sizes", font = ("Roboto", 13), fg="#D6D2D2", bg="#161010").place(relx = 0.05, rely = 0.3)
        tk.Label(setting_panel, text = "Save transparent background",font = ("Roboto", 13), fg="#D6D2D2", bg="#161010").place(relx = 0.05, rely = 0.25)
        tk.Checkbutton(setting_panel,  bg="#161010", variable=isSaveTransparent).place(relx = 0.7, rely = 0.25)

        tk.Checkbutton(setting_panel, variable = inputsize_checkbox, bg="#161010", command = lambda: use_input_reso_handler(inputsize_checkbox.get(),customreso_cbeckbox, height_entry, width_entry)).place(relx = 0.7, rely = 0.298)

        tk.Label(setting_panel, text="Use Custom Sizes", font=("Roboto", 13), fg="#D6D2D2", bg="#161010").place(relx=0.05, rely=0.35)

        customreso_cbeckbox = tk.Checkbutton(setting_panel, variable= temp, bg="#161010",command=lambda: [checkbox(height_entry, width_entry)])
        customreso_cbeckbox.place(relx=0.7, rely=0.348)

        tk.Label(setting_panel, text="Height (Pixels): ", font=("Roboto", 12), fg="#D6D2D2", bg="#161010").place(relx=0.05,rely=0.4)
        height_entry = tk.Entry(setting_panel, state='readonly',  textvariable=height_entry_var, width=5,
                                font=("Roboto", 12), fg="#D6D2D2", bg="#161010", bd=3)

        height_entry.place(relx=0.4, rely=0.4)

        tk.Label(setting_panel, text="Width (Pixels): ", font=("Roboto", 12), fg="#D6D2D2", bg="#161010").place(relx=0.05,rely=0.45)

        width_entry = tk.Entry(setting_panel, state='readonly', textvariable=width_entry_var, width=5, font=("Roboto", 12),
                               fg="#D6D2D2", bg="#161010", bd=3)

        width_entry.place(relx=0.4, rely=0.45)
        height_error_label = tk.Label(setting_panel, font=("Roboto", 10), fg="#ff7045", bg="#161010")
        height_error_label.place(relx=0.575, rely=0.405)
        width_error_label = tk.Label(setting_panel, font=("Roboto", 10), fg="#ff7045", bg="#161010")
        width_error_label.place(relx=0.575, rely=0.455)

        tk.Button(setting_panel, height=2, width=30, text="Cancel", font=("Roboto", 13), fg="white", bg="#DC4343", borderwidth=0, highlightthickness=0,
                  cursor="hand2", command=setting_panel.destroy).place(relx = 0.07, rely=0.85)
        tk.Button(setting_panel, height=2, width=30, text="Apply Changes", font=("Roboto", 13), fg="white", bg="#303E8C", borderwidth=0, highlightthickness=0,
                  cursor="hand2", command=lambda: [
                save_settings(height_error_label, width_error_label, output_error_label, setting_panel,  ifcheck_var)]).place(
            relx=0.07, rely=0.75)

        tk.Label(setting_panel)

        checkbox(height_entry, width_entry)

        return height_error_label, width_error_label, output_error_label, output_loc_entry, setting_panel, customreso_cbeckbox, height_entry, width_entry

    def use_input_reso_handler(inputsize_checkbox,customreso_cbeckbox,  height_entry, width_entry):
        global ifcheck_var

        if inputsize_checkbox == True:
            ifcheck_var = 0
            temp.set(False)
            height_entry.configure(state = "disabled")
            width_entry.configure(state = "disabled")
        else:
            ifcheck_var = 1
            temp.set(True)
            customreso_cbeckbox.configure(state="normal")
            height_entry.configure(state="normal")
            width_entry.configure(state="normal")

    def checkbox(height_entry, width_entry):
        # check if checkbox is checked or not
        global ifcheck_var
        global temp
        global inputsize_checkbox

        if temp.get() is True:
            inputsize_checkbox.set(False)
            height_entry.configure(state="normal")
            width_entry.configure(state="normal")

        else:
            height_entry.configure(state="readonly")
            width_entry.configure(state="readonly")

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
            conf.set_save_transparent(1 if isSaveTransparent.get() is True else 0)
            conf.set_checkbox_state(1 if ifcheck_var is True else 0)
            conf.write()
            setting_panel.destroy()
        else:
            output_error_label.configure(text="Path Not Found!")

    def update_preview(img):
        global imm
        global preview

        img.thumbnail((350, 350), resample=1)
        p = ImageTk.PhotoImage(img)
        imm.append(p)
        preview.configure(height=330, width=315, image=p)

    def start_thread():
        if input_array:
            t1 = Thread(target=start_process)
            t1.daemon = True
            t1.start()

    def stop_process():
        global stopped
        global stop_btn

        stopped = True
        stop_btn.destroy()

    def start_process():
        #access permanent variables
        global background_path
        global input_folder_path
        global width_var
        global height_var
        global output_loc
        global preview
        global imm
        global column_size
        global inputsize_checkbox
        global stop_btn
        global stopped
        global isModelPresent

        #check if all needed variables are populated
        try:
            if not isModelPresent:
                text = "Pretrained Model not found!"
                error_handler(text, True)
            elif not os.path.exists(output_loc):
                text = "Output path does not exists or is not set!"
                error_handler(text, True)
            else:
                background = Image.open(background_path)
                i = 0
                stopped = False
                stop_btn = tk.Button(menu_frame, height=3, width=25, text="STOP", font=("Roboto", 16), fg="#e0efff",
                                     bg="#DC4343", activebackground="#4a9eff", cursor="hand2", borderwidth=0,
                                     highlightthickness=0, command=stop_process)
                stop_btn.place(relx=0.025, rely=0.87)

                for im in input_array:

                    im_label_array[i].configure(text="Processing")
                    im_label_array[i].place(relx=0.05, rely=0.1)

                    if i > 0:
                        im_label_array[i - 1].configure(text="Done")

                    if stopped:
                        im_label_array[i].configure(text="Stopped")
                        break

                    img = Image.open(im)
                    name = os.path.basename(im)
                    name = name.split('.')[0] + '.png'

                    if inputsize_checkbox.get():
                        img, transparent = main.process_v2(img, background, isSaveTransparent.get())
                    else:
                        img, transparent = main.process(img, background, (width_var, height_var),
                                                        isSaveTransparent.get())

                    img.save(os.path.join(output_loc, name))

                    if transparent is not None:
                        transparent_name = name.split('.')[0] + "_transparent" + ".png"
                        try:
                            path = os.path.join(output_loc, "Transparent Images")
                            os.mkdir(path)
                        except:
                            pass

                        transparent.save(os.path.join(path, transparent_name))

                    update_preview(img)

                    if i == len(input_array) - 1:
                        im_label_array[i].configure(text="Done")

                    i += 1

                text = "Processing done!"
                done_handler(text)
                stop_btn.destroy()

        except AttributeError:
            text = "No selected Background!"
            error_handler(text, True)
        except IOError:
            text = "Cannot Open Images! \nImages does not exist or deleted!"
            error_handler(text, True)
        except Exception as e:
            error_handler(e, True)

        column_size = 4

    def drop_inside_list_box(event):
        global isHomeBool
        #access essential variable
        global input_folder_path
        global input_array
        #assign it with data from event
        input_folder_path = event.data

        if input_folder_path:
            isNotBigger = False
            isCorrupted = False
            index = 0

            if os.path.isdir(input_folder_path):
                temp_var = os.listdir(input_folder_path)

            if input_folder_path.endswith(".png") or input_folder_path.endswith(".jpeg") or input_folder_path.endswith(".jpg"):
                temp_var = input_folder_path.split()

            for file in temp_var:
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    try:
                        temp = Image.open(os.path.join(input_folder_path, file))

                        if temp.width > 512 and temp.height > 512:
                            index += 1
                            input_array.append(os.path.join(input_folder_path, file))
                        else:
                            isNotBigger = True

                    except UnidentifiedImageError:
                        isCorrupted = True

            if isNotBigger and isCorrupted:
                text = "Some images are corrupted and smaller than 512x512!"
                error_handler(text, True)

            elif isNotBigger:
                text = "Images must be bigger than 512x512!"
                error_handler(text, False)

            elif isCorrupted:
                text = "Some images are corrupted!"
                error_handler(text, True)

            if index > 0:
                input_gallery_gui()
                isHomeBool = False
                checkI_home_handler()

    def get_input_handler():
        global isHomeBool
        #access essential variable
        global input_folder_path
        #assign it with data from event
        input_folder_path = filedialog.askdirectory(initialdir = "/Desktop" if input_folder_path is None else input_folder_path,title = "Select Input Path")

        if input_folder_path:
            isNotBigger = False
            isCorrupted = False
            index = 0
            for file in os.listdir(input_folder_path):
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    try:
                        temp = Image.open(os.path.join(input_folder_path, file))

                        if temp.width > 512 and temp.height > 512:
                            index += 1
                            input_array.append(os.path.join(input_folder_path, file))
                        else:
                            isNotBigger = True

                    except UnidentifiedImageError:
                        isCorrupted = True

            if isNotBigger and isCorrupted:
                text = "Some images are corrupted and smaller than 512x512!"
                error_handler(text, True)

            elif isNotBigger:
                text = "Images must be bigger than 512x512!"
                error_handler(text, False)

            elif isCorrupted:
                text = "Some images are corrupted!"
                error_handler(text, True)

            if index > 0:
                input_gallery_gui()
                isHomeBool = False
                checkI_home_handler()
            else:
                text = "No images found!"
                error_handler(text, False)

    def clear():
        global foreground_input_list_box
        global input_array
        global isHomeBool
        global column_size
        global preview
        global imm
        global im_label_array
        global del_btn_disabled
        global clicked
        global use_cam_btn_disabled

        input_array.clear()
        imm.clear()
        is_selected.clear()
        checkbox_array.clear()
        im_label_array.clear()
        use_cam_btn_disabled.destroy()
        preview.configure(image = None)

        for widgets in foreground_input_list_box.winfo_children():
            widgets.destroy()

        tk.Label(foreground_input_list_box, text="Drop image folder here", font=("Roboto", 20), fg="#D6D2D2",
                 bg="#2C2B2B").place(relx=0.25, rely=0.35)
        tk.Label(foreground_input_list_box, text="or", font=("Roboto", 20), fg="#D6D2D2", bg="#2C2B2B").place(relx=0.35,
                                                                                                              rely=0.41)
        tk.Button(foreground_input_list_box, text="Browse", height=1, width=20, font=("Roboto", 17), fg = "#e0efff", bg = "#127DF4", activebackground="#4a9eff", cursor="hand2", borderwidth=0, highlightthickness=0, command=get_input_handler).place(
            relx=0.255, rely=0.50)

        if clicked:
            del_btn_disabled.destroy()
            clicked = False

        isHomeBool = True
        checkI_home_handler()

    def select_img():
        global checkbox_array
        global is_selected
        global clicked
        global isHomeBool
        global del_btn_disabled
        global select_lbl

        if not clicked:
            i=0
            select_lbl.configure(text = "Deselect")
            del_btn.configure(state="normal", cursor = "hand2")

            for btn in del_btn.winfo_children():
                btn.destroy()

            for frame in view_frame.winfo_children():
                is_selected.append(tk.BooleanVar())
                checkbox = tk.Checkbutton(frame, variable=is_selected[i])
                checkbox_array.append(checkbox)
                x = (int(frame.winfo_width()) - 25) / int(frame.winfo_width())
                checkbox.place(relx=x,rely=0.1)

                i += 1
            clicked = True
        else:
            select_lbl.configure(text="Select")
            del_btn.configure(state= "disabled", cursor = "arrow")

            for checkbox in checkbox_array:
                checkbox.destroy()

            is_selected.clear()
            checkbox_array.clear()
            clicked = False

    def delete_selected():
        global clicked
        global is_selected
        global checkbox_array

        i = 0
        j = -1

        for selected in is_selected:
            if selected.get():
                j += 1
                del input_array[i - j]
            i += 1

        if len(input_array) == 0:
            clear()
        else:
            del_btn_disabled = tk.Label(del_btn, image=delete_image_disable, bg="#323232")
            del_btn_disabled.place(relx=0, rely=0)
            input_gallery_gui()
            is_selected.clear()
            checkbox_array.clear()

        clicked = False
        select_lbl.configure(text="Select")
        del_btn.configure(state="disabled", cursor="arrow")

    def click_image(id):
        global clicked

        if not clicked:
            select_img()

        if len(is_selected) > 0:
            if not is_selected[id].get():
                is_selected[id].set(1)
            else:
                is_selected[id].set(0)

    def show_input_thread():
        t3 = Thread(target = create_container)
        t3.daemon = True
        t3.start()

    def create_container():
        global view_frame
        global im_label_array
        global checkbox_array
        global container_array

        row_dimension = 0
        column_cimension = 0

        i = 0
        for file in input_array:
            # if file is an image then create an image widget
            image = Image.open(file)
            if column_size == 4:
                image.thumbnail((215, 215), resample=1)
            if column_size == 3:
                image.thumbnail((280, 280), resample=1)
            if column_size == 2:
                image.thumbnail((420, 420), resample=1)

            image = ImageTk.PhotoImage(image)
            images.append(image)

            view_frame.update()
            if view_frame is not None and view_frame.winfo_height() > 630:
                scrollbar = ttk.Scrollbar(display_frame, command=display_canvas.yview)
                scrollbar.place(relx=1, rely=0, relheight=0.89, anchor='ne')
                display_canvas.configure(yscrollcommand=scrollbar.set)

            if column_cimension < column_size:
                image_frame = tk.Frame(view_frame, height=image.height(), width=image.width(), bg="#2C2B2B", bd=0, relief="groove")
                image_frame.grid(row=row_dimension, column=column_cimension)
                # change the h and w of tk.Button when trying display the image
                container = tk.Button(image_frame, image=image, borderwidth= 0, highlightthickness=0, command=lambda id=i :click_image(id))
                container_array.append(container)
                container.place(relx=0.05, rely=0.1)
                im_label = tk.Label(image_frame)
                im_label_array.append(im_label)
                column_cimension += 1

            if column_cimension == column_size:
                row_dimension += 1
                column_cimension = 0
            i+=1

    def input_gallery_gui():
        global images
        global view_frame
        global foreground_input_list_box
        global input_array
        global view_frame
        global foreground_input_list_box
        global display_frame
        global display_canvas

        im_label_array.clear()

        def on_configure(event):
            display_canvas.configure(scrollregion=display_canvas.bbox('all'))

        def _on_mousewheel(event):
            display_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        ttkstyle = ttk.Style()
        ttkstyle.theme_use("classic")
        ttkstyle.configure("Vertical.TScrollbar", background="#363434",arrowsize = 1, borderwidth = 0, troughcolor = "#2b2a2a", relief = "groove")

        display_frame = tk.Frame(foreground_input_list_box, height=720, width=870, bg="#2C2B2B")
        display_frame.place(relx=0, rely=0)
        display_canvas = tk.Canvas(display_frame, bg="#2C2B2B", height=630, width=960, borderwidth=0, highlightthickness=0, )
        display_canvas.place(relx=0, rely=0)
        view_frame = tk.Frame(display_canvas, bg="#2C2B2B")
        view_frame.bind('<Configure>', on_configure)
        mainwindow.bind("<MouseWheel>", _on_mousewheel)
        display_canvas.create_window(0, 0, window=view_frame)

        show_input_thread()

    def checkI_home_handler():
        global isHomeBool
        global input_array
        global select_btn_disabled
        global del_btn_disabled
        global clean_btn_disabled
        global use_cam_btn_disabled
        global column_size
        global column_handler_btn_disabled
        global column_label

        if len(input_array) > 0:
            if isHomeBool == True:
                select_btn.configure(state = "disabled",cursor="arrow")
                del_btn.configure(state="disabled",cursor="arrow")
                clean_btn.configure(state = "disabled",cursor="arrow")
                use_cam_btn.configure(state="normal", cursor="hand2")
                column_handler_btn.configure(state = "disabled", cursor = "arrow")

                if column_label["text"] == "Large":
                    column_handler_btn_disabled = tk.Label(frame1, image= small_image_disabled, bg = "#323232")
                if column_label["text"] == "Medium":
                    column_handler_btn_disabled = tk.Label(frame1, image=medium_image_disabled, bg = "#323232")
                if column_label["text"] == "Small":
                    column_handler_btn_disabled = tk.Label(frame1, image=large_image_disabled, bg = "#323232")

                column_handler_btn_disabled.place(relx=0.235, rely=0.015)

                select_btn_disabled = tk.Label(frame1, image = select_image_disable, bg = "#323232")
                select_btn_disabled.place(relx=0.07,rely=0.015)

                del_btn_disabled = tk.Label(del_btn, image=delete_image_disable, bg = "#323232")
                del_btn_disabled.place(relx = 0, rely = 0)

                clean_btn_disabled = tk.Label(frame1, image=clear_image_disable, bg = "#323232")
                clean_btn_disabled.place(relx=0.18, rely=0.015)

                try:
                    use_cam_btn_disabled.destroy()
                except:
                    pass

            else:
                select_btn.configure(state = "normal", cursor = "hand2")
                clean_btn.configure(state = "normal", cursor = "hand2")
                use_cam_btn.configure(state="disabled",cursor="arrow")
                column_handler_btn.configure(state="normal", cursor="hand2")

                select_btn_disabled.destroy()
                clean_btn_disabled.destroy()
                column_handler_btn_disabled.destroy()

                try:
                    use_cam_btn_disabled.destroy()
                except:
                    pass

                use_cam_btn_disabled = tk.Label(frame1, image=camera_image_disable, bg="#323232")
                use_cam_btn_disabled.place(relx=0.655, rely=0.015)
        else:
            isHomeBool = True
            select_btn.configure(state="disabled",cursor="arrow")
            del_btn.configure(state="disabled",cursor="arrow")
            clean_btn.configure(state="disabled",cursor="arrow")
            use_cam_btn.configure(state="normal", cursor="hand2")
            column_handler_btn.configure(state="disabled", cursor="arrow")

            select_btn_disabled = tk.Label(frame1, image=select_image_disable, bg = "#323232")
            select_btn_disabled.place(relx=0.07, rely=0.015)

            del_btn_disabled = tk.Label(del_btn, image=delete_image_disable, bg="#323232")
            del_btn_disabled.place(relx=0, rely=0)

            clean_btn_disabled = tk.Label(frame1, image=clear_image_disable, bg="#323232")
            clean_btn_disabled.place(relx=0.18, rely=0.015)

            if column_label["text"] == "Large":
                column_handler_btn_disabled = tk.Label(frame1, image=small_image_disabled, bg="#323232")
            if column_label["text"] == "Medium":
                column_handler_btn_disabled = tk.Label(frame1, image=medium_image_disabled, bg="#323232")
            if column_label["text"] == "Small":
                column_handler_btn_disabled = tk.Label(frame1, image=large_image_disabled, bg="#323232")

            column_handler_btn_disabled.place(relx=0.235, rely=0.015)

            try:
                use_cam_btn_disabled.destroy()
            except:
                pass

    def add_image_handler():
        global input_array
        global isHomeBool
        temp_len = len(input_array)
        index = 0
        num = 0
        isNotBigger = False
        isCorrupted = False

        for image in filedialog.askopenfilenames(initialdir = "/Desktop" if input_folder_path is None else input_folder_path, title = "Add Image/s", filetypes = (("image files",".jpg"),("image files",".png"), ("image files",".jpeg"))):
            num += 1
            try:
                temp = Image.open(image)

                if temp.width > 512 and temp.height > 512:
                    index += 1
                    input_array.append(image)
                else:
                    isNotBigger = True

            except UnidentifiedImageError:
                isCorrupted = True

        if isNotBigger and isCorrupted:
            text = "Some images are corrupted and smaller than 512x512!"
            error_handler(text, True)

        elif isNotBigger:
            text = "Images must be bigger than 512x512!"
            error_handler(text, False)

        elif isCorrupted:
            text = "Some images are corrupted!"
            error_handler(text, True)

        if index > 0 and len(input_array) > temp_len:
            #input_array += added_images
            select_btn.configure(state="normal")
            clean_btn.configure(state="normal")
            input_gallery_gui()
            isHomeBool = False
            checkI_home_handler()

    def update_column_handler():
        global column_size
        global view_frame
        global display_frame
        global display_canvas

        if column_size == 4:
            column_size = 2
        else:
            column_size += 1

        if column_size == 4:
            column_handler_btn.configure(image = large_image)
            column_label.configure(text = "Small", bg = "#323232")
            column_label.place(relx=0.24)
        elif column_size == 3:
            column_handler_btn.configure(image = medium_image)
            column_label.configure(text="Medium", bg = "#323232")
            column_label.place(relx = 0.235)
        elif column_size == 2:
            column_handler_btn.configure(image = small_image)
            column_label.configure(text="Large", bg = "#323232")
            column_label.place(relx=0.24)

            try:
                if view_frame is not None and view_frame.winfo_height() > 630:
                    scrollbar = ttk.Scrollbar(display_frame, command=display_canvas.yview)
                    scrollbar.place(relx=1, rely=0, relheight=0.89, anchor='ne')
                    display_canvas.configure(yscrollcommand=scrollbar.set)
            except:
                pass

        for widget in foreground_input_list_box.winfo_children():
            widget.destroy()

        input_gallery_gui()

    def initialize_stream():
        global cmodnet

        try:
            pretrained_ckpt = "pretrained/modnet_webcam_portrait_matting.ckpt"
            cmodnet = cam_modnet.cam_modnet(pretrained_ckpt)
        except:
            text = "Pretrained Model not found!"
            error_handler(text, True)

    def capture():
        global frame_update
        global preview_frame
        global imm
        global isSaveTransparent
        global transparent
        global frame_np

        background = Image.open(background_path)

        if frame_update is not None:
            if inputsize_checkbox.get():
                height_var, width_var = frame_np.shape[0:2]

            img, transparent = main.process_capture(frame_np, background, (width_var, height_var),
                                            isSaveTransparent.get())

            name = time.strftime("%Y%m%d-%H%M%S") + '.png'
            img.save(os.path.join(output_loc, name))

            img.save(os.path.join(output_loc, name))

            if transparent is not None:
                transparent_name = name.split('.')[0] + "_transparent" + ".png"
                try:
                    path = os.path.join(output_loc, "Transparent Images")
                    os.mkdir(path)
                except:
                    pass

                transparent.save(os.path.join(path, transparent_name))

            img.thumbnail((400,400))
            imgtk = ImageTk.PhotoImage(image=img)
            imm.append(imgtk)
            preview.configure(height=330, width=315, image = imgtk)

    def press(event):
        try:
            int(event.char)
        except:
            capture()

    def create_grid(frame):
        width, height = frame.size
        x1 = int(width/3)
        y1 = int(height/3)

        frame = np.array(frame)

        frame = cv2.line(frame, (x1,0), (x1, height), (0,0,0), thickness=1)
        frame = cv2.line(frame, (x1*2, 0), (x1*2, height), (0, 0, 0), thickness=1)
        frame = cv2.line(frame, (0, y1), (width, y1), (0, 0, 0), thickness=1)
        frame = cv2.line(frame, (0, y1*2), (width, y1*2), (0, 0, 0), thickness=1)

        return Image.fromarray(frame)

    def set_grid():
        global isGrid

        if isGrid:
            isGrid = False
        else:
            isGrid = True

    def thread_process_stream():
        global frame_update
        global streaming
        global frame_np
        global preview_stream
        global load_lbl
        global camera
        global width_var
        global height_var
        global t1
        global transparent
        global stop_camera_btn
        global grid_btn
        global isGrid

        current_background = background_path
        bg = Image.open(background_path)

        stop_camera_btn = tk.Button(use_camera_frame, height=2, width=9, text="Stop", font=("Roboto", 12), fg="#e0efff",
                                    bg="#ba6032",
                                    activebackground="#ba6032", borderwidth=0, highlightthickness=0, cursor="hand2",
                                    command=stop_camera_handler)

        grid_btn = tk.Button(use_camera_frame, height=2, width=9, text="Grid", font=("Roboto", 12), fg="#e0efff",
                                    bg="#4369D9",
                                    borderwidth=0, highlightthickness=0, cursor="hand2",
                                    command=set_grid)

        while True:
            try:
                if frame_np is not None and streaming:
                    if current_background != background_path:
                        bg = Image.open(background_path)
                        current_background = background_path

                    frame_update, transparent = cmodnet.update(frame_np, bg, inputsize_checkbox.get(), (width_var, height_var), isSaveTransparent.get())

                    load_lbl.destroy()
                    img = Image.fromarray(frame_update)
                    img.thumbnail((900,600))

                    if isGrid:
                        img = create_grid(img)

                    imgtk = ImageTk.PhotoImage(image=img)
                    preview_stream.config(image=imgtk)
                    preview_stream.image = imgtk

                    # center preview
                    x = ((930 - img.width) / 2) / 930
                    y = ((600 - img.height) / 2) / 600

                    preview_stream.place(relx=x, rely=y)
                    stop_camera_btn.place(relx=0.78, rely=0.05)
                    grid_btn.place(relx=0.66, rely = 0.05)


            except Exception as e:
                streaming = False
                break

    def stream():
        global streaming
        global streamer
        global frame_np
        global fg_np
        global load_lbl
        global cap

        t2 = Thread(target = thread_process_stream)
        t2.daemon = True
        load_lbl.configure(text = "Connecting to camera")

        cap = cv2.VideoCapture(camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while True:
            if not streaming:
                break

            _, frame = cap.read()

            if frame is not None and streaming:
                frame_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if not t2.is_alive():
                    try:
                        t2.start()
                    except RuntimeError:
                        pass

    def stop_camera_handler():
        global isClick_camera
        global streaming
        global cap
        global preview_stream
        global start_cam_btn
        global stop_camera_btn
        global grid_btn

        streaming = False

        preview_stream.destroy()
        stop_camera_btn.destroy()
        grid_btn.destroy()

        start_cam_btn = tk.Button(frame_preview, height=3, width=25, text="Start Camera Capture", font=("Roboto", 14),
                                  fg="#ffffff", bg="#4369D9", activebackground="#314d9e", borderwidth=0,
                                  highlightthickness=0, cursor="hand2", command=start_stream)
        start_cam_btn.place(relx=0.35, rely=0.40)

        try:
            cap.release()
            cv2.destroyAllWindows()
        except:
            streaming = False

    def start_stream():
        global camera_chosen
        global camera
        global cmodnet
        global start_cam_btn
        global frame_preview
        global load_lbl
        global streaming
        global t1
        global preview_stream
        global use_camera_frame

        preview_stream = tk.Label(frame_preview, bg="#2C2B2B")

        try:
            streaming = True

            start_cam_btn.destroy()
            load_lbl = tk.Label(frame_preview, text="Setting up camera", font=("Roboto", 20), fg="#D6D2D2",
                                bg="#2C2B2B")
            load_lbl.place(relx=0.35, rely=0.40)

            # setup camera
            camera = cam_lists.index(camera_chosen.get())

            t1 = Thread(target=stream)
            t1.daemon = True
            time.sleep(2)
            t1.start()

            mainwindow.bind('<KeyPress>', press)

        except AttributeError:
            text = "Cannot open background!"
            error_handler(text, True)

    def use_camera_handler():
        global isClick_camera
        global camera_chosen
        global cam_lists
        global init_thread
        global start_cam_btn
        global frame_preview
        global use_camera_frame
        global streaming

        if not isClick_camera:
            init_thread = Thread(target=initialize_stream)
            init_thread.daemon = True
            init_thread.start()

            camera_chosen = tk.StringVar()

            streaming = False

            # get camera lists
            graph = FilterGraph()
            cam_lists = graph.get_input_devices()

            use_camera_frame = tk.Frame(mainwindow, height= 720, width=850, bg = "#323232")
            use_camera_frame.place(relx = 0, rely = 0)

            frame_preview = tk.Frame(use_camera_frame, width = 930, height = 609,bg = "#2C2B2B")
            frame_preview.place(relx= 0.005, rely=0.141)

            camera_chosen.set(cam_lists[0])
            tk.Label(use_camera_frame, font = ("Roboto", 12), text = "Choose Camera Device: ", fg = "#D6D2D2", bg = "#323232").place(relx = 0.01, rely = 0.03)
            dropdown = ttk.OptionMenu(use_camera_frame, camera_chosen, cam_lists[0], *cam_lists)
            dropdown.place(relx = 0.02, rely = 0.08)

            start_cam_btn = tk.Button(frame_preview, height = 3, width = 25, text = "Start Camera Capture", font = ("Roboto", 14), fg = "#ffffff", bg = "#4369D9",activebackground="#314d9e", borderwidth= 0, highlightthickness= 0,cursor = "hand2", command = start_stream)
            start_cam_btn.place(relx=0.35,rely=0.40 )

            capturebtn = tk.Button(menu_frame, height=3, width=25, text="CAPTURE", font=("Roboto", 16), fg="#e0efff", bg="#4369D9",
                      activebackground="#4a9eff", cursor="hand2", borderwidth=0, highlightthickness=0,
                      command=capture)
            capturebtn.place(relx=0.025, rely=0.87)

            tk.Button(use_camera_frame,height = 2, width = 9, text = "Exit", font = ("Roboto", 12), fg = "#e0efff", bg = "#8f2615", activebackground="#ba6032", borderwidth= 0, highlightthickness= 0,cursor = "hand2",command = lambda: exit_handler()).place(relx=0.9,rely=0.05)
            isClick_camera = True

            def exit_handler():
                global isClick_camera
                global streaming
                global cap

                if streaming:
                    text = "Stop the camera first to exit!"
                    error_handler(text, True)
                else:
                    use_camera_frame.destroy()
                    isClick_camera = False
                    capturebtn.destroy()
                    try:
                        cap.release()
                        cv2.destroyAllWindows()
                    except:
                        streaming = False
                isClick_camera = False

    # start of main gui creationg with TkinterDnD wrapper
    mainwindow = TkinterDnD.Tk()

    # initialize ipbr
    def initialize_ipbr():
        global main
        global isModelPresent
        try:
            main = ipbr.main()
            isModelPresent = True
        except FileNotFoundError:
            text = "Pretrained Model not found!"
            error_handler(text, True)
            isModelPresent = False

    init_ipbr = Thread(target=initialize_ipbr)
    init_ipbr.start()

    # load config
    conf = config.conf()
    output_loc, background_path, save_transparent, ifcheck_var, width_var, height_var, backgrounds_array = conf.get_conf()

    # global variables
    height_entry_var = tk.StringVar()
    width_entry_var = tk.StringVar()
    temp = tk.BooleanVar()
    inputsize_checkbox = tk.BooleanVar()
    isSaveTransparent = tk.BooleanVar()
    temp_output_loc = output_loc
    yindex = 0.1
    im_index = 0
    view_frame = None
    input_folder_path = ""
    input_array = []
    im_label_array = []
    container_array = []
    checkbox_array = []
    is_selected = []
    id_array = []
    imm = []
    images = []
    col_d = 0
    row_d = 0
    isHomeBool = True
    column_size = 4
    clicked = False
    isClick_camera = False
    stopped = False
    isGrid = False
    mainwindow_width = 1200
    mainwindow_height = 720

    # convert str to int
    width_var = int(width_var)
    height_var = int(height_var)

    # set checkboxes for settings
    if ifcheck_var == '1':
        inputsize_checkbox.set(False)
    else:
        inputsize_checkbox.set(True)

    if save_transparent == '1':
        isSaveTransparent.set(True)
    else:
        isSaveTransparent.set(False)

    # set default background preview
    if  len(backgrounds_array) > 0:
        if background_path:
            background_image = Image.open(background_path)
            background_image.thumbnail((250, 250))
            background_image = ImageTk.PhotoImage(background_image)
        else:
            background_image = None
    else:
        background_image = None

    #create and assign icons image
    add_image_icon = Image.open("resources/images/add_image.png")
    add_image_icon.thumbnail((50,50))
    add_image_icon = ImageTk.PhotoImage(add_image_icon)

    select_image = Image.open("resources/images/select_image.png")
    select_image.thumbnail((50,50))
    select_image = ImageTk.PhotoImage(select_image)

    select_image_disable = Image.open("resources/images/Select Image-disabled.png")
    select_image_disable.thumbnail((50,50))
    select_image_disable = ImageTk.PhotoImage(select_image_disable)

    delete_image = Image.open("resources/images/delete_image.png")
    delete_image.thumbnail((50,50))
    delete_image = ImageTk.PhotoImage(delete_image)

    delete_image_disable = Image.open("resources/images/Delete Image-disabled.png")
    delete_image_disable.thumbnail((50,50))
    delete_image_disable = ImageTk.PhotoImage(delete_image_disable)

    clear_image = Image.open("resources/images/Clear.png")
    clear_image.thumbnail((50,50))
    clear_image = ImageTk.PhotoImage(clear_image)

    clear_image_disable = Image.open("resources/images/Clear-disabled.png")
    clear_image_disable.thumbnail((50,50))
    clear_image_disable = ImageTk.PhotoImage(clear_image_disable)

    camera_image = Image.open("resources/images/Camera.png")
    camera_image.thumbnail((50,50))
    camera_image = ImageTk.PhotoImage(camera_image)

    camera_image_disable = Image.open("resources/images/Camera-disabled.png")
    camera_image_disable.thumbnail((50,50))
    camera_image_disable = ImageTk.PhotoImage(camera_image_disable)

    trash_image = Image.open("resources/images/trash.png")
    trash_image.thumbnail((20,20))
    trash_image = ImageTk.PhotoImage(trash_image)

    small_image = Image.open("resources/images/2.png")
    small_image.thumbnail((50, 50))
    small_image = ImageTk.PhotoImage(small_image)

    small_image_disabled = Image.open("resources/images/2_disabled.png")
    small_image_disabled.thumbnail((50,50))
    small_image_disabled = ImageTk.PhotoImage(small_image_disabled)

    medium_image = Image.open("resources/images/3.png")
    medium_image.thumbnail((50, 50))
    medium_image = ImageTk.PhotoImage(medium_image)

    medium_image_disabled = Image.open("resources/images/3-disabled.png")
    medium_image_disabled.thumbnail((50,50))
    medium_image_disabled = ImageTk.PhotoImage(medium_image_disabled)

    large_image = Image.open("resources/images/4.png")
    large_image.thumbnail((50, 50))
    large_image = ImageTk.PhotoImage(large_image)

    large_image_disabled = Image.open("resources/images/4-disabled.png")
    large_image_disabled.thumbnail((50,50))
    large_image_disabled = ImageTk.PhotoImage(large_image_disabled)

    add_background_icon = tk.PhotoImage(file = "resources/images/add_background_icon.png")
    icon2 = ("resources/images/logo.ico")


    # set mainwindow to pop in center
    screen_width = mainwindow.winfo_screenwidth()
    screen_height = mainwindow.winfo_screenheight()
    #configure mainwindow / root
    mainwindow.iconbitmap(icon2)
    mainwindow.geometry(f"{mainwindow_width}x{mainwindow_height}+{int((screen_width / 2) - (mainwindow_width / 2))}+{int((screen_height / 2) - (mainwindow_height / 2))}")
    mainwindow.title("Intelligent Portrait Background Replacement")
    mainwindow.configure(bg = "#323232")
    mainwindow.resizable(False, False)

    #create main window widgets
    frame1 = tk.Frame(mainwindow, height= 55, width = 900, bg = "#323232").place(x=0,y=0)
    add_btn = tk.Button(frame1, image = add_image_icon,bg = "#323232", height = 50, width = 50,  bd = 2, command = add_image_handler, cursor = "hand2", borderwidth= 0 , highlightthickness= 0)
    add_btn.place(relx = 0.015, rely = 0.015)
    tk.Label(frame1, text = "Add", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232").place(relx = 0.02, rely = 0.1)
    select_btn = tk.Button(frame1, image = select_image, command = lambda : [del_btn.configure(state="normal"), select_img()], bg = "#323232", height = 50, width = 50, borderwidth= 0 , highlightthickness= 0)
    select_btn.place(relx=0.07,rely=0.015)
    select_lbl = tk.Label(frame1, text="Select", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232")
    select_lbl.place(relx = 0.0725, rely = 0.1)
    del_btn = tk.Button(frame1, image = delete_image, command = delete_selected, bg = "#323232", height = 50, width = 50,borderwidth= 0 , highlightthickness= 0)
    del_btn.place(relx = 0.125, rely = 0.015)
    tk.Label(frame1, text="Delete", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232").place(relx = 0.1275, rely = 0.1)
    clean_btn = tk.Button(frame1, image = clear_image, bg = "#323232", height = 50, width = 50,command = clear, borderwidth= 0 , highlightthickness= 0)
    clean_btn.place(relx = 0.18, rely = 0.015)
    tk.Label(frame1, text="Clear", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232").place(relx = 0.1865, rely = 0.1)
    column_handler_btn = tk.Button(frame1, image = large_image, bg = "#323232", height = 50, width = 50, command = update_column_handler, borderwidth= 0 , highlightthickness= 0)
    column_handler_btn.place(relx=0.235,rely=0.015)
    column_label = tk.Label(frame1, text = "Small", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232")
    column_label.place(relx = 0.24, rely = 0.1)
    use_cam_btn = tk.Button(frame1, image = camera_image, command =use_camera_handler,bg = "#323232", height = 50, width = 50,borderwidth= 0 , highlightthickness= 0)
    use_cam_btn.place(relx=0.655,rely=0.015)
    tk.Label(frame1, text="Use Camera", font = ("Roboto", 10), fg = "#D6D2D2", bg = "#323232").place(relx = 0.6425, rely = 0.1)

    foreground_input_list_box = tk.Listbox(mainwindow, selectmode= tk.SINGLE, width = 200, height = 38, bg = "#2C2B2B", bd = 1, relief = "groove", borderwidth= 0, highlightthickness=0 )
    foreground_input_list_box.drop_target_register(DND_FILES)
    foreground_input_list_box.dnd_bind("<<Drop>>", drop_inside_list_box)
    foreground_input_list_box.place(relx= 0.005, rely=0.141)
    tk.Label(foreground_input_list_box, text= "Drop image folder here", font = ("Roboto", 20), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.25, rely = 0.35)
    tk.Label(foreground_input_list_box, text= "or", font = ("Roboto", 20), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.35, rely = 0.41)
    tk.Button(foreground_input_list_box, text = "Browse", height = 1, width=20, font = ("Roboto", 17),  fg = "#e0efff", bg = "#4369D9", activebackground="#4a9eff", cursor = "hand2", borderwidth= 0, highlightthickness= 0,command= get_input_handler).place(relx= 0.255, rely = 0.50)

    #create menu frame widget
    menu_frame = tk.Frame(mainwindow, height= 720, width=350, relief="groove", bg = "#323232")
    menu_frame.place(relx= 0.73, rely= 0)
    #tk.Label(menu_frame, text = "Chosen Background Image Preview: ", font = ("Roboto", 12), fg = "#D6D2D2", bg = "#2C2B2B").place(relx= 0.05, rely = 0.02)
    background_preview = tk.Label(menu_frame, bg = "#2C2B2B", bd =2, relief = "groove", borderwidth= 0, highlightthickness=0)
    background_preview.place(relx = 0.02, rely = 0.02)
    background_preview.configure(height=160, width=310, image=background_image)
    preview_frame = tk.Frame(menu_frame, height= 500, width= 310, bg = "#323232")
    preview_frame.place(relx=0.02, rely=0.385)
    preview = tk.Label(preview_frame, height= 22, width= 315, bg = "#2C2B2B" )
    preview.place(relx = 0, rely =0)
    tk.Button(menu_frame, height = 1, width = 25, text = "Change Background", font = ("Roboto", 16), fg = "#e0efff", bg = "#303E8C", activebackground="#4a9eff", cursor ="hand2",borderwidth= 0, highlightthickness= 0, command=background_panel_gui).place(relx= 0.025, rely= 0.26)
    tk.Button(menu_frame, height = 1, width = 25, text = "Settings", font = ("Roboto", 16), fg = "#e0efff", bg = "#303E8C", activebackground="#4a9eff", cursor ="hand2",borderwidth= 0, highlightthickness= 0,command = open_settings).place(relx= 0.025, rely= 0.32)
    start_btn = tk.Button(menu_frame, height = 3, width = 25, text = "START", font = ("Roboto", 16), fg = "#e0efff", bg = "#4369D9", activebackground="#4a9eff", cursor ="hand2",borderwidth= 0, highlightthickness= 0, command = start_thread)
    start_btn.place(relx=0.025, rely=0.87)
    checkI_home_handler()

    #make main window display in loop
    mainwindow.mainloop()
