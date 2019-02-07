import os, shutil


#TODO: Have a function determine the size of a file using os.stat(path)[6] . Then have the system
#Keep track of its progress and display whenever a file has been proccessed AND its % counter
#has gone up to the next integer
def update(src,dst):
    """Updates dst from src. Recursively copies all subdirectories and files of src if they are not in dst or are out of date.
       Also removes files in dst that are not in src.

       If src is a file, if it is not in the directory dst, or is out of date in dst, copy it over

          src (str): directory path or file path
          dst (str): directory path
    """
    if not os.path.exists(src) or not os.path.exists(dst) :
        return

    #check if dst is IN src. Leads to Spooky infinite recursion. much 2spooky4me
    if os.path.realpath(dst).find(os.path.realpath(src))!=-1:
        return

    if os.path.isfile(src):
        copyfile(src,dst)
        return

    if(src.find('git\\object')!=-1):
        #A permission error with git dirs often occurs. I dont need git files that much so they wont be copied over for now.
        return

    for item in os.listdir(dst):
        #If item is in dst but not src, remove it
        if item not in os.listdir(src):
                print('removing ' + item)
                remove(dst+"\\"+item)

    for item in os.listdir(src):
        #If the item is in src but not dst, copy it over
        if item not in os.listdir(dst):
            print(item)
            Item=src+'\\'+item
            if os.path.isfile(Item):
                copyfile(Item,dst)
            if os.path.isdir(Item):
                print('copying' + Item)
                shutil.copytree(Item,dst+'\\'+item)


        #If item is in both src and dst, if item is a file copy it over, if it is a directory update dst's version
        if item in os.listdir(dst):
            Item=src+'\\'+item
            if os.path.isfile(Item):
                copyfile(Item,dst)
            else:
                update(Item,dst+'\\'+item)


def copyfile(src,dst):
    """Copies file 'src' to folder 'dst'. If file already exists in dst with
    same name, only copy if src has been modified more recently than the """
    filename=src.split("\\")[-1]
    if filename in os.listdir(dst):
        #If the file exists in dst then check for time modified
        if os.stat(src).st_mtime-os.stat(dst+"\\"+filename).st_mtime>1:

            #If src file has been modified more recently, copy it
            print('copying 4' + src)
            print("src has been modified more recently.\n" + str(os.stat(src).st_mtime) + "\n"+ str(os.stat(dst+"\\"+filename).st_mtime) )
            try:
                shutil.copy2(src,dst)
                return
            except IOError:
                print("perms denied")
    else:
        #If src not in dst, copy it
        print('copying 6' + src)
        shutil.copy2(src,dst)

def get_path_input(msg):
    """Returns valid path for file or directory through sanitized user input"""
    path = raw_input(msg)
    while True:
        if not os.access(path,os.F_OK):
            path = raw_input("path was invalid or permission not granted, please enter a valid path")
        else:
            print("path has been selected")
            return path

def remove(path):
    """Remove file or folder from PC."""
    try:
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            for y in os.listdir(path):
                remove(path+"\\"+y)
            os.rmdir(path)
    except:
        print("Could not remove " + path)

def date_of_last(path):
    """Returns most recent time that the file or a content of the folder was modified
            path: File or Directory
    """
    if os.path.isfile(path):
        #return time of modification
        return os.stat(path)[8]
    if os.path.isdir(path):
        #if path is a directory, return date of most recently modified file in the directory.
        if len(os.listdir(path))>0:
            return max([date_of_last(path+"\\"+x) for x in os.listdir(path)])
        else:
            return 0

def gui(src="Path of Src Directory",dst="Path of Destination Directory"):
    #This Probably deserves its own file, but having the entire app be exactly 2 files is awkward so here we are
    import Tkinter as tk
    from tkFileDialog import askdirectory


    def choose_src():
        src=askdirectory()
        top_left.config(text=src)

        #If program has already run but they change src/dst, runbtn will work again
        run_button.config(text='Run')
        run_button.config(command = run_btn)

    def choose_dst():
        global dst
        dst=askdirectory()
        middle_left.config(text=dst)

        #If program has already run but they change src/dst, runbtn will work again
        run_button.config(text='Run')
        run_button.config(command = run_btn)

    root=tk.Tk()
    root.title("Update-Folder")

    top_label=tk.Label(root)
    top_left=tk.Label(top_label,width=60)
    top_left.config(text=src,bg="white")
    top_left.pack(padx=5, side=tk.LEFT)

    top_right=tk.Button(top_label, text='Choose Src Directory', width=25, command=choose_src)
    top_right.config(text="Choose Src")
    top_right.pack( side=tk.RIGHT)

    middle_label=tk.Label(root)
    middle_left=tk.Label(middle_label,width=60)
    middle_left.config(text=dst,bg="white")
    middle_left.pack(padx=5, side=tk.LEFT)

    middle_right=tk.Button(middle_label, text='Choose Src Directory', width=25, command=choose_dst)
    middle_right.config(text="Choose Dst")
    middle_right.pack(side=tk.RIGHT)

    def run_btn():
        src=top_left.cget("text")
        dst=middle_left.cget("text")

        print(src + " " + dst)
        print(os.path.exists(dst))

        if not os.path.exists(src) or not os.path.exists(dst) :
            run_button.config(text='Error: path or src does not exist')
            return
        if os.path.realpath(dst).find(os.path.realpath(src))!=-1:
            run_button.config(text='Error: dst is IN src')
            return

        run_button.config(text='Running')
        update(src,dst)
        run_button.config(text='Finished Running. Click to close.')
        run_button.config(command = lambda: root.destroy())

    run_button=tk.Button(root, text='Run', width=45, command = run_btn)

    top_label.pack()
    middle_label.pack()
    run_button.pack()

    root.mainloop()


def main():
    #Default src/dst if you use the program often
    src = "J:\\T"
    dst = "C:\\Users\\Thomas\\Desktop\\T\\Update"
    gui(src,dst)

if __name__=="__main__":
    # This version is for desktop
    main()
