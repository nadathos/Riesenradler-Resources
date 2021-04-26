import os, sys, random, shutil, argparse
from pathlib import Path

"""
    usage:
        -sourcedir: Where to sample files from
        -destdir: Where to copy sample to
        -amount: How many files to sample

    This script is used for randomly copying a set amount of files from a large sample library.
    The files are then put into a multisample for musical sampling.
    // Riesenradler

"""

parser = argparse.ArgumentParser(description='Choose random files from a parent directory and copy them into another.')
parser.add_argument('-sourcedir', metavar='Source', type=str,
                    help='a path to look for files')
parser.add_argument('-destdir', metavar='Destination', type=str,
                    help='a path to save chosen files')
parser.add_argument('-amount', metavar='Amount', type=int,
                    help='how large is the random sample')


args = parser.parse_args()

def get_random_files2(source, amount, exts=['wav', 'mp3', 'flac']):
    Samplefiles = []
    for ext in exts:
        file_list = list(Path(source).glob(f"**/*.{ext}"))
        if not len(file_list):
            print(f"No files matched that extension: {ext}")
            continue
        Samplefiles.extend(file_list)

    if len(Samplefiles):
        Samplesize = min(amount,len(Samplefiles))
        print(f"Found {Samplesize} files!")
        return random.sample(Samplefiles, amount)

    print(f"No files with extensions {exts} found!")


if __name__ == '__main__':
    files = get_random_files2(args.sourcedir, args.amount)
    try:
        if os.path.isdir(args.destdir):
            for f in files:
                Dest = Path(args.destdir) / f.name
                shutil.copy2(f, Dest, follow_symlinks = False)
        else:
            print(f"The destination path doesn|t exist!")
    except:
        print(f"Something went wrong while copying the files!")
