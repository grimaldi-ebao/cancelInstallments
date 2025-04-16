import os
import logging
import json
from datetime import datetime, time



def merge_files_from_folder(folder_path, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):  # Check if it is a file
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())  # Write file content to output file
                        outfile.write("\n")  # Add a newline after each file's content
        print(f"All files merged into '{output_file}' successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")




def logger():
    #format = "%(asctime)s: %(message)s"
    now = datetime.now()

    logging.basicConfig(
        filename='logfile{0}.log'.format(now.strftime("%Y%m%d_%H%M%S")),  # Name of the log file
        level=logging.DEBUG,  # Set the minimum logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        #datefmt="%H:%M:%S"
    )

def start():
    logger()
    merge_files_from_folder('out', 'output_total.txt')
    # println(content)
    #process(content)
    # run_in_threads(content)

if __name__ == '__main__':
    try:
        start()
    except:
        print("main error...")
    finally:
        print('Finish')