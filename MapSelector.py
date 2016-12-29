# from tkinter import Tk, StringVar, IntVar, Checkbutton, Button, filedialog, Label
import tkinter as tk
from tkinter import filedialog, DISABLED, NORMAL
import os
import shutil

class MainWindow:
    country_list = [["Albania", 0],
                    ["Andorra", 0],
                    ["Austria", 0],
                    ["Belarus", 0],
                    ["Belgium", 0],
                    ["Bosnia_Herzegovina", 0],
                    ["Bulgaria", 0],
                    ["Croatia", 0],
                    ["Czech_Republic", 0],
                    ["Denmark", 0],
                    ["Estonia", 0],
                    ["Finland", 0],
                    ["Former_Yugoslav", 0],
                    ["France", 0],
                    ["Germany", 0],
                    ["Georgia", 0],
                    ["Gibraltar", 0],
                    ["Greece", 0],
                    ["Hungary", 0],
                    ["Iceland", 0],
                    ["Ireland", 0],
                    ["Italy", 0],
                    ["Kazakhstan", 0],
                    ["Kosovo", 0],
                    ["Latvia", 0],
                    ["Liechtenstein", 0],
                    ["Lithuania", 0],
                    ["Luxembourg", 0],
                    ["Malta", 0],
                    ["Moldova", 0],
                    ["Monaco", 0],
                    ["Montenegro", 0],
                    ["Netherlands", 0],
                    ["Norway", 0],
                    ["Poland", 0],
                    ["Portugal", 0],
                    ["Romania", 0],
                    ["Russia", 0],
                    ["San_Marino", 0],
                    ["Serbia", 0],
                    ["Slovakia", 0],
                    ["Slovenia", 0],
                    ["Spain", 0],
                    ["Sweden", 0],
                    ["Switzerland", 0],
                    ["Turkey", 0],
                    ["Ukraine", 0],
                    ["United_Kingdom", 0],
                    ["Vatican_City", 0]]
    MAX_LINES = 20
    START_ROW = 5

    def __init__(self, master):
        self.master = master
        master.title("Map Selector 0.1")

        self.close_button = tk.Button(master, text="Quit", command=master.quit)
        self.close_button.grid(row=0, column=2, pady=10)

        self.selectAllButton = tk.Button(master, text="Select All/None", command=self.select_all_checkbuttons)
        self.selectAllButton.grid(row=15, column=2)
        self.select_all_cb_status = True

        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.grid(row=0)

        self.map_folder_path_var = tk.StringVar()
        self.map_folder_path_var.set("Select map root folder")
        self.map_folder_path = ""
        self.country_filesize_sum = 0

        self.copy_maps_button = tk.Button(master, text="Copy maps", command=self.copy_maps)
        self.copy_maps_button.grid(row=20, column=2)
        
        self.copy_maps_label_var = tk.StringVar()
        self.copy_maps_label_var.set("")
        self.copy_maps_label = tk.Label(master, textvariable=self.copy_maps_label_var)
        self.copy_maps_label.grid(row=21, column=2)

        self.map_folder_label = tk.Label(master, textvariable=self.map_folder_path_var)
        self.map_folder_label.grid(row=2, columnspan=3, pady=10)
        
        self.map_size_label_var = tk.StringVar()
        self.map_size_label_var.set("Total map size:  0 MB")
        self.map_size_label = tk.Label(master, textvariable=self.map_size_label_var)
        self.map_size_label.grid(row=17, column=2)

        self.cbTexts = {}
        self.cbVars = {}
        self.cb = {}
        grid_row = self.START_ROW
        for indx, country in enumerate(self.country_list):
            self.cbVars[indx] = tk.IntVar()
            self.cbVars[indx].trace("w", lambda a, b, c, d=indx, e=country[0]: self.get_country_filesize(d, e))
            self.cb[indx] = tk.Checkbutton(master, text=country[0], variable=self.cbVars[indx],
                                           onvalue=1, offvalue=0, height=1, width=20, anchor="w", state=DISABLED)
            self.cb[indx].grid(row=grid_row, column=int(indx/self.MAX_LINES))
            grid_row += 1
            if grid_row >= self.MAX_LINES + self.START_ROW:
                grid_row = self.START_ROW

    def select_folder(self):
        self.map_folder_path = tk.filedialog.askdirectory(initialdir='.')
        self.map_folder_path_var.set(self.map_folder_path)
        self.enable_checkbutton()

        # Get filesizes for all countries
        for index, country in enumerate(self.country_list):
            self.country_filesize_sum = 0
            for rootd, dirs, files in os.walk(self.map_folder_path):
                for file in files:
                    if file.lower().find(country[0].lower()) > -1:
                        country_filesize = os.path.getsize(os.path.join(rootd, file))
                        self.country_filesize_sum += country_filesize
            country[1] = self.country_filesize_sum

    def get_country_filesize(self, index, country_name):
        size_sum = 0
        for index, country in enumerate(self.country_list):
            size_sum += country[1]*self.cbVars[index].get()
        size_sum_string = "Total map size:  " + "{:.1f}".format(size_sum/1024/1024) + " MB"
        self.map_size_label_var.set(size_sum_string )

    def enable_checkbutton(self):
        for index in range(len(self.country_list)):
            self.cb[index].configure(state=NORMAL)

    def select_all_checkbuttons(self):
        for i in self.cbVars:
            if (self.select_all_cb_status):
                self.cbVars[i].set(1)
            else:
                self.cbVars[i].set(0)
        self.select_all_cb_status = not self.select_all_cb_status

    def copy_maps(self):
        self.copy_maps_label_var.set("Maps copied.")
        dir_up = os.path.dirname(self.map_folder_path)
        new_dir = os.path.join(dir_up, "MyMaps")
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)
        print(new_dir)
        print(os.path.join(self.map_folder_path, "license"))
        license_dir_src = os.path.join(self.map_folder_path, "license")
        license_dir_dst = os.path.join(new_dir, "license")
        if not os.path.isdir(license_dir_dst):
            shutil.copytree(license_dir_src, license_dir_dst)


root = tk.Tk()
main_window = MainWindow(root)
root.mainloop()