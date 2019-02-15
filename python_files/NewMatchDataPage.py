import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from tkinter.filedialog import askopenfilename
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
from python_files import Constants as C
from python_files import NewAtackPage
from python_files import NewPassPage

AUTOSAVE_AFTER = 10
autosave_counter = 0


class NewMatchDataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = ""
        self.file_exists = False
        self.attacks = []
        self.passes = []
        self.output_object = {"attacks": self.attacks, "passes": self.passes}
        self.img = mpimg.imread("../data/volleyball_court.png")

        title = tk.Label(self, text="New Data", font=("Helvetica", 20))
        self.team_name_label = tk.Label(self, text="Team name")
        self.opponent_name_label = tk.Label(self, text="Opponent name")

        self.team_name_entry = tk.Entry(self, textvariable=tk.StringVar())
        self.team_name_entry.focus_set()
        self.opponent_name_entry = tk.Entry(self, textvariable=tk.StringVar())

        self.create_file_button = tk.Button(self, text="Create new match",
                                            command=lambda: self.second_screen())
        self.opponent_name_entry.bind('<Return>', self.second_screen)

        self.get_existing_file_button = tk.Button(self, text="Add to existing match",
                                                  command=lambda: self.get_existing_file())

        self.back_button = tk.Button(self, text="Back", command=lambda: self.destroy())

        title.grid(row=0, column=1, pady=2*C.NORMAL_PADDING)
        self.team_name_label.grid(row=1, column=0, pady=C.NORMAL_PADDING)
        self.team_name_entry.grid(row=1, column=1, columnspan=2, pady=C.NORMAL_PADDING)
        self.opponent_name_label.grid(row=2, column=0, pady=C.NORMAL_PADDING)
        self.opponent_name_entry.grid(row=2, column=1, columnspan=2, pady=C.NORMAL_PADDING)
        self.back_button.grid(row=3, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.get_existing_file_button.grid(row=3, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.create_file_button.grid(row=3, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def get_existing_file(self, event=None):
        filename = askopenfilename()
        if filename == '':
            return
        self.file_exists = True
        self.filename = filename.split("/")[-1]
        with open(filename, "r") as file:
            self.output_object = json.load(file)
        self.attacks = self.output_object["attacks"] if "attacks" in self.output_object.keys() else []
        self.passes = self.output_object["passes"] if "passes" in self.output_object.keys() else []
        self.output_object["attacks"] = self.attacks
        self.output_object["passes"] = self.passes
        self.second_screen()

    def second_screen(self, event=None):
        if not self.file_exists:
            tn = self.team_name_entry.get()
            on = self.opponent_name_entry.get()
            date = datetime.datetime.today().strftime('%d-%m-%Y')
            self.filename = date + "-" + on + "-" + tn + ".json"
        self.cleanup_first_screen()
        self.setup_second_screen()

    def cleanup_first_screen(self):
        self.team_name_label.destroy()
        self.team_name_entry.destroy()
        self.opponent_name_label.destroy()
        self.opponent_name_entry.destroy()
        self.create_file_button.destroy()
        self.get_existing_file_button.destroy()
        self.back_button.destroy()

    def setup_second_screen(self):
        self.focus_set()
        new_attack_button = tk.Button(self, text="Add new attack",
                                      command=lambda: self.add_new_attack())
        self.bind('<a>', lambda x: self.add_new_attack())

        new_pass_button = tk.Button(self, text="Add new pass",
                                      command=lambda: self.add_new_pass())
        self.bind('<p>', lambda x: self.add_new_pass())

        self.flip_field = tk.IntVar()
        fo_checkbox = tk.Checkbutton(self, text="Flip field orientation", variable=self.flip_field)

        save_and_quit_button = tk.Button(self, text="Save and go back",
                                         command=lambda: self.save_and_destroy())
        self.bind('<s>', lambda x: self.save_and_destroy())

        new_attack_button.grid(row=1, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        new_pass_button.grid(row=2, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        save_and_quit_button.grid(row=3, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        fo_checkbox.grid(row=3, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def add_new_attack(self):
        global autosave_counter
        plt.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])
        points = plt.ginput(2, show_clicks=True)
        attack_popup = NewAtackPage.NewAttackPopup(self)
        self.master.wait_window(attack_popup.top)

        new_attack = [self.orientation()*points[0][0], self.orientation()*points[0][1],
                      self.orientation()*points[1][0], self.orientation()*points[1][1],
                      int(attack_popup.shirt_number), attack_popup.hit.get(), len(self.attacks)]
        self.attacks.append(new_attack)
        plt.close()
        autosave_counter += 1
        if autosave_counter == 10:
            autosave_counter = 0
            with open("../data/{}".format(self.filename), "w") as file:
                json.dump(self.output_object, file)

    def add_new_pass(self):
        global autosave_counter
        plt.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])
        points = plt.ginput(2, show_clicks=True)
        pass_popup = NewPassPage.NewPassPopup(self)
        self.master.wait_window(pass_popup.top)

        new_pass = [self.orientation()*points[0][0], self.orientation()*points[0][1],
                      self.orientation()*points[1][0], self.orientation()*points[1][1],
                      int(pass_popup.shirt_number), pass_popup.received.get(), pass_popup.upper.get(), len(self.passes)]
        self.passes.append(new_pass)
        plt.close()
        autosave_counter += 1
        if autosave_counter == 10:
            autosave_counter = 0
            with open("../data/{}".format(self.filename), "w") as file:
                json.dump(self.output_object, file)

    def save_and_destroy(self):
        with open("../data/{}".format(self.filename), "w") as file:
            json.dump(self.output_object, file)
        self.destroy()

    def orientation(self):
        if self.flip_field.get() == 1:
            return -1
        else:
            return 1
