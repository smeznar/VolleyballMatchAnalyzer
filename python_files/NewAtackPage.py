import tkinter as tk
from python_files import Constants as C


class NewAttackPopup(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.geometry("300x100")
        self.shirt_number = 0
        shirt_number_label = tk.Label(self.top, text="Shirt number")
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.shirt_number_entry = tk.Entry(self.top, validate='key', validatecommand=vcmd)
        add_button = tk.Button(self.top, text='Add attack',
                               command=lambda: self.cleanup())

        hit_label = tk.Label(self.top, text="Hit, Miss or Pass:")
        self.hit = tk.StringVar()
        self.hit.set("P")
        hit_rb = tk.Radiobutton(self.top, text="Hit", variable=self.hit, value="H")
        miss_rb = tk.Radiobutton(self.top, text="Miss", variable=self.hit, value="M")
        pass_rb = tk.Radiobutton(self.top, text="Pass", variable=self.hit, value="P")
        self.shirt_number_entry.bind('<h>', lambda x: self.hit.set("H"))
        self.shirt_number_entry.bind('<m>', lambda x: self.hit.set("M"))
        self.shirt_number_entry.bind('<p>', lambda x: self.hit.set("P"))
        self.shirt_number_entry.focus_set()
        self.top.bind('<Return>', self.cleanup)

        shirt_number_label.grid(row=0, column=0)
        self.shirt_number_entry.grid(row=0, column=1, columnspan=2)
        hit_label.grid(row=1, column=1)
        hit_rb.grid(row=2, column=0)
        miss_rb.grid(row=2, column=1)
        pass_rb.grid(row=2, column=2)
        add_button.grid(row=3, column=1, pady=C.NORMAL_PADDING)
        self.top.columnconfigure(0, weight=1)
        self.top.columnconfigure(1, weight=1)
        self.top.columnconfigure(2, weight=1)

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
