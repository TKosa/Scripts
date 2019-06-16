import os
from utilityFns import *
from tkinter import *
from tkinter.filedialog import askdirectory

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master,width=100)
        self.master = master
        self.input_frame = InputFrame(self)
        self.pack()

    def run(self):
        src = self.input_frame.src_row.label.cget("text")
        dst = self.input_frame.dst_row.label.cget("text")
        runBtn = self.input_frame.runBtn
        
        if not os.path.exists(src) or not os.path.exists(dst):
            runBtn.config(text='Error: path or src does not exist')
            return

        if os.path.realpath(dst).find(os.path.realpath(src)) != -1:
            runBtn.config(text='Error: dst is IN src')
            return

        runBtn.config(text='Running')
        update(src, dst)

        runBtn.config(text='Run')
        runBtn.config(command=self.run)



class InputFrame(Frame):
    def __init__(self, master):
        super().__init__(master,width=100)

        self.src_row = SelectDirectoryRow(self, "Src")
        self.dst_row = SelectDirectoryRow(self, "Dst")

        self.runBtn = Button(self, text="Run", command=master.run)
        self.runBtn.pack()

        self.pack()

class SelectDirectoryRow(Frame):
    #A frame with a button and label. On button click, user selects directory, which then appears in label.

    def __init__(self, master, text=""):
        super().__init__(master,width=100)

        self.label = Label(self, text="", bg="white", width=65)
        self.label.pack(padx=5, side=LEFT)

        self.button = Button(self, text=text, width=25, command=self.onClick)
        self.button.pack(side=LEFT)

        self.pack(fill=X)

    def onClick(self):
        self.label.config(text=askdirectory())





if __name__=="__main__":
    # This version is for desktop
    root = Tk()
    root.title("Update-Folder")
    app = Application(master=root)
    root.mainloop()
