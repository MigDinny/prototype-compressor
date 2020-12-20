
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
    def __init__(self):
        pass
    
    #lzw encode
    def encode_LZW(self,data):
        size = 16
        maximum_table_size = pow(2,int(size))
        dictionary_size = 512                   
        dictionary = {str(i): i for i in range(dictionary_size)}
        string = ""
        compressed_data = np.arange(0,dtype=np.uint16)
        
        for symbol in data:
            if (len(string)==0):
                string_plus_symbol = str(symbol)
            else:             
                string_plus_symbol = string + "#" + str(symbol)
    
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data = np.append(compressed_data, [*dictionary].index(string))
                if (len(dictionary) < maximum_table_size-1):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = str(symbol)
     
        if string in dictionary:
            compressed_data = np.append(compressed_data, [*dictionary].index(string))
        
        #print(max(compressed_array), len(compressed_array))
        compressed_data = np.append(compressed_data, maximum_table_size-1)
        #compressed_data = np.append(compressed_data, compressed_array)
        return compressed_data
    
    
    def encode(self, filein, fileout, chunkSize=50000, vertical=False):

        data =  mpimg.imread(filein)
        
        pt = PredictiveTransform()
        data = pt.encode(data, vertical)
        data[:] += 255
        
        strPoint = 0
        endPoint = chunkSize
        data1D = data.flatten()
        compressed_data = np.array([], dtype = np.uint16)

        compressed_data = np.append(compressed_data, np.array([data.shape[0], data.shape[1]], dtype = np.uint16))
        #count =0
        while (strPoint < len(data1D)):
            #print(count)
            comp = np.array(self.encode_LZW(data1D[strPoint:endPoint]))
            compressed_data = np.append(compressed_data, comp)
            strPoint = endPoint
            endPoint += chunkSize
            if(endPoint>len(data1D)):
                endPoint = len(data1D)
            #count += 1

        compressed_data = compressed_data.astype(np.uint16)
        np.save(fileout, compressed_data)
        return compressed_data

    def decode_LZW(self, data, size):
        maximum_table_size = pow(2,int(size))
        decoded_data = np.array([], dtype=np.int16)
        decoded_array = np.array([], dtype=np.int16)
        next_code = 512
        dictionary_size = 512
        string =  np.array([], dtype=np.int16)
        dictionary = [[] for x in range(maximum_table_size)]
    
        for i in range(dictionary_size):
            dictionary[i] = np.array([i])
        
        count = 0
        for code in data:
            if (len(decoded_array)>100000):
                decoded_data = np.append(decoded_data, decoded_array)
                decoded_array = np.array([], dtype=np.uint16)
            
            if (code == maximum_table_size-1):
                dictionary = [[] for x in range(maximum_table_size)]
                next_code = 512
                string =  np.array([], dtype=np.uint16)
                for i in range(dictionary_size):
                    dictionary[i] = np.array([i])
                count += 1
                
                decoded_data = np.append(decoded_data, decoded_array)
                decoded_array = np.array([], dtype=np.uint16)
            else:
                if (np.array_equal(dictionary[code],[])):
                    dictionary[code] = np.array(np.append(string, [string[0]]))
        
                decoded_array = np.append(decoded_array, dictionary[code])
                if (next_code < maximum_table_size -1 and len(string) > 0):
                    dictionary[next_code] = np.array(np.append(string, [dictionary[code][0]]))
                    next_code += 1
                string = dictionary[code]
        
        decoded_data = np.append(decoded_data, decoded_array)
        return decoded_data
    
    def decode(self, filein, fileout, vertical=False):
        comp_data =  np.load(filein)
        heigth = comp_data[0]
        length = comp_data[1]
        comp_data = comp_data[2:]

        size = round(math.log(max(comp_data),2))

        decoded_data = self.decode_LZW(comp_data, size)
        decoded_data = decoded_data.astype(np.uint8)
        decoded_data[:] -= 255
        image_data = np.reshape(decoded_data, (heigth, length)) 

        pt = PredictiveTransform()
        image_data = pt.decode(image_data, vertical)
        imageio.imwrite(fileout, image_data)
        
        return decoded_data

    