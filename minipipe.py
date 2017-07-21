'''
Author: Lina Tran
Date: July 14, 2017

Pipeline using motion correction and pre_cnmfe to motion correct, downsample,
and turn files into .tiffs

Requirements:

tiffcp
    install tiffcp using:
    $ apt-get install libtiff-tools

Command Line Usage:

$ python minipipe.py file1.mkv file2.mkv file3.mkv -d 4 -c 5000 --correct_motion
    -t 1.8 --target_frame 0

-d: downsample factor
-c chunk_size
--correct_motion if you want to motion correct_motion
-t if you want to indicate threshold
-target_frame if you want to choose a frame other than the first to reference
'''

from pre_cnmfe import process_chunks
import argparse
from os import system, path

def get_args():
    parser = argparse.ArgumentParser(description='Convert and downsample .mkv files to .tiff')
    parser.add_argument('input', help='files', nargs='+')
    parser.add_argument('-d', '--downsample', help='downsample factor, default is 4', type=int, default=4)
    parser.add_argument('-c', '--chunk_size', help='chunk_size of frames, default is 2000', type=int, default=2000)
    parser.add_argument('--motion_corr', dest='correct_motion', help='motion correct the given video', action='store_true')
    parser.add_argument('--no_motion_corr', dest='correct_motion', help='motion correct the given video', action='store_false')
    parser.set_defaults(correct_motion=True)
    parser.add_argument('-t', '--threshold', help='threshold for moco, default is 1.0', type=float, default=1.0)
    parser.add_argument('--target_frame', help='target frame to reference, default is 0', type=int, default=0)
    return parser.parse_args()


def main():
    args = get_args()
    for filename in args.input:
        directory = path.dirname(filename)
        print("Processing {}".format(filename))
        save_name = filename.replace('.mkv', '_proc')
        process_chunks(filename, args.chunk_size, args.downsample, args.correct_motion, args.threshold, 0.05, args.target_frame)
        system("tiffcp {}/*_temp_* {}.tiff".format(directory, save_name))
        system("rm {}/*_temp_*".format(directory))


if __name__ == '__main__':
    main()
