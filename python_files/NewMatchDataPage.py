import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from tkinter.filedialog import askopenfilename
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json


class NewMatchDataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = ""
        self.file_exists = False
        self.attacks = []
        self.output_object = {"attacks": self.attacks}
        self.img = mpimg.imread("../data/volleyball_court.png")

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

        self.team_name_label.pack()
        self.team_name_entry.pack()
        self.opponent_name_label.pack()
        self.opponent_name_entry.pack()
        self.create_file_button.pack()
        self.get_existing_file_button.pack()

    def get_existing_file(self, event=None):
        filename = askopenfilename()
        if filename == '':
            return
        self.file_exists = True
        self.filename = filename.split("/")[-1]
        with open(filename, "r") as file:
            self.output_object = json.load(file)
        self.attacks = self.output_object["attacks"]
        self.second_screen()

    def second_screen(self, event=None):
        if not self.file_exists:
            tn = self.team_name_entry.get()
            on = self.opponent_name_entry.get()
            date = datetime.datetime.today().strftime('%d-%m-%Y')
            self.filename = tn + "-" + on + "-" + date + ".json"
        self.cleanup_first_screen()
        self.setup_second_screen()

    def cleanup_first_screen(self):
        self.team_name_label.destroy()
        self.team_name_entry.destroy()
        self.opponent_name_label.destroy()
        self.opponent_name_entry.destroy()
        self.create_file_button.destroy()
        self.get_existing_file_button.destroy()

    def setup_second_screen(self):
        self.focus_set()
        new_attack_button = tk.Button(self, text="Add new Attack",
                                      command=lambda: self.add_new_attack())
        self.bind('<a>', lambda x: self.add_new_attack())
        self.flip_field = tk.IntVar()
        fo_checkbox = tk.Checkbutton(self, text="Flip field orientation", variable=self.flip_field)

        save_and_quit_button = tk.Button(self, text="Save and go back to main menu",
                                         command=lambda: self.save_and_destroy())
        self.bind('<s>', lambda x: self.save_and_destroy())

        new_attack_button.pack()
        fo_checkbox.pack()
        save_and_quit_button.pack()

    def add_new_attack(self):
        plt.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])
        points = plt.ginput(2, show_clicks=True)
        attack_popup = NewAttackPopup(self)
        self.master.wait_window(attack_popup.top)

        new_attack = [self.orientation()*points[0][0], self.orientation()*points[0][1],
                      self.orientation()*points[1][0], self.orientation()*points[1][1],
                      int(attack_popup.shirt_number), attack_popup.hit.get(), len(self.attacks)]
        self.attacks.append(new_attack)
        plt.close()

    def save_and_destroy(self):
        with open("../data/{}".format(self.filename), "w") as file:
            json.dump(self.output_object, file)
        self.destroy()

    def orientation(self):
        if self.flip_field.get() == 1:
            return -1
        else:
            return 1


class NewAttackPopup(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.shirt_number = 0
        shirt_number_label = tk.Label(self.top, text="Attacker's shirt number")
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.shirt_number_entry = tk.Entry(self.top, validate='key', validatecommand=vcmd)
        add_button = tk.Button(self.top, text='Add attack',
                               command=lambda: self.cleanup())

        hit_label = tk.Label(self.top, text="Hit, Miss or Pass")
        self.hit = tk.StringVar()
        self.hit.set("P")
        hit_rb = tk.Radiobutton(self.top, text="Hit", variable=self.hit, value="H")
        miss_rb = tk.Radiobutton(self.top, text="Miss", variable=self.hit, value="M")
        pass_rb = tk.Radiobutton(self.top, text="Pass", variable=self.hit, value="P")
        self.shirt_number_entry.bind('<h>', lambda x: self.hit.set("H"))
        self.shirt_number_entry.bind('<m>', lambda x: self.hit.set("M"))
        self.shirt_number_entry.bind('<p>', lambda x: self.hit.set("P"))
        self.shirt_number_entry.focus_set()

        shirt_number_label.pack()
        self.shirt_number_entry.pack()
        add_button.pack()
        hit_label.pack()
        hit_rb.pack(anchor=tk.W)
        miss_rb.pack(anchor=tk.W)
        pass_rb.pack(anchor=tk.W)
        self.top.bind('<Return>', self.cleanup)

    def cleanup(self, event=None):
        self.shirt_number = self.shirt_number_entry.get()
        self.top.destroy()

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
