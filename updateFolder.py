import os
from utilityFns import *
from tkinter import *
from tkinter.filedialog import askdirectory

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.input_frame = InputFrame(self)

        #TODO add event log
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

        self.output_frame = OutputFrame(self, src, dst)
        #update(src, dst)

        runBtn.config(text='Run')
        runBtn.config(command=self.run)


class InputFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.src_row = self.SelectDirectoryRow(self, "Src", "C:\\Users\\Thomas\\Desktop\\github\\Update-Folder\\testA")
        self.dst_row = self.SelectDirectoryRow(self, "Dst", "C:\\Users\\Thomas\\Desktop\\github\\Update-Folder\\testB")

        self.runBtn = Button(self, text="Run", command=master.run)
        self.runBtn.pack()

        self.pack()

    class SelectDirectoryRow(Frame):
        # A frame with a button and label. On button click, user selects directory, which then appears in label.

        def __init__(self, master, btntext="", labeltext=""):
            super().__init__(master)

            self.label = Label(self, text=labeltext, bg="white", width=65)
            self.label.pack(padx=5, side=LEFT)

            self.button = Button(self, text=btntext, width=25, command=self.onClick)
            self.button.pack(side=LEFT)

            self.pack(fill=X)

        def onClick(self):
            self.label.config(text=askdirectory())


class OutputFrame(Frame):
    #Container for both viewer widgets

    def __init__(self, master, src, dst):
        super().__init__(master)

        src_viewer = self.FolderViewer(self, src)
        dst_viewer = self.FolderViewer(self, dst)

        self.pack()

    class FolderViewer(Frame):
        """
        Shows folder and subfolders
            updates in real time as app makes changes
        Highlights differences
            removed files shown in red, added in green, modified in yellow

        """
        def __init__(self, master, folder):
            super().__init__(master)

            self.FileLineFrame(self, os.getcwd())

            self.pack(side=LEFT)

        class FileLineFrame(Frame):

            def __init__(self, master, path, spaces=0):
                super().__init__(master)
                filename = os.path.basename(path)

                # Button to display filetype (file or directory), and to expand/collapse if dir
                self.button = Button(self)
                if os.path.isdir(path):
                    self.button['image'] = closedFolderImage
                elif os.path.isfile(path):
                    self.button['image'] = fileImage
                self.button.pack()

                #filename label
                self.nameLabel = Label(self, text=filename, bg="white")
                #filesize label

                self.pack()


if __name__=="__main__":
    # This version is for desktop
    root = Tk()
    root.title("Update-Folder")

    global fileImage, closedFolderImage, openFolderImage
    fileImage = PhotoImage(file="./res/file.png")
    closedFolderImage = PhotoImage(file="./res/closed_folder.png")
    openFolderImage = PhotoImage(file="./res/open_folder.png")

    app = Application(master=root)
    root.mainloop()
