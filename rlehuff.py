"""

module:: RLEHuffmanCodec
    :synopsis: This codec encodes an image using Run-Length Encoding with Huffman Codes afterwards. This codec also makes a predictive transformation in order to decrease entropy.
moduleauthor:: Miguel Dinis <miguelbarroso@student.dei.uc.pt>
moduleauthor:: Edgar Duarte <edgarduarte@student.dei.uc.pt> (reviser)

Several libs are imported here:
    matplotlib
    numpy
    json
    imageio
    HuffmanCodec
    PredictiveTransform

RLE was coded by Miguel Dinis.
HuffmanCodec was coded by "soxofaan" as in https://github.com/soxofaan/dahuffman. His library is being used here, "HuffmanCodec".


"""

from huffmancodec import HuffmanCodec
import matplotlib.image as mpimg
import json
import numpy as np
from predictive import PredictiveTransform
import imageio

class RLEHuffmanCodec:
    """
    This codec makes a predictive transformation before encoding. RLE is used to encode and HuffmanCodes afterwards.

    Use only encode() and decode()
    """ 

    def __init__(self):
        """
        Codec constructor. Apparently empty :( 
        """
        pass


    def rle_encode(self, data):
        """
        Encodes a given data using RLE.

        Parameters:
            data (string): the data to be encoded

        Returns:
            string: RLE encoded data
        """

        encoded = ""
        lastChar = data[0]
        counter = 1
        datalen = len(data)

        for i in range(1, datalen):
            currentChar = data[i]

            if (currentChar == lastChar):
                counter += 1
                lastChar = currentChar
            else:
                if (counter >= 3):
                    encoded += str(counter) + "*" + str(lastChar) + "#"
                else:
                    encoded += (str(lastChar) + "#")*counter

                counter = 1
                lastChar = currentChar
        
            if (i == datalen - 1):
                if (data[i] != data[i-1]):
                    encoded += str(data[i])
                    return encoded

                if (data[i] == data[i-1] and data[i] != data[i-2]):
                    encoded += str(data[i]) + "#" + str(data[i])
                    return encoded
                
                encoded += str(counter) + "*" + str(lastChar)
                return encoded
    

    def rle_decode(self, code):
        """
        Decodes a given RLE encoded data.

        Parameters:
            code (string): RLE encoded data

        Returns:
            string: RLE decoded data
        """

        dec = []
        s = code.split("#")
        for symbol in s:
            if ("*" in symbol):
                k = symbol.split("*")
                q = int(k[0])
                p = k[1]
                for i in range(0, q):
                    dec.append(p)
            else:
                dec.append(symbol)
        return dec

    
    def huff_encode(self, data):
        """
        Encodes a given data using Huffman codes.

        Uses HuffmanCodec library.

        Parameters:
            data (string): data to be encoded

        Returns:
            string: encoded data
            array: table with the occurrences 

        """

        codec = HuffmanCodec.from_data(data, eof='EOF')
        enc = codec.encode(data)
        table = codec.get_code_table()

        return enc, table

   
    def huff_decode(self, code, table):
        """
        Decodes a given data and a given table of occurrences using Huffman codes.

        Uses HuffmanCodec library.    

        Parameters:
            code (string): data to be decoded
            table (array): table to be used to decode

        Returns:
            string: decoded data

        """

        codec = HuffmanCodec(table, eof = 'EOF')
        dec = codec.decode(code)

        return "".join(dec)

    
    def encode(self, filein, fileout, filetreeout, vertical=False):
        """
        Transforms using PredictiveTransform and encodes a given file and outputs it in another file.

        Vertical option, if chosen, calls the predictive transformer in Vertical mode, which will predict the values in a vertical order.

        Parameters: 
            filein (string): file to be encoded (.bmp format)
            fileout (string): file to be created as output (.rlehuff format)
            filetreeout (string): file to be created as a table resource (.json format)
            vertical (boolean): if True, calls Predictive in vertical mode. Default: False.

        """

        # read data from file
        data = mpimg.imread(filein)
        heigth, length = data.shape

        pt = PredictiveTransform()

        data = pt.encode(data, vertical)
        data = data.flatten()
        data = list(data)

        # encode RLE
        rle_enc = self.rle_encode(data)
        sp = rle_enc.split("#")

        # generate symbols for the huffman
        first = True
        hufflist = []
        for symbol in sp:
            if (first):
                first = False
            else:
                hufflist.append("#")

            if ("*" in symbol):
                temp = symbol.split("*")
                hufflist.append(temp[0])
                hufflist.append("*")
                hufflist.append(temp[1])
    
            else:
                hufflist.append(symbol) 
        
        # actual encoding
        huff_enc, huff_table = self.huff_encode(hufflist)
        
        # save encoding in file
        f = open(fileout, "wb")
        f.write(huff_enc)
        f.close()

        
        # save tree in a JSON file
        huff_table = { i : {"value1" : huff_table[i][0], "value2" : huff_table[i][1]} for i in huff_table}
        huff_table["size"] = {"length" : length, "heigth" : heigth}

        with open(filetreeout, "w") as fp:
            json.dump(huff_table,fp, indent=4)

    
    def decode(self, filein, fileout, filetreein, vertical=False):
        """
        Decodes a given file and outputs the decoded data into a .bmp (bitmap) file.

        Vertical option must be the same as used when encoding.

        Parameters:
            filein (string): file to be decoded (probably in .rlehuff format)
            fileout (string): file to be created and outputted (preferably .bmp format)
            filetreein (string): file to be used a resource for the huffman encoding (probably .json format)
            vertical (boolean): if True, calls predictive in Vertical mode. Default: False. 
        """

        # load tree
        data = {}

        with open(filetreein) as f:
            data = f.read()
    
        js = json.loads(data)

        length , height = js["size"]["length"], js["size"]["heigth"]
        js.pop("size")

        table = { i: (js[i]["value1"],js[i]["value2"]) for i in js}

        # load data from file
        f = open(filein, "rb")
        enc = f.read()
        f.close()

        # decode huffman first and then RLE
        huff_dec = self.huff_decode(enc, table)

        rle_dec = self.rle_decode(huff_dec)

        rle_dec = np.array(rle_dec)  
        
        rle_dec = rle_dec.reshape(height,length)
        rle_dec = rle_dec.astype("int16")       

        pt = PredictiveTransform()
        rle_dec = pt.decode(rle_dec, vertical)
        rle_dec = rle_dec.astype("uint8")

        imageio.imwrite(fileout,rle_dec)
        
