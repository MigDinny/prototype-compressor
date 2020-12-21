"""

module:: LZWCodec
    :synopsis: This codec encodes an image using LZW algorithm. This codec also makes a predictive transformation in order to decrease entropy.
moduleauthor:: Rodrigo Ferreira <rodrigoferreira@student.dei.uc.pt>
moduleauthor:: Miguel Dinis <miguelbarroso@student.dei.uc.pt> (reviser)

Several libs are imported here:
    matplotlib
    numpy
    math
    imageio (to store the output info in a .bmp file)
    PredictiveTransform


This LZW Algorithm was coded by "adityagupta3006" as in https://github.com/adityagupta3006/LZW-Compressor-in-Python

This codec was made by Rodrigo Ferreira based on the above. 

"""

import numpy as np
import matplotlib.image as mpimg
import math
import imageio
from predictive import PredictiveTransform

class LZWCodec:
    """
    This codec makes a predictive transformation before encoding. LZW is used to encode and decode afterwards.

    Use only encode() and decode()
    """ 

    def __init__(self):
        """
        Codec constructor.
        """
        pass


    def encode_LZW(self,data):
        """
        Encodes a given data using LZW.

        Parameters:
            data (array): the data to be encoded

        Returns:
            array: LZW encoded data
        """

        #initialize dictionary and defines max size
        size = 16
        max_dic_size = pow(2,int(size))
        dictionary_size = 512                   
        dictionary = {str(i): i for i in range(dictionary_size)}
        string = ""
        compressed_data = np.arange(0,dtype=np.uint16)
        
        #encodes data
        for symbol in data:
            if (len(string)==0):
                string_plus_symbol = str(symbol)
            else:             
                string_plus_symbol = string + "#" + str(symbol)
    
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data = np.append(compressed_data, [*dictionary].index(string))

                #while having space add new combination to dictionary
                if (len(dictionary) < max_dic_size-1):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = str(symbol)
     
        if string in dictionary:
            compressed_data = np.append(compressed_data, [*dictionary].index(string))
        
        #append number that represents resetting the dictionary
        compressed_data = np.append(compressed_data, max_dic_size-1)

        return compressed_data


    def encode(self, filein, fileout, chunkSize=50000, vertical=False):
        """
        Transforms using PredictiveTransform and encodes a given file and outputs it in another file.

        Vertical option, if chosen, calls the predictive transformer in Vertical mode, which will predict the values in a vertical order.
        ChunckSize option, if given value, this will be the new size of each chunk of data to encode.

        Parameters: 
            filein (string): file to be encoded (.bmp format)
            fileout (string): file to be created as output (.npy format)
            chunckSize (int): size of the chunks to encode. Default: 50000
            vertical (boolean): if True, calls Predictive in vertical mode. Default: False.
        """

        # read data from file
        data =  mpimg.imread(filein)
    
        pt = PredictiveTransform()
        data = pt.encode(data, vertical)
        data[:] += 255
        
        #splits the data in chunks to encode
        strPoint = 0
        endPoint = chunkSize
        data1D = data.flatten()
        #stores the shape of the image
        compressed_data = np.array([data.shape[0], data.shape[1]], dtype = np.uint16)

        while (strPoint < len(data1D)):
            #encodes the chunk with LZW
            comp = np.array(self.encode_LZW(data1D[strPoint:endPoint]), dtype = np.uint16)
            compressed_data = np.append(compressed_data, comp)

            strPoint = endPoint
            endPoint += chunkSize
            if(endPoint>len(data1D)):
                endPoint = len(data1D)

        #save encoding in file
        np.save(fileout, compressed_data)


    def decode_LZW(self, data, size):
        """
        Decodes a given data using LZW.

        Parameters:
            data (array): the data to be decoded
            size (int): 2^size is the max size of the dictionary

        Returns:
            array: LZW decoded data
        """
        
        #initialize dictionary and defines max size
        max_dic_size = pow(2,int(size))
        decoded_data = np.array([], dtype=np.int16)
        decoded_array = np.array([], dtype=np.int16)
        next_code = 512
        dictionary_size = 512
        dictionary = [[] for x in range(max_dic_size)]
        for i in range(dictionary_size):
            dictionary[i] = np.array([i])

        nums =  np.array([], dtype=np.int16)


        for code in data:
            #to increase efficiency the array is reseted when the length is bigger than 100000
            if (len(decoded_array)>100000):
                decoded_data = np.append(decoded_data, decoded_array)
                decoded_array = np.array([], dtype=np.uint16)
            
            #reset the dictionary and clean decoded_array
            if (code == max_dic_size-1):
                dictionary = [[] for x in range(max_dic_size)]
                next_code = 512
                nums =  np.array([], dtype=np.uint16)
                for i in range(dictionary_size):
                    dictionary[i] = np.array([i])
                
                decoded_data = np.append(decoded_data, decoded_array)
                decoded_array = np.array([], dtype=np.uint16)
            else:
                #decoded data
                if (np.array_equal(dictionary[code],[])):
                    dictionary[code] = np.array(np.append(nums, [nums[0]]))
        
                decoded_array = np.append(decoded_array, dictionary[code])
                if (next_code < max_dic_size -1 and len(nums) > 0):
                    dictionary[next_code] = np.array(np.append(nums, [dictionary[code][0]]))
                    next_code += 1
                nums = dictionary[code]
        
        #join the rest of the decoded data
        decoded_data = np.append(decoded_data, decoded_array)

        return decoded_data
    

    def decode(self, filein, fileout, vertical=False):
        """
        Decodes a given file and outputs the decoded data into a .bmp (bitmap) file.

        Vertical option must be the same as used when encoding.

        Parameters:
            filein (string): file to be decoded (in .npy format)
            fileout (string): file to be created and outputted (preferably .bmp format)
            vertical (boolean): if True, calls predictive in Vertical mode. Default: False. 
        """

        #load data
        comp_data =  np.load(filein)

        #get shape of the image
        heigth = comp_data[0]
        length = comp_data[1]
        comp_data = comp_data[2:]

        #get the size of the dictionary
        size = round(math.log(max(comp_data),2))

        #decode using LZW
        decoded_data = self.decode_LZW(comp_data, size)
        decoded_data = decoded_data.astype(np.uint8)

        #shift of 8 bits and reshape to the format of the image
        decoded_data[:] -= 255
        image_data = np.reshape(decoded_data, (heigth, length)) 

        pt = PredictiveTransform()
        image_data = pt.decode(image_data, vertical)

        #save image
        imageio.imwrite(fileout, image_data)
        