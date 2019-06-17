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
        self.grid(sticky="news")

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

        self.output_frame = OutputFrame(self, src, dst).pack(fill=X)
        #update(src, dst)

        runBtn.config(text='Run')
        runBtn.config(command=self.run)


class InputFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.src_row = self.SelectDirectoryRow(self, "Set Src", "C:\\Users\\Thomas\\Desktop\\github\\Update-Folder\\testA")
        self.dst_row = self.SelectDirectoryRow(self, "Set Dst", "C:\\Users\\Thomas\\Desktop\\github\\Update-Folder\\testB")

        self.runBtn = Button(self, text="Run", command=master.run)
        self.runBtn.pack()

        self.pack()

    class SelectDirectoryRow(Frame):
        # A frame with a button and label. On button click, user selects directory, which then appears in label.

        def __init__(self, master, btntext="", labeltext=""):
            super().__init__(master)

            self.label = Label(self, text=labeltext, bg="white")
            self.label.pack(padx=5, side=LEFT)

            self.button = Button(self, text=btntext, command=self.onClick)
            self.button.pack(side=LEFT)

            self.pack(fill=X)

        def onClick(self):
            self.label.config(text=askdirectory())


class OutputFrame(Frame):
    #Container for both viewer widgets

    def __init__(self, master, src, dst):
        super().__init__(master, bg="white")

        src_viewer = self.FolderViewer(self, src, 0)
        dst_viewer = self.FolderViewer(self, dst, 1)



    class FolderViewer():
        """
        Shows folder and subfolders
            updates in real time as app makes changes
        Highlights differences
            removed files shown in red, added in green, modified in yellow

        """
        def __init__(self, master, path, colNum):
            self.master=master

            list_of_subdirs = []
            populate_list_of_subdirectories(path, list_of_subdirs)
            rowNum = 0

            for file in list_of_subdirs:
                self.addEntry(file, rowNum, colNum)
                rowNum += 1





        def addEntry(self, path, rowNum, colNum):
            self.Entry(self.master, path, rowNum, colNum)
            #self.master.rowconfigure(rowNum,weight=1)

        class Entry:
            def __init__(self, master, path, rowNum, colNum, spaces=0):
                filename = os.path.basename(path)

                # Button to display filetype (file or directory), and to expand/collapse if dir
                self.button = Button(master)
                if os.path.isdir(path):
                    self.button['image'] = closedFolderImage
                elif os.path.isfile(path):
                    self.button['image'] = fileImage
                self.button.grid(row=rowNum, column=4*colNum, sticky=W)

                #print("button", path, rowNum, 2*colNum)


                #filename label
                self.nameLabel = Label(master, text=filename, bg="white")
                self.nameLabel.grid(row=rowNum,column=4*colNum+1, sticky="EW")
                self.nameLabel.grid_columnconfigure(4*colNum+1,weight=1)
                #print("Label", path, rowNum, 2*colNum+1)


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
