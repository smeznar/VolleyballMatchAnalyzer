import tkinter as tk
from match_data_gatherer import Constants
from match_data_gatherer import StartPage
from match_data_gatherer import NewMatchDataPage


class WMAApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(Constants.APPLICATION_NAME)
        self.geometry("1000x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage.StartPage, NewMatchDataPage.NewMatchDataPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = WMAApp()
    app.mainloop()
