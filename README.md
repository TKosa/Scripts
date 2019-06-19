# Update-Folder
Recursively copies files and folder heirarchy to ensure destination folder is a replica of source, without wasting time on unnecessary copying.

Made this for my personal files that I kept transferring from laptop to desktop, back and forth.
The set of all files is pretty big, but I'd only add a few memes between switching from one device to the other, so recopying 5gb was extensive.

This script takes two paths src and dest, and copies files and folders from src to dest, keeping the structure of the directories.
If files already exist in dest it'll check the date modified, and have the most recently modified file stay/be-copied-into dest. 
If a file is in dest but NOT in src, it will remove the file from dest so the two match.

In the GUI, modified files are orange, deleted files are red, added files are green.

<img src="https://github.com/TKosa/Update-Folder/update-folder.png" width="500">
