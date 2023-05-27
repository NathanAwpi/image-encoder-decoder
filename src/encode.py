import sys
import os
import cv2
from imwatermark import WatermarkEncoder
import wmlib

def main():

    messageLen = 32 # Change this line for different message lengths

    # Incorrect args format
    if len(sys.argv) != 4:
        print("The command should be formatted as:\nencode.py input-folder output-folder message\nQuotations are only necessary if the path or message has spaces.")
        exit(0)

    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    message = sys.argv[3]

    # Incorrect message length
    if len(message) != messageLen:
        print("The message must be exactly", messageLen, "characters long. Your message is", len(message), "characters long.")
        exit(0)

    # Get the images
    images = wmlib.find_images(inputFolder)

    numImages = len(images)
    numCompleted = 1

    # Encode each image
    for image in images:
        print("Encoding image ", numCompleted, "/", numImages, end="\r")
        encode_single_image(image, generate_output_path(image, inputFolder, outputFolder), message)
        numCompleted += 1

    print("Finished encoding", numImages, "images.")

def encode_single_image(imagePath, outputPath, message):
    '''
    Encodes a single image and saves it the the givem path.
    imagePath: String. The  path to the image.
    outputPath: String. The path the i=mage will be saved to. Thje paht should include the file name.
    message: The message to encode the image with.
    '''

    # Open the image
    bgr = cv2.imread(imagePath)

    # Encode the image
    encoder = WatermarkEncoder()
    encoder.set_watermark('bytes', message.encode('utf-8'))
    bgr_encoded = encoder.encode(bgr, 'dwtDctSvd')

    # Save the image
    cv2.imwrite(outputPath, bgr_encoded)
    
def generate_output_path(image, inputFolder, outputFolder):
    '''
    Generates the output path for an image. Creates any directories that don't exist.
    image: String. The path to the image.
    inputfolder: String. The path to the root folder that is being searched for images.
    outputFolder: String. The folder the images will be saved to.
    '''
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