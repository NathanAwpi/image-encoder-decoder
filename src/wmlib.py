import os
import collections

'''
This is a series of small helper functions, mostly to do with strings and arrays.
'''

def find_images(inputFolder):
    '''
    Finds all the images in the input directory. Also searches subdirectories for images.
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
    '''
    Given an array of strings, concatenates them into a single string.
    For example, arrConcat(["abcd", "efgh"]) would return "abcdefgh"
    '''
    toReturn = ""
    for s in strArr:
        toReturn = toReturn + s
    return toReturn

def shiftDown(strArr, n):
    '''
    Shifts all elements in the array down by the specified amount.
    For example, shiftDown(["abcd", "efgh", "ghij"], 2) would return ["ghij", "abcd", "efgh"]
    '''
    for i in range(n):
        strArr = strArr[1:] + strArr[:1]
    return strArr

def shiftRight(strArr, n):
    '''
    Shifts all elements in the array right by the specified amount.
    For example, shiftRight(["abcd", "efgh"], 2) would return ["cdab", "ghef"]
    '''
    for i in range(len(strArr)):
        strArr[i] = strArr[i][n:] + strArr[i][:n]
    return strArr

def decodeString(str):
    '''
    Adds zeroes to the beginning of the string until its length is a multiple of 8
    For example, decodeString("0010101") would return "00010101
    '''
    remainder = 8 - (len(str) % 8)
    str = ('0' * remainder) + str
    return str

def bitToStr(bits):
    '''
    Given a string of bits, converts it to an ASCII string.
    '''
    n = int("0b" + bits, 2)
    n1 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return n1

def strAvg(arr):
    '''
    Returns the most common value of each character in a list of strings.
    For example, strAvg([[1, 0, 1], [1, 1, 0], [[1, 0, 0]]) it would return "100"
    '''

    if len(arr) == 0:
        return ""
    
    toReturn = ""
    for i in range(len(arr[0])):
        tmp = ""
        for j in range(len(arr)):
            try:
                tmp = tmp + arr[j][i]
            except:
                pass
        counter = collections.Counter(tmp)
        result = counter.most_common(1)[0][0]
        toReturn = toReturn + result

    return toReturn

def similarity(a, b):
    '''
    Given 2 strings, returns the percentage of characters that are equal.
    For example, similarity("abcd", "abcc") would return 0.75
    '''
    same = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            same = same + 1
    return same / len(a)