from pyspectools import ftmw_analysis as fa
from pyspectools import parsecat as pc
import pandas as pd
import numpy as np
import os
import sys
from scipy.optimize import curve_fit
from uncertainties import ufloat
import peakutils


def find_peaks(xdata, ydata, thres=0.3, min_dist=1):
    # Finds the peak intensities in ydata, and returns the
    # corresponding frequencies
    indexes = peakutils.indexes(ydata, thres=thres)
    peak_frequencies = np.array(xdata[indexes].astype(float))
    peak_intensities = np.array(ydata[indexes].astype(float))
    return peak_frequencies, peak_intensities

def lorentzian_func(x, amplitude, center, width, offset):
    # Stock Lorenztian
    return amplitude / np.pi * (0.5 * width)/((x - center)**2. + (0.5 * width)**2.)

def doppler_pair(x, a1, a2, w1, w2, center, doppler_splitting, offset):
    """ Function for a pair of Doppler peaks """
    return lorentzian_func(x, a1, center - doppler_splitting, w1, offset) + \
           lorentzian_func(x, a2, center + doppler_splitting, w2, offset)

def fit_doppler_pair(fft_df, center=None):
    if "Fit" not in list(fft_df.keys()):
        fft_df["Fit"] = np.zeros(len(fft_df["Frequency"]))
    if center is not None:
        # If a center is provided as a list of frequencies, take the average
        center = np.average(center)
    elif center is None:
        # If no center guess, take center of the frequency window
        center = (fft_df["Frequency"].min() + fft_df["Frequency"].max()) / 2.
    initial = [0.5, 0.5, 0.01, 0.01, center, 0.001, 0.]
    bounds = (
        [0., 0., 1e-4, 1e-4, center - 0.1, 0., -np.inf],
        [np.inf, np.inf, 0.05, 0.05, center + 0.1, 0.1, np.inf]
    )
    # Call the scipy fitting wrapper
    popt, pcov = curve_fit(
        doppler_pair,
        fft_df["Frequency"],
        fft_df["Intensity"],
        p0=initial,
        bounds=bounds
    )

    fft_df["Fit"] += doppler_pair(fft_df["Frequency"], *popt)
    fit_results = dict()
    sigmas = np.sqrt(np.diag(pcov))
    names = ["A1", "A2", "W1", "W2", "Frequency", "Doppler-width", "Offset"]
    for name, value, sigma in zip(names, popt, sigmas):
        fit_results[name] = ufloat(value, sigma)
    return fit_results

if __name__ == "__main__":
    print("The script is able to take an FFT spectrum, and determine the")
    print("Doppler-splitting automatically.")
    fft_path = input("If you would like this done, please provide a filepath.        ")
    if len(fft_path) > 1:
        if os.path.isfile(fft_path) is True:
            fft_df = fa.parse_spectrum(fft_path)
            print("Finding peaks...")
            peak_freq, peak_int = find_peaks(fft_df["Frequency"], fft_df["Intensity"])
            fit_results = fit_doppler_pair(fft_df, peak_freq)
            width = fit_results["Doppler-width"].n
            horn_width = np.average([fit_results["W1"].n, fit_results["W2"].n])
            print("Using a Doppler-width of " + str(width))
            print("Using an average horn-width of " + str(horn_width))
        else:
            print("FFT file not found. Exiting.")
            sys.exit()
    else:
        width = float(input("Please provide a Doppler-width in MHz.        "))
        horn_width = float(input("Please provide the width of a horn in MHz.        "))

    min_freq = input("Please specify the lowest frequency in MHz.  (Default: 0)         ")
    if min_freq:
        min_freq = float(min_freq)
    else:
        min_freq = 0.
    max_freq = input("Please specify the highest frequency in MHz. (Default: 300,000)        ")
    if max_freq:
        max_freq = float(max_freq)
    else:
        max_freq = 300000.
    #npoints = input("Please specify the number of data points. (Default: 10,000)        ")
    #if npoints:
    #    npoints = int(npoints)
    #else:
    #    npoints = 10000

    cat_path = input("Please specify the catalog filepath.        ")
    if cat_path:
        if os.path.isfile(cat_path) is True:
            cat_df = pc.pick_pickett(cat_path)

    frequency = np.arange(min_freq, max_freq, 0.005)
    intensities = np.zeros(frequency.size)

    for center, intensity in zip(cat_df["Frequency"], cat_df["Intensity"]):
        intensities += doppler_pair(
            frequency,
            10**intensity,
            10**intensity,
            horn_width,
            horn_width,
            center,
            width,
            0.
        )
    spectrum_df = pd.DataFrame(data=list(zip(frequency, intensities)), columns=["Frequency", "Intensity"])
    spectrum_df["Intensity"] = spectrum_df["Intensity"] / spectrum_df["Intensity"].max()
    spectrum_df.loc[spectrum_df["Intensity"] > 1e-3].to_csv("synthetic_spectrum.csv", index=False)
