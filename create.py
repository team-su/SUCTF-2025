import os


dir = os.listdir('./')

for d in dir:
    if os.path.isdir(d) and d != '.git': 
        for e in os.listdir(d):
            wp = f"./{d}/{e}/writeup"
            if not os.path.exists(wp) or not os.path.exists(wp + "/README.md"):
                print("bad dir ", wp)
            print( "|" + d + "|" + e + "|" + f"[{wp}]({wp})" + "|" )