import os
import hashlib
import zlib
from tkinter import *
from tkinter.filedialog import askdirectory

def getBMCFWInfo(fwName):
    bmcFWVersionPattern = b'\x46\x57\x5f\x56\x45\x52\x53\x49\x4f\x4e'
    bmcFWDatePattern = b'\x46\x57\x5f\x44\x41\x54\x45'

    print('------------------------------------------------------------------')
    print(fwName)

    with open(fwName, "rb") as fwVer:
        verSearch = re.search(bmcFWVersionPattern, fwVer.read())
        fwVer.seek(int(verSearch.start()))
        firmwareVersion=fwVer.read(18)
        fwVer.close()
    print(str(firmwareVersion))

    with open(fwName, "rb") as fwDate:
        dateSearch = re.search(bmcFWDatePattern, fwDate.read())
        fwDate.seek(int(dateSearch.start()))
        firmwareDate = fwDate.read(19)
        fwDate.close()
    print(str(firmwareDate))
    return str(firmwareVersion)

def read_chunks(file_handle, chunk_size=8192):
    while True:
        data = file_handle.read(chunk_size)
        if not data:
            break
        yield data

def md5(file_handle):
    hasher = hashlib.md5()
    for chunk in read_chunks(file_handle):
        hasher.update(chunk)
    return hasher.hexdigest()

def getM5Checksum(fileName):
    try:
        with open(fileName, 'rb') as f:
            hash_string_Romima = md5(f)
    except IOError as e:
        print('ERROR! Get MD5 checksum has something wrong.')
    return hash_string_Romima

def getChecksum32(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def getFileAmount(PendingRootdir):

    fileNum = 0
    for lists in os.listdir(PendingRootdir):
        sub_path = os.path.join(PendingRootdir, lists)
        #print(sub_path)
        if os.path.isfile(sub_path):
            fileNum = fileNum+1

    #print(fileNum)
    return fileNum

def get_dirname():
    Tk().withdraw()
    print("Initializing Dialogue...\nPlease select a directory.")
    dirname = askdirectory(initialdir=os.getcwd(),title='Please select ROM images directory')
    if len(dirname) > 0:
        print ("You chose %s" % dirname)
        return dirname
    else:
        dirname = os.getcwd()
        print ("\nNo directory selected - initializing with %s \n" % os.getcwd())
        return dirname

#
# In ReleaseNote_pattern.txt, update related release information
#
def modRelNote(relNoteTempFile, newImgVer, reldate, ImgChkSum_32, ImgChkSum_MD5, ImgEncChkSum_MD5):
    lineNumber = 0
    titleVer = 'Version '
    contentVer = 'BMC Firmware Version: '
    contentDate = 'Release Date: '
    contentChksum32 = '1. rom.ima with checksum          : '
    contentChksumMD5 = '2. rom.ima with MD5 checksum      : '
    contentEncChksumMD5 = '3. rom.ima_enc with MD5 checksum  : '

    with open(relNoteTempFile, 'r+') as relPatternFile:
        for line in relPatternFile.readlines():
            lineNumber += 1

            titleVerIndex = line.find(titleVer) # lind.find will return index that was found. If cannot find the string, it will return -1.
            if titleVerIndex != -1:
                updatedLine = "".join((line[:titleVerIndex + len(titleVer)], newImgVer, line[(titleVerIndex + 15):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine)

            contentVerIndex = line.find(contentVer)
            if contentVerIndex != -1:
                updatedLine = "".join((line[:contentVerIndex + len(contentVer)], newImgVer, line[(contentVerIndex + 29):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine)

            contentDateIndex = line.find(contentDate)
            if contentDateIndex != -1:
                updatedLine = "".join((line[:contentDateIndex + len(contentDate)], reldate, line[(contentDateIndex + 24):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine)

            contentChksum32Index = line.find(contentChksum32)
            if contentChksum32Index != -1:
                updatedLine = "".join((line[:contentChksum32Index + len(contentChksum32)], ImgChkSum_32, line[(contentChksum32Index + 44):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine)

            contentChksumMD5Index = line.find(contentChksumMD5)
            if contentChksumMD5Index != -1:
                updatedLine = "".join((line[:contentChksumMD5Index + len(contentChksumMD5)], ImgChkSum_MD5, line[(contentChksumMD5Index + 68):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine)

            contentEncChksumMD5Index = line.find(contentEncChksumMD5)
            if contentEncChksumMD5Index != -1:
                updatedLine = "".join((line[:contentEncChksumMD5Index + len(contentEncChksumMD5)], ImgEncChkSum_MD5, line[(contentEncChksumMD5Index + 92):]))
                # print(lineNumber)
                # print(updatedLine)
                replaceLine(relNoteTempFile, lineNumber - 1, updatedLine + '\n')

def replaceLine(fileName, lineNum, text):
    lines = open(fileName, 'r').readlines()
    lines[lineNum] = text
    out = open(fileName, 'w')
    out.writelines(lines)
    out.close()
