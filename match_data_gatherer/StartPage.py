import tkinter as tk


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Volleyball Match Analyzer")
        label.pack(side="top", fill="x", pady=10)
        data_collect_button = tk.Button(self, text="New Match Data",
                                        command=lambda: controller.show_frame("NewMatchDataPage"))
        data_collect_button.pack()
