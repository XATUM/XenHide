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


def decode_image(img_path):
    final_type = determine_type(img_path)
    if final_type == ".png":
        message = lsb.reveal(img_path)
    elif final_type in (".jpg", ".jpeg"):
        message = exifHeader.reveal(img_path)
    else:
        raise ValueError(f"Unsupported file type: {final_type}")
    return message if message else ""


def main():
    file_reveal = input("File with path: ")
    final_type = determine_type(file_reveal)
    if final_type == "":
        print("Please specify filetype (/or its not supported):", end=" ")
        final_type = input().strip().lower()
        if not final_type.startswith("."):
            final_type = "." + final_type
    print()
    try:
        secret = decode_image(file_reveal)
        print(secret)
        writef = input("Save file? (y/n): ")
        if writef.lower() in ("y", "yes", "yeah"):
            savef = input("Where to and how to save: ")
            with open(savef, "w") as f:
                f.write(str(secret))
    except ValueError as e:
        print(e)
        exit(0)


if __name__ == '__main__':
    main()