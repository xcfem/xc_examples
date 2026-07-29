#!/bin/bash

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion1/motion1 --random-seed 42

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion2/motion2 --random-seed 25

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion3/motion3 --random-seed 10

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion4/motion4 --random-seed 2

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion5/motion5 --random-seed 50

python generate_spectrum_compatible_motion.py --target-csv target_horiz_spectrum.csv --out-prefix output/horiz_accel/motion6/motion6 --random-seed 39
