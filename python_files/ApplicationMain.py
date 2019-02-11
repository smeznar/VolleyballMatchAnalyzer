import tkinter as tk
from python_files import Constants
from python_files import StartPage


class AppMain(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(Constants.APPLICATION_NAME)
        self.geometry(Constants.WINDOW_SIZE)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.show_frame(StartPage.StartPage)

    def show_frame(self, page_class):
        frame = page_class(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


if __name__ == '__main__':
    app = AppMain()
    app.mainloop()
