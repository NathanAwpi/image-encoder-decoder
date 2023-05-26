import sys
import cv2
from imwatermark import WatermarkDecoder
import math
import watermarklib

messageLenBits = 256
messageLenSqrt = int(math.sqrt(messageLenBits))

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("The command should be formatted as:\ndecode.py input-file\nOR\ndecode.py folder-path -m\nQuotations are necessary if the path has spaces.")
        exit(0)

    if len(sys.argv) == 2:
        singleImage()
    else:
        multipleImages()

# Unfinished
def multipleImages():
    paths = watermarklib.find_images(sys.argv[1])

    watermark = None

    for path in paths:

        bgr = cv2.imread(path)

        decoder = WatermarkDecoder('bytes', messageLenBits) # Change this line for different message lengths
        wm = decoder.decode(bgr, 'dwtDctSvd')

    # Given the list of 16 binary sequences:
    # For each sequence, try it out in every order
    # If it starts with an underscore, add it to the list

    prevSols = []

    f = 0

    for w in watermark:
        print(f)
        str = decodeString(bin(int(w.hex(), base=16))[2:]) # Convert from bytes type to bits
        strArr = []
        for i in range(messageLenSqrt):
            strArr.append(str[i * messageLenSqrt : (i + 1) * messageLenSqrt])

        for i in range(messageLenSqrt):
            for j in range(messageLenSqrt):
                try:
                    s = arrConcat(shiftRight(shiftDown(strArr, i), j))
                    n = int("0b" + s, 2)
                    n1 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
                    if n1[0] == "_" and not n1 in prevSols:
                        prevSols.append(n1)
                        print(n1)
                except:
                    pass
        
        f = f + 1
        # print(len(prevSols))

def singleImage():
    print("Decoding image...")
    inputFile = sys.argv[1]

    bgr = cv2.imread(inputFile)

    decoder = WatermarkDecoder('bytes', messageLenBits) # Change this line for different message lengths
    watermark = decoder.decode(bgr, 'dwtDctSvd')

    # Given the list of 16 binary sequences:
    # For each sequence, try it out in every order
    # If it starts with an underscore, add it to the list

    prevSols = []

    # f = 0

    for w in watermark:
        # print(f)
        str = decodeString(bin(int(w.hex(), base=16))[2:]) # Convert from bytes type to bits
        strArr = []
        for i in range(messageLenSqrt):
            strArr.append(str[i * messageLenSqrt : (i + 1) * messageLenSqrt])

        for i in range(messageLenSqrt):
            for j in range(messageLenSqrt):
                try:
                    s = arrConcat(shiftRight(shiftDown(strArr, i), j))
                    n = int("0b" + s, 2)
                    n1 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
                    if n1[0] == "_" and not n1 in prevSols:
                        prevSols.append(n1)
                except:
                    pass
        
        # f = f + 1
        # print(len(prevSols))
    if(len(prevSols) > 0):
        print("Possible solutions:")
        for p in prevSols:
            print(p)

    else:
        print("No possible solutions found.")

def arrConcat(strArr):
    toReturn = ""
    for s in strArr:
        toReturn = toReturn + s
    return toReturn

def shiftDown(strArr, n):
    for i in range(n):
        strArr = strArr[1:] + strArr[:1]
    return strArr

def shiftRight(strArr, n):
    for i in range(len(strArr)):
        strArr[i] = strArr[i][n:] + strArr[i][:n]
    return strArr

# Adds zeroes to the beginning of the string until its length is a multiple of 8
def decodeString(str):
    remainder = 8 - (len(str) % 8)
    str = ('0' * remainder) + str
    return str

if(__name__ == "__main__"):
    main()