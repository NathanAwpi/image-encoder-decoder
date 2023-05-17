import sys
import os
import cv2
from imwatermark import WatermarkEncoder

def main():

    if len(sys.argv) != 4:
        print("The command should be formatted as:\nencode.py input-folder output-folder message\nQuotations are necessary if the path or message has spaces.")
        exit(0)

    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    message = sys.argv[3]

    if len(message) != 32:
        print("The message must be exactly 32 characters long.")
        exit(0)

    images = find_images(inputFolder)

    numImages = len(images)
    numCompleted = 1

    for image in images:
        print("Encoding image ", numCompleted, "/", numImages, end="\r")
        encode_single_image(image, generate_output_path(image, inputFolder, outputFolder), message)
        numCompleted += 1

    print("Finished encoding", numImages, "images.")

def encode_single_image(imagePath, outputPath, message):
    bgr = cv2.imread(imagePath)

    encoder = WatermarkEncoder()
    encoder.set_watermark('bytes', message.encode('utf-8'))
    bgr_encoded = encoder.encode(bgr, 'dwtDctSvd')

    cv2.imwrite(outputPath, bgr_encoded)

def find_images(inputFolder):
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
    
def generate_output_path(image, inputFolder, outputFolder):
    # The image path
    path = outputFolder + image[len(inputFolder):]

    # There is already an image in the target directory with the same name
    if os.path.exists(path):
        os.remove(path)

    # Create the directory chain
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    return path

if(__name__ == "__main__"):
    main()