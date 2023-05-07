#!/bin/bash

BREAD_LOC=bread.jpg
ENDPOINT=predict
PORT=8000
while getopts "b:e:p:" opt; do
    case $opt in
        b)
            BREAD_LOC="$OPTARG"
            echo "Using $BREAD_LOC as bread picture"
            ;;
        e)
            ENDPOINT="$OPTARG"
            echo "Hitting endpoint $ENDPOINT"
            ;;
        p)
            PORT="$OPTARG"
            echo "Hitting port $PORT"
            ;;
    esac
done

set -x
curl -X POST -F "image=@${BREAD_LOC}" http://localhost:${PORT}/${ENDPOINT}
