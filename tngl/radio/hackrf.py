import os
import json
import time
import hashlib
import uuid

import subprocess
import argparse

from tqdm import tqdm
from datetime import datetime

class HackRFSweep:
    def __init__(self, serial_number=None, freq_min=900, freq_max=930, amp_enable=1, antenna_enable=1, lna_gain=16, vga_gain=0, bin_width=2445, output_dir="./output"):
        self.serial_number = serial_number
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.amp_enable = amp_enable
        self.antenna_enable = antenna_enable
        self.lna_gain = lna_gain
        self.vga_gain = vga_gain
        self.bin_width = bin_width
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_sweep(self, duration=10, sweep_time=1, num_records=10):
        for _ in tqdm(range(num_records)):
            id_ = HackRFSweep.random_md5()
            batch_timestamp = datetime.utcnow().strftime(f"%Y%m%d_%H%M%S_{id_}")
            data_filename = os.path.join(self.output_dir, f"{batch_timestamp}.sigmf-data")
            meta_filename = os.path.join(self.output_dir, f"{batch_timestamp}.sigmf-meta")

            HackRFSweep.run_hackrf_sweep(data_filename, duration, self.freq_min, self.freq_max, self.bin_width)
            self.generate_metadata(meta_filename, data_filename, batch_timestamp, id_=id_)
    
    def generate_metadata(self, meta_filename, data_filename, batch_timestamp, id_=""):
        metadata = {
            "global": {
                "core:datatype": "ci8_le",  # Updated to reflect HackRF's 8-bit signed integer format
                "core:version": "1.0.0",
                "core:description": "HackRF Sweep Data for Analysis.",
                "core:hash": id_,
                "core:author": "FORWARD.ML LLC",
                "core:datafile": data_filename,
                "core:meta_time": batch_timestamp,
                "core:sample_rate": 20 * 1e6, # 20 MHz
                "core:bin_width": self.bin_width,
                "core:frequency_min": self.freq_min * 1e6,  # Convert MHz to Hz
                "core:frequency_max": self.freq_max * 1e6,
                "core:hw": "HackRF"
            },
            "captures": [
                {
                    "core:sample_start": 0,
                    "core:frequency": self.freq_min * 1e6,
                    "core:datetime": batch_timestamp
                }
            ],
            "annotations": []
        }
        
        with open(meta_filename, "w") as f:
            json.dump(metadata, f, indent=4)
        # print(f"Metadata file saved: {meta_filename}")

    @staticmethod
    def run_hackrf_sweep(data_filename, duration=20, freq_min=2350, freq_max=2550, bin_width=2445):
        command = [
            "hackrf_sweep",
            "-f", f"{int(freq_min)}:{int(freq_max)}",
            "-B",  # Binary output mode
            "-w", str(bin_width),
            "-r", data_filename
        ]

        # print(f"Running command: {' '.join(command)}")

        # Start the process
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            time.sleep(duration)  # Let it run for `duration` seconds
            process.terminate()  # Gracefully terminate
            process.wait(timeout=2)  # Allow it to exit cleanly
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if needed
            # print("Process forcefully terminated.")

        # print("HackRF sweep completed.")

    @staticmethod
    def random_md5():
        random_uuid = uuid.uuid4().hex # Generate a random UUID
        md5_hash = hashlib.md5(random_uuid.encode()).hexdigest()  # Compute MD5 hash
        return md5_hash
