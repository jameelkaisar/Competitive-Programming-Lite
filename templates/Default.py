def solution():
    # Solution {N}


try:
    import sys
    import os
    if (os.path.exists(".cpl_files/{N}.in.txt")):
        sys.stdin = open(".cpl_files/{N}.in.txt","r")
        sys.stdout = open(".cpl_files/{N}.out.txt","w")
except:
    pass

t = int(input())
while t:
    solution()
    t -= 1
