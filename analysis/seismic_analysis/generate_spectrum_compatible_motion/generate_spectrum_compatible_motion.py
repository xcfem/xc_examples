#!/usr/bin/env python3
"""
generate_spectrum_compatible_motion.py

Command-line driver for generating a synthetic ground-motion acceleration
time history that is spectrum-compatible with a user-supplied target
response spectrum.

USAGE
-----
    # Use a built-in example target spectrum (e.g. ASCE 7 design spectrum
    # shape) and a synthetically generated seed motion:
    python generate_spectrum_compatible_motion.py --demo

    # Use your own target spectrum from a 2-column CSV file (period[s], Sa[g]):
    python generate_spectrum_compatible_motion.py \
        --target-csv my_target_spectrum.csv \
        --duration 20 --dt 0.005 --damping 0.05 \
        --out-prefix results/site1

    # Use your own seed accelerogram (1-column CSV of acceleration values, g)
    # instead of a synthetic seed:
    python generate_spectrum_compatible_motion.py \
        --target-csv my_target_spectrum.csv \
        --seed-csv my_seed_accel.csv --seed-dt 0.005 \
        --out-prefix results/site1

Outputs (written next to --out-prefix):
    <prefix>_acc.csv        time, acceleration (matched motion)
    <prefix>_vel.csv        time, velocity
    <prefix>_disp.csv       time, displacement
    <prefix>_spectra.png    target vs seed vs matched response spectra
    <prefix>_timehist.png   acceleration / velocity / displacement plots
    <prefix>_summary.txt    PGA/PGV/PGD, misfit history, run parameters
"""

import argparse
import sys
import numpy as np
import spectral_matching as sm
from misc_utils import log_messages as lmsg

def get_argument_parser():
    ''' Return the argument parser to use.'''
    retval= argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    retval.add_argument("--demo", action="store_true",
                   help="Run with a built-in demo ASCE7-like target spectrum and synthetic seed.")
    retval.add_argument("--target-csv", type=str, default=None,
                   help="CSV file with header row, columns: period(s), Sa(g)")
    retval.add_argument("--seed-csv", type=str, default=None,
                   help="Optional CSV (single column) of a seed acceleration time history, in g.")
    retval.add_argument("--seed-dt", type=float, default=None,
                   help="Time step (s) of --seed-csv, required if that option is used.")
    retval.add_argument("--duration", type=float, default=30.0,
                   help="Duration (s) of synthetic seed motion if no --seed-csv given. "
                        "Longer duration gives finer FFT frequency resolution (df=1/duration), "
                        "which materially improves matching accuracy at long periods -- "
                        "don't go much below 20-30s if your target spectrum extends past T~2s.")
    retval.add_argument("--dt", type=float, default=0.005,
                   help="Time step (s) of synthetic seed motion if no --seed-csv given.")
    retval.add_argument("--damping", type=float, default=0.05,
                   help="Damping ratio for response spectrum matching (default 0.05).")
    retval.add_argument("--max-iter", type=int, default=150)
    retval.add_argument("--relaxation", type=float, default=0.75,
                   help="Under-relaxation factor in (0,1] for the iterative correction (default 0.65). "
                        "Lower = more stable but slower convergence; 1.0 = full correction each pass "
                        "(often oscillates instead of converging).")
    retval.add_argument("--tol", type=float, default=0.03,
                   help="Convergence tolerance on max relative spectral misfit.")
    retval.add_argument("--random-seed", type=int, default=42,
                   help="RNG seed for synthetic seed motion generation (reproducibility).")
    retval.add_argument("--out-prefix", type=str, default="output/motion",
                   help="Path prefix for output files (directories created as needed).")
    return retval

def getSpectralMatchingFromArgs(args):
    ''' Creates a SpectralMatching object from the given arguments.

    :param args: arguments extracted from the command line.
    '''
    return sm.SpectralMatching(demo= args.demo, targetCSV= args.target_csv, seedCSV= args.seed_csv, seedDt= args.seed_dt, duration= args.duration, timeStep= args.dt, dampingRatio= args.damping, maxIter= args.max_iter, relaxation= args.relaxation, tol= args.tol, outputPrefix= args.out_prefix)
    

def main():
    # Parse arguments.
    p= get_argument_parser()
    args= p.parse_args()
    spectralMatching= getSpectralMatchingFromArgs(args)

    result= spectralMatching.getSpectralMatchingMotion(randomSeed= args.random_seed)
    pga = result.getPGA()
    pgv = result.getPGV()
    pgd = result.getPGD()
    # NOTE: match_spectrum tracks and returns the BEST iterate seen (misfit
    # is not strictly monotonic across iterations), so report that value --
    # not simply the last entry in the per-iteration history log below.
    final_misfit = result.getFinalMisfit()

    print(f"Done. Iterations: {len(result.history_misfit)}, final misfit: {final_misfit:.4f}")
    print(f"PGA={pga:.3f}  PGV={pgv:.3f}  PGD={pgd:.3f}")
    print(f"Outputs written with prefix: {args.out_prefix}_*")


if __name__ == "__main__":
    main()
