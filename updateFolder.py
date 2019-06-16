import os
from utilityFns import *

def gui(src="Path of Src Directory",dst="Path of Destination Directory"):

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
    tk.La
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
