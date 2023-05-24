import sys
import cv2
from imwatermark import WatermarkDecoder

def main():

    if len(sys.argv) != 2:
        print("The command should be formatted as:\ndecode.py input-file\nQuotations are necessary if the path has spaces.")
        exit(0)

    inputFile = sys.argv[1]

    bgr = cv2.imread(inputFile)

    decoder = WatermarkDecoder('bytes', 256) # Change this line for different message lengths
    watermark = decoder.decode(bgr, 'dwtDctSvd')
    print(watermark.decode('utf-8'))

if(__name__ == "__main__"):
    main()