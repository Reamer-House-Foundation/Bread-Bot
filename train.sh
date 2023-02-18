#!/bin/bash
# This script was created to simply save off the CLI which was used for initial training
python3 run_image_classification.py --train_dir data/ --output_dir ./outputs/ --remove_unused_columns False --do_train --do_eval
