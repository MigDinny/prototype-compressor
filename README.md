This software is easy to use.

Steps:

    1 - Check if all modules are installed (pip command can be used). Check if all other dependent files are in the same directory (including data/ folder with the dataset).
        - numpy
        - matplotlib
        - imageio
        - json 
        - all others that might come up as necessary

        How to install? Run the following in an admin-elevated command line, for example: pip install numpy 
    
    2 - Change the main.py file as you want.
        There are 4 default dataset images. Each one has 2 methods of encoding (LZW and RLEHuff).
        You just need to uncomment the one you want to encode/decode.
        LZW encodings accept a chunk size value but there is a default value which, individually, have the best pre-calculated cost-benefit.

    2 - Run the main.py file. No args are accepted. All stuff must be handled in the main.py code.

        Example on the command line: python main.py

    3 - Enjoy the output. Check if any file was outputted and created (probably).


Any problem/question/suggestion?

Send an email to one of the following:

Miguel Dinis <miguelbarroso@student.dei.uc.pt>
Edgar Duarte <edgarduarte@student.dei.uc.pt>
Rodrigo Ferreira <rodrigoferreira@student.dei.uc.pt>
