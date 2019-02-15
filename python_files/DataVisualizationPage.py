import tkinter as tk
from python_files import Constants as C
from python_files import AttackVisualizationPage
from python_files import PassVisualizationPage
from tkinter.filedialog import askopenfilename
import json


class VisualizationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.selected_file = "-1"
        self.data = None

        title = tk.Label(self, text="Data Visualization", font=("Helvetica", 20))
        visualize_attacks_button = tk.Button(self, text="Visualize attacks",
                                             command=lambda: self.visualize_attacks())
        visualize_passes_button = tk.Button(self, text="Visualize passes",
                                            command=lambda: self.visualize_passes())
        back_button = tk.Button(self, text="Back",
                                command=lambda: self.destroy())
        select_file_button = tk.Button(self, text="Select file",
                                       command=lambda: self.select_file())

        title.grid(row=0, column=1, pady=2*C.NORMAL_PADDING)
        visualize_attacks_button.grid(row=1, column=1, pady=C.NORMAL_PADDING)
        visualize_passes_button.grid(row=2, column=1, pady=C.NORMAL_PADDING)
        back_button.grid(row=3, column=0, pady=C.NORMAL_PADDING)
        select_file_button.grid(row=3, column=2, pady=C.NORMAL_PADDING)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def select_file(self):
        filename = askopenfilename()
        if filename == '':
            return
        with open(filename, "r") as file:
            self.data = json.load(file)

    def visualize_attacks(self):
        if self.data is None:
            self.select_file_popup()
        else:
            AttackVisualizationPage.AttackVisualizationPage(self,
                                                            self.data["attacks"] if "attacks" in self.data.keys() else [])

    def visualize_passes(self):
        if self.data is None:
            self.select_file_popup()
        else:
            PassVisualizationPage.PassVisualizationPage(self,
                                                        self.data["passes"] if "passes" in self.data.keys() else [])

    def select_file_popup(self):
        top = tk.Toplevel()
        top.geometry("300x100")
        top.title("File Not Selected")
        msg = tk.Label(top, text="Please select a file before visualization")
        button = tk.Button(top, text="Dismiss", command=top.destroy)
        msg.pack(pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)
        button.pack(pady=C.NORMAL_PADDING, padx=C.NORMAL_PADDING)

