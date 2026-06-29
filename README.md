Bistatic-Locator-and-Oscillation-Weapon-BLOW
Passive, jam‑proof drone detection via GNSS shadow, CMOS clock ELINT, and ultrasonic sonar pings. Same array focuses a resonant acoustic beam to neutralise—no RF, no projectiles, just a very bad day for MEMS gyros. Fully COTS. Here is a complete, professional README.md for the B.L.O.W. repository. It’s designed to clearly explain the invention, protect your rights, and help collaborators understand the system at a glance.

```markdown
# B.L.O.W. – Bistatic Locator and Oscillation Weapon

**Passive, jam‑proof drone detection and surgical acoustic neutralisation.**
No radar, no jammers, no projectiles—just physics the drone cannot hide.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](LICENSE)
[![Patent Pending](https://img.shields.io/badge/Status-Patent%20Pending-red.svg)](PATENT_PENDING.md)



 Overview

B.L.O.W. is a fully passive counter‑drone system that fuses three independent detection
modalities—**GNSS forward‑scatter radar**, **camera clock ELINT**, and **ultrasonic
altimeter ping sonar**—to provide real‑time 3D tracking from kilometres down to
centimetres, without ever emitting a detectable signal.

The same ultrasonic phased array used for tracking is then switched to transmit
mode, focusing a precisely aimed **27 kHz resonance beam** that saturates the
target drone’s MEMS gyroscope. The drone loses attitude control instantly and
crashes—with no RF interference, no explosives, and no collateral damage.

Every component is **commercial off‑the‑shelf (COTS)**, the toolchain is
open‑source, and the system requires no spectrum licences.



 Key Features

- **100% passive detection** – emits nothing, can’t be jammed or located
- **Three independent sensing modes** – GNSS shadow, CMOS clock RF, ultrasonic sonar
- **Shared‑aperture kill** – same ultrasonic array tracks and neutralises
- **Sub‑centimetre close‑in precision** – thanks to 40 kHz TDOA beamforming
- **Real‑time sensor fusion** – Unscented Kalman Filter with environmental compensation
- **All COTS hardware** – buildable with a modest budget and standard tools
- **Portable and rapid‑deploy** – designed for field use



 How It Works

 1. GNSS Shadow & Forward‑Scatter Mapper
An array of ground‑based GPS receivers watches for the tiny dip in satellite
signal strength (and simultaneous forward‑scatter spike) caused by a drone
crossing the line‑of‑sight. The time‑difference‑of‑arrival of these “shadows”
at multiple stations gives a **long‑range (3 km) 3D position fix**.

 2. Camera CMOS Clock ELINT Tracker
Every digital camera sensor leaks a continuous tone at its pixel‑clock frequency
(24–72 MHz and harmonics). A four‑element phase‑coherent array homes in on this
signal, giving **bearing and elevation** even if the drone is not transmitting
video.

 3. Ultrasonic Altimeter Ping Sonar Array
Consumer drones constantly emit 40 kHz ultrasonic pulses for altitude hold and
obstacle avoidance. A 16‑element MEMS microphone array captures these pings,
and an FPGA computes **TDOA‑based 3D position** with centimetre accuracy at
update rates up to 25 Hz.

 4. Ultrasonic MEMS Gyro Kill
After lock‑on, the same array switches to transmit. A phased beam of
**>140 dB SPL at 27 kHz**—the mechanical resonance of common MEMS gyroscopes—
is focused onto the target. The gyro saturates, the flight controller panics,
and the drone tumbles **within one second**.



 Repository Structure

```

drone-defence/
├── LICENSE                  # GNU AGPLv3 + attribution addendum
├── PATENT_PENDING.md        # Patent status notice
├── README.md                # This file
├── .gitignore
├── firmware/                # FPGA Verilog sources
│   ├── tdoa_core_optimized.v
│   ├── tx_beamformer_optimized.v
│   ├── adc_reader.v
│   ├── pulse_detector.v
│   ├── capture_buffer_dualport.v
│   ├── tdoa_correlator_optimized.v
│   └── uart_tx.v
├── software/                # Host‑side Python nodes & scripts
│   ├── kalman_tracker.py
│   ├── fusion_ukf.py
│   ├── calibration.py
│   ├── health_monitor_daemon.py
│   └── setup_rt_kernel.sh
├── hardware/                # PCB design & BOM
│   ├── ultrasonic_tile.kicad_sch
│   ├── ultrasonic_tile.kicad_pcb
│   ├── bom_optimized.csv
│   └── system_integration_optimized.md
└── docs/                    # Full patent disclosure & guides
├── BLOW_Defence_System.md
├── BLOW_Patent_Disclosure.md
└── sim_target_gen_guide.md

```

---

## Getting Started

### Prerequisites
- **FPGA development:** Xilinx Vivado 2023.x (targeting Artix‑7 XC7A35T)
- **Host computer:** Ubuntu 22.04 with PREEMPT_RT kernel (or Jetson Orin)
- **ROS2 Humble** with Eclipse Iceoryx transport
- **KiCad 7** for PCB viewing/modification
- **GNSS‑SDR** (modified, see `docs/`)

### Building the FPGA Image
1. Open Vivado, create a new project for the Arty A7‑35T.
2. Add all `.v` files from `firmware/`.
3. Synthesise, implement, and generate the bitstream.
4. Load onto the Arty A7 using the Vivado Hardware Manager.

### Running the Software
```bash
# One‑time RT kernel setup
sudo ./software/setup_rt_kernel.sh

# Launch the fusion tracker
source /opt/ros/humble/setup.bash
python3 software/fusion_ukf.py
```

Calibration

Follow the step‑by‑step guide in hardware/system_integration_optimized.md.
Critical steps include:

· 24‑hour GNSS station survey (RTKLIB static PPP)
· Ultrasonic array self‑calibration with a reference pinger
· ELINT array phase calibration
· TX beamformer focal spot verification


Key Hardware Components

Module Component Function
GNSS Antenna Taoglas GPDF1575.A RHCP patch, GPS L1
GNSS SDR USRP B210 + GPSDO Coherent multi‑channel receiver
ELINT SDR KerberosSDR 4‑channel phase‑coherent DF
MEMS Microphone Vesper VM3011 Ultrasonic ping capture (40 kHz)
ADC ADS127L11 (×2) 24‑bit simultaneous sampling
FPGA Xilinx Artix‑7 XC7A35T TDOA correlator, beamformer
Transducer Murata MA40S4S Ultrasonic TX/RX element
GaN FET EPC2032 + LMG1210 High‑efficiency 27 kHz burst driver
Environmental Bosch BME280 Sound‑speed compensation

A complete, up‑to‑date bill of materials is maintained in hardware/bom_optimized.csv.


Legal & Intellectual Property

Patent Pending

The methods, apparatus, and system architecture disclosed in this repository
are the subject of a pending patent application. The open‑source license
below grants rights only to the software code; it does not grant a
licence to the underlying invention. Unauthorised use of the patented
technology may constitute infringement.

See PATENT_PENDING.md for full details.

Software License

The software in this repository is licensed under the GNU Affero General
Public License v3.0, with an additional attribution requirement:

“This software includes the B.L.O.W. drone defence system, originally
developed by [Your Name]. The name ‘B.L.O.W.’ may not be used to endorse
or promote products derived from this software without specific prior
written permission.”

See LICENSE for the complete text.

This means:

· You may use, study, modify, and redistribute the code.
· You must make your modified source available under the same AGPL terms,
  even if you only offer it as a network service.
· You must retain the attribution notice in all copies.
· The license does not grant a patent licence.


Contributing

Because the core technology is patent‑pending, we currently accept
contributions only for documentation, test infrastructure, and non‑core
build scripts. If you have ideas for significant functional changes,
please open an issue first to discuss licensing and intellectual property
implications.

Acknowledgements

B.L.O.W. was designed as a proof‑of‑concept that passive physics can be
weaponised for drone defence. It builds on the work of countless open‑source
projects: GNSS‑SDR, GNU Radio, ROS2, KiCad, and the RT‑kernel community.

No emissions. No warnings. Just a very bad day for MEMS gyros.


 blow/
├── LICENSE
├── PATENT_PENDING.md
├── README.md
├── .gitignore
├── firmware/
│   ├── tdoa_core_optimized.v
│   ├── tx_beamformer_optimized.v
│   ├── adc_reader.v
│   ├── pulse_detector.v
│   ├── capture_buffer_dualport.v
│   ├── tdoa_correlator_optimized.v
│   └── uart_tx.v
├── software/
│   ├── kalman_tracker.py
│   ├── fusion_ukf.py
│   ├── calibration.py
│   ├── health_monitor_daemon.py
│   └── setup_rt_kernel.sh
├── hardware/
│   ├── ultrasonic_tile.kicad_sch
│   ├── ultrasonic_tile.kicad_pcb
│   ├── bom_optimized.csv
│   └── system_integration_optimized.md
└── docs/
    ├── BLOW_Defence_System.md
    ├── invention_disclosure.pdf
    └── sim_target_gen_guide.md

