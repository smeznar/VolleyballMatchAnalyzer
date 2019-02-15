import matplotlib as mpl
mpl.use("TkAgg")
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from python_files import Constants as C


class PassVisualizationPage(tk.Toplevel):
    def __init__(self, master, pass_data):
        tk.Toplevel.__init__(self)
        self.geometry(C.VISUALIZATION_ATTACK_DIMENSIONS)
        self.img = mpimg.imread("../data/volleyball_court.png")

        self.pass_data = pass_data
        title = tk.Label(self, text="Pass Visualization", font=("Helvetica", 20))

        shirt_number_label = tk.Label(self, text="Shirt number")
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.shirt_number_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.all_players = tk.IntVar()
        shirt_number_checkbox = tk.Checkbutton(self, text="All players", variable=self.all_players)

        self.received = tk.IntVar()
        received_checkbox = tk.Checkbutton(self, text="Received", variable=self.received)
        self.miss = tk.IntVar()
        miss_checkbox = tk.Checkbutton(self, text="Missed", variable=self.miss)
        self.upper = tk.IntVar()
        upper_checkbox = tk.Checkbutton(self, text="Upper", variable=self.upper)
        self.lower = tk.IntVar()
        lower_checkbox = tk.Checkbutton(self, text="Lower", variable=self.lower)

        self.fig = plt.Figure()
        self.subplot = self.fig.add_subplot(111)
        self.subplot.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        back_button = tk.Button(self, text="Back",
                                command=lambda: self.destroy())
        show_pass_button = tk.Button(self, text="Show pass",
                                     command=lambda: self.show_passes())

        title.grid(row=0, column=1, pady=2*C.NORMAL_PADDING)
        shirt_number_label.grid(row=1, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.shirt_number_entry.grid(row=1, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        shirt_number_checkbox.grid(row=1, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        received_checkbox.grid(row=2, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        miss_checkbox.grid(row=2, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        upper_checkbox.grid(row=3, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        lower_checkbox.grid(row=3, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, rowspan=2)
        back_button.grid(row=6, column=0, pady=C.NORMAL_PADDING)
        show_pass_button.grid(row=6, column=2, pady=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def show_passes(self):
        self.subplot.cla()
        self.subplot.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])

        show_all = self.all_players.get()
        shirt_num = self.shirt_number_entry.get()
        if shirt_num == '':
            shirt_num = -1
        else:
            shirt_num = int(shirt_num)

        r = self.received.get()
        m = self.miss.get()
        u = self.upper.get()
        l = self.lower.get()
        rm_set = set()
        if r == 1:
            rm_set.add("R")
        if m == 1:
            rm_set.add("M")
        ul_set = set()
        if u == 1:
            ul_set.add("U")
        if l == 1:
            ul_set.add("L")

        [self.draw_passes(pa) for pa in self.pass_data
         if (show_all or pa[C.ATTACK_SHIRT_NUMBER] == shirt_num) and (pa[C.PASS_RM] in rm_set) and (pa[C.PASS_UL] in ul_set)]
        self.canvas.draw()

    def draw_passes(self, attack):
        style = ''
        if attack[C.PASS_RM] == "R":
            style += 'g'
        elif attack[C.PASS_RM] == "M":
            style += 'r'
        else:
            style += 'y'
        if attack[C.PASS_UL] == "L":
            style += '-'
        elif attack[C.PASS_UL] == "U":
            style += ':'
        else:
            style += '-.'
        self.subplot.plot([attack[0], attack[2]], [attack[1], attack[3]], style)

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
