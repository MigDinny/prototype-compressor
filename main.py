"""

module:: Main File - RLE+HUFFMAN and LZW compressors
    :synopsis: Here it's called each codec.
moduleauthor:: Miguel Dinis <miguelbarroso@student.dei.uc.pt>


Both libs are imported as well as the Time library so we can measure how long each algorithm takes.

Just select the right image to encode/decode and uncomment it.

Notes: 
    RLEHuffmanCodec needs to store a tree in a separate JSON file.

    LZWCodec accepts a chunk size as parameter but it has a default value.

    Both accept a "vertical" parameter which, when transforming (predictive), does it in a horizontal or vertical direction. Default is horizontal.
    When decoding, the option must be the same as when encoded.

More information on how to run this in the README file and in the Article.

"""


from rlehuff import RLEHuffmanCodec
from lzw import LZWCodec
import time


if __name__ == '__main__':

    # Both algorithm instances.

    codecRLEHUFF = RLEHuffmanCodec()
    codecLZW     = LZWCodec()


    # EGG - RLE + HUFF

    """

    t1 = time.time()
    codecRLEHUFF.encode("data/original/egg.bmp", "data/egg.rlehuff", "data/egg-RLEHUFF.json")
    print("Encoder time elapsed: ", time.time() - t1)
    
    t1 = time.time() 
    codecRLEHUFF.decode("data/egg.rlehuff", "data/egg-RLEHUFF-DECODED.bmp", "data/egg-RLEHUFF.json")
    print("Decoder time elapsed: ", time.time() - t1)
    
    """

    # EGG - LZW

    """

    t1 = time.time()
    codecLZW.encode("data/original/egg.bmp", "data/egg.lzw", 100000)
    print("Encoder time elapsed: ", time.time() - t1)

    t1 = time.time()
    codecLZW.decode("data/egg.lzw.npy", "data/egg-LZW-DECODED.bmp")
    print("Decoder time elapsed: ", time.time() - t1)

    """

    # PATTERN - RLE + HUFF

    """

    t1 = time.time()
    codecRLEHUFF.encode("data/original/pattern.bmp", "data/pattern.rlehuff", "data/pattern-RLEHUFF.json")
    print("Encoder time elapsed: ", time.time() - t1)
    
    t1 = time.time() 
    codecRLEHUFF.decode("data/pattern.rlehuff", "data/pattern-RLEHUFF-DECODED.bmp", "data/pattern-RLEHUFF.json")
    print("Decoder time elapsed: ", time.time() - t1)
    
    """

    # PATTERN - LZW

    """

    t1 = time.time()
    codecLZW.encode("data/original/pattern.bmp", "data/pattern.lzw", 250000)
    print("Encoder time elapsed: ", time.time() - t1)

    t1 = time.time()
    codecLZW.decode("data/egg.pattern.npy", "data/pattern-LZW-DECODED.bmp")
    print("Decoder time elapsed: ", time.time() - t1)

    """

    # ZEBRA - RLE + HUFF

    """

    t1 = time.time()
    codecRLEHUFF.encode("data/original/zebra.bmp", "data/zebra.rlehuff", "data/zebra-RLEHUFF.json", vertical=True)
    print("Encoder time elapsed: ", time.time() - t1)
    
    t1 = time.time() 
    codecRLEHUFF.decode("data/zebra.rlehuff", "data/zebra-RLEHUFF-DECODED.bmp", "data/zebra-RLEHUFF.json", vertical=True)
    print("Decoder time elapsed: ", time.time() - t1)
    
    """

    # ZEBRA - LZW

    """

    t1 = time.time()
    codecLZW.encode("data/original/zebra.bmp", "data/zebra.lzw", vertical=True)
    print("Encoder time elapsed: ", time.time() - t1)

    t1 = time.time()
    codecLZW.decode("data/zebra.lzw.npy", "data/zebra-LZW-DECODED.bmp", vertical=True)
    print("Decoder time elapsed: ", time.time() - t1)

    """

    # LANDSCAPE - RLE + HUFF

    """

    t1 = time.time()
    codecRLEHUFF.encode("data/original/landscape.bmp", "data/landscape.rlehuff", "data/landscape-RLEHUFF.json", vertical=True)
    print("Encoder time elapsed: ", time.time() - t1)
    
    t1 = time.time() 
    codecRLEHUFF.decode("data/landscape.rlehuff", "data/landscape-RLEHUFF-DECODED.bmp", "data/landscape-RLEHUFF.json", vertical=True)
    print("Decoder time elapsed: ", time.time() - t1)
    
    """

    # LANDSCAPE - LZW

    """

    t1 = time.time()
    codecLZW.encode("data/original/landscape.bmp", "data/landscape.lzw", 100000, vertical=True)
    print("Encoder time elapsed: ", time.time() - t1)

    t1 = time.time()
    codecLZW.decode("data/landscape.lzw.npy", "data/landscape-LZW-DECODED.bmp", vertical=True)
    print("Decoder time elapsed: ", time.time() - t1)

    """