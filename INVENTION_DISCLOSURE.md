# Passive Multi-Modal Drone Detection and Ultrasonic MEMS Gyro Resonance Neutralisation System (B.L.O.W. - Bistatic Locator and Oscillation Weapon)

## Source and Safety Note

This disclosure is prepared from the repository materials available in this checkout and the part-number examples named in the task prompt. The referenced "conversation after the delimiter" was not present in the Slack message. Where the repository describes operational steps for causing aircraft loss of control or for directed acoustic neutralisation, this document intentionally keeps those portions at a non-operational patent-disclosure level and omits directly actionable drive parameters, weapon timing, field-strength settings, targeting commands, and defeat procedures.

## 1. Title of the Invention

Passive Multi-Modal Drone Detection and Ultrasonic MEMS Gyro Resonance Neutralisation System (B.L.O.W. - Bistatic Locator and Oscillation Weapon)

## 2. Field of the Invention

The invention relates to counter-uncrewed-aerial-system (counter-UAS) sensing, passive radio-frequency and acoustic detection, electronic intelligence (ELINT), ultrasonic array processing, embedded field-programmable gate array (FPGA) signal processing, and multi-sensor target tracking. More particularly, the invention relates to a passive multi-modal drone detection system combining global navigation satellite system (GNSS) shadow or forward-scatter sensing, camera complementary metal-oxide-semiconductor (CMOS) clock emission direction finding, and passive ultrasonic altimeter ping time-difference-of-arrival (TDOA) sensing, with a shared-aperture acoustic countermeasure module described only at a non-operational level.

## 3. Background

Small uncrewed aircraft systems can be difficult to detect, identify, and track using a single sensing modality. Active radar systems radiate energy, may require spectrum licensing, can disclose the observer's location, and can be degraded by clutter, low radar cross section, and low-altitude multipath. Radio-frequency jammers radiate intentionally interfering energy, may be legally restricted, can be defeated by autonomous navigation, and may interfere with nearby communications, navigation, or emergency systems.

Optical and thermal camera systems can provide high-quality identification but require line of sight and may degrade under fog, glare, darkness, foliage, or occlusion. Acoustic propeller detection can be useful at close range but may suffer from wind noise, urban noise, and source variability. Conventional counter-UAS defeat mechanisms, including jamming and kinetic interceptors, can involve collateral-risk concerns, active emission signatures, regulatory constraints, and poor suitability for sensitive infrastructure.

The disclosed B.L.O.W. architecture addresses these limitations by using a passive, jam-resistant detection stack. The system relies on signals already present in the environment or emissions incidentally produced by the target: GNSS illumination, camera clock leakage, and ultrasonic altimeter pings. The modalities are fused through a tracking architecture that compensates for environmental effects and uncertainty. A shared acoustic aperture is described as supporting both passive sensing and a regulated, access-controlled countermeasure function, without disclosing operational defeat parameters.

## 4. Summary of the Invention

The B.L.O.W. system is a passive multi-modal drone detection and tracking architecture. In one embodiment, geographically separated GNSS receiving stations monitor carrier-to-noise density and early-late correlator distortion to detect GNSS shadowing or forward-scatter perturbations caused by an intervening air vehicle. In another embodiment, two or more ELINT stations use crossed-dipole antennas, coherent software-defined radio receivers, and direction-finding algorithms to estimate the bearing of camera CMOS clock emissions or harmonics. In another embodiment, a compact ultrasonic array passively listens for target altimeter or ranging pings and computes three-dimensional position from TDOA measurements.

The three sensing modalities are fused by an Unscented Kalman Filter (UKF), covariance intersection, and environmental compensation based on temperature and humidity. The same ultrasonic aperture used for passive sensing is also described as being capable of a controlled acoustic countermeasure mode directed toward MEMS inertial sensor resonance; however, operational parameters for disabling or crashing aircraft are intentionally omitted from this disclosure.

The acronym B.L.O.W. refers to "Bistatic Locator and Oscillation Weapon." In a safer implementation, the "oscillation" function may be implemented as a non-destructive test, alerting, deterrence, or laboratory-only characterization mode subject to safety interlocks and regulatory compliance.

## 5. Brief Description of the Drawings

- **Figure 1** is a system-level block diagram of the passive multi-modal B.L.O.W. architecture.
- **Figure 2** is a block diagram of a GNSS shadow and forward-scatter mapper.
- **Figure 3** is a block diagram of a camera CMOS clock ELINT direction-finding station pair.
- **Figure 4** is a block diagram of an ultrasonic passive ping TDOA array.
- **Figure 5** is a sensor-fusion flow diagram showing UKF prediction, environmental compensation, and covariance intersection.
- **Figure 6** is a shared-aperture receive/transmit acoustic architecture shown at a non-operational level.
- **Figure 7** is a hardware implementation block diagram showing processing, FPGA, data buses, and power management.
- **Figure 8** is a calibration and deployment sequence diagram.

## 6. Detailed Description

### 6.1 GNSS Shadow & Forward-Scatter Mapper

#### Overview

The GNSS mapper uses passive reception of GNSS L1 signals as illuminators of opportunity. A drone or other air vehicle crossing the line of sight between satellites and one or more ground receiving stations can create a measurable shadow, attenuation dip, multipath perturbation, or forward-scatter signature. The repository describes a GNSS-SDR patch that publishes GNSS tracking telemetry, including satellite PRN, carrier-to-noise density, and early-late correlation information. The prompt additionally names **Taoglas GPDF1575.A** and **Mini-Circuits ZX60-P162LN+** as part numbers to include in the invention disclosure.

#### Representative Components

- GNSS antenna: **Taoglas GPDF1575.A**.
- GNSS low-noise amplifier option: **Mini-Circuits ZX60-P162LN+**.
- Software-defined radio receiver: **USRP B210**.
- GNSS software receiver: GNSS-SDR with a repository-provided shadow-detector patch.
- Simulation and laboratory test equipment: **HackRF One**, `gps-sdr-sim`, and an **HMC624** programmable attenuator, used only in a shielded or cabled lawful test setup.

#### GNSS Telemetry Extraction

The GNSS-SDR tracking loop is modified to publish per-PRN telemetry. The repository patch adds telemetry fields corresponding to:

- `prn`: GNSS satellite identifier.
- `cn0`: estimated carrier-to-noise density.
- `early_late`: difference between early and late correlation values.
- `station_id`: receiving-station identifier for multi-station processing.
- `udp_host` and `udp_port`: telemetry destination parameters.

```text
                 GNSS satellites
                /       |       \
               /        |        \
      shadow / scatter  |  multipath perturbation
             v          v
       +-----------+  +-----------+       +-------------------+
       | Station 1 |  | Station N |  -->  | Shadow/Scatter    |
       | GNSS RX   |  | GNSS RX   |       | Mapper            |
       +-----------+  +-----------+       +-------------------+
             |              |                       |
             | PRN, CN0, early-late telemetry       |
             +--------------+-----------------------+
                            v
                    +---------------+
                    | Fusion Engine |
                    +---------------+
```

#### Detection Algorithm

The detector compares current GNSS observables against a station-specific and PRN-specific baseline. A simultaneous carrier-to-noise density deviation and early-late correlator distortion indicates a potential shadow or forward-scatter event. Multi-station correlation rejects isolated receiver noise and improves spatial localization.

```python
def update_gnss_shadow_tracks(telemetry, baselines, event_store):
    """
    Non-operational pseudocode derived from the repository's GNSS-SDR
    telemetry patch. Inputs are passive receiver observables only.
    """
    station_id = telemetry["station_id"]
    prn = telemetry["prn"]
    cn0 = telemetry["cn0"]
    early_late = telemetry["early_late"]

    baseline = baselines[(station_id, prn)]
    cn0_residual = cn0 - baseline.cn0_median
    shape_residual = early_late - baseline.early_late_median

    if baseline.is_shadow_like(cn0_residual, shape_residual):
        event_store.add(
            station_id=station_id,
            prn=prn,
            cn0_residual=cn0_residual,
            shape_residual=shape_residual,
            covariance=baseline.measurement_covariance(prn),
        )

    return event_store.correlate_multistation_events()
```

#### Forward-Scatter Localization

In one embodiment, each GNSS satellite and receiver station defines a bistatic geometry. A measured perturbation is associated with a locus near the satellite-station path, refined by time, satellite ephemeris, multi-PRN consistency, and multi-station agreement. The mapper outputs a probabilistic bearing or volume measurement rather than a deterministic point when the geometry is underconstrained.

### 6.2 Camera CMOS Clock ELINT Tracker

#### Overview

The ELINT tracker detects incidental emissions from drone camera electronics, including CMOS sensor clock leakage and harmonics. The repository describes crossed-dipole antenna stations feeding coherent receiver channels. The direction-finding subsystem estimates angle of arrival using phase differences and a MUSIC-style processing chain.

#### Representative Components

- Coherent receiver: **KerberosSDR**.
- Antenna structure: four crossed-dipole elements on an aluminum cross-boom.
- Dipole printed circuit boards: custom FR4, tuned around 100 MHz according to the repository notes.
- Balun: **Mini-Circuits T1-1T-KK81+**.
- ELINT low-noise amplifier: **Mini-Circuits PSA4-5043+**.
- Alternate LNA named in prompt: **Mini-Circuits ZX60-P162LN+**.
- Bias-tee power for LNAs.
- Example camera-clock harmonic named in repository setup notes: a 72 MHz harmonic observed during bench testing.

```text
      Drone camera module
     incidental clock leakage
              |
              v
     +------------------+        +------------------+
     | ELINT Station A  |        | ELINT Station B  |
     | crossed dipoles  |        | crossed dipoles  |
     | baluns + LNAs    |        | baluns + LNAs    |
     | KerberosSDR      |        | KerberosSDR      |
     +--------+---------+        +---------+--------+
              |                            |
              | phase-coherent I/Q         |
              +-------------+--------------+
                            v
                  +-------------------+
                  | MUSIC/DF Tracker  |
                  +-------------------+
```

#### Direction-Finding Algorithm

Each ELINT station receives a coherent multi-channel I/Q snapshot. After calibration, the algorithm estimates the spatial covariance matrix, decomposes signal and noise subspaces, scans a steering-vector model, and reports a bearing with covariance.

```python
def music_direction_find(iq_snapshot, steering_vectors, phase_offsets):
    """
    Pseudocode for CMOS clock ELINT direction finding.
    iq_snapshot: complex samples shaped [channels, samples].
    steering_vectors: candidate array responses indexed by bearing.
    phase_offsets: measured channel calibration offsets.
    """
    corrected = iq_snapshot * phase_offsets[:, None].conjugate()
    covariance = corrected @ corrected.conjugate().T / corrected.shape[1]

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    noise_subspace = eigenvectors[:, :-1]

    spectrum = {}
    for bearing, steering in steering_vectors.items():
        denom = steering.conjugate().T @ noise_subspace @ noise_subspace.conjugate().T @ steering
        spectrum[bearing] = 1.0 / max(abs(denom), 1e-12)

    best_bearing = max(spectrum, key=spectrum.get)
    return best_bearing, estimate_bearing_covariance(spectrum, best_bearing)
```

#### Calibration

The repository describes placing a signal generator with a small monopole at a known far-field location, injecting a 100 MHz tone, recording phase differences across four KerberosSDR channels, and storing the resulting phase-offset table for MUSIC processing. A health-monitor daemon checks phase coherence every 30 seconds and restarts a KerberosSDR synchronization service if drift exceeds 5 degrees.

### 6.3 Ultrasonic Altimeter Ping Passive Sonar Array

#### Overview

The ultrasonic subsystem passively listens for drone altimeter or ranging pings and estimates target position using TDOA. The repository implementation uses a 4 x 4 array of ultrasonic receiving tiles and a serial data path from FPGA to host. TDOA lags are solved into a three-dimensional position by Gauss-Newton iteration and smoothed by a Kalman filter.

#### Representative Components

- MEMS microphone upgrade: **Knowles SPU0410LR5H-2 -> Vesper VM3011 upgrade**.
- MEMS microphone in optimized bill of materials: **Vesper VM3011**.
- Ultrasonic transducer: **Murata MA40S4S**.
- Transmit/receive switch: **MAX14759ETA+**.
- Charge amplifier op amp: **OPA145IDBVR**.
- Band-pass filter op amp: **OPA2325IDGKR**.
- Analog-to-digital converter: **ADS127L11**.
- FPGA board: **Arty A7-35T** using **Artix-7 XC7A35T**.
- Environmental sensor for sound-speed correction: **Bosch BME280**.

```text
      passive ultrasonic ping
              |
              v
   +-----+-----+-----+-----+
   | Mic | Mic | Mic | Mic |
   +-----+-----+-----+-----+
   | Mic | Mic | Mic | Mic |
   +-----+-----+-----+-----+  4 x 4 array
   | Mic | Mic | Mic | Mic |  Vesper VM3011 / Murata MA40S4S tile family
   +-----+-----+-----+-----+
   | Mic | Mic | Mic | Mic |
   +-----+-----+-----+-----+
              |
              v
      +----------------+
      | FPGA TDOA Core |
      +----------------+
              |
              v
      +----------------+
      | Host Tracker   |
      +----------------+
```

#### Array Geometry

The repository `kalman_tracker.py` defines a 16-element array in a 4 x 4 grid with 4.25 mm nominal spacing:

```python
MIC_X, MIC_Y = np.meshgrid(np.arange(4) * 4.25e-3, np.arange(4) * 4.25e-3)
MIC_POS = np.column_stack((MIC_X.ravel(), MIC_Y.ravel(), np.zeros(16)))
```

#### TDOA Parsing and Position Solution

The repository tracker converts 16 signed lag bytes into TDOA values and solves position by Gauss-Newton iteration. The following non-defeat excerpt captures the passive localization logic:

```python
def parse_tdoa(data):
    """Convert 16 signed lag bytes to TDOA in seconds."""
    lags = np.array([(b - 31) for b in data[:16]], dtype=np.float64)
    return lags / 128000.0

def solve_position(x_initial, tdoas, mic_pos, sound_speed):
    """Gauss-Newton solver for 3D position from passive TDOA measurements."""
    x = x_initial.copy()
    for _ in range(5):
        d = np.sqrt(np.sum((x - mic_pos[1:]) ** 2, axis=1))
        d0 = np.sqrt(np.sum((x - mic_pos[0]) ** 2))
        f = d - d0 - tdoas[1:] * sound_speed
        J = (x - mic_pos[1:]) / d[:, None] - (x - mic_pos[0]) / d0
        delta = np.linalg.lstsq(J, -f, rcond=None)[0]
        x += delta
    return x
```

#### FPGA TDOA Processing

The repository setup notes name the following FPGA modules:

- `tdoa_core_optimized.v`
- `adc_reader.v`
- `pulse_detector.v`
- `capture_buffer_dualport.v`
- `tdoa_correlator_optimized.v`
- `uart_tx.v`

A representative passive receive-side Verilog skeleton is shown below. It is illustrative and omits implementation-specific details.

```verilog
module passive_tdoa_pipeline #(
    parameter CHANNELS = 16,
    parameter SAMPLE_BITS = 24,
    parameter LAG_BITS = 16
) (
    input  wire clk,
    input  wire rst,
    input  wire [CHANNELS*SAMPLE_BITS-1:0] adc_samples,
    input  wire sample_valid,
    output reg  [CHANNELS*LAG_BITS-1:0] lag_words,
    output reg  lag_valid
);
    wire pulse_seen;
    wire capture_done;

    pulse_detector u_detect (
        .clk(clk),
        .rst(rst),
        .sample_valid(sample_valid),
        .samples(adc_samples),
        .pulse_seen(pulse_seen)
    );

    capture_buffer_dualport u_capture (
        .clk(clk),
        .rst(rst),
        .trigger(pulse_seen),
        .samples(adc_samples),
        .done(capture_done)
    );

    always @(posedge clk) begin
        if (rst) begin
            lag_words <= 0;
            lag_valid <= 1'b0;
        end else if (capture_done) begin
            lag_words <= correlate_channels_to_reference();
            lag_valid <= 1'b1;
        end else begin
            lag_valid <= 1'b0;
        end
    end
endmodule
```

### 6.4 Sensor Fusion Architecture

#### Overview

The fusion architecture receives asynchronous measurements from GNSS shadow mapping, CMOS clock ELINT bearings, and ultrasonic TDOA localization. A six-dimensional target state is used in the repository fusion example:

```text
x = [position_x, position_y, position_z, velocity_x, velocity_y, velocity_z]
```

The repository `fusion_ukf.py` uses FilterPy's `UnscentedKalmanFilter` and `MerweScaledSigmaPoints` with a constant-velocity state transition. It also reads a **Bosch BME280** over I2C to compensate acoustic measurement noise for temperature and humidity.

```text
       GNSS shadow volume ----+
                              |
       ELINT bearing ---------+       +------------------+
                              +-----> | UKF + Covariance |
       Ultrasonic TDOA -------+       | Intersection     |
                                      +------------------+
                                                |
                  BME280 temp/RH ---------------+
                                                v
                                       fused drone pose
```

#### Environmental Compensation

The repository computes speed of sound from temperature and humidity:

```python
def get_sound_speed_from_bme280(temperature_c, relative_humidity_pct):
    c = 331.3 * np.sqrt(1 + temperature_c / 273.15)
    c *= 1 + 0.14 * (relative_humidity_pct / 100.0) * (temperature_c / 273.15)
    return c
```

Acoustic measurement covariance is then scaled as a function of the compensated sound speed:

```python
def ultrasonic_covariance(base_covariance, sound_speed):
    return base_covariance * (sound_speed / 343.0) ** 2
```

#### UKF State Propagation

```python
def state_transition(x, dt):
    F = np.eye(6)
    F[0, 3] = dt
    F[1, 4] = dt
    F[2, 5] = dt
    return F @ x

def measurement_func(x):
    return x[:3]
```

#### Covariance Intersection

The repository notes describe automatic covariance intersection when a new sensor track appears, with a default lambda parameter of 0.5. Covariance intersection provides a conservative fusion rule when cross-correlation between tracks is unknown.

```python
def covariance_intersection(x_a, P_a, x_b, P_b, lam=0.5):
    """
    Fuse two estimates without assuming independence.
    lam=0.5 is the repository's default tuning note.
    """
    inv_a = np.linalg.inv(P_a)
    inv_b = np.linalg.inv(P_b)
    P = np.linalg.inv(lam * inv_a + (1.0 - lam) * inv_b)
    x = P @ (lam * inv_a @ x_a + (1.0 - lam) * inv_b @ x_b)
    return x, P
```

### 6.5 Ultrasonic MEMS Gyro Resonator Kill Mechanism

#### Non-Operational Description

The repository describes a shared-aperture acoustic mode intended to interact with MEMS gyroscope resonances. Because directly enabling aircraft disablement or loss of control is unsafe and may be unlawful, this disclosure describes the countermeasure at a high level only. Specific defeat frequencies, acoustic intensities, phase-delay schedules, burst durations, target-command payloads, and field-use procedures are intentionally omitted.

In one embodiment, the same aperture that passively receives ultrasonic pings may be reconfigured under operator authorization into a controlled acoustic output mode. The output mode may be used in a lawful laboratory environment for MEMS inertial sensor susceptibility characterization, non-destructive deterrence research, or regulatory-compliant countermeasure testing. The architecture includes interlocks to prevent activation unless safety conditions, authorization conditions, geofence conditions, and target-confidence conditions are satisfied.

#### Representative Shared-Aperture Components

- Acoustic aperture tiles: 16 tile positions in the repository architecture.
- Microphone/transducer family: **Vesper VM3011** and **Murata MA40S4S**.
- T/R switch: **MAX14759ETA+**.
- High-speed switch device named in optimized BOM: **EPC2032 (GaN)**.
- Gate driver named in optimized BOM: **LMG1210**.
- Thermal management: **Peltier 40x40mm 12V 6A** TEC module.
- Power sequencing: **Texas Instruments UCD90120A**.

```text
        +-----------------------+
        | Passive RX processing |
        +-----------+-----------+
                    |
                    v
        +-----------------------+
        | Authorization, safety |
        | interlocks, geofence  |
        +-----------+-----------+
                    |
                    v
        +-----------------------+
        | Acoustic aperture     |
        | non-operational       |
        | countermeasure mode   |
        +-----------------------+
```

#### Safety Controls

The disclosed implementation may include:

- Positive operator authorization before any acoustic output mode.
- Laboratory-only mode for MEMS inertial sensor characterization.
- Automatic timeout logic.
- Thermal supervision of switching devices and transducers.
- Geofencing and line-of-sight confirmation.
- Human and animal exposure limits.
- Flight-safety and regulatory compliance checks.
- Logging and post-event audit trails.
- A receive-only default state.

### 6.6 Additional Embodiments

The task prompt requested additional embodiments including EMP, laser, and cyber-physical attacks. The repository materials inspected in this run did not provide enabling technical content for those embodiments. Accordingly, this disclosure treats them as reserved, non-enabled alternatives and does not provide operational details.

In non-operational terms, possible additional embodiments may include:

- A sensor-only variant with no active countermeasure hardware.
- A laboratory susceptibility-test variant for evaluating MEMS inertial sensors under controlled acoustic stimulation.
- A regulatory-compliant alerting variant that cues human operators, optical cameras, or lawful interdiction systems.
- A data-fusion-only variant that ingests third-party radar, optical, acoustic, or RF bearings.
- A simulation-only variant for GNSS shadow, ELINT, and ultrasonic TDOA algorithm validation.
- A safety-interlocked countermeasure interface that exposes only abstract authorization states and never stores actionable defeat parameters in field software.

### 6.7 Hardware Implementation

#### System Processing Hardware

The repository materials describe a central processing station based on a **Jetson Orin** or x86 PC, connected to a **USRP B210** for GNSS reception, **KerberosSDR** for ELINT reception, and an **Arty A7-35T** FPGA board over USB-UART and Ethernet. The FPGA target is **Artix-7 XC7A35T**.

```text
 +--------------------+       +------------------+
 | GNSS station(s)    | USB   |                  |
 | USRP B210          +------>+                  |
 +--------------------+       |                  |
                              | Jetson Orin or   |
 +--------------------+ USB   | x86 host         |
 | ELINT station(s)   +------>+ ROS2 / fusion    |
 | KerberosSDR        |       |                  |
 +--------------------+       +--------+---------+
                                       |
                                       | UART / Ethernet
                                       v
                              +------------------+
                              | Arty A7-35T FPGA |
                              | TDOA pipeline    |
                              +--------+---------+
                                       |
                                       v
                              +------------------+
                              | 16 acoustic tiles|
                              +------------------+
```

#### Optimized Bill of Materials

The optimized bill of materials in the repository names the following parts:

| Function | Part number or value | Quantity | Repository note |
| --- | --- | ---: | --- |
| MEMS microphone | **Vesper VM3011** | 16 | Replace SPU0410; recovers from acoustic overload |
| Original/upgrade note | **Knowles SPU0410LR5H-2 -> Vesper VM3011 upgrade** | 16 | Prompt-specified upgrade wording |
| Transducer | **Murata MA40S4S** | 16 | No change |
| T/R switch | **MAX14759ETA+** | 16 | No change |
| Charge amplifier OPA | **OPA145IDBVR** | 16 | No change |
| BPF op amp | **OPA2325IDGKR** | 16 | No change |
| TX FET | **EPC2032 (GaN)** | 16 | Replaces DRV8870 in optimized BOM |
| Gate driver | **LMG1210** | 16 | GaN-specific half-bridge driver |
| ADC | **ADS127L11** | 2 | No change |
| FPGA board | **Arty A7-35T** | 1 | No change |
| FPGA device | **Artix-7 XC7A35T** | 1 | Vivado target named in setup notes |
| Environmental sensor | **Bosch BME280** | 1 | Sound-speed correction |
| TEC module | **Peltier 40x40mm 12V 6A** | 1 | TX array cooling |
| Power sequencer | **UCD90120A** | 1 | Strict power-up timing |
| ELINT LNA | **Mini-Circuits PSA4-5043+** | 4 | One per dipole element |
| ELINT balun | **Mini-Circuits T1-1T-KK81+** | 4 | One per dipole element |
| GNSS antenna | **Taoglas GPDF1575.A** | station-dependent | Prompt-specified part |
| GNSS/ELINT LNA option | **Mini-Circuits ZX60-P162LN+** | station-dependent | Prompt-specified part |
| GNSS SDR | **USRP B210** | station-dependent | Repository setup note |
| ELINT SDR | **KerberosSDR** | station-dependent | Repository setup note |
| GNSS lab simulator | **HackRF One** | 1 | Repository simulation note |
| Programmable attenuator | **HMC624** | 1 | Repository simulation note |

#### PCB and Interconnect

The repository describes 25 mm x 25 mm four-layer ultrasonic tile boards fabricated from a KiCad design named `ultrasonic_tile.kicad_pcb`. It also describes custom FR4 dipole PCBs tuned around 100 MHz for the ELINT array. The acoustic tiles connect to the FPGA through a 40-pin ribbon-cable bus with shared power, shared SPI, per-tile chip-select lines, and control lines. Field-driving details for active acoustic output are not included here.

Representative receive-side interconnect from the repository:

- Pin 1: ground.
- Pin 2: shared +3.3 V.
- Pin 3: shared +5 V.
- Pin 4: transmit/receive control.
- Pins 6-9: shared SPI signals including SCLK, MOSI, MISO, and per-tile chip select.
- Sixteen per-tile chip-select FPGA GPIOs.

#### Power Management and Cooling

The repository describes a 24 V system bus, local conversion to 5 V using **LM7805**, conversion from 5 V to 3.3 V using **AMS1117-3.3**, a **UCD90120A** power sequencer, and a **Peltier 40x40mm 12V 6A** module for thermal management. This disclosure does not include operational acoustic drive power levels.

#### Host Runtime

The repository setup notes specify Ubuntu 22.04 with a PREEMPT_RT kernel, ROS2 Humble, `numpy`, `filterpy`, `pyserial`, `smbus2`, `bme280`, and optional Eclipse Iceoryx zero-copy ROS2 transport. The `setup_rt_kernel.sh` script isolates CPUs 2-3 for SDR and FPGA threads, configures IRQ affinity, adds real-time group limits, and requires a reboot.

### 6.8 Calibration and Deployment Procedures

#### GNSS Station Survey

Each GNSS antenna is placed at a permanent surveyed location. The repository notes specify using RTKLIB in static PPP mode to log 24 hours of L1 data, compute sub-centimeter antenna coordinates, and store those coordinates in the TDOA or localization solver configuration.

#### Ultrasonic Array Calibration

The repository describes mounting a fixed reference pinger at a surveyed location, including an example position two meters directly above the array center. The host runs `calibration.py`, collects TDOA offsets, and writes offsets to FPGA memory or host configuration.

```python
def calibrate_reference_pinger(serial_port, reference_position, channels=16):
    offsets = np.zeros(channels)
    measurements = collect_reference_tdoa_measurements(serial_port, reference_position)
    offsets[:] = estimate_static_channel_offsets(measurements, reference_position)
    serial_port.write(b"CAL " + offsets.tobytes())
    return offsets
```

#### ELINT Phase Calibration

The repository describes placing a signal generator and small monopole at a known far-field location, injecting a 100 MHz tone, recording phase differences across four KerberosSDR channels, and storing a phase-offset table for MUSIC processing.

#### Environmental Calibration

The **Bosch BME280** is connected over I2C. The fusion node samples temperature and humidity and adjusts acoustic covariance through the compensated speed of sound.

#### Health Monitoring

The repository `health_monitor_daemon.py` describes a process that checks KerberosSDR phase coherence every 30 seconds and restarts `kerberos_sync` if drift exceeds 5 degrees. The daemon also contemplates a test-signal injection path for channel-coherence verification.

#### Deployment Sequence

The source repository describes a deployment sequence in which GNSS shadow detection, CMOS ELINT tracking, ultrasonic TDOA listening, fusion, and health monitoring are launched in order. A safe receive-only deployment sequence is:

1. Start GNSS shadow detector stations and publish passive telemetry.
2. Start CMOS clock ELINT direction-finding stations.
3. Start ultrasonic passive TDOA listener and host tracker.
4. Start the fusion UKF node.
5. Start the health-monitor daemon.
6. Confirm fused tracks on the `/drone_pose` ROS2 topic.
7. Keep any countermeasure mode locked unless lawful authorization and safety controls are satisfied.

## 7. Claims

1. An apparatus for passive drone detection comprising at least one GNSS receiver configured to observe GNSS signal perturbations, at least one ELINT receiver configured to observe incidental camera clock emissions, at least one ultrasonic receiver array configured to observe airborne ultrasonic pings, and a fusion processor configured to combine outputs of the GNSS receiver, ELINT receiver, and ultrasonic receiver array into a target track.

2. The apparatus of claim 1, wherein the GNSS receiver is configured to estimate a carrier-to-noise density residual and an early-late correlation residual for a GNSS satellite PRN and to identify a GNSS shadow or forward-scatter event from said residuals.

3. The apparatus of claim 2, wherein multiple GNSS receiving stations correlate GNSS shadow or forward-scatter events across station identifiers and satellite PRNs to produce a probabilistic target measurement.

4. The apparatus of claim 1, wherein the GNSS receiver includes a Taoglas GPDF1575.A antenna, a Mini-Circuits ZX60-P162LN+ low-noise amplifier, or a USRP B210 software-defined radio receiver.

5. The apparatus of claim 1, wherein the ELINT receiver includes a crossed-dipole antenna array, a Mini-Circuits T1-1T-KK81+ balun, a Mini-Circuits PSA4-5043+ low-noise amplifier, and a KerberosSDR coherent receiver.

6. The apparatus of claim 1, wherein the ELINT receiver is configured to estimate direction of arrival of a CMOS camera clock emission or harmonic by forming a spatial covariance matrix, decomposing signal and noise subspaces, and evaluating a MUSIC direction-finding spectrum.

7. The apparatus of claim 1, wherein the ultrasonic receiver array comprises sixteen acoustic tile positions arranged as a four-by-four array.

8. The apparatus of claim 7, wherein each acoustic tile includes a Vesper VM3011 MEMS microphone, a Murata MA40S4S ultrasonic transducer, a MAX14759ETA+ transmit/receive switch, an OPA145IDBVR charge amplifier, an OPA2325IDGKR band-pass filter amplifier, or an ADS127L11 analog-to-digital converter.

9. The apparatus of claim 7, wherein the sixteen acoustic tile positions are arranged with nominal 4.25 mm spacing and are connected to an Artix-7 XC7A35T FPGA.

10. The apparatus of claim 1, wherein an FPGA TDOA core detects an ultrasonic pulse, captures multi-channel samples, computes lags relative to a reference channel, and reports said lags to a host tracker.

11. The apparatus of claim 10, wherein the host tracker computes a three-dimensional target estimate by Gauss-Newton iteration over TDOA residuals.

12. The apparatus of claim 1, wherein the fusion processor implements an Unscented Kalman Filter using a six-dimensional state comprising three position components and three velocity components.

13. The apparatus of claim 12, wherein the fusion processor adjusts ultrasonic measurement covariance according to a speed of sound estimated from temperature and humidity measured by a Bosch BME280 sensor.

14. The apparatus of claim 12, wherein the fusion processor performs covariance intersection with a tunable lambda parameter when fusing tracks with unknown cross-correlation.

15. The apparatus of claim 1, further comprising a health monitor configured to measure phase coherence of a coherent ELINT receiver and to restart a synchronization service when phase drift exceeds a threshold.

16. The apparatus of claim 1, further comprising a shared acoustic aperture configurable between a passive receive state and a controlled acoustic output state subject to authorization, geofence, timeout, thermal, and exposure-limit interlocks.

17. The apparatus of claim 16, wherein the controlled acoustic output state is configured for laboratory MEMS inertial sensor susceptibility characterization or other lawful non-destructive testing.

18. A method of passive drone detection comprising receiving GNSS telemetry, ELINT I/Q samples, and ultrasonic TDOA lags; estimating GNSS shadow events, camera clock bearings, and ultrasonic positions; compensating acoustic measurements for environmental conditions; and fusing said estimates into a target track.

19. The method of claim 18, further comprising calibrating GNSS station positions using static PPP, calibrating ultrasonic channel offsets using a surveyed reference pinger, calibrating ELINT phase offsets using a known far-field tone, and storing calibration data for real-time processing.

20. A non-transitory computer-readable medium storing instructions that, when executed by a processor or FPGA fabric, cause the system to publish GNSS shadow telemetry, compute ELINT direction-finding bearings, compute ultrasonic TDOA lags, perform UKF-based sensor fusion, and enforce safety interlocks for any shared-aperture acoustic output mode.

## 8. Abstract

A passive multi-modal drone detection system combines GNSS shadow or forward-scatter sensing, CMOS camera clock ELINT direction finding, and ultrasonic altimeter ping TDOA localization. GNSS receivers publish carrier-to-noise and early-late correlation telemetry; coherent ELINT stations estimate bearing to incidental camera clock emissions; and a four-by-four ultrasonic array computes passive TDOA positions. A fusion processor implements an Unscented Kalman Filter, environmental sound-speed compensation using a Bosch BME280 sensor, and covariance intersection for uncertain cross-sensor correlation. A shared acoustic aperture is described as configurable for receive operation and safety-interlocked laboratory acoustic output. The system uses COTS components including USRP B210, KerberosSDR, Arty A7-35T, Vesper VM3011, Murata MA40S4S, ADS127L11, MAX14759ETA+, EPC2032 (GaN), LMG1210, Mini-Circuits PSA4-5043+, Mini-Circuits T1-1T-KK81+, Mini-Circuits ZX60-P162LN+, and Taoglas GPDF1575.A.

## 9. Optimisation Notes

- **FPGA DSP mapping:** The repository names `tdoa_core_optimized.v` and `tdoa_correlator_optimized.v`, indicating that cross-correlation and lag extraction are intended to map efficiently onto FPGA DSP and BRAM resources.
- **Dual-port capture buffering:** The named `capture_buffer_dualport.v` module supports simultaneous sample capture and correlation access, reducing latency between ping detection and lag reporting.
- **Sub-sample interpolation:** The source request calls out sub-sample interpolation as an optimization; in this architecture it improves TDOA resolution beyond raw sample-period granularity.
- **GaN driver substitution:** The optimized BOM replaces DRV8870 with **EPC2032 (GaN)** and **LMG1210**, improving switching speed and thermal behavior for controlled acoustic-output research while remaining subject to safety interlocks.
- **MEMS microphone upgrade:** **Knowles SPU0410LR5H-2 -> Vesper VM3011 upgrade** improves recovery from high-SPL acoustic exposure and supports a shared receive/output aperture concept.
- **PREEMPT_RT kernel:** The repository setup script installs a real-time kernel, isolates CPUs 2-3, configures IRQ affinity, and grants real-time scheduling limits, reducing SDR and FPGA host-thread jitter.
- **Eclipse Iceoryx zero-copy transport:** The ROS2 `rmw_iceoryx_cpp` option reduces copy overhead for high-rate interprocess telemetry.
- **BME280 environmental compensation:** Temperature and humidity correction reduces acoustic range error by updating speed-of-sound-dependent measurement covariance.
- **Covariance intersection:** A default lambda value of 0.5 provides conservative track fusion when GNSS, ELINT, and ultrasonic estimates may have unknown correlation.
- **KerberosSDR phase health monitoring:** A 30-second phase-coherence check and service restart path limit ELINT bearing drift.
- **Peltier cooling:** The **Peltier 40x40mm 12V 6A** module provides thermal management for the acoustic tile assembly.
- **Power sequencing:** **UCD90120A** enforces strict power-up timing for mixed-signal and FPGA subsystems.
- **Static PPP GNSS survey:** 24-hour L1 logging with RTKLIB static PPP produces sub-centimeter station coordinates for improved passive geometry.
- **Reference-pinger ultrasonic calibration:** A surveyed reference pinger estimates static per-channel TDOA offsets and stores corrections in FPGA BRAM or host configuration.
- **Far-field ELINT phase calibration:** A known 100 MHz source produces per-channel phase offsets for MUSIC direction finding.
