import sys
import re
import hashlib
import zlib
import re
import linecache
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

def updateRelNote(fileName, newImgVer, date, ImgChkSum_32, ImgChkSum_MD5, ImgEncChkSum_MD5):

    with open(fileName, 'r+') as file:
        lines = file.readlines()
        replaceTitleVer = '        MF5A AST2500(A2) BMC FW Release Version ' + newImgVer + '\n'
        replaceFWVer = 'Version: ' + newImgVer + '\n'
        replaceDate = 'Release Date: ' + date + '\n'
        replaceRomImachk32 = '1. rom.ima with checksum          : ' + ImgChkSum_32 + '\n'
        replaceRomImachkMD5 = '2. rom.ima with MD5 checksum      : ' + ImgChkSum_MD5 + '\n'
        replaceRomImaEncchkMD5 = '3. rom.ima_enc with MD5 checksum  : ' + ImgEncChkSum_MD5 + '\n'

        # Refer to file ReleaseNoteTemplate.txt to inset string.
        lines.insert(1, replaceTitleVer)
        lines.insert(3, replaceFWVer)
        lines.insert(4, replaceDate)
        lines.insert(9, '\n')
        lines.insert(12, '\n')
        lines.insert(14, replaceRomImachk32)
        lines.insert(15, replaceRomImachkMD5)
        lines.insert(16, replaceRomImaEncchkMD5)

        file.seek(0)

        file.writelines(lines)
