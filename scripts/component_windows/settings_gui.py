import tkinter as tk
from tkinter import filedialog

#define global variables here
#temporary holder variables
outputpath_temp = ""

#official variables
location_path = ""
enhancement_option = ""
image_height = 0
image_width = 0
class Settings_GUI:
    #define function for settigns gui
    def settings_gui():
        settings_window = tk.Toplevel()
        settings_window.title("Settings")
        settings_window.geometry("600x600")
        settings_window.resizable(False, False)

        #temporarily stores settings and only passed to global variables if "Save" button is clicked
        location_path_temp = ""
        enhancement_option_temp = tk.StringVar()
        #define local functions heres
        def close_window():
            # these prints for the debugging purposes
            # print(f"Temporary Enchancement Option: {enhancement_option_temp.get()}")
            # print(f" Enchancement Option: {enhancement_option}")
            # print(f"Location Path Temp {outputpath_temp}")
            # print(f"Location Path {location_path}")
            settings_window.destroy()

        def printshit():
            print(f"Temporary Enchancement Option: {enhancement_option_temp.get()}")

        def save_settings_handler():
            #global variables
            global location_path
            global enhancement_option
            global outputpath_temp
            global image_height
            global image_width

            #local variables
            error_in_height = False
            error_in_width = False
            
            try:
                image_height = int(height_input.get())
                error_in_height = False
                height_error.configure(text = "")
            except  ValueError:
                error_in_height = True
            
            try: 
                image_width = int(width_input.get())
                error_in_width = False
                width_error.configure(text = "")
            except ValueError:
                error_in_width = True

            if(error_in_height == True):
                height_error.configure(text = "Invalid Value (Numst be a number integer)", fg = "red")
                
            elif(error_in_width == True):
                width_error.configure(text = "Invalid Value (Numst be a number integer)", fg = "red")

            else:
                location_path = outputpath_temp
                enhancement_option = enhancement_option_temp.get()
                # these prints for the debugging purposes
                # print(f"Temporary Enchancement Option: {enhancement_option_temp.get()}")
                # print(f" Enchancement Option: {enhancement_option}")
                # print(f"Location Path {location_path}")
                # print(f"Location Path Temp {outputpath_temp}")
                print(f"Temp height: {image_height} ; Temp width: {image_width}")
                #if no errors then no error message
                height_error.configure(text = "")
                width_error.configure(text = "")
                settings_window.destroy()
            

        
        def getoutputpath_handler():
            global outputpath_temp
            outputpath_temp = filedialog.askdirectory(initialdir= "/Desktop", title = "Select Output Folder Location")
            # print(outputpath_temp)
            

        #initialize widgets
        outputloc_label = tk.Label(settings_window, text = "OUTPUT LOCATION", font = ("Tahoma", 13), bg = "#F3F3F3")
        outputpath_text = tk.Label(settings_window,  font = ("Tahoma", 13), width = 35, text = location_path, bd = 3, relief= "groove", fg = "black")
        outputloc_button = tk.Button(settings_window, text = "X", height = 1, width = 3, fg = "black", font = ("Tahoma", 13), bg = "#F3F3F3", command= getoutputpath_handler)
        auto_enhance_label = tk.Label(settings_window, text = "AUTO ENHANCEMENT", fg = "black", font = ("Tahoma", 13), bg = "#F3F3F3")
        enable_radio = tk.Radiobutton(settings_window, text = 'Enable', variable = enhancement_option_temp, value = "enable", command = printshit)
        disable_radio = tk.Radiobutton(settings_window, text = "Disable", variable = enhancement_option_temp, value = "disable", command = printshit)
        resolution_label = tk.Label(settings_window, text = "Resolution", fg = "black", font = ("Tahoma", 13), bg = "#F3F3F3")
        height_label = tk.Label(settings_window, text = "Height:", fg = "black", font = ("Tahoma", 12), bg = "#F3F3F3")
        height_input = tk.Entry(settings_window, bd = 3, relief= "groove", width = 10, font = ("Tahoma", 13))
        pixels_label1 = tk.Label(settings_window, text = "Pixels", fg = "black", font = ("Tahoma", 12), bg = "#F3F3F3")
        height_error = tk.Label(settings_window, text = "", font = ("Tahoma", 12))
        width_label = tk.Label(settings_window, text = "Width:", fg = "black", font = ("Tahoma", 12), bg = "#F3F3F3")
        width_input = tk.Entry(settings_window, bd = 3, relief = "groove", width = 10, font = ("Tahoma", 13))
        pixels_label2 = tk.Label(settings_window, text = "Pixels", fg = "black", font = ("Tahoma", 12))
        width_error = tk.Label(settings_window, text = "", font = ("Tahoma", 12))
        save_button = tk.Button(settings_window, height = 1, width = 13, text = "Save", fg = "white", font = ("Tahoma", 15), bg = "#DF5F02", command = save_settings_handler)
        cancel_button = tk.Button(settings_window, height = 1, width = 13, text = "Cancel", fg = "black", font = ("Tahoma", 15), bg = "#F3F3F3", command = close_window)
        #create / position widgets
        outputloc_label.place(relx= 0.05, rely= 0.11)
        outputpath_text.place(relx = 0.35, rely = 0.1, height = 37)
        outputloc_button.place(relx= 0.85, rely= 0.1)
        auto_enhance_label.place(relx= 0.05, rely= 0.2)
        enable_radio.place(relx= 0.1, rely= 0.25)
        disable_radio.place(relx= 0.1, rely= 0.32)
        resolution_label.place(relx= 0.05, rely= 0.45)
        height_label.place(relx= 0.075, rely= 0.5175)
        height_input.place(relx= 0.175, rely= 0.5175, height = 30)
        pixels_label1.place(relx= 0.3, rely= 0.52)
        height_error.place(relx= 0.4, rely = 0.52)
        width_label.place(relx= 0.075, rely= 0.6)
        width_input.place(relx= 0.175, rely= 0.6, height = 30)
        pixels_label2.place(relx= 0.3, rely= 0.6)
        width_error.place(relx= 0.4, rely = 0.6)
        save_button.place(relx= 0.4, rely= 0.8)
        cancel_button.place(relx= 0.7, rely= 0.8)

