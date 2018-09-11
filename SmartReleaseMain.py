import os
import shutil
import zipfile
import webbrowser
import funModule

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

def main():
    # Setup related paths
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
    pendingZIPFile = input(CBLUE + 'Enter the folder name that you would like to update:' + CEND)
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
        exit()

    #
    # Collect rom.ima information
    #

    # Search Firmware Version in BMC ROM image
    # get rom.ima information
    print('Get BMC firmware information from NEW ROM image...')
    newRomImgInfo = funModule.getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMIma))
    # print(newRomImgInfo)

    # get rom.ima_enc information
    # newRomImgEncInfo = getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMImaEnc))
    print('\r\n')

    print('Get BMC firmware information from OLD ROM image...')
    oldRomImgInfo = funModule.getBMCFWInfo("%s%s" % (waitForUpdate_Folder, bmcROMIma))
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
    formalReleaseFolderName = input(CBLUE + 'Enter the name of the Formal Release Folder: (Project Name + Firmware Version)' + CEND)
    os.rename(outputFolder + pendingZIPFile, outputFolder + formalReleaseFolderName)

    print(CEND + '\r\n')

    # Calculate checksum-32 for rom.ima
    RomimaChkSum32 = funModule.getChecksum32(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    print('rom.ima with checksum-32: ' + RomimaChkSum32)

    # Calculate MD5 checksum for rom.ima and rom.ima_enc
    RomimaMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    RomimaEncMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMImaEnc)
    print('rom.ima with MD5 checksum: ' + RomimaMD5ChkSum)
    print('rom.ima_enc with MD5 checksum: ' + RomimaEncMD5ChkSum)

    # fill in related release information to ReleaseNote.ext

    # Open text editor
    webbrowser.open(outputFolder + formalReleaseFolderName + '/' + 'ReleaseNote.txt')

    # Compress Formal Release Folder

    # Calculate the MD5 checksum of the zip file.


if __name__ == '__main__':
    main()
