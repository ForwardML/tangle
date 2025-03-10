import argparse
from tngl.radio.hackrf import HackRFSweep

def main():
    parser = argparse.ArgumentParser(description="Record HackRF sweep data with configurable parameters.")
    parser.add_argument("--frequency_low", type=float, required=True, help="Lower frequency bound in MHz")
    parser.add_argument("--frequency_high", type=float, required=True, help="Upper frequency bound in MHz")
    parser.add_argument("--gain_db", type=float, default=0.0, help="Gain in dB (default: 20)")
    parser.add_argument("-o", "--output", type=str, default="./output", help="Output directory for SigMF files.")
    parser.add_argument("-d", "--duration", type=int, default=20, help="Duration of the sweep in seconds (default: 20).")
    parser.add_argument("-r", "--records", type=int, default=10, help="Number of records to record per sweep.")
    
    args = parser.parse_args()
    
    hackrf = HackRFSweep(
        freq_min=args.frequency_low, 
        freq_max=args.frequency_high, 
        vga_gain=args.gain_db, 
        output_dir=args.output
    )
    hackrf.run_sweep(duration=args.duration, sweep_time=0.25, num_records=args.records)

if __name__ == "__main__":
    main()
