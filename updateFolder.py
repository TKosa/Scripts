import os
from utilityFns import *
from tkinter import *
from tkinter.filedialog import askdirectory

global src,dst
src = "C:\\UF-Demo\\Master"
dst = "C:\\UF-Demo\\Copy"

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self.master = master
        self.input_frame = InputFrame(self)
        self.input_frame.grid()
        self.output_frame=None

        #TODO add event log
        self.pack(fill=X)

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

        #runBtn.config(text='Running')



        state_dict = {} #Key is path, item is array of dirents
        change_dict = {}
        populate_statedict(dst, state_dict)
        update(src, dst, state_dict, change_dict)

        try:
            self.output_frame.destroy()
        except AttributeError:
            pass
        self.output_frame = OutputFrame(self, dst, state_dict, change_dict)



        runBtn.config(text='Run')
        runBtn.config(command=self.run)


class InputFrame(Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        global src, dst
        self.src_row = self.SelectDirectoryRow(self, 0, "Set Src", src)
        self.dst_row = self.SelectDirectoryRow(self, 1, "Set Dst", dst)

        self.runBtn = Button(self, text="Run", command=master.run)
        self.runBtn.pack(fill=X)


    class SelectDirectoryRow(Frame):
        # A frame with a button and label. On button click, user selects directory, which then appears in label.

        def __init__(self, master, row, btntext="", labeltext=""):
            super().__init__(master, bg="white")

            self.label = Label(self, text=labeltext, bg="white")
            self.label.pack(side=LEFT)

            self.button = Button(self, text=btntext, command=self.onClick)
            self.button.pack(side=RIGHT)

            self.pack(fill=X)

        def onClick(self):
            self.label.config(text=askdirectory())


class OutputFrame(Frame):
    #Container for both viewer widgets

    def __init__(self, master, root, dirstate, changes={}):
        super().__init__(master, bg="white")

        self.FV = self.FolderViewer(self, root, dirstate, changes)
        self.grid(column=0, sticky="ew")


    class FolderViewer():
        """
        Shows folder and subfolders after app has run
        Highlights differences
            removed files shown in red, added in green, modified in yellow

        """
        def __init__(self, master, root, dir_state, changes):
            self.master=master
            self.rowNum = 0
            print(dir_state)
            print(changes)
            self.addEntries(root, dir_state, changes)

        def addEntries(self, path, dir_state, changes, spaces = 0):
            # Adds file/folder at path, and all subdirectories, to output frame
            for file in dir_state[path]:
                newpath = path+'/'+file
                self.Entry(self.master, newpath, self.rowNum, changes, spaces)
                self.rowNum += 1
                try:
                    check_is_folder = dir_state[newpath] #Will throw error if <path> is not folder
                    self.addEntries(newpath, dir_state, changes, spaces+2)
                except KeyError:
                    pass


        class Entry:
            def __init__(self, master, path, rowNum, changes, spaces=0):
                filename = os.path.basename(path)
                self.filenameLabel = Label(master, text=" "*spaces+filename, bg="white")
                self.filenameLabel.grid(row=rowNum,column=0, sticky="W")
                change = changes.get(path)
                if changes is not None:
                    if change == "remove":
                        self.filenameLabel.configure(fg="red")
                    if change == "copy":
                        self.filenameLabel.configure(fg="green")
                    if change == "mod":
                        self.filenameLabel.configure(fg="orange")

def test():
    src = "C:/Users/Thomas/Desktop/github/Update-Folder/testA"
    dst = "C:/Users/Thomas/Desktop/github/Update-Folder/testB"
    state_dict = {}
    change_dict = {}
    populate_statedict(dst, state_dict)
    update(src, dst, state_dict, change_dict)


if __name__=="__main__":
    # This version is for desktop
    root = Tk()
    root.title("Update-Folder")
    app = Application(master=root)
    root.mainloop()
