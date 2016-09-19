import os, shutil

def update(src,dst):
    """Updates dst from src. Recursively copies all subdirectories and files of src if they are not in dst or are out of date.
       Also removes files in dst that are not in src.
          src (str): directory path or file path
          dst (str): directory path
    """
    if os.path.isfile(src):
        copyfile(src,dst)
        return

    elif os.path.isdir(src):
        foldername=src.split("\\")[-1]
        if foldername not in os.listdir(dst):
            #If the folder isn't in dst copy it
            shutil.copytree(src,dst+"\\"+foldername)
        else:
            #If the foldername of src is in dst, remove content that is in dst's copy of src, but not in src
            for x in os.listdir(dst+'\\'+foldername):
                if x not in os.listdir(src):
                    remove(dst+'\\'+foldername+"\\"+x)
            #Then update what copy what IS in src to dst (checking for time modified)
            for x in os.listdir(src):
                update(src+"\\"+x, dst+"\\"+foldername)

    else:
        print("not a folder or a file!?")
        return

def copyfile(src,dst):
    """Copies file 'src' to folder 'dst'. If file already exists in dst with
    same name, only copy if src has been modified more recently than the copy"""
    filename=src.split("\\")[-1]
    if filename in os.listdir(dst):
        #If the file exists in dst then check for time modified
        if os.stat(src).st_mtime>os.stat(dst+"\\"+filename).st_mtime:
            #If src file has been modified more recently, copy it
            shutil.copy2(src,dst)
        #If the file exists in dst but is more recent than the src version, return without copying over
        return
    #If src not in dst, copy it
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
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        for y in os.listdir(path):
            remove(path+"\\"+y)
        os.rmdir(path)

def main():
    path1=get_path_input("Enter the path of the updated version ")
    path2=get_path_input("Enter the path where the file/folder to be updated resides in ")
    update(path1,path2)
    raw_input("Process Complete. Press enter to exit. ")

if __name__=="__main__":
    main()
