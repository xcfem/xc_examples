# Synthetic ground motion compatible with a given spectrum

The approach used in this algorithm is he iterative frequency-domain spectral matching method (similar to what's used in tools like RspMatch/SeismoMatch): you start from a seed accelerogram, compute its response spectrum via a SDOF (single-degree-of-freedom) solver, compare it to the target spectrum, and iteratively scale the Fourier amplitude spectrum until the response spectrum converges to the target — while preserving the phase (and thus the non-stationary character) of the seed motion.

The procedure of the Python script in this folder is:

1. Generates (or accepts) a seed accelerogram.
2. Computes the elastic response spectrum via exact piecewise-linear SDOF recursion (fast, no numerical integration error).
3. Iteratively adjusts the Fourier spectrum in the frequency domain to match a target spectrum.
4. Applies baseline correction so velocity/displacement don't drift.
5. Plots seed vs. matched time histories and spectra.

The components are:
- `spectral_matching.py` — the core library.
- `generate_spectrum_compatible_motion.py` with three usage modes:


  ```
  # Quick demo with a built-in ASCE7-like target spectrum
  python generate_spectrum_compatible_motion.py --demo --out-prefix output/demo

  # Your own target spectrum (2-col CSV: period_s, Sa_g)
  python generate_spectrum_compatible_motion.py --target-csv my_target.csv \
    --duration 25 --dt 0.01 --out-prefix output/site1

  # Your own seed record instead of a synthetic one
  python generate_spectrum_compatible_motion.py --target-csv my_target.csv \
    --seed-csv my_seed.csv --seed-dt 0.01 --out-prefix output/site1
  ```

The script writes acceleration/velocity/displacement CSVs, spectra + time-history plots, and a summary with convergence stats.

Worth knowing as you use this:

- **Frequency resolution matters a lot for long periods** — FFT bin spacing is 1/duration, so short seed durations starve long-period matching. Keep duration ≥ 20–30s if your spectrum extends past ~2s.

- **The misfit doesn't converge monotonically** (normal for this method) — the code tracks and returns the best iterate seen, not just the last one, and reports that honestly as achieved_misfit.

- Getting a very dense period grid (a stress-teste with 100 points from 0.04–6s was performed to check this) to converge below a tight 3% tolerance everywhere is genuinely hard; a realistic grid like your actual code's required matching periods (e.g., ASCE 7's typically ~10–30 points) converges cleanly.

