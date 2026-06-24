# Changelog

All notable changes to this project will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.0.9] — 2026-06-24

### Added
- Added ESP32 Arduino firmware project (`Software/ESP32/TcpIp_Server`) for servo control via web UI and TCP/IP server.
- Added DIN rail holder CAD/STL assets to project documentation:
	- `Step/DIN Rail Holder Serial Board.step`
	- `STL/DIN Rail Holder Serial Board.stl`
	- `Assembly/DIN Rail Holder.jpeg`
- Added dedicated ESP32 documentation in `Software/ESP32/Readme.md`.

### Changed
- Updated `ReadMe.md` (DE/EN) to include DIN rail holder image preview and links for the new STEP/STL files.
- Updated `Software/Readme.md` (DE/EN) with a direct reference to the ESP32 firmware documentation.
- Expanded `Software/ESP32/Readme.md` with:
	- fixed, tested Arduino package/library version set
	- explicit separation of USB serial monitor baud (`115200`) and servo UART baud (`1000000`)
	- TCP/IP server command reference and usage examples

---

## [1.0.8] — 2026-06-05

### Changed
- Corrected some scew lengths in BOM list ( bill of material )
- Corrected the depth for the hex holes in the base plate, so that a M2x20 screw can be screwed in - before the screw was to short
- Corrected the hole diameter of the 4 flange holes ( it is now for M3 heat inserts instead of M4 heat inserts)
- Corrected the hight of the swingarms
- Updated STL Files accordingly
- Updated STP File accordingly

---
## [1.0.7] — 2026-06-04

### Changed
- Added donate button and badges

## [1.0.6] — 2026-05-30

### Changed
- enlarge counterbores in turning head by 0.5 mm


## [1.0.5] — 2026-05-30

### Changed
- Modified Final.JPG and Tools.JPG, so that git recognized a change and I am now able to push the changes

## [1.0.4] — 2026-05-30

### Changed
- Renamed Tools.jpg to Tools.JPG, so that it will no be displayed in the readme.md 

## [1.0.3] — 2026-05-30

### Changed
- Removed vlc-help.txt file which was accidentally added
- Renamed Final.jpg to Final.JPG, so that it will no be displayed in the readme.md 

## [1.0.2] — 2026-05-30

### Changed
- Added animated GIF previews for the demo videos in the main README.
- Standardized the project naming in the README files to ST3215 Servo Gripper.


## [1.0.1] — 2026-05-30

### Changed


## [1.0.0] — 2026-05-30

### Added
- initial version
