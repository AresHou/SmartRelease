import os
import shutil
import zipfile
import re
import hashlib

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
print('The folder that you want to update:')
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
newRomImgEncInfo = getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMImaEnc))
print('\r\n')

print('Get BMC firmware information from OLD ROM image...')
oldRomImgInfo = getBMCFWInfo("%s%s" % (waitForUpdate_Folder, bmcROMIma))
# print(oldRomImgInfo)

# getBMCFWInfo(bmcROMImaEncPathName)

# Compare if firmware version is the same for NEW and OLD one
if newRomImgInfo == oldRomImgInfo :
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

#with open(bmcRomImgFolder + bmcROMIma, "rb") as fwVer:
#    verSearch = re.search(bmcFWVersionPattern, fwVer.read())
#    fwVer.close()

#print("BMC Firmware Version:", verSearch .group())
#print("Offset:", verSearch .start())

# Search Firmware Date in BMC ROM image
#with open(bmcRomImgFolder + bmcROMIma, "rb") as fwDate:
#    dateSearch = re.search(bmcFWDatePattern, fwDate.read())
#    fwDate.close()

#print("BMC Firmware Date:", dateSearch .group())
#print('Offset: ' + hex(dateSearch .start()))
print(CEND + '\r\n')

# Calculate MD5 checksum of rom.aim

# Calculate the MD5 checksum of the zip file.
# filename = "my_data.txt"
# m = hashlib.md5()

# with open(pendingZIPFile, "rb") as f:
  # 分批讀取檔案內容，計算 MD5 雜湊值
  #for chunk in iter(lambda: f.read(4096), b""):
  #  m.update(chunk)

# h = m.hexdigest()
# print(h)