import sys
import os

print("Competitive Programming Lite Solution Tester")
print('""""""""""""""""""""""""""""""""""""""""""""')

if len(sys.argv) > 1:
    t = int(sys.argv[1].split("_", 1)[0])
else:
    t = int(input("Enter Question Number to Test: "))

size = os.get_terminal_size()[0]//2 - 5

with open(f".cpl_files/{t}.tst.txt", "r") as f:
    tst_str = f.readlines()
with open(f".cpl_files/{t}.out.txt", "r") as f:
    out_str = f.readlines()

tst_len = len(tst_str)
out_len = len(out_str)

for i in range(max(tst_len, out_len)):
    if i < tst_len:
        tst_res = tst_str[i].strip()
    else:
        tst_res = ""
    if i < out_len:
        out_res = out_str[i].strip()
    else:
        out_res = ""
    if tst_res == out_res:
        mat_res = " | | "
    else:
        mat_res = " |X| "
    print(tst_res.ljust(size, " ") + mat_res + out_res.ljust(size, " "))

print()
if "".join(tst_str).strip() == "".join(out_str).strip():
    print("Test Result: SUCCESS")
else:
    print("Test Result: FAIL")
