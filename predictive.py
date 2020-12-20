"""

module:: PredictiveTransform
    :synopsis: This transformer transforms (wow) an image using a predictive approach, decreasing entropy.
moduleauthor:: Edgar Duarte <edgarduarte@student.dei.uc.pt>

Several libs are imported here:
    numpy


This transformer codec was made by Edgar Duarte.

"""

import numpy as np


# Predictive Transformer
class PredictiveTransform:

    def __init__(self):
        pass

    # Encodes the function f[i] -= f[i-1], i>=1 horizontally
    def horizontalEncode(self, image):
        image2 = np.copy(image)
        image2 = image2.astype("int16")
        height, length = image2.shape
        
        image2[:,1:] = np.subtract(image2[:,1:], image2[:,:length-1])

        return image2

    # Decodes the function f[i] -= f[i-1], i>=1 horizontally
    def horizontalDecode(self, information):
        information2 = np.copy(information)
        height, length = information2.shape
        for i in range(1,length):
            information2[:,i] +=  information2[:,i-1]
        information2 = information2.astype("uint8")
        return information2
        
    # Encodes the function f[i] -= f[i-1], i>=1 vertically
    def verticalEncode(self, image):
        image2 = np.copy(image)
        image2 = image2.astype("int16")
        height, length = image2.shape
        
        image2[1:,:] = np.subtract(image2[1:,:], image2[:height-1 ,: ])
        return image2

    # Decodes the function f[i] -= f[i-1], i>=1 vertically
    def verticalDecode(self, information):
        information2 = np.copy(information)
        height, length = information2.shape
        for i in range(1, height):
            information2[i,:] += information2[i-1,:]
        information2 = information2.astype("uint8")
        return information2

    # Transforms data using Predictive algorithm
    def encode(self, information, vertical=False):
        if (vertical):
            encoded_information = self.verticalEncode(information)
        else:
            encoded_information = self.horizontalEncode(information)
        
        return encoded_information

    # Reverts a transformation
    def decode(self, information, vertical=False):
        if (vertical):
            decoded_information = self.verticalDecode(information)
        else:
            decoded_information = self.horizontalDecode(information)
        
        return decoded_information
