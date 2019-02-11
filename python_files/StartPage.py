import tkinter as tk
from python_files import NewMatchDataPage
from python_files import DataVisualizationPage
from python_files import Constants as C


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=C.APPLICATION_NAME, font=("Helvetica", 20))
        label.grid(row=0, pady=2*C.NORMAL_PADDING)
        data_collect_button = tk.Button(self, text="New Match Data",
                                        command=lambda: controller.show_frame(NewMatchDataPage.NewMatchDataPage))
        data_visualize_button = tk.Button(self, text="Visualize Data",
                                          command=lambda: controller.show_frame(DataVisualizationPage.VisualizationPage))
        data_collect_button.grid(row=1, pady=C.NORMAL_PADDING)
        data_visualize_button.grid(row=2, pady=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
