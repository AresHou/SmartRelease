import os
import shutil
import zipfile
import webbrowser
import funModule

from datetime import date

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
    releaseNoteTemplateFolder = rootDir + '/releaseNoteTemplate/'

    bmcROMIma = 'rom.ima'
    bmcROMImaEnc = 'rom.ima_enc'
    ReleaseNoteTemplate = 'ReleaseNoteTemplate.txt'
    tempReleaseFile = 'releaseNote_temp.txt'

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

    #
    # Choose a zip file that users want to update.
    #
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

    # Search Firmware Version in BMC ROM image and get rom.ima information
    print('Get BMC firmware information from NEW ROM image...')
    newRomImgVer = funModule.getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMIma))
    # print(newRomImgVer)

    # get rom.ima_enc information
    # newRomImgEncVer = getBMCFWInfo("%s%s" % (bmcRomImgFolder, bmcROMImaEnc))
    print('\r\n')

    print('Get BMC firmware information from OLD ROM image...')
    oldRomImgVer = funModule.getBMCFWInfo("%s%s" % (waitForUpdate_Folder, bmcROMIma))
    # print(oldRomImgVer)

    # getBMCFWInfo(bmcROMImaEncPathName)

    #
    # Compare if firmware version is the same for NEW and OLD one
    #
    if newRomImgVer == oldRomImgVer:
        print('\r\n')
        print(CRED + 'Exit! The BMC firmware version on NEW and OLD birany are the same!' + CEND)
        print('New: ' + newRomImgVer + '\r\n' + 'Old: ' + oldRomImgVer)
        exit()

    #
    # copy new BMC ROM image to the folder that users want to compress with zip
    #
    src = bmcRomImgFolder
    dest = waitForUpdate_Folder
    print('\r\n')
    try:
        print('Copy new ROM images to updated folder: ' + dest)
        shutil.copy(src + bmcROMIma, dest)
        shutil.copy(src + bmcROMImaEnc, dest)
    except:
        print('Failed to copy!')
        exit()

    #
    # Rename formal release folder
    #
    formalReleaseFolderName = input(CBLUE + 'Enter the name of the Formal Release Folder: (Project Name + Firmware Version)' + CEND)
    os.rename(outputFolder + pendingZIPFile, outputFolder + formalReleaseFolderName)

    print(CGREEN)
    print('The previous release folder: ' + pendingFolder + pendingZIPFile)
    print('The current release folder: ' + formalReleaseFolderName)
    print('New version of BMC firmware: ' + newRomImgVer)
    print(CEND)
    print(CEND + '\r\n')

    #
    # Calculate checksum-32 for rom.ima
    #
    RomimaChkSum32 = funModule.getChecksum32(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    print('rom.ima with checksum-32: ' + RomimaChkSum32)

    #
    # Calculate MD5 checksum for rom.ima and rom.ima_enc
    #
    RomimaMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    RomimaEncMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMImaEnc)
    print('rom.ima with MD5 checksum: ' + RomimaMD5ChkSum)
    print('rom.ima_enc with MD5 checksum: ' + RomimaEncMD5ChkSum)

    #
    # fill in related release information to ReleaseNote.ext
    #
    src_relNote = releaseNoteTemplateFolder
    dest_relNote = releaseNoteTemplateFolder
    shutil.copy(src_relNote + ReleaseNoteTemplate, dest_relNote + tempReleaseFile)

    # Get date
    today = str(date.today())
    # print('Today is : ' today)

    relNoteFileName = releaseNoteTemplateFolder + tempReleaseFile
    # Search and replace related information
    result = funModule.updateRelNote(relNoteFileName, newRomImgVer, today, RomimaChkSum32, RomimaMD5ChkSum, RomimaEncMD5ChkSum)
    if result == 0:
        print(CRED + 'Exit! Search and replace Release Note has something wrong!' + CEND)
        exit()

    # Open text editor
    # webbrowser.open(outputFolder + formalReleaseFolderName + '/' + 'ReleaseNote.txt')

    #
    # Compress Formal Release Folder
    #

if __name__ == '__main__':
    main()