# -*- coding: utf-8 -*-
'''
spectral_matching.py

Generate a synthetic ground-motion acceleration time history whose elastic
response spectrum matches (or closely envelopes) a user-supplied target
response spectrum.

Method
------
Iterative frequency-domain spectral matching (the approach used by tools
such as RspMatch / SeismoMatch, based on Lilhanand & Tseng (1988) and the
simpler Fourier-scaling scheme popularized by Al Atik & Abrahamson (2010)):

    1. Start from a "seed" accelerogram (a real record, or a synthetically
       generated white-noise motion shaped by an amplitude envelope and
       a target Fourier amplitude spectrum consistent with a point-source
       or user PSD).
    2. Compute the seed's elastic pseudo-acceleration response spectrum
       Sa_seed(T) at a set of periods, using an EXACT piecewise-linear
       SDOF recursive solver (Nigam & Jennings, 1969) -- this avoids the
       numerical-integration error you'd get from a naive Newmark loop
       and is fast enough to call once per iteration.
    3. At each period T_i, form the ratio target Sa(T_i) / Sa_seed(T_i).
       Map that ratio onto the Fourier amplitude spectrum in a
       neighborhood of frequency f_i = 1/T_i (with a smoothing/tapering
       window across neighboring periods so the correction is smooth in
       frequency), leaving the Fourier PHASE unchanged.
    4. Inverse FFT back to the time domain, re-baseline (so velocity and
       displacement do not drift), and repeat until the spectral misfit
       is below tolerance or max iterations reached.

This produces a motion that keeps the time-domain character (duration,
non-stationarity, phasing) of the seed while matching the target response
spectrum in the frequency domain -- the standard approach for generating
spectrum-compatible motions for time-history analysis.
'''

from __future__ import annotations

__author__= "Ana Ortega (AO_O) Luis C. Pérez Tato"
__copyright__= "Copyright 2026, AO_O LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "ana.Ortega@ciccp.es l.pereztato@ciccp.es"

import sys
import numpy as np
from dataclasses import dataclass, field
from misc_utils import log_messages as lmsg

# --------------------------------------------------------------------------
# 1. Exact piecewise-linear SDOF response (Nigam & Jennings recursion)
# --------------------------------------------------------------------------

def sdof_response_spectrum(acc, dt, periods, zeta=0.05):
    '''
    Compute pseudo-spectral acceleration (Sa), spectral velocity (Sv),
    spectral displacement (Sd) for a suite of SDOF oscillators subjected
    to ground acceleration `acc`, using the exact piecewise-linear
    recursive solution (assumes ground acceleration varies linearly
    between samples -- exact for that assumption, no time-step error).

    :param acc: ndarray
        Ground acceleration time history (same units as g or m/s^2 -- be
        consistent; output Sa will be in the same units).
    :param dt: float
        Time step (s).
    :param periods: ndarray
        Natural periods (s) at which to evaluate the spectrum. T=0 is
        handled as a special case (Sa = PGA).
    :param zeta: float
        Damping ratio (default 5%).

    :returns: Sa, Sv, Sd: ndarrays, same shape as `periods`
    '''
    acc = np.asarray(acc, dtype=float)
    n = len(acc)
    periods = np.asarray(periods, dtype=float)
    Sa = np.zeros_like(periods)
    Sv = np.zeros_like(periods)
    Sd = np.zeros_like(periods)

    pga = np.max(np.abs(acc))

    for k, T in enumerate(periods):
        if T <= 1e-8:
            Sa[k] = pga
            Sv[k] = 0.0
            Sd[k] = 0.0
            continue

        wn = 2.0 * np.pi / T
        wd = wn * np.sqrt(1.0 - zeta ** 2)
        w2 = wn ** 2
        w3 = wn ** 3

        # Precompute recursion coefficients (Nigam & Jennings, 1969)
        ewt = np.exp(-zeta * wn * dt)
        cwd = np.cos(wd * dt)
        swd = np.sin(wd * dt)

        A = ewt * (zeta / np.sqrt(1 - zeta ** 2) * swd + cwd)
        B = ewt * (swd / wd)
        C = (1.0 / w2) * (
            (2 * zeta / (wn * dt)) +
            ewt * (
                ((1 - 2 * zeta ** 2) / (wd * dt) - zeta / np.sqrt(1 - zeta ** 2))
                * swd
                - (1 + 2 * zeta / (wn * dt)) * cwd
            )
        )
        D = (1.0 / w2) * (
            1 - (2 * zeta / (wn * dt)) +
            ewt * (
                ((2 * zeta ** 2 - 1) / (wd * dt)) * swd
                + (2 * zeta / (wn * dt)) * cwd
            )
        )
        Ap = -ewt * ((wn / np.sqrt(1 - zeta ** 2)) * swd)
        Bp = ewt * (cwd - (zeta / np.sqrt(1 - zeta ** 2)) * swd)
        Cp = (1.0 / w2) * (
            -1.0 / dt
            + ewt * (
                ((wn / np.sqrt(1 - zeta ** 2)) + (zeta / (dt * np.sqrt(1 - zeta ** 2)))) * swd
                + (1.0 / dt) * cwd
            )
        )
        Dp = (1.0 / (w2 * dt)) * (1 - ewt * (cwd + (zeta / np.sqrt(1 - zeta ** 2)) * swd))

        u = 0.0
        v = 0.0
        umax = 0.0
        vmax = 0.0
        for i in range(n - 1):
            p1 = -acc[i]
            p2 = -acc[i + 1]
            u_new = A * u + B * v + C * p1 + D * p2
            v_new = Ap * u + Bp * v + Cp * p1 + Dp * p2
            u, v = u_new, v_new
            au = abs(u)
            av = abs(v)
            if au > umax:
                umax = au
            if av > vmax:
                vmax = av

        Sd[k] = umax
        Sv[k] = vmax
        Sa[k] = umax * w2  # pseudo-spectral acceleration = wn^2 * Sd

    return Sa, Sv, Sd


# --------------------------------------------------------------------------
# 2. Seed accelerogram generation (if the user has no real seed record)
# --------------------------------------------------------------------------

def saragoni_hart_envelope(t, t1=0.1, t2_frac=0.6, eps=0.2, eta=0.05):
    '''
    Saragoni & Hart (1974) style compound envelope: rises as a power law,
    holds a strong-motion plateau, then decays exponentially. Produces a
    realistic non-stationary amplitude shape for a synthetic seed.

    :param t: time vector
    :param t1: time (s) at which the rise ends / plateau begins
    :param t2_frac: fraction of total duration marking end of plateau
    :param eps: controls decay rate after plateau (smaller = slower decay)
    :param eta: target amplitude fraction at end of record (controls decay 
                const)
    :returns: envelope.
    '''
    T = t[-1]
    t2 = t2_frac * T
    env = np.ones_like(t)
    rise = t < t1
    env[rise] = (t[rise] / t1) ** 2
    decay = t > t2
    # exponential decay constant so envelope hits `eta` at T
    b = -np.log(eta) / (T - t2)
    env[decay] = np.exp(-b * (t[decay] - t2))
    return env


def generate_seed_motion(duration, dt, envelope_params=None, seed=None,
                          corner_freq=0.3, kappa=0.03):
    '''
    Generate a broadband seed accelerogram: filtered white noise shaped by
    a Saragoni-Hart envelope, with a simple Brune-like high-frequency decay
    (kappa filter) so the raw seed already has roughly realistic frequency
    content before spectral matching does the fine adjustment.

    :param duration: total duration (s)
    :param dt: time step (s)
    :param corner_freq: approx corner frequency (Hz) of the source spectrum shape
    :param kappa: high-frequency spectral decay parameter (site kappa, s)

    :returns: t, acc  (acc is unscaled -- spectral matching will rescale it)
    '''
    rng = np.random.default_rng(seed)
    n = int(np.round(duration / dt))
    if n % 2 == 1:
        n += 1
    t = np.arange(n) * dt

    # white noise -> FFT
    white = rng.standard_normal(n)
    F = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, d=dt)

    # simple omega-squared-like shaping + kappa high-freq decay, avoids
    # divide-by-zero at f=0
    f_safe = np.where(freqs == 0, freqs[1] if len(freqs) > 1 else 1.0, freqs)
    shape = (f_safe ** 2) / (1.0 + (f_safe / corner_freq) ** 2)
    shape *= np.exp(-np.pi * kappa * f_safe)
    shape[0] = 0.0

    F_shaped = F * shape
    acc = np.fft.irfft(F_shaped, n=n)

    # apply amplitude envelope
    env = saragoni_hart_envelope(t)
    acc = acc * env

    # normalize to unit std before returning (matching stage will scale it)
    acc = acc / (np.std(acc) + 1e-12)
    return t, acc


# --------------------------------------------------------------------------
# 3. Baseline correction
# --------------------------------------------------------------------------

def baseline_correct(acc, dt, poly_order=2):
    '''
    Remove drift from velocity/displacement by fitting and subtracting a
    low-order polynomial from the ACCELERATION trace such that the
    integrated velocity and displacement end near zero. A common simple
    approach: fit polynomial to acceleration itself (order 1-2) and
    subtract -- adequate for synthetic/matched motions. For processing
    real recorded data, prefer filtering (high-pass Butterworth) instead.
    '''
    n = len(acc)
    t = np.arange(n) * dt
    coeffs = np.polyfit(t, acc, poly_order)
    trend = np.polyval(coeffs, t)
    return acc - trend


def integrate(acc, dt):
    '''Trapezoidal integration -> velocity, displacement.'''
    vel = np.concatenate(([0.0], np.cumsum((acc[1:] + acc[:-1]) * 0.5 * dt)))
    disp = np.concatenate(([0.0], np.cumsum((vel[1:] + vel[:-1]) * 0.5 * dt)))
    return vel, disp


# --------------------------------------------------------------------------
# 4. Iterative frequency-domain spectral matching
# --------------------------------------------------------------------------

@dataclass
class MatchResult:
    t: np.ndarray
    acc: np.ndarray
    periods: np.ndarray
    target_Sa: np.ndarray
    final_Sa: np.ndarray
    seed_Sa: np.ndarray
    history_misfit: list = field(default_factory=list)
    achieved_misfit: float = float("nan")  # misfit of the RETURNED motion (best iterate)


def match_spectrum(
    seed_acc,
    dt,
    target_periods,
    target_Sa,
    zeta=0.05,
    max_iter=150,
    tol=0.03,
    freq_smooth_window=1,
    scale_limit=(0.3, 3.0),
    relaxation=0.75,
    patience=40,
):
    '''
    Iteratively adjust the Fourier amplitude spectrum of `seed_acc` so its
    SDOF response spectrum matches `target_Sa` at `target_periods`.

    :param seed_acc: ndarray
        Seed acceleration time history.
    :param dt: float
        Time step (s).
    :param target_periods: ndarray
        Periods (s) at which target spectrum is defined, ascending order.
    :param target_Sa: ndarray
        Target pseudo-spectral acceleration at target_periods (same units
        as you want the output acceleration to be in, e.g. g or m/s^2).
    :param zeta: float
        Damping ratio for spectrum matching (should match the target
        spectrum's damping, typically 5%).
    :param max_iter: int
        Maximum number of matching iterations.
    :param tol: float
        Convergence tolerance on max relative spectral misfit (e.g. 0.03
        = 3%).
    :param freq_smooth_window: int
        Number of neighboring FFT bins over which each period's
        correction ratio is smoothed/tapered. Default is 1 (no
        smoothing): smoothing sounded like a good idea to avoid a jagged
        Fourier spectrum, but in testing it blurred corrections across
        periods that are close together and made convergence noticeably
        worse -- lightly damped SDOF responses at nearby periods are
        already coupled through the oscillator's own bandwidth, and
        adding an extra smoothing kernel on top over-couples them. Try a
        small value (3) only if the matched time history looks visibly
        jagged.
    :param scale_limit: (min, max)
        Hard limits on the per-iteration correction ratio to keep the
        iteration stable.
    :param relaxation: float in (0, 1]
        Under-relaxation factor applied to the correction ratio each
        iteration (effective_ratio = 1 + relaxation*(ratio-1)). A value
        of 1.0 applies the full correction each pass, which tends to
        overshoot and oscillate/plateau instead of converging (target and
        achieved spectra "hunt" around each other). Values around
        0.5-0.7 trade a few extra iterations for stable, monotonic
        convergence -- this is standard practice in spectral-matching
        codes (RspMatch etc. use a similar damped update).
    :param patience: int
        Frequency-domain spectral matching does not converge strictly
        monotonically -- the misfit can dip to a good value and then
        drift back up on later iterations (this is normal, not a bug,
        and is why this function tracks and returns the BEST iterate
        seen, not simply the last one). `patience` stops the loop early
        if `patience` iterations pass with no improvement on the best
        misfit found so far, to avoid wasting iterations once the
        result has plateaued.

    :returns: MatchResult
    '''
    acc = np.array(seed_acc, dtype=float).copy()
    n = len(acc)
    if n % 2 == 1:
        acc = acc[:-1]
        n -= 1

    freqs = np.fft.rfftfreq(n, d=dt)
    history = []

    # avoid T=0 in matching frequencies (handled as PGA anchor already in
    # sdof solver); ensure periods sorted ascending
    order = np.argsort(target_periods)
    T_targets = np.asarray(target_periods)[order]
    Sa_targets = np.asarray(target_Sa)[order]

    best_acc = acc.copy()
    best_misfit = np.inf
    iters_since_best = 0

    for iteration in range(1, max_iter + 1):
        Sa_current, _, _ = sdof_response_spectrum(acc, dt, T_targets, zeta=zeta)

        ratio = Sa_targets / np.maximum(Sa_current, 1e-12)
        misfit = np.max(np.abs(ratio - 1.0))
        history.append(misfit)

        if misfit < best_misfit:
            best_misfit = misfit
            best_acc = acc.copy()
            iters_since_best = 0
        else:
            iters_since_best += 1

        if misfit < tol:
            break
        if iters_since_best >= patience:
            break

        # under-relax: move only partway toward the full correction each
        # pass -- prevents the overshoot/oscillation that a full-strength
        # update produces (see `relaxation` docstring above)
        ratio = 1.0 + relaxation * (ratio - 1.0)
        ratio = np.clip(ratio, *scale_limit)

        # Map period-domain ratios onto the FFT frequency axis.
        # For each FFT bin frequency f, find corresponding period T=1/f,
        # interpolate the ratio curve (in log-period space) at that T.
        F = np.fft.rfft(acc)
        amp = np.abs(F)
        phase = np.angle(F)

        f_nonzero = freqs[1:]  # skip DC
        T_bins = 1.0 / f_nonzero

        # interpolate ratio (log-period, linear ratio) with clamping at
        # the ends of the target period range
        log_T_targets = np.log(T_targets)
        log_T_bins = np.log(T_bins)
        ratio_bins = np.interp(
            log_T_bins, log_T_targets, ratio,
            left=ratio[0], right=ratio[-1]
        )

        # light smoothing across neighboring bins (moving average) to
        # avoid a jagged correction spectrum
        if freq_smooth_window > 1:
            kernel = np.ones(freq_smooth_window) / freq_smooth_window
            ratio_bins = np.convolve(ratio_bins, kernel, mode="same")

        scale = np.concatenate(([1.0], ratio_bins))  # keep DC bin unscaled
        amp_new = amp * scale
        F_new = amp_new * np.exp(1j * phase)
        acc = np.fft.irfft(F_new, n=n)
        # NOTE: do NOT baseline-correct inside this loop. A polynomial
        # detrend removes low-frequency (long-period) content -- exactly
        # what the correction step just added to match long-period
        # targets -- so doing it every iteration makes the loop fight
        # itself and stall well above tolerance. Baseline correction is
        # applied once, after the loop, as pure post-processing.

    acc = baseline_correct(best_acc, dt, poly_order=2)
    Sa_final, _, _ = sdof_response_spectrum(acc, dt, T_targets, zeta=zeta)
    Sa_seed0, _, _ = sdof_response_spectrum(seed_acc, dt, T_targets, zeta=zeta)

    t = np.arange(len(acc)) * dt
    return MatchResult(
        t=t,
        acc=acc,
        periods=T_targets,
        target_Sa=Sa_targets,
        final_Sa=Sa_final,
        seed_Sa=Sa_seed0,
        history_misfit=history,
        achieved_misfit=float(np.max(np.abs(Sa_targets / np.maximum(Sa_final, 1e-12) - 1.0))),
    )

def load_two_col_csv(path):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:, 0], data[:, 1]


def load_one_col_csv(path):
    return np.loadtxt(path, delimiter=",", skiprows=0).ravel()

def asce7_like_target_spectrum(periods, Ss=1.5, S1=0.6, TL=8.0):
    """
    Simple ASCE 7 - style design response spectrum shape (for demo
    purposes only -- NOT a substitute for site-specific hazard analysis).
    Ss = short-period spectral accel (g), S1 = 1s spectral accel (g).
    """
    Sds = (2.0 / 3.0) * Ss
    Sd1 = (2.0 / 3.0) * S1
    T0 = 0.2 * Sd1 / Sds
    Ts = Sd1 / Sds

    Sa = np.zeros_like(periods)
    for i, T in enumerate(periods):
        if T <= T0:
            Sa[i] = Sds * (0.4 + 0.6 * T / T0) if T0 > 0 else Sds
        elif T <= Ts:
            Sa[i] = Sds
        elif T <= TL:
            Sa[i] = Sd1 / T
        else:
            Sa[i] = Sd1 * TL / T ** 2
    return Sa

def make_period_grid(t_min=0.04, t_max=6.0, n=100):
    """
    Default period grid for the demo. t_min is kept well above the Nyquist
    period of typical dt (e.g. dt=0.005-0.01s -> Nyquist period 0.01-0.02s)
    since response-spectrum matching becomes numerically unstable for
    target periods within a factor of ~2 of the Nyquist period (there's
    almost no Fourier content left to adjust at that frequency).
    """
    return np.geomspace(t_min, t_max, n)

def get_target_spectrum(targetCSV= None):
    ''' Return the target spectrum.

    :param targetCSV: CSV file with header row, columns: period(s), Sa(g).
    '''
    if targetCSV:
        T_target, Sa_target = load_two_col_csv(targetCSV)
        order= np.argsort(T_target)
        T_target, Sa_target = T_target[order], Sa_target[order]
    else:
        T_target = make_period_grid()
        Sa_target = asce7_like_target_spectrum(T_target)
    return T_target, Sa_target


def get_seed_motion(T_target, Sa_target, timeStep= .005, duration= 30.0, randomSeed= 42, dampingRatio= .05, seedCSV= None, seedDt= None):
    ''' Return the acceleration history to be used as seed.

    :param T_target: periods of the target spectrum.
    :param Sa_target: spectral accelerations of the target spectrum.
    :param timeStep: time step (s) of synthetic seed motion (if no seedCSV 
                     given).
    :param duration: Duration (s) of synthetic seed motion if no seedCSV given.
                     Longer duration gives finer FFT frequency resolution
                     (df=1/duration), which materially improves matching 
                     accuracy at long periods -- don't go much below 20-30s 
                     if your target spectrum extends past T~2s.
    :param randomSeed: RNG seed for synthetic seed motion generation
                      (reproducibility).
    :param dampingRatio: Damping ratio for response spectrum matching
                         (default 0.05).
    :param seedCSV: optional CSV (single column) of a seed acceleration time 
                    history, in g.
    :param seedDt: time step (s) of seed_csv, required seed_csv is not none.
    '''
    if seedCSV:
        if seedDt is None:            
            methodName= sys._getframe(0).f_code.co_name
            msg= methodName+'; seedDt is required when using seedCSV.'
            lmsg.error(msg)
            sys.exit(1)
        seedAcc = load_one_col_csv(seedCSV)
        dt= seedDt
        seedAcc= baseline_correct(seedAcc, dt, poly_order=2)
    else:
        t, seedAcc= generate_seed_motion(duration, timeStep, seed= randomSeed)
        dt = timeStep
        # rough amplitude pre-scaling so the iteration starts in the right
        # ballpark: scale seed so its PGA-period Sa matches target's peak
        Sa_seed_probe, _, _ = sdof_response_spectrum(seedAcc, dt, T_target, zeta= dampingRatio)
        scale0 = np.max(Sa_target) / (np.max(Sa_seed_probe) + 1e-12)
        seedAcc = seedAcc * scale0
    return seedAcc, dt
