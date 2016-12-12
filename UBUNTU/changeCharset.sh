#!/bin/bash

while getopts "f:t:w:" arg; do
  case $arg in
    f)
      FROM=${OPTARG^^}
      ;;
    t)
      TO=${OPTARG^^}
      ;;
    w)
      TARGET="*.${OPTARG}"
      ;;
  esac
done

#FROM=US-ASCII
#TO=UTF-8
#TARGET="*.$1"

#echo "from: $FROM to: $TO TARGET: $TARGET"

ICONV="iconv -f $FROM -t $TO"
# Convert
find $(pwd)/ -type f -name $TARGET | while read fn; do
echo ${fn}
cp ${fn} ${fn}.bak
$ICONV < ${fn}.bak > ${fn}
rm ${fn}.bak
done
