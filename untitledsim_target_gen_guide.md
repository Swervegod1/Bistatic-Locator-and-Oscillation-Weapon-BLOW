# Simulating a GNSS Shadow with HackRF One
1. Install gps-sdr-sim: `git clone https://github.com/osqzss/gps-sdr-sim.git`
2. Generate a GPS baseband file with a single satellite PRN:
   `./gps-sdr-sim -e brdc3540.14n -l 30.0,-90.0,100 -t 2026/06/28,12:00:00 -d 300 -o static.bin`
3. Stream with HackRF: `hackrf_transfer -t static.bin -f 1575420000 -s 2600000 -x 0`
4. Use a programmable attenuator (e.g. HMC624) on the HackRF output to create a simulated "shadow dip" by periodically lowering the gain.
5. The GNSS‑SDR chain will detect the shadow as if a drone passed.