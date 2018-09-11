import os
import sys
import shutil
import zipfile
import re
import hashlib
import webbrowser
import zlib

from shutil import copyfile

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

# Get current path
CBOLD = '\33[1m'
CITALIC = '\33[3m'
CURL = '\33[4m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLINK = '\33[5m'
CBLINK2 = '\33[6m'

CEND = '\033[0m'

rootDir = os.getcwd()
pendingFolder = rootDir + '/pending/'
outputFolder = rootDir + '/output/'
bmcRomImgFolder = rootDir + '/bmcRomImg/'

bmcROMIma = 'rom.ima'
bmcROMImaEnc = 'rom.ima_enc'

print ("Getting current path: " + rootDir)
print ("pending folder path: " + pendingFolder)
print ("output folder path: " + outputFolder)
print(CEND + '\r\n')

#
# Go through all pending folders with .zip extension and list all of them for user's choice.
#
print('In the folder ' + pendingFolder + ', you have the following pending zip file:')
print('------------------------------------------------------------------------------------------------------------')
print(CBOLD + CYELLOW)
for root, dirs, files in os.walk(pendingFolder):
   # for name in files:
      print(files)

print(CEND + '\r\n')

# Choose a zip file that users want to update.
pendingZIPFile = input('Please enter the project neme that you would like to update:')
print('Your choise is: ' + pendingZIPFile)
waitForUpdate_Folder = outputFolder + pendingZIPFile + '/'
print('The folder that you want to release:')
print(waitForUpdate_Folder)

#
# Decompress the Release folder that users choose.
#
try:
    releaseFolderZip = zipfile.ZipFile(pendingFolder + pendingZIPFile + '.zip')

    # After decompressing, put the file to folder output.
    releaseFolderZip.extractall(outputFolder)

    releaseFolderZip.close()
    print('Decompression is finished. ' + '\r\n')
except:
    print(CRED + CBLINK + 'Error! Please check your pending again!' + CEND)

#
# Collect rom.ima information
#
# Search Firmware Version in BMC ROM image

# get rom.ima information
print('Get BMC firmware information from NEW ROM image...')
newRomImgInfo = getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMIma))
# print(newRomImgInfo)

# get rom.ima_enc information
# newRomImgEncInfo = getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMImaEnc))
print('\r\n')

print('Get BMC firmware information from OLD ROM image...')
oldRomImgInfo = getBMCFWInfo("%s%s" % (waitForUpdate_Folder, bmcROMIma))
# print(oldRomImgInfo)

# getBMCFWInfo(bmcROMImaEncPathName)

# Compare if firmware version is the same for NEW and OLD one
if newRomImgInfo == oldRomImgInfo:
    print('\r\n')
    print(CRED + 'Exit! The BMC firmware version on NEW and OLD birany are the same!' + CEND)
    print('New: ' + newRomImgInfo + '\r\n' + 'Old: ' + oldRomImgInfo)
    exit()

# copy new BMC ROM image to the folder that users want to compress with zip
src = bmcRomImgFolder
dest = waitForUpdate_Folder
print('\r\n')
try:
    print('Copy new ROM images to updated folder: ' + dest)
    shutil.copy(src + bmcROMIma, dest)
    shutil.copy(src + bmcROMImaEnc, dest)
except:
    print('Failed to copy!')

# Rename formal release folder
print(CGREEN)
print('The previous release folder: ' + pendingZIPFile )
print('New version of BMC firmware: ' + newRomImgInfo)
print(CEND)
formalReleaseFolderName = input('Please enter the name of the Formal Release Folder: (Project Name + Firmware Version)')
os.rename(outputFolder + pendingZIPFile, outputFolder + formalReleaseFolderName)

print(CEND + '\r\n')

# Calculate checksum-32 for rom.ima
RomimaChkSum32 = getChecksum32(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
print('rom.ima with checksum-32: ' + RomimaChkSum32)

# Calculate MD5 checksum for rom.ima and rom.ima_enc
RomimaMD5ChkSum = getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
RomimaEncMD5ChkSum = getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMImaEnc)
print('rom.ima with MD5 checksum: ' + RomimaMD5ChkSum)
print('rom.ima_enc with MD5 checksum: ' + RomimaEncMD5ChkSum)

# fill in related release information to ReleaseNote.ext

# Open text editor
webbrowser.open(outputFolder + formalReleaseFolderName + '/' + 'ReleaseNote.txt')

# Compress Formal Release Folder

# Calculate the MD5 checksum of the zip file.
