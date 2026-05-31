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
    img_type=input("Enter the image name ").strip().lower()
    src_path = input("Enter path of the file: ")
    secret_file = input("enter file to hide: ")
    with open(secret_file,"r") as f:
        secret_message=f.read()

    final_type=determine_type(img_type)
    if final_type =="":
        print("Please specify filetype: /or its not supported",end=" ")
        final_type=input().strip().lower()
        if not final_type.startswith("."):
            final_type="."+final_type
    print()
    if final_type == ".png":
        secret = n.lsb.hide(src_path,secret_message)
        secret.n.save(input("where to and how to save: "))
    elif final_type in(".jpg",".jpeg"):
        fStore = input("where to and how to save: ")
        secret = n.exifHeader.hide(src_path,fStore,secret_message=secret_message)
    else:
        print("Sorry, File Type- ",final_type," is not supported")
        exit(0)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 main()

