import os,shutil
""" TODO: Have a function determine the size of a file using os.stat(path)[6] . Then have the system
 Keep track of its progress and display whenever a file has been proccessed AND its % counter
 has gone up to the next integer """


def update(src,dst, changes=[]):
    """Updates directory dst from src. Recursively copies all subdirectories and files of src if they are not in dst or are out of date.
       Also removes files in dst that are not in src.

          src (str): directory path
          dst (str): directory path
          changes (list): optional list in which changes are recorded as tuple 
          ( path,  "remove"/"copy"/"mod")
    """
    if not is_valid(src,dst):
        return

    # if(src.find('git''object')!=-1):
    #     #A permission error with git dirs often occurs. I dont need git files that much so they wont be copied over for now.
    #     return

    #If the item is in dst but not src, remove it
    for item in os.listdir(dst):
        srcfiles = list(os.listdir(src))
        if item not in srcfiles:
                dstpath = dst+'/'+item
                remove(dstpath)
                changes[dstpath] = "remove"

    # If the item is in src but not dst, copy it over
    for item in os.listdir(src):
        srcpath = src + '/' + item

        if item not in os.listdir(dst):
            if os.path.isfile(srcpath):
                shutil.copy2(srcpath, dst)
            if os.path.isdir(srcpath):
                shutil.copytree(srcpath, dst+'/'+item)
            changes[dst+'/'+item] = "copy"


        # Item is in src and dst. If file, update if most recent. If directory update dst's version.
        else:
            if os.path.isfile(srcpath):
                if isFileMoreRecent(srcpath, dst+'/'+item):
                    shutil.copy2(srcpath, dst)
                    changes[dst+'/'+item] = "mod"
            else:
                update(srcpath, dst + '/' + item)

    return changes

def is_valid(src,dst):
    if not os.path.exists(src) or not os.path.exists(dst):
        print("source or dst does not exist")
        return False

    #check if dst is IN src. Leads to Spooky infinite recursion. much 2spooky4me
    if os.path.realpath(dst).find(os.path.realpath(src))!=-1:
        return False

    if not os.path.isdir(src) or not os.path.isdir(dst):
        return False

    return True



def isFileMoreRecent(filePath,toCompareWithPath):
    if os.stat(filePath).st_mtime - os.stat(toCompareWithPath).st_mtime > 0:
        return True
    return False

def get_path_input(msg):
    """Returns valid path for file or directory through sanitized user input"""
    path = input(msg)
    while True:
        if not os.access(path,os.F_OK):
            path = input("path was invalid or permission not granted, please enter a valid path")
        else:
            print("path has been selected")
            return path

def remove(path):
    """Remove file or folder from PC."""
    global changes
    try:
        if os.path.isfile(path):
            os.remove(path)
            changes.append(("f", path, "remove"))
        if os.path.isdir(path):
            for y in os.listdir(path):
                remove(path+"'/'"+y)
            os.rmdir(path)
            changes.append(("d", path, "remove"))

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
            return max([date_of_last(path+"'/'"+x) for x in os.listdir(path)])
        else:
            return 0

def populate_list_of_subdirectories(dir,list):
    for file in os.listdir(dir):
        path = dir+"/"+file
        list.append(path)
        if os.path.isdir(path):
            populate_list_of_subdirectories(path,list)
