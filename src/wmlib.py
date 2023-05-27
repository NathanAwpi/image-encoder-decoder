import os
import collections

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

def bitToStr(bits):
    n = int("0b" + bits, 2)
    n1 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return n1

def strAvg(arr):
    
    toReturn = ""
    for i in range(len(arr[0])):
        tmp = ""
        for j in range(len(arr)):
            tmp = tmp + arr[j][i]
        counter = collections.Counter(tmp)
        result = counter.most_common(1)[0][0]
        toReturn = toReturn + result

    return toReturn

def similarity(a, b):
    same = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            same = same + 1
    return same / len(a)