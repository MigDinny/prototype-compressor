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
    """
    This class encodes or decodes a 2D array using a predictive transformation. The main objective of this algorithm is to reduce entropy of the
    given information.

    Use only encode() or decode()
    """
    def __init__(self):
        """
        Constructor. It is empty
        """
        pass


    def horizontalEncode(self, initial_data):
        """
        Encodes each line of the given data via the function f(i) = f(i) - f(i-1), with i ∈ [1, array_lenght], being i the index of the current pixel

        Parameters: 
            initial_data (2D array): array that will be encoded
        
        Returns:
            2D array: encoded array
        """
        final_data = np.copy(initial_data)
        final_data = final_data.astype("int16")
        _ , length = final_data.shape
        
        final_data[:,1:] = np.subtract(final_data[:,1:], final_data[:,:length-1])

        return final_data


    def horizontalDecode(self, initial_data):
        """
        Decodes each line of the given data (that was previously encoded) via the function f(i) = f(i) + f(i-1), with i ∈ [1, array_lenght],being
        i the index of the current pixel

        Parameters: 
            initial_data (2D array): array that will be decoded
        
        Returns:
            2D array: decoded array
        """
        final_data = np.copy(initial_data)
        _ , length = final_data.shape
        for i in range(1,length):
            final_data[:,i] +=  final_data[:,i-1]
        final_data = final_data.astype("uint8")
        return final_data
        

    def verticalEncode(self, initial_data):
        """
        Encodes each column of the given data via the function f(i) = f(i) - f(i-1), with i ∈ [1, array_heigth], being i the index of the current pixel

        Parameters: 
            initial_data (2D array): array that will be encoded
        
        Returns:
            2D array: encoded array
        """
        final_data = np.copy(initial_data)
        final_data = final_data.astype("int16")
        height , _ = final_data.shape
        
        final_data[1:,:] = np.subtract(final_data[1:,:], final_data[:height-1 ,: ])
        return final_data


    def verticalDecode(self, initial_data):
        """
        Decodes each column of the given data via the function f(i) = f(i) - f(i-1), with i ∈ [1, array_heigth], being i the index of the current pixel

        Parameters: 
            initial_data (2D array): array that will be decoded
        
        Returns:
            2D array: decoded array
        """

        final_data = np.copy(initial_data)
        height , _ = final_data.shape
        for i in range(1, height):
            final_data[i,:] += final_data[i-1,:]
        final_data = final_data.astype("uint8")
        return final_data

    # Transforms data using Predictive algorithm
    def encode(self, data, vertical=False):
        """
        Encodes data using a predictive transformer
        
        It can encode both horizontaly and verticaly, being the method chosen by the user, although the default setting is to encode 
        horizontaly.

        Parameters:
            data (2D array): data to be encoded
            vertical (boolean): if True it encodes using a vertical predictive encoder. Default: False, encodes horizontaly

        Returns:
            2D array: encoded data
        """
        if (vertical):
            encoded_data = self.verticalEncode(data)
        else:
            encoded_data = self.horizontalEncode(data)
        
        return encoded_data


    def decode(self, data, vertical=False):
        """
        Decodes data using a predictive transformer
        
        Should be decoded with the same transformation as it was encoded, which means, if you encode with a vertical encoder you have to decode with the 
        vertical decoder or else the result array will have unexpected results.

        Parameters:
            data (2D array): data to be decoded
            vertical (boolean): if True it encodes using a vertical predictive encoder. Default: False, encodes horizontaly

        Returns:
            2D array: decoded data
        """
        if (vertical):
            decoded_data = self.verticalDecode(data)
        else:
            decoded_data = self.horizontalDecode(data)
        
        return decoded_data
