# onboardapi - digital twin

This **demo application** serves as a **sandbox** and **example use case** for exploring the [onboardapi](https://github.com/Rheinmetall/onboardapi) and gaining practical understanding through **hands‑on application**.

### Scenario

- **Drone** takes off from a **3 × 3 km valley**.
- The valley is under **heightened fire protection**.
- **Sequentially** reported are **unextinguished campfires** that the **drone** must **investigate**.
- Investigation succeeds when the **campfire** is **visible** on the drone’s camera to a sufficient extent (also reachable via **zoom**).
- Once a **campfire** has been **investigated**, it is **extinguished**, and the **next position** is announced.
- The cycle **repeats**.

> This simulation demonstrates how the `OnboardAPI` can be leveraged to control drone navigation and sensor data for **campfire detection and suppression**.

### Minimal system requirements

| Operating System | Operating System Version                          | CPU                                                               | Graphics API                                 |
|------------------|---------------------------------------------------|-------------------------------------------------------------------|----------------------------------------------|
| Windows          | Windows 10 version 21H1 (build 19043) or newer    | x86 / x64 with SSE2 support                                       | DX11                                         |


### Interfaces opened by the application

| Service    | Client | Interface Name |
| -------- | ------- | ------- |
| MultiMount  | - | MultiMount |
| CoordinateFrame | - | CoordinateFrame |
| Camera | - | Camera |
| -    | HidJoystick | HidJoystick |
| ObjectManager | - | ObjectManager |

The interfaces are opened on Domain Id **2**.

### Interfaces you should open to communicate with the application

| Service    | Client | Interface Name |
| -------- | ------- | ------- |
| -  | MultiMount | MultiMount |
| - | CoordinateFrame | CoordinateFrame |
| - | Camera | Camera |
| HidJoystick    | - | HidJoystick |
| - | ObjectManager | ObjectManager |

# Supported messages in this application

## 🚁 Drone

**Message**: `HidJoystick → ReportAxis`

| Parameter     | Type   | Description              | Range            |
|---------------|--------|--------------------------|------------------|
| `KeyAxisIndex`| int    | Axis index (0 – 3)       | 0 – 3            |
| `Value`       | float  | Movement value           | -1.0 – 1.0       |

| `KeyAxisIndex` | Axis      | Direction (Left/Right, etc.) |
|----------------|-----------|------------------------------|
| 0              | X‑Axis    | Left / Right                 |
| 1              | Z‑Axis    | Forward / Backward           |
| 2              | Y‑Rotation| Yaw Left / Yaw Right         |
| 3              | Y‑Axis    | Down / Up                    |

---

## 🔗 Gimbal (attached to the Drone)

**Message**: `HidJoystick → ReportAxis`

| Parameter     | Type   | Description              | Range            |
|---------------|--------|--------------------------|------------------|
| `KeyAxisIndex`| int    | Axis index (4 – 6)       | 4 – 6            |
| `Value`       | float  | Movement value           | -1.0 – 1.0       |

| `KeyAxisIndex` | Axis      | Direction (Left/Right, etc.) |
|----------------|-----------|------------------------------|
| 4              | Y‑Rotation| Yaw Left / Yaw Right         |
| 5              | X‑Rotation| Pitch Down / Pitch Up        |
| 6              | Z‑Rotation| Roll Left / Roll Right       |

---

**Message**: `MultiMount → NotifyAxisRotations`

| Parameter     | Type   | Description                             |
|---------------|--------|-----------------------------------------|
| `AxisRotations`| array | One or more rotation commands           |

Each element:

| Field   | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| `AxisId`| string | `"Yaw"`, `"Pitch"`, or `"Roll"`             |
| `Angle` | float  | Relative angle (no limit) ‑360 ° → 360 °   |


## 📷 Camera (on the Gimbal)

**Message**: `Camera → ConfigZoomLevel`

| Parameter | Type  | Description | Range |
|-----------|-------|-------------|-------|
| `Level`   | float | Zoom level  | 0.0 – 7.0 |

---

## 📊 Quick‑Reference Table

| Device  | Message                           | Parameters                          | Notes                     |
|---------|-----------------------------------|-------------------------------------|---------------------------|
| Drone   | `HidJoystick → ReportAxis`        | `KeyAxisIndex`, `Value` (0 – 3)      |                           |
| Gimbal  | `HidJoystick → ReportAxis`        | `KeyAxisIndex`, `Value` (4 – 6)      |                           |
| MultiMount | `NotifyAxisRotations`            | `AxisRotations[ {AxisId, Angle} ]` | Unlimited relative angles |
| Camera  | `Camera → ConfigZoomLevel`        | `Level` (0.0 – 7.0)                 |                           |

## Keyboard input

|Key       | Action              |
|----------|---------------------|
|W         | Fly forward         |
|A         | Fly left            |
|S         | Fly backward        |
|D         | Fly right           |
|Q         | Turn left           |
|E         | Turn right          |
|Space     | Fly upwards         |
|Left Ctrl | Fly downwards       |
|Left      | Move camera left    |
|Up        | Move camera up      |
|Right     | Move camera right   |
|Down      | Move camera down    |
|ESC       | Exit                |

## Python sample controller

`examples/OnboardAPISampleController.py` shows a sample implementation for controlling the drone over keyboard.
The sample application needs to listen to the external HidJoystick inputs. Therefore the internal inputs have to
be disabled by setting `EnableApplicationControllerInput` to `false` in the `OnboardAPISettings.json` config file of the application.

### Dependencies:

See `requirements.txt`.

to be installed via

```shell
python -m pip install -r requirements.txt
```

*Happy coding!*

## Credits:

Sound Effect by <a href="https://pixabay.com/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=24258">freesound_community</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=24258">Pixabay</a>

## License

This project consists of two parts with different licensing terms:

- **Sample codes and presets:** Licensed under [Eclipse Public License 2.0](LICENSE-EPL-2.0.txt).
- **Binary:** Distributed under [EULA-RME-SDK-1.0](EULA-RME-SDK-1.0.txt).

##  Disclaimer

Your use is governed solely by the terms of the LICENSE file in this repository. Where explicitly indicated in individual source files, a Secondary License may apply; the respective license notices control.

The software is provided “as is,” without warranties or representations of any kind, express or implied, including but not limited to merchantability, fitness for a particular purpose, and non infringement. To the extent permitted by law, liability is disclaimed. Mandatory statutory rights remain unaffected, including liability for intent, gross negligence, and for injury to life, body, or health.

There is no entitlement to support, maintenance, or updates. Community support may be provided on a voluntary, best effort basis via GitHub issues. Any commercial offerings or SLAs, if available, are separate and not part of this project. For commercial support inquiries, please contact: opensource.rme@rheinmetall.com.

Please report security vulnerabilities confidentially according to the SECURITY policy at opensource.rme@rheinmetall.com and do not post sensitive or personal information in public issues. For details, see SECURITY.md.

By contributing to this project, you confirm you have the rights necessary to license your contributions and you license them under the EPL 2.0. The rules in CONTRIBUTING.md apply; depending on the project, a DCO sign off or a Contributor License Agreement (CLA) may be required.

Company and product names and logos in this repository are trademarks or trade names of Rheinmetall/onboardapi No trademark or naming rights are granted by the license. Any use requires prior written consent.

Use, distribution, and import of this software may be subject to export control, sanctions, and other applicable laws. You are responsible for complying with all applicable requirements.
In case of any discrepancy, the LICENSE text prevails. This notice is for convenience only and does not modify the license.