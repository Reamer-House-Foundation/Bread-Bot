#!/bin/bash
# This script was created to simply save off the CLI which was used for initial training

TRAIN_DIR=data/train
OUTPUT_DIR=outputs
while getopts "t:o:" opt; do
    case $opt in
        t)
            TRAIN_DIR="$OPTARG"
            echo "Using $TRAIN_DIR as training dir"
            ;;
        o)
            OUTPUT_DIR="$OPTARG"
            echo "Using $OUTPUT_DIR as output dir"
            ;;

    esac
done

python3 run_image_classification.py --train_dir $TRAIN_DIR --output_dir $OUTPUT_DIR --remove_unused_columns False --do_train --do_eval
