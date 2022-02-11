import sys
import shutil

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = int(input("Enter File Name: "))

shutil.copyfile(f"{file_name}", ".cpl_files/Main.java")
