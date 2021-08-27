import argparse
import glob
import os
import random
import shutil

import numpy as np

from utils import get_module_logger


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /mnt/data
    """
    # Get data from file
    try:
        files = [filename for filename in glob.glob(f'{data_dir}/*.tfrecord')]
    except Exception as error:
        print('Access files is not possible!')
    
    # Shuffle files
    np.random.shuffle(files)
    
    # Split files in: Train, validation and test
    files_train, files_val, files_test = np.split(files, [int(.75*len(files)), int(.9*len(files))])
    
    # Test size of split files               
    assert len(files) == len(files_train) + len(files_val) + len(files_test)
    
    # create directories and move the files
    train = os.path.join(data_dir, 'train')
    val = os.path.join(data_dir, 'val')
    test = os.path.join(data_dir, 'test')
    
    # Check if directory exist, otherwise create it
    # font: https://www.geeksforgeeks.org/python-os-makedirs-method/
    try:
        if not os.path.exists(train):
            os.makedirs(train)
            print("Directory '%s' created" %train)
    except:
        os.makedirs(train, exist_ok = True)
        print("Directory '%s' exists" %train)
        
    # Move the train files to folder {data_dir}/train
    # font: https://docs.python.org/3/library/shutil.html
    for file in files_train:
        shutil.move(file, train)
        
    try:
        if not os.path.exists(val):
            os.makedirs(val)
            print("Directory '%s' created" %val)
    except:
        os.makedirs(train, exist_ok = True)
        print("Directory '%s' exists" %val)
        
    # Move the validation files to folder {data_dir}/val
    for file in files_val:
        shutil.move(file, val)
        
        
    try:
        if not os.path.exists(test):
            os.makedirs(test)
            print("Directory '%s' created" %test)
    except:
        os.makedirs(train, exist_ok = True)
        print("Directory '%s' exists" %test)
    
    # Move the test files to folder {data_dir}/test
    for file in files_val:
        shutil.move(file, test)
    

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True,
                        help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)