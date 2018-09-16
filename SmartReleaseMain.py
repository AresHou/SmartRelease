import os
import shutil
import zipfile
import string
import funModule

from datetime import date
from subprocess import call

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

    smartReleaseVer = 'v0.1'
    maintainer = 'Wen-Hua Team'

    # Setup related paths
    rootDir = os.getcwd()
    pendingFolder = rootDir + '/pending/'
    outputFolder = rootDir + '/output/'
    bmcRomImgFolder = rootDir + '/bmcRomImg/'
    releaseNoteTemplateFolder = rootDir + '/releaseNoteTemplate/'
    EDITOR = os.environ.get('EDITOR', 'gedit')

    bmcROMIma = 'rom.ima'
    bmcROMImaEnc = 'rom.ima_enc'
    ReleaseNoteTemplate = 'ReleaseNoteTemplate.txt'
    tempReleaseFile = 'releaseNote_temp.txt'

    #
    # Show SmartRelease Information
    #
    print(CBOLD)
    print('==================================================================')
    print('SmartRelease Version: ' + smartReleaseVer)
    print('Maintainer: ' + maintainer)
    print('==================================================================')
    print(CEND)

    #
    # Show related paths
    #
    print ("Getting current path: " + rootDir)
    print ("pending folder path: " + pendingFolder)
    print ("output folder path: " + outputFolder)

    #
    # Check if folder output exists. If it does, remove output folder.
    #
    if os.path.isdir(outputFolder):
        shutil.rmtree(outputFolder)

    #
    # Delete the contents of a folder bmcRomImg.
    #
    print('Delete the contents of a folder bmcRomImg' + '\n')
    os.system('rm -rf %s/*' % bmcRomImgFolder)

    #
    # Check if folder pending is empty.
    #
    if len(os.listdir(pendingFolder)) == 0:
        print(CRED + 'ERROR! Folder \"pending\" is empty' + CEND)
        exit()

    #
    # Launch file browser to select BMC ROM images
    #
    bmcOutputDirName = funModule.get_dirname()
    # print(bmcOutputDirName)

    #
    # Copy BMC ROM images from AMI build to specific folder "bmcRomImg"
    #
    try:
        print('Copy BMC ROM images that you would like to release to ' + bmcRomImgFolder)
        shutil.copy(bmcOutputDirName + '/' + bmcROMIma, bmcRomImgFolder)
        shutil.copy(bmcOutputDirName + '/' + bmcROMImaEnc, bmcRomImgFolder)
        print('Copy done.')
    except:
        print(CRED + 'Failed to copy BMC ROM images!' + CEND)
        exit()

    fileAmount = funModule.getFileAmount(pendingFolder)
    # print('fileAmount:' + str(fileAmount))
    print('\n')

    if fileAmount == 1:
        print('The folder in pending:')
        for subdir, dirs, files in os.walk(pendingFolder):
            print(CYELLOW)
            print(files)
            print(CEND)

        # Convert list to string
        pendingZIPFile = ''.join(map(str, files))

        # get file name without extension name
        pendingZIPFile = os.path.splitext(pendingZIPFile)[0]
        #print(pendingZIPFile)
    else:
        #
        # Go through all pending folders with .zip extension and list all of them for user's choice.
        #
        print('In the folder ' + pendingFolder + ', you have the following pending zip file:')
        print(
            '------------------------------------------------------------------------------------------------------------')
        print(CBOLD + CYELLOW)
        for root, dirs, files in os.walk(pendingFolder):
            print(files)
        print(CEND)

        #
        # Choose a zip file that users want to update.
        #
        pendingZIPFile = input(CBLUE + 'Enter the folder name that you would like to update:' + CEND)

        extensionName = os.path.splitext(pendingZIPFile)[-1]
        # print('Extension Name: ' + extensionName)

        # Check if file name contains extenstion
        if extensionName == '.zip':
            # get file name without extension name
            pendingZIPFile = os.path.splitext(pendingZIPFile)[0]
            #print(pendingZIPFile)
            print('Your choice is: ' + CYELLOW + pendingZIPFile + CEND)

    waitForUpdate_Folder = outputFolder + pendingZIPFile + '/'

    print('The folder that you want to release:')
    print(waitForUpdate_Folder)
    print('\n')

    #
    # Decompress the Release folder that users choose to folder output.
    #
    try:
        releaseFolderZip = zipfile.ZipFile(pendingFolder + pendingZIPFile + '.zip')

        # After decompressing, put the file to folder output.
        releaseFolderZip.extractall(outputFolder)

        releaseFolderZip.close()
        # print('Decompression is finished. ' + '\n')
    except:
        print(CRED + CBLINK + 'Error! Please check your folder \"pending\" again!' + CEND)
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
        print(CRED + 'Exit! The BMC firmware version between new and previous binary are the same!' + CEND)
        print('New: ' + newRomImgVer + '\r\n' + 'Old: ' + oldRomImgVer)
        # Remove all of folders in output folder.
        shutil.rmtree(outputFolder)
        exit()

    #
    # copy new BMC ROM image to the folder that users want to compress with zip
    #
    src = bmcRomImgFolder
    dest = waitForUpdate_Folder
    print('\r\n')
    try:
        print('Copy new ROM images to the folder that you want to update: ' + dest)
        shutil.copy(src + bmcROMIma, dest)
        shutil.copy(src + bmcROMImaEnc, dest)
    except:
        print(CRED + 'Failed to copy!' + CEND)
        exit()

    #
    # Convert new Firmware Version to human readable.
    #
    try:
        romVerIndex = newRomImgVer.index('=')
        RomVerHumanReadable = newRomImgVer[romVerIndex + 1:-1]

        # Rename formal release folder
        verIndex = pendingZIPFile.index('v')
        prjName = pendingZIPFile[:verIndex + 1]
        prjName = prjName + '0'
        formalReleaseFolderName = prjName + RomVerHumanReadable

        for c in string.punctuation:
            formalReleaseFolderName = formalReleaseFolderName.replace(c, "")
        # print('The full release folder name will be: ' + formalReleaseFolderName)

        # formalReleaseFolderName = formalReleaseFolderName[0:-2]
        # print('The new release folder will be: ' + formalReleaseFolderName)

        os.rename(outputFolder + pendingZIPFile, outputFolder + formalReleaseFolderName)

        print(CBLUE)
        print('The previous release folder: ' + pendingFolder + pendingZIPFile)
        print('The formal release folder  : ' + outputFolder + formalReleaseFolderName)
        print('New version of BMC firmware: ' + RomVerHumanReadable)
        print(CEND)
    except:
        print(CRED)
        print('Firmware Version string in BMC ROM image is: ' + newRomImgVer)
        print("ERROR! Cannot find out character '=' in that string!")
        print(CEND)
        exit()

    print('Get checksum information...')

    #
    # Calculate checksum-32 for rom.ima
    #
    RomimaChkSum32 = funModule.getChecksum32(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    print(CBLUE + 'rom.ima with checksum-32     : ' + RomimaChkSum32)

    #
    # Calculate MD5 checksum for rom.ima and rom.ima_enc
    #
    RomimaMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMIma)
    RomimaEncMD5ChkSum = funModule.getM5Checksum(outputFolder + formalReleaseFolderName + '/' + bmcROMImaEnc)
    print('rom.ima with MD5 checksum    : ' + RomimaMD5ChkSum)
    print('rom.ima_enc with MD5 checksum: ' + RomimaEncMD5ChkSum)
    print(CEND)

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
    result = funModule.updateRelNote(relNoteFileName, RomVerHumanReadable, today, RomimaChkSum32, RomimaMD5ChkSum, RomimaEncMD5ChkSum)
    if result == 0:
        print(CRED + 'Exit! Search and replace Release Note has something wrong!' + CEND)
        exit()

    FormalReleaseNote = outputFolder + formalReleaseFolderName + '/' + 'ReleaseNote.txt'

    formalRelFile = open(FormalReleaseNote)
    tempRelFile = open(relNoteFileName, 'a+')

    shutil.copyfileobj(formalRelFile, tempRelFile)

    tempRelFile.close()
    formalRelFile.close()

    formalRelFolderPath = outputFolder + formalReleaseFolderName

    os.rename(releaseNoteTemplateFolder + tempReleaseFile, releaseNoteTemplateFolder + 'ReleaseNote.txt')
    shutil.copy2(releaseNoteTemplateFolder + 'ReleaseNote.txt', formalRelFolderPath)

    print('Editor popup... Please fill in and save related information to ReleaseNote.txt.')
    print('After that. the formael release folder with extension .zip will be placed to the following path:' + '\r\n' + formalRelFolderPath)

    # Open text editor
    call([EDITOR, outputFolder + formalReleaseFolderName + '/' + 'ReleaseNote.txt'])

    #
    # Compress Formal Release Folder
    #
    print('Compress the release folder ' + '\"' + formalReleaseFolderName + '\"' + ' ...' +'\n')
    shutil.make_archive(formalRelFolderPath, 'zip', formalRelFolderPath)
    print(CGREEN + 'Complete! Please go to path ' + outputFolder + ' and get folder \"' + formalReleaseFolderName + '.zip' + '\"' + CEND)


if __name__ == '__main__':
    main()
