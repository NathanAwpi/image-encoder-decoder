import numpy as np
import copy
import cv2
import pywt
import math
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)


class EmbedDwtDctSvd(object):
    def __init__(self, watermarks=[], wmLen=8, scales=[0,36,0], block=4):
        self._watermarks = watermarks
        self._wmLen = wmLen
        self._scales = scales
        self._block = block

    def encode(self, bgr):
        (row, col, channels) = bgr.shape

        yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)

        for channel in range(2):
            if self._scales[channel] <= 0:
                continue

            ca1,(h1,v1,d1) = pywt.dwt2(yuv[:row//4*4,:col//4*4,channel], 'haar') # Get the layers of the image
            self.encode_frame(ca1, self._scales[channel]) # Encode the message

            yuv[:row//4*4,:col//4*4,channel] = pywt.idwt2((ca1, (h1,v1,d1)), 'haar') # Put the layers of the image back together
            # print("yuv:", yuv[0,:16])

        bgr_encoded = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        return bgr_encoded

    def decode(self, bgr):

        (row, col, channels) = bgr.shape

        allBits = [] # Used to store all possible readings of bits
        index = 0

        for x in range(self._block):
            for y in range(self._block):

                sys.stdout.write("\033[K")
                print("Decoding frame", index, "/", self._block **2, end="\r")

                yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)

                scores = [[] for i in range(self._wmLen)]
                for channel in range(2):
                    if self._scales[channel] <= 0:
                        continue

                    ca1,(h1,v1,d1) = pywt.dwt2(yuv[:row//4*4,:col//4*4,channel], 'haar')

                    scores = self.decode_frame(ca1, self._scales[channel], scores, x, y)

                avgScores = list(map(lambda l: np.array(l).mean(), scores))

                bits = (np.array(avgScores) * 255 > 127)

                allBits.append(bits)

                index = index + 1

        print("Decoding frame", self._block ** 2, "/", self._block ** 2)

        return allBits

    def decode_frame(self, frame, scale, scores, x, y):
        frame = frame[x:, y:]
        (row, col) = frame.shape
        sqrtWmLen = int(math.sqrt(self._wmLen))

        for i in range(row // (sqrtWmLen * self._block)):
            for j in range(col // (sqrtWmLen * self._block)):
                
                num = 0

                for k in range(sqrtWmLen):
                    for l in range(sqrtWmLen):
                        iOffset = sqrtWmLen * i * self._block
                        jOffset = sqrtWmLen * j * self._block

                        block = frame[k * self._block + iOffset : (k + 1) * self._block + iOffset,
                                    l * self._block + jOffset : (l + 1) * self._block + jOffset]

                        score = self.infer_dct_svd(block, scale)
                        wmBit = num % self._wmLen
                        scores[wmBit].append(score)
                        num = num + 1
        return scores

    def diffuse_dct_svd(self, block, wmBit, scale):
        u,s,v = np.linalg.svd(cv2.dct(block))

        s[0] = (s[0] // scale + 0.25 + 0.5 * wmBit) * scale
        return cv2.idct(np.dot(u, np.dot(np.diag(s), v)))

    def infer_dct_svd(self, block, scale):
        u,s,v = np.linalg.svd(cv2.dct(block))

        score = 0
        score = int ((s[0] % scale) > scale * 0.5)
        return score
        if score >= 0.5:
            return 1.0
        else:
            return 0.0

    def encode_frame(self, frame, scale):
        '''
        frame is a matrix (M, N)

        we get K (watermark bits size) blocks (self._block x self._block)

        For i-th block, we encode watermark[i] bit into it
        '''

        (row, col) = frame.shape
        # print("Rows:", row, ", Cols:", col)
        sqrtWmLen = int(math.sqrt(self._wmLen))
        for i in range(row // (sqrtWmLen * self._block)):
            for j in range(col // (sqrtWmLen * self._block)):
                
                num = 0

                for k in range(sqrtWmLen):
                    for l in range(sqrtWmLen):
                        # large offset + small offset
                        # large offset = sqrtWmLen * self._block * i
                        # small offset = k * self._block OR (k + 1) * self._block
                        iOffset = sqrtWmLen * i * self._block
                        jOffset = sqrtWmLen * j * self._block

                        block = frame[k * self._block + iOffset : (k + 1) * self._block + iOffset,
                                    l * self._block + jOffset: (l + 1) * self._block + jOffset]
                        
                        wmBit = self._watermarks[(num % self._wmLen)]


                        diffusedBlock = self.diffuse_dct_svd(block, wmBit, scale)
                        frame[k * self._block + iOffset : (k + 1) * self._block + iOffset,
                            l * self._block + jOffset : (l + 1) * self._block + jOffset] = diffusedBlock

                        num = num+1

                        # if k == 0 and i == 1 and j == 0:
                        #     print("Pos:", k * self._block + iOffset, "-", (k + 1) * self._block + iOffset,
                        #           "/", l * self._block + jOffset, "-", (l + 1) * self._block + jOffset,
                        #           "|", wmBit, "|", self.infer_dct_svd(diffusedBlock, scale))
                        # print("Wrote bit", diffusedBlock, "to position", k, "/", l)
