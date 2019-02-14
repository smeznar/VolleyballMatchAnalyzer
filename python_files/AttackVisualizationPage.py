import matplotlib as mpl
mpl.use("TkAgg")
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from python_files import Constants as C


class AttackVisualizationPage(tk.Toplevel):
    def __init__(self, master, attack_data):
        tk.Toplevel.__init__(self)
        self.geometry(C.VISUALIZATION_ATTACK_DIMENSIONS)
        self.img = mpimg.imread("../data/volleyball_court.png")

        self.attack_data = attack_data
        title = tk.Label(self, text="Attack Visualization", font=("Helvetica", 20))

        shirt_number_label = tk.Label(self, text="Shirt number")
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.shirt_number_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.all_players = tk.IntVar()
        shirt_number_checkbox = tk.Checkbutton(self, text="All players", variable=self.all_players)

        self.hit = tk.IntVar()
        hit_checkbox = tk.Checkbutton(self, text="Hit", variable=self.hit)
        self.miss = tk.IntVar()
        miss_checkbox = tk.Checkbutton(self, text="Miss", variable=self.miss)
        self.passed = tk.IntVar()
        pass_checkbox = tk.Checkbutton(self, text="Pass", variable=self.passed)

        self.fig = plt.Figure()
        self.subplot = self.fig.add_subplot(111)
        self.subplot.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)

        back_button = tk.Button(self, text="Back",
                                command=lambda: self.destroy())
        show_attacks_button = tk.Button(self, text="Show attack",
                                        command=lambda: self.show_attacks())

        title.grid(row=0, column=1, pady=2*C.NORMAL_PADDING)
        shirt_number_label.grid(row=1, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.shirt_number_entry.grid(row=1, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        shirt_number_checkbox.grid(row=1, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        hit_checkbox.grid(row=2, column=0, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        miss_checkbox.grid(row=2, column=1, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        pass_checkbox.grid(row=2, column=2, pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, rowspan=2)
        back_button.grid(row=5, column=0, pady=C.NORMAL_PADDING)
        show_attacks_button.grid(row=5, column=2, pady=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def show_attacks(self):
        self.subplot.cla()
        self.subplot.imshow(self.img, extent=[-12.5, 12.5, -7.875, 7.875])

        show_all = self.all_players.get()
        shirt_num = self.shirt_number_entry.get()
        if shirt_num == '':
            shirt_num = -1
        else:
            shirt_num = int(shirt_num)

        h = self.hit.get()
        m = self.miss.get()
        p = self.passed.get()
        hmp_set = set()
        if h == 1:
            hmp_set.add("H")
        if m == 1:
            hmp_set.add("M")
        if p == 1:
            hmp_set.add("P")

        [self.draw_attack(at) for at in self.attack_data
         if (show_all or at[C.ATTACK_SHIRT_NUMBER] == shirt_num) and (at[C.ATTACK_HMP] in hmp_set)]
        self.canvas.draw()

    def draw_attack(self, attack):
        if attack[C.ATTACK_HMP] == "H":
            self.subplot.plot([attack[0], attack[2]], [attack[1], attack[3]], 'g-')
        if attack[C.ATTACK_HMP] == "M":
            self.subplot.plot([attack[0], attack[2]], [attack[1], attack[3]], 'r-')
        if attack[C.ATTACK_HMP] == "P":
            self.subplot.plot([attack[0], attack[2]], [attack[1], attack[3]], 'y-')

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
