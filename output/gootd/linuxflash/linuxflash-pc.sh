#!/bin/sh
filename=`cat ../rom_enc.txt`
echo ""
echo BMC firmware image: $filename
./yafuflash2.sh -vyes -cd -fb -pipmi -pauth -pnet -psnmp -pssh -pkvm ../../$filename
