import pandas as pd
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import os
from datetime import datetime

def load_all_ecg_data(year):
    """Load all ECG files for a specific year"""
    data = []
    base_path = 'electrocardiograms'
    
    # Get all files for the specified year
    files = [f for f in os.listdir(base_path) if f.startswith(f'ecg_{year}')]
    
    for file in sorted(files):
        with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
            # Skip header lines and read data
            lines = f.readlines()[13:]
            values = [float(line.split(',')[1]) for line in lines if line.strip() and ',' in line]
            data.extend(values)
    
    return np.array(data)

def detect_abnormal_beats(ecg_data, sampling_rate=512.469):
    """Detect abnormal beats using adaptive thresholding"""
    # Apply bandpass filter (5-15 Hz)
    nyquist = sampling_rate / 2
    b, a = signal.butter(3, [5/nyquist, 15/nyquist], btype='band')
    filtered = signal.filtfilt(b, a, ecg_data)
    
    # Find R-peaks
    peaks, _ = signal.find_peaks(filtered, 
                                distance=int(sampling_rate*0.5),
                                height=np.mean(filtered))
    
    # Calculate RR intervals
    rr_intervals = np.diff(peaks) / sampling_rate
    
    # Detect abnormal beats using moving window statistics
    window_size = 10
    abnormal_idx = []
    
    for i in range(len(rr_intervals)):
        start = max(0, i - window_size)
        end = min(len(rr_intervals), i + window_size)
        window = rr_intervals[start:end]
        
        mean_rr = np.mean(window)
        std_rr = np.std(window)
        
        if abs(rr_intervals[i] - mean_rr) > 2 * std_rr:
            abnormal_idx.append(i)
    
    return peaks, np.array(abnormal_idx), rr_intervals

def spectral_analysis(rr_intervals, sampling_rate=512.469):
    """Perform spectral analysis of HRV"""
    # Interpolate RR intervals
    time_points = np.cumsum(rr_intervals)
    interpolated_time = np.linspace(time_points[0], time_points[-1], len(rr_intervals))
    interpolated_rr = np.interp(interpolated_time, time_points, rr_intervals)
    
    # Remove mean and apply window
    detrended = interpolated_rr - np.mean(interpolated_rr)
    windowed = detrended * signal.windows.hann(len(detrended))
    
    # Calculate FFT with proper scaling
    yf = fft(windowed)
    xf = fftfreq(len(windowed), 1/sampling_rate)[:len(windowed)//2]
    power = 2.0/len(windowed) * np.abs(yf[0:len(windowed)//2])**2
    
    # Calculate frequency bands with error handling
    vlf_power = np.sum(power[(xf >= 0.0033) & (xf < 0.04)])
    lf_power = np.sum(power[(xf >= 0.04) & (xf < 0.15)])
    hf_power = np.sum(power[(xf >= 0.15) & (xf < 0.4)])
    
    # Safe division for LF/HF ratio
    lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 0
    
    metrics = {
        'VLF Power': vlf_power,
        'LF Power': lf_power,
        'HF Power': hf_power,
        'LF/HF Ratio': lf_hf_ratio
    }
    
    return metrics, xf, power

def analyze_yearly_data(year):
    """Analyze ECG data for a specific year"""
    print(f"\nAnalyzing ECG data for {year}...")
    
    # Load data
    ecg_data = load_all_ecg_data(year)
    
    # Detect abnormal beats
    peaks, abnormal_idx, rr_intervals = detect_abnormal_beats(ecg_data)
    
    # Perform spectral analysis
    spectral_metrics, freqs, power = spectral_analysis(rr_intervals)
    
    return {
        'ecg_data': ecg_data,
        'peaks': peaks,
        'abnormal_idx': abnormal_idx,
        'rr_intervals': rr_intervals,
        'spectral_metrics': spectral_metrics,
        'freqs': freqs,
        'power': power
    }

def plot_comparative_analysis(results_2021, results_2022):
    """Plot comparative analysis between 2021 and 2022"""
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    
    # Plot ECG samples and abnormal beats
    for idx, (year, results) in enumerate(zip(['2021', '2022'], 
                                            [results_2021, results_2022])):
        axes[0, idx].plot(results['ecg_data'][:1000], 'b-', label='ECG Signal')
        axes[0, idx].scatter(results['peaks'][:10], 
                           results['ecg_data'][results['peaks'][:10]], 
                           color='g', label='Normal R-peaks')
        
        if len(results['abnormal_idx']) > 0:
            abnormal_peaks = results['peaks'][results['abnormal_idx']]
            axes[0, idx].scatter(abnormal_peaks[:10], 
                               results['ecg_data'][abnormal_peaks[:10]], 
                               color='r', label='Abnormal Beats')
        
        axes[0, idx].set_title(f'ECG Signal and Abnormal Beats ({year})')
        axes[0, idx].legend()
        
        # Plot RR intervals
        axes[1, idx].plot(results['rr_intervals'], 'b-')
        axes[1, idx].set_title(f'RR Intervals ({year})')
        axes[1, idx].set_ylabel('RR Interval (s)')
        
        # Plot power spectral density
        axes[2, idx].plot(results['freqs'], results['power'])
        axes[2, idx].set_title(f'Power Spectral Density ({year})')
        axes[2, idx].set_xlabel('Frequency (Hz)')
        axes[2, idx].set_ylabel('Power')
    
    plt.tight_layout()
    plt.show()

def main():
    # Analyze both years
    results_2021 = analyze_yearly_data('2021')
    results_2022 = analyze_yearly_data('2022')
    
    # Print statistical summary
    for year, results in zip(['2021', '2022'], [results_2021, results_2022]):
        print(f"\nResults for {year}:")
        print("-" * 40)
        print(f"Total Beats: {len(results['peaks'])}")
        print(f"Abnormal Beats: {len(results['abnormal_idx'])} "
              f"({len(results['abnormal_idx'])/len(results['peaks'])*100:.2f}%)")
        
        print("\nSpectral Analysis:")
        for metric, value in results['spectral_metrics'].items():
            print(f"{metric:.<20} {value:>10.2f}")
    
    # Plot comparative analysis
    plot_comparative_analysis(results_2021, results_2022)

if __name__ == "__main__":

       main() 