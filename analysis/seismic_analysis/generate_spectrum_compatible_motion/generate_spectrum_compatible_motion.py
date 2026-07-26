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
    

def main():
    # Parse arguments.
    p= get_argument_parser()
    args = p.parse_args()

    import os
    os.makedirs(os.path.dirname(args.out_prefix) or ".", exist_ok=True)

    # ---- 1. Target spectrum ----
    if(args.target_csv or args.demo):
        T_target, Sa_target = sm.get_target_spectrum(targetCSV= args.target_csv)
    else:
        methodName= sys._getframe(0).f_code.co_name
        msg= methodName+'; supply --target-csv <file> or use --demo.'
        lmsg.error(msg)
        sys.exit(1)

    # ---- 2. Seed motion ----
    seed_acc, dt= sm.get_seed_motion(T_target= T_target, Sa_target= Sa_target, timeStep= args.dt, duration= args.duration, randomSeed= args.random_seed, dampingRatio= args.damping, seedCSV= args.seed_csv, seedDt= args.seed_dt)
    
    # ---- 3. Spectral matching ----
    result = sm.match_spectrum(
        seed_acc, dt, T_target, Sa_target,
        zeta=args.damping, max_iter=args.max_iter, tol=args.tol,
        relaxation=args.relaxation,
    )

    vel, disp = sm.integrate(result.acc, dt)

    pga = np.max(np.abs(result.acc))
    pgv = np.max(np.abs(vel))
    pgd = np.max(np.abs(disp))
    # NOTE: sm.match_spectrum tracks and returns the BEST iterate seen (misfit
    # is not strictly monotonic across iterations), so report that value --
    # not simply the last entry in the per-iteration history log below.
    final_misfit = result.achieved_misfit

    # ---- 4. Save outputs ----
    np.savetxt(f"{args.out_prefix}_acc.csv",
               np.column_stack([result.t, result.acc]),
               delimiter=",", header="time_s,accel_g", comments="")
    np.savetxt(f"{args.out_prefix}_vel.csv",
               np.column_stack([result.t, vel]),
               delimiter=",", header="time_s,vel", comments="")
    np.savetxt(f"{args.out_prefix}_disp.csv",
               np.column_stack([result.t, disp]),
               delimiter=",", header="time_s,disp", comments="")

    with open(f"{args.out_prefix}_summary.txt", "w") as f:
        f.write("Spectrum-compatible synthetic ground motion - summary\n")
        f.write("=" * 55 + "\n")
        f.write(f"dt (s):                {dt}\n")
        f.write(f"duration (s):          {result.t[-1]:.3f}\n")
        f.write(f"damping used:          {args.damping}\n")
        f.write(f"iterations run:        {len(result.history_misfit)}\n")
        f.write(f"achieved max misfit:   {final_misfit:.4f}  (tol={args.tol})  "
                f"[motion returned = best iterate found, not necessarily the last one run]\n")
        f.write(f"PGA:                   {pga:.4f}\n")
        f.write(f"PGV:                   {pgv:.4f}\n")
        f.write(f"PGD:                   {pgd:.4f}\n")
        f.write("\nMisfit per iteration (raw -- not necessarily monotonic; "
                "see achieved_misfit above for what was actually returned):\n")
        for i, m in enumerate(result.history_misfit, 1):
            f.write(f"  iter {i:3d}: {m:.4f}\n")

    # ---- 5. Plots ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
        axes[0].plot(result.t, result.acc, lw=0.7)
        axes[0].set_ylabel("Accel (g)")
        axes[0].set_title("Spectrum-matched synthetic motion")
        axes[1].plot(result.t, vel, lw=0.7, color="tab:orange")
        axes[1].set_ylabel("Velocity")
        axes[2].plot(result.t, disp, lw=0.7, color="tab:green")
        axes[2].set_ylabel("Displacement")
        axes[2].set_xlabel("Time (s)")
        fig.tight_layout()
        fig.savefig(f"{args.out_prefix}_timehist.png", dpi=150)
        plt.close(fig)

        fig2, ax = plt.subplots(figsize=(7, 5))
        ax.plot(result.periods, result.target_Sa, "k-", lw=2, label="Target")
        ax.plot(result.periods, result.seed_Sa, "b--", lw=1, label="Seed (before matching)")
        ax.plot(result.periods, result.final_Sa, "r-", lw=1.5, label="Matched")
        ax.set_xscale("log")
        ax.set_xlabel("Period (s)")
        ax.set_ylabel(f"Pseudo-Sa (g), damping={args.damping}")
        ax.set_title("Response spectrum matching result")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        fig2.tight_layout()
        fig2.savefig(f"{args.out_prefix}_spectra.png", dpi=150)
        plt.close(fig2)
    except ImportError:
        print("matplotlib not available -- skipping plots, CSV/summary still written.")

    print(f"Done. Iterations: {len(result.history_misfit)}, final misfit: {final_misfit:.4f}")
    print(f"PGA={pga:.3f}  PGV={pgv:.3f}  PGD={pgd:.3f}")
    print(f"Outputs written with prefix: {args.out_prefix}_*")


if __name__ == "__main__":
    main()
