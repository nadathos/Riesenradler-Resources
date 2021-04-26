import os, sys, random, shutil, argparse
from pathlib import Path

"""
    usage:
        -sourcedir: Where to read lyrics from, must be txt
        -destdir: Where to write lyrics to, filename will be the same as source

    This script is for capitalizing lyrics (first letter in each line)
    // Riesenradler

"""

parser = argparse.ArgumentParser(description='Capitalize each line of song lyrics')
parser.add_argument('-sourcedir', metavar='Source', type=str,
                    help='a path to look for files')
parser.add_argument('-destdir', metavar='Destination', type=str,
                    help='a path to save chosen files')


args = parser.parse_args()

def capitalize(source):
    OutTxt = []
    try:
        with open(source, 'r') as file:
            for Line in file.readlines():
                Format = Line.strip()
                if len(Format) > 0:
                    Tmp = Format[0].upper() + Format[1:]
                    OutTxt.append(Tmp)
                else:
                    OutTxt.append("\n")
        return OutTxt
    except:
        print(f"Could not open file {source}")


if __name__ == '__main__':
    capitalized = capitalize(args.sourcedir)
    try:
        if os.path.isdir(args.destdir):
            with open(Path(args.destdir) / Path(args.sourcedir).name, 'w') as f:
                for item in capitalized:
                    f.write(f"{item}\n")
        else:
            print(f"The destination path {args.destdir + args.sourcedir.name} doesn|t exist!")
    except:
        print(f"Something went wrong while write to destination!")
