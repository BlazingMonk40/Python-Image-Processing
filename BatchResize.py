from dis import Bytecode
import os
import sys

from PIL import Image

newFileName = "_ResizedImages"

def IndexOf(substring, string):
    index = -1
    for i in range(0, len(string)):
        if(string[i] == substring):
            index = i+1
    return index

def makeFileSameDir():
    #Put new folder inside picture folder
    newFolderPath = sys.argv[1]+"\\"+newFileName
    if (not os.path.exists(newFolderPath)):
        os.mkdir(newFolderPath)
    return newFolderPath
def makeFileUpDir():
    #Put new folder inside one directory up
    upDirIndex = IndexOf("/", sys.argv[1])
    if(upDirIndex == -1):
        upDirIndex = IndexOf("\\", sys.argv[1])
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
    newDirectory = makeFileUpDir()                            #Path to new folder for Resized Images
    for i in range (0, len(file_list)):
            if(not newFileName in file_list[i]):
                imageName = file_list[i]                        #Get image name
                imagePath = sys.argv[1]+"\\"+imageName          #Get image path
                image = Image.open(imagePath)                   #Get image at image path
                
                newImagePath = newDirectory+"/"+imageName  #Make new file path for the resized image
                
                printFileProcessing()
                
                resizedImage = image.resize((1920,1080))        #Resize Image
                resizedImage.save(newImagePath, "JPEG")         #Save image to new file path
                
                printFileDone()
    
    print(getFolderSize(sys.argv[1])[0])
    print(getFolderSize(newDirectory)[0] + " Compression:", str(getPercentChange(getFolderSize(sys.argv[1])[1][0], getFolderSize(newDirectory)[1][0]))[0:5],"%")
                
else:
    print("Error! No files recieved.")
