import os

def find_images(inputFolder):
    '''
    Finds all the images in the input directory. Also searched subdirectories for images.
    Returns: String[] of the paths to the images.
    '''
    print("Scanning subdirectories for images...")

    numFound = 0
    arr = []

    # Find all the images in the directory and in subdirectories
    for root, dirs, files in os.walk(inputFolder, topdown=False):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                numFound += 1
                print("Found", numFound, "images.", end="\r")

                arr.append(os.path.join(root, file))

    print("Found", numFound, "images.")
    return arr