import os, glob, pathlib, argparse
import subprocess
import math

Usage = """
        videosplit.py -sourcedir SOURCE -destdir DEST -length INSECONDS

        Will take all videos from SOURCE and cut them into chunks of desired length. Will save these chunks into DEST.
        Needs FFMPEG and FFPROBE to function.

        // Riesenradler

        """
parser = argparse.ArgumentParser(description='Take long mp4 video files from directory, cut them into chunks of specified length and put them into another directory')
parser.add_argument('-sourcedir', metavar='Source', type=str,
                    help='a path to look for files')
parser.add_argument('-destdir', metavar='Destination', type=str,
                    help='a path to save chosen files')
parser.add_argument('-length', metavar='ChunkLength', type=int,
                    help='length in second of the chunks')

args = parser.parse_args()

FFMPEG = pathlib.Path(".\\tools\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe")
FFPROBE = pathlib.Path(".\\tools\\ffmpeg-4.4-full_build\\bin\\ffprobe.exe")


if __name__ == '__main__':
    Error = "None"
    try:
        if os.path.isdir(args.sourcedir):
            for filepath in glob.iglob(args.sourcedir + "/*.mp4"):
                SourceFile = pathlib.Path(filepath)
                FileName = SourceFile.name
                DestFileBase = pathlib.Path(args.destdir) / FileName

                FileLength = -1

                try:
                    FileLengthGetter = subprocess.run([str(FFPROBE), "-v", "error", "-show_entries", "format=duration"
                    ,                        "-of", "default=noprint_wrappers=1:nokey=1", str(SourceFile) ],
                                                        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                    FileLength, Error = float(FileLengthGetter.stdout), FileLengthGetter.stderr

                except:
                    print("FFPROBE error, could not retreive video length!")


                Chunks = math.ceil(FileLength / args.length)
                try:
                    for I in range(Chunks):
                        StartSec = I*args.length
                        EndSec = min((I+1)*args.length, FileLength)
                        DestFile = DestFileBase.parent / (DestFileBase.stem + f"_{I}" + DestFileBase.suffix)

                        print(f'Current Start {StartSec}, end {EndSec}, difference {EndSec-StartSec}\nFilelength {FileLength}')

                        if os.path.isfile(DestFile):
                            os.remove(DestFile)

                        Process = subprocess.run([str(FFMPEG), "-i", str(SourceFile), "-ss", str(StartSec), "-t", str(EndSec), "-c", "copy", str(DestFile)],
                                                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                        StdOut, Error = Process.stdout, Process.stderr
                except:
                    print(f"FFMPEG error, could not cut file into chunks {Error}")
        else:
            print(f"Invalid Sourcepath {args.sourcedir}")
    except:
        print(f"Something went wrong splitting. Error: {Error}\nUsage: {Usage}")
