
import os
import sys
import datetime
import shutil

from PIL import Image
from moviepy.editor import *

media_path = "M:\\Trailcam"
pi = True

if(not os.path.exists("BatchResizeLogFiles")):
    os.mkdir("BatchResizeLogFiles")
if(os.path.exists("BatchResizeLogFiles")): 
    filename = "BatchResize_ErrorLog "+str(datetime.datetime.now().replace(microsecond=0))+".txt"
    filename = filename.replace(":", ",")
    filename = os.path.join("BatchResizeLogFiles", filename)
    error_log = open(str(filename), 'w')
else:
    print("Error Log File could not be established.")
    sys.exit()

newFileName = "_ResizedVideos"
def printSpacer(symbol = "-", length = 10):
        """Prints a line of symbols."""
        rtn_string = ""
        for i in range(length):
            rtn_string += str(symbol)
        
        return rtn_string

def IndexOf(substring, string):
    index = -1
    for i in range(0, len(string)):
        if(string[i] == substring):
            index = i+1
    return index

def makeFileUpDir(dir):
    """Put new folder inside one directory up"""
    dir = os.path.normpath(dir)
    upDirPath = dir+newFileName
    if(not os.path.exists(upDirPath)):
        os.mkdir(upDirPath)
    return upDirPath

def Process(media_path):
    media_path = os.path.normpath(media_path)
    if(not os.path.exists(media_path)): print("No such directory found!")
    else:
        startTime = datetime.datetime.now()
        newDirectory = makeFileUpDir(media_path)#Path to new folder for Resized Videos
        
        old_dir = ""
        count = 0
        for dir, subdirs, files in os.walk(media_path):
            
                #C:\Users\popta\Desktop\100Media\100Media_Resized
                if(dir == os.path.normpath(media_path)): continue #Don't repeat the root directory
                dir = os.path.normpath(dir)
                old_dir_basename = os.path.basename(old_dir)
                dir_split0 = os.path.basename(os.path.split(dir)[0])
                if(not old_dir == "" and not old_dir_basename == dir_split0):
                    newDirectory = os.path.join(os.path.split(newDirectory)[0], os.path.basename(dir))
                else:
                    old_dir = dir
                    dir_name = os.path.basename(dir)
                    newDirectory = os.path.join(newDirectory, dir_name)
                if(not os.path.exists(newDirectory)):
                    os.mkdir(newDirectory)
                for file in files:
                    try:
                        ext = os.path.splitext(file)[-1].lower()
                        #Check for correct file extension and that the file has not already been resized
                        if(ext == ".avi" or ext == ".mp4"):
                            print(dir + "/" + file)
                            if("__" in file): 
                                count += 1 
                                continue
                            if(newFileName in file): continue
                            videoName = file                       #Get video name
                            videoPath = os.path.join(dir,videoName)          #Get video path
                            video = VideoFileClip(videoPath)       #Get video at video path
                            
                            print("\n Already processed: ",count,"\n")             
                            
                            newVideoPath = os.path.join(newDirectory,videoName)       #Make new file path for the resized video
                            
                            fileStartTime = datetime.datetime.now()
                            
                            resizedVideo = video.resize(.75)       #Resize video
                            #Codecs: libx264, mpeg4, rawvideo, png libvorbis, libvpx || || libx264, mpeg4 
                            resizedVideo.write_videofile(newVideoPath, codec='libx264', threads = 10)     #Save video to new file path
                            completedResizeVideoPath = os.path.join(dir,"__"+videoName)
                            os.rename(videoPath, completedResizeVideoPath)
                            fileEndTime = datetime.datetime.now()
                            print("--------------------\n"+videoName+" Compression Start Time: ",fileStartTime.replace(microsecond=0),"\n")
                            print(videoName+" Compression End Time: ",fileEndTime.replace(microsecond=0))
                            print("\n"+videoName+" Compression Time to Complete: ",(fileEndTime.replace(microsecond=0) - fileStartTime.replace(microsecond=0)),"\n--------------------\n")
                            #printFileDone()
                        else:
                            print('Wrong file type for file:', file)
                    except KeyboardInterrupt as e:
                        print("\n A Keyboard Interrupt occured.")
                        error_statement = (str(datetime.datetime.now().replace(microsecond=0)), "Keyboard Interrupt")
                        sys.exit()
                    except Exception as e:
                        print("\nAn Error occurred on: ", file, "\n")
                        error_statement = (str(datetime.datetime.now().replace(microsecond=0)), videoPath)
                        error_log.write(printSpacer(length = 100)+"\n")
                        error_log.write("Error occured during video processing: \n" + str(e).splitlines()[0])
                        error_log.write("\n"+str(error_statement)+"\n")
                        error_log.write(printSpacer(length = 100)+"\n")
                        error_log.flush()
                        #continue
        
        endTime = datetime.datetime.now()
        #os.rename(dir, dir+"_ResizingComplete")
        print("\n--------------------\nProgram Start Time: "+str(startTime)+"\n")
        print("Program End Time: ",endTime.replace(microsecond=0),"\n")
        print("Program Time to Complete: ",(endTime.replace(microsecond=0) - startTime.replace(microsecond=0)),"\n--------------------\n")


def VideoProcessing():
    
    if(len(sys.argv) > 1):
        Process(sys.argv[1])
    elif(os.path.exists(media_path)):
        Process(media_path)
    else:
        print("Args not found")
            



    
def ImageProcessing():
    newFileName = "_ResizedImages"
    
    def LastIndexOf(substring, string):
        """Returns the index of the last occurence of a substring"""
        index = -1
        for i in range(0, len(string)):
            if(string[i] == substring):
                index = i+1
        return index

    def makeFileSameDir():
        """Put new folder inside picture folder"""
        newFolderPath = sys.argv[1]+"\\"+newFileName
        if (not os.path.exists(newFolderPath)):
            os.mkdir(newFolderPath)
        return newFolderPath
    def makeFileUpDir():
        """Put new folder inside one directory up"""
        upDirIndex = LastIndexOf("/", sys.argv[1])
        if(upDirIndex == -1):
            upDirIndex = LastIndexOf("\\", sys.argv[1])
        fileName = sys.argv[1][upDirIndex:]
        upDir = sys.argv[1][0:upDirIndex]+fileName
        upDirPath = upDir+newFileName
        if(not os.path.exists(upDirPath)):
            os.mkdir(upDirPath)
        #print("path:", upDirPath)
        return upDirPath


    def getPercentChange(v1, v2):
        """
        Note: Order of params matters - 
        Larger, Smaller = %Decrease | 
        Smaller, Larger = %Increase
        """
        change = ((v2-v1)/v1)*100
        return abs(change)

    def printFileProcessing():
        print("Processing: ", "File name: ",imageName, "Image Resolution: ",
                        image.size, "File Size: ",os.path.getsize(imagePath)," bytes")
    def printFileDone():
        print("Done: ", "File name: ",imageName, "Image Resolution: ",resizedImage.size, "File Size: ",
                        os.path.getsize(newImagePath)," bytes", "Compression: ", 
                        str(getPercentChange(os.path.getsize(imagePath), os.path.getsize(newImagePath)))[0:6]+"%")

    def getFolderSize(folderPath):
        """
        @param folderPath: Path to folder
        """
        rawSizeBytes = 0
        for ele in os.scandir(folderPath):
            rawSizeBytes+=os.path.getsize(ele)
        
        sizeUnit = byteConversion(rawSizeBytes)

        return ("Folder: "+folderPath+"\nSize: "+str(sizeUnit[0])[0:5]+sizeUnit[1], sizeUnit)


    def byteConversion(bytes):
        kilobyte = 1024
        megabyte = 1024 * kilobyte #1,048,576
        gigabyte = 1024 * megabyte #1,073,741,824
        terabyte = 1024 * gigabyte #1,099,511,627,776
        unit = ""
        if(bytes/terabyte > 1):
            bytes /= terabyte
            unit = "TB"
        elif(bytes/gigabyte > 1):
            bytes /= gigabyte
            unit = "GB"
        elif(bytes/megabyte > 1):
            bytes /= megabyte
            unit = "MB"
        elif(bytes/kilobyte > 1):
            bytes /= kilobyte
            unit = "KB"
        else:
            bytes = bytes
            unit = "Bytes"
        return bytes, unit

    #Get sorted list of directories from folder given in argv[1]
    if(len(sys.argv) > 1):
        file_list = [x for x in sorted([x for x in os.listdir(sys.argv[1])])]
        #C:\Users\popta\Desktop\100Media\100Media_Resized
        newDirectory = makeFileUpDir()                              #Path to new folder for Resized Images
        for i in range (0, len(file_list)):
            if(str(file_list[i])[-4:0] == ".JPG" or ".PNG"):
                if(not newFileName in file_list[i]):
                    imageName = file_list[i]                        #Get image name
                    imagePath = sys.argv[1]+"\\"+imageName          #Get image path
                    image = Image.open(imagePath)                   #Get image at image path
                    
                    newImagePath = newDirectory+"/"+imageName  #Make new file path for the resized image
                    
                    printFileProcessing()
                    
                    resizedImage = image.resize((960,540))        #Resize Image
                    resizedImage.save(newImagePath, "JPEG")         #Save image to new file path
                    
                    printFileDone()
            else:
                print('Wrong file type for file:', file_list[i])
        
        print(getFolderSize(sys.argv[1])[0])
        print(getFolderSize(newDirectory)[0] + " Compression:", str(getPercentChange(getFolderSize(sys.argv[1])[1][0], getFolderSize(newDirectory)[1][0]))[0:5],"%")
                    
    else:
        print("Error! No files recieved.")

def main():
    try:
        if(len(sys.argv) > 2):
            type = sys.argv[2]
        else:
            if(not pi):
                type = input("For Image Processing Enter '0':\nFor Video Processing Enter '1':\nInput: ")
                if type == '0':
                    ImageProcessing()
                elif type == '1':
                    print(media_path)
                    VideoProcessing()
            else:
                VideoProcessing()
    except SystemExit as sys_exit:
        print("System Error.")
        error_log.write(printSpacer('*', 50))
        error_log.write("\nSystem exited at: " + str(datetime.datetime.now().replace(microsecond=0))+"\n"+str(sys_exit))
        error_log.write(printSpacer("*", 50))
        error_log.close()
        sys.exit()

    finally:
        return 0

if __name__ == "__main__":
    main()