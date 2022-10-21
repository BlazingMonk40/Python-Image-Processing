import datetime
import os
import sys
from moviepy.editor import *


if(not os.path.exists("VideoMakerLogFiles")):
    os.mkdir("VideoMakerLogFiles")
if(os.path.exists("VideoMakerLogFiles")): 
    filename = "VideoMaker_ErrorLog.txt"
    filename = os.path.join("VideoMakerLogFiles", filename)
    error_log = open(str(filename), 'w')
else:
    print("Error! Log File could not be established.")
    sys.exit()

def IndexOf(substring, string):
        index = -1
        for i in range(0, len(string)):
            if(string[i] == substring):
                index = i+1
        return index

newFileName = "_Movie"

def printSpacer(symbol = "-", length = 10):
        """Prints a line of symbols."""
        rtn_string = ""
        for i in range(length):
            rtn_string += str(symbol)
        
        return rtn_string

def makeFileUpDir(dir):
        """Put new folder inside one directory up"""
        dir = os.path.normpath(dir)
        upDirPath = dir+newFileName
        if(not os.path.exists(upDirPath)):
            os.mkdir(upDirPath)
        return upDirPath

def printRuntime(start_time:datetime, end_time:datetime):
    print("\n--------------------\nProgram Start Time: ",start_time.replace(microsecond=0),"\n")
    print("Program End Time: ",end_time.replace(microsecond=0),"\n")
    print("Program Time to Complete: ",(end_time.replace(microsecond=0) - start_time.replace(microsecond=0)),"\n--------------------\n")
            

def VideoMaker():
    if(len(sys.argv) > 1):
        if(not os.path.exists(sys.argv[1])): 
            print("No such directory found!")
        else:
            try:
                startTime = datetime.datetime.now()
                newDirectory = makeFileUpDir(sys.argv[1])#Path to new folder for Resized Videos
                clips = []
                for dir, subdirs, files in os.walk(sys.argv[1]):
                    print("\nGathering files from '" + os.path.basename(dir) + "' please wait...")
                    for file in files:
                        clips.append(VideoFileClip(os.path.join(sys.argv[1], file)))
                        
                print("\nFiles gathered. Building movie...\n")
                movie = concatenate_videoclips(clips)
                
                newMoviePath = os.path.join(newDirectory, os.path.split(sys.argv[1])[1])
                movie.write_videofile(newMoviePath+".avi", codec = "libx264", preset="superfast")
                endTime = datetime.datetime.now()
                printRuntime(startTime, endTime)

                print("Moive made successfully!")
            except KeyboardInterrupt as e:
                print("\n A Keyboard Interrupt occured.")
                error_statement = (str(datetime.datetime.now().replace(microsecond=0)), "Keyboard Interrupt")
                sys.exit()
            except Exception as e:
                print("\nAn Error occurred on: ", file, "\n")
                error_statement = (str(datetime.datetime.now().replace(microsecond=0)), newMoviePath)
                error_log.write(printSpacer(length = 100)+"\n")
                error_log.write("Error occured during video processing: \n" + str(e).splitlines()[0])
                error_log.write("\n"+str(error_statement)+"\n")
                error_log.write(printSpacer(length = 100)+"\n")
                error_log.flush()
           

def main():
    VideoMaker()

if __name__ == "__main__":
    main()