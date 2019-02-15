import tkinter as tk
from python_files import Constants as C


class NewPassPopup(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.geometry("300x100")
        self.shirt_number = 0
        shirt_number_label = tk.Label(self.top, text="Shirt number")
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.shirt_number_entry = tk.Entry(self.top, validate='key', validatecommand=vcmd)
        add_button = tk.Button(self.top, text='Add pass',
                               command=lambda: self.cleanup())

        received_label = tk.Label(self.top, text="Received or Missed:")
        upper_label = tk.Label(self.top, text="Upper or Lower:")
        self.received = tk.StringVar()
        self.received.set("R")
        self.upper = tk.StringVar()
        self.upper.set("U")
        received_rb = tk.Radiobutton(self.top, text="Received", variable=self.received, value="R")
        miss_rb = tk.Radiobutton(self.top, text="Missed", variable=self.received, value="M")
        upper_rb = tk.Radiobutton(self.top, text="Upper", variable=self.upper, value="U")
        lower_rb = tk.Radiobutton(self.top, text="Lower", variable=self.upper, value="L")
        self.shirt_number_entry.bind('<r>', lambda x: self.received.set("R"))
        self.shirt_number_entry.bind('<m>', lambda x: self.received.set("M"))
        self.shirt_number_entry.bind('<u>', lambda x: self.upper.set("U"))
        self.shirt_number_entry.bind('<l>', lambda x: self.upper.set("L"))
        self.shirt_number_entry.focus_set()
        self.top.bind('<Return>', self.cleanup)

        shirt_number_label.grid(row=0, column=0)
        self.shirt_number_entry.grid(row=0, column=1, columnspan=2)
        received_label.grid(row=1, column=0)
        received_rb.grid(row=1, column=1)
        miss_rb.grid(row=1, column=2)
        upper_label.grid(row=2, column=0)
        upper_rb.grid(row=2, column=1)
        lower_rb.grid(row=2, column=2)
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
