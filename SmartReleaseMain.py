import os
import shutil
import zipfile

def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

# Get current path
CBOLD = '\33[1m'
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

print ("Getting current path: " + rootDir)
print ("pending folder path: " + pendingFolder)
print ("output folder path: " + outputFolder)

# Go through all pending folder with .zip extension and list all of them for user's choice.
print(CBOLD + 'In the folder ' + pendingFolder + ', you have the following pending zip file:')
print('---------------------------')
for root, dirs, files in os.walk(pendingFolder):
   for name in files:
      print(files)

print(CEND + '\r\n')
# Choose a zip file that users want to update.
pendingZIPFile = input('Please enter the project neme that you would like to update:')
print('Your choise is: ' + pendingZIPFile)

# Decompress the Release folder that users choose.
try:
    releaseFolderZip = zipfile.ZipFile(pendingFolder + pendingZIPFile + '.zip')

    # After decompressing, put the file to folder output.
    releaseFolderZip.extractall(outputFolder)

    releaseFolderZip.close()
except:
    print(CRED + CBLINK + 'Error! Please check your pending again!'+ CEND)

# Calculate ROM's CRC

# Calculate the CRC of the zip file.