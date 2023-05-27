import sys
import cv2
from imwatermark import WatermarkDecoder
import math
import wmlib

messageLenBits = 256 # Change this line for different message lengths
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
    images = wmlib.find_images(sys.argv[1])

    decoder = WatermarkDecoder('bytes', messageLenBits)

    possibleSols = []
    strSols = []

    print("Found", len(images), "images.")

    index = 1

    for img in images:

        sys.stdout.write("\033[F\033[F\033[K")
        print("Decoding image", index, "/", len(images))

        bgr = cv2.imread(img)
        wm = decoder.decode(bgr, 'dwtDctSvd')

        sols = []
        _strSols = []

        # Get the lists of all the combinations of bits that can be added to the array
        for w in wm:
            str = wmlib.decodeString(bin(int(w.hex(), base=16))[2:]) # Convert from bytes type to bits
            strArr = []
            for i in range(messageLenSqrt):
                strArr.append(str[i * messageLenSqrt : (i + 1) * messageLenSqrt])

            for i in range(messageLenSqrt):
                for j in range(messageLenSqrt):
                    # Check if the bits can form valid ASCII; if they can, add the bits to the solutions array
                    try:
                        s = wmlib.arrConcat(wmlib.shiftRight(wmlib.shiftDown(strArr, i), j))
                        n = int("0b" + s, 2)
                        n1 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
                        if n1[0] == "_" and not n1 in sols:
                            sols.append(s)
                            _strSols.append(n1)
                    except:
                        pass

        possibleSols.append(sols)
        strSols.append(_strSols)

        index = index + 1

    print("Finished decoding images.")

    print("\nBase solutions:")
    for s in strSols:
        for s1 in s:
            print(s1)

    # Part of a correction mechanism I'm working on.
    # Essentially, a lot of the decoded strings have 25-30 correct characters, but 2-7 incorrect characters.
    # This code attempts to correct those inconsistencies.
    endSols = []

    for l in range(len(possibleSols)):
        for i in range(len(possibleSols[l])):

            similarEnough = [] # the array of strings that are similar enough to the base string that they can be used to help correct inconsistencies
            for j in range(len(possibleSols)):
                for k in range(len(possibleSols[j])):
                    # compare strings 1 and 2
                    percent_similar = wmlib.similarity(possibleSols[l][i], possibleSols[j][k])

                    # if more than 80%? (can be changed) of the bits match, add string 2 to string 1's list of similar strings
                    if percent_similar > 232 / 256:
                        similarEnough.append(possibleSols[j][k])

                # at the end, make the new string equal to the rounded average of each of the bits
                similarEnough.append(possibleSols[l][i])
                s = wmlib.strAvg(similarEnough)
                if not s in endSols:
                    endSols.append(s)

    print("\nAveraged possible solutions:")
    for s in endSols:
        str = wmlib.bitToStr(s)
        if str.count("`") <= 2: # If a string has more than 2 `s in it, it's probably garbage
            print(str)

    # takes the average of the average. It's pretty accurate when all of the images are severely cropped.
    print("\nDoubly averaged solution:")
    strEndSols = []
    for s in endSols:
        s1 = wmlib.bitToStr(s)
        if s1.count("`") < 2: # If a string has more than 2 `s in it, it's probably garbage
            strEndSols.append(s1)
    print(wmlib.strAvg(strEndSols))

def singleImage():
    '''
    Decodes a single image.
    '''

    print("Decoding image...")
    inputFile = sys.argv[1]

    bgr = cv2.imread(inputFile)

    decoder = WatermarkDecoder('bytes', messageLenBits)
    watermark = decoder.decode(bgr, 'dwtDctSvd')

    print("Finished decoding frames.")

    sols = []

    for w in watermark:
        str = wmlib.decodeString(bin(int(w.hex(), base=16))[2:]) # Convert from bytes type to bits

        # Initialize an array of 8-character (8-bit) strings.
        strArr = []
        for i in range(messageLenSqrt):
            strArr.append(str[i * messageLenSqrt : (i + 1) * messageLenSqrt])

        for i in range(messageLenSqrt):
            for j in range(messageLenSqrt):
                # Check if the bits can form valid ASCII; if they can, add the ASCII to the solutions array
                try:
                    # Shift the elements in the array appropriately to check all possible orderings of bits
                    s = wmlib.arrConcat(wmlib.shiftRight(wmlib.shiftDown(strArr, i), j))

                    n1 = wmlib.decodeString(s)
                    if n1[0] == "_" and not n1 in sols:
                        sols.append(n1)
                except:
                    pass
        
    if(len(sols) > 0):
        print("Possible solutions:")
        for p in sols:
            print(p)

    else:
        print("No possible solutions found.")

if(__name__ == "__main__"):
    main()