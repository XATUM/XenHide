# imports
import stegano as n

def findIndex(filename):
    i = len(filename) - 1
    while i >= 0:
        if filename[i] == ".":
            return i
        i -= 1
    return -1

def determine_type(img_type):
    exPoint = findIndex(img_type)
    if exPoint == -1:
        return ""
    return img_type[exPoint:]



def main():
    file_reveal=input("File with path: ")
    final_type=determine_type(file_reveal)
    x = False

    if final_type =="":
        print("Please specify filetype (/or its not supported):",end=" ")
        final_type=input().strip().lower()
        if not final_type.startswith("."):
            final_type="."+final_type
    print()
    if final_type == ".png":
        print(n.lsb.reveal(file_reveal))
        secret = n.lsb.reveal(file_reveal)
        writef = input("save file? (y/n): ")


    elif final_type in(".jpg",".jpeg"):
        print(n.exifHeader.reveal(file_reveal))
        secret = n.exifHeader.reveal(file_reveal)
        writef = input("save file? (y/n): ")


    else:
        print("Sorry, File Type- ",final_type," is not supported")
        exit(0)

    if writef in ("y","yes","yeah"):
        x = True
    else:
        exit(0)

    if x:
        savef = input("where to and how to save: ")
        with open(savef, "w") as f:
            f.write(str(secret))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 main()

