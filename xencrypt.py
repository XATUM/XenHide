from stegano import lsb, exifHeader

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

def encode_image(img_path, message, out_path):
    final_type = determine_type(img_path)
    if final_type == ".png":
        secret = lsb.hide(img_path, message)
        secret.save(out_path)
    elif final_type in (".jpg", ".jpeg"):
        exifHeader.hide(img_path, out_path, secret_message=message)
    else:
        raise ValueError(f"Unsupported file type: {final_type}")

def main():
    img_type = input("Enter the image name ").strip().lower()
    src_path = input("Enter path of the file: ")
    secret_file = input("Enter file to hide: ")
    with open(secret_file, "r") as f:
        secret_message = f.read()
    final_type = determine_type(img_type)
    if final_type == "":
        print("Please specify filetype (/or its not supported):", end=" ")
        final_type = input().strip().lower()
        if not final_type.startswith("."):
            final_type = "." + final_type
    print()
    try:
        out_path = input("Where to and how to save: ")
        encode_image(src_path, secret_message, out_path)
        print("✓ Done!")
    except ValueError as e:
        print(e)
        exit(0)

if __name__ == '__main__':
    main()