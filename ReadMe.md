# ST3215 Servo Gripper

[![GitHub last commit](https://img.shields.io/github/last-commit/ThorstenBrach/ST3215-Servo-Gripper?style=for-the-badge)](https://github.com/ThorstenBrach/ST3215-Servo-Gripper/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ThorstenBrach/ST3215-Servo-Gripper?style=for-the-badge)](https://github.com/ThorstenBrach/ST3215-Servo-Gripper/issues)
[![GitHub stars](https://img.shields.io/github/stars/ThorstenBrach/ST3215-Servo-Gripper?style=for-the-badge)](https://github.com/ThorstenBrach/ST3215-Servo-Gripper/stargazers)
[![Build Type](https://img.shields.io/badge/Build-DIY%20Robotics-1f6feb?style=for-the-badge)](#de-ueberblick)
[![Files](https://img.shields.io/badge/CAD-STEP%20%2B%20STL-0a7d2a?style=for-the-badge)](#de-stl)
[![Assembly](https://img.shields.io/badge/Guide-25%20Assembly%20Steps-f59e0b?style=for-the-badge)](./Assembly/Readme.md)
[![BOM](https://img.shields.io/badge/BOM-Complete-informational?style=for-the-badge)](./Material/Readme.md)
[![Status](https://img.shields.io/badge/Status-Prototype-success?style=for-the-badge)](#de-roadmap)
[![Software](https://img.shields.io/badge/Software-In%20Development-orange?style=for-the-badge)](./Software/Readme.md)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-Keep%20a%20Changelog-blueviolet?style=for-the-badge)](./CHANGELOG.md)

<a id="language-selection"></a>

## Sprache / Language

- Deutsch: [Zur deutschen Version](#de-start)
- English: [Jump to English version](#en-start)

![Servo Gripper Overview](./Assembly/Overview.JPG)
![Servo Gripper Final](./Assembly/Final.JPG)

---

<a id="de-start"></a>

## Deutsch

[Zur Sprachauswahl](#language-selection)

Kompakter, kraftvoller ST3215 Servo Gripper zum Selberbauen mit 3D-Druckteilen, STEP-Modell, detaillierter Montageanleitung und kompletter Materialliste.

### Inhaltsverzeichnis

- [Projekt auf einen Blick](#de-ueberblick)
- [Demovideos](#de-videos)
- [Ordnerstruktur](#de-ordner)
- [Materialliste](#de-bom)
- [3D-Dateien (STL)](#de-stl)
- [CAD-Datei (STEP)](#de-step)
- [Montageanleitung](#de-assembly)
- [Software](#de-software)
- [Druck- und Setup-Hinweise](#de-hinweise)
- [Roadmap](#de-roadmap)
- [Mitwirken](#de-contrib)
- [Changelog](#de-changelog)
- [Lizenz](#de-license)

<a id="de-ueberblick"></a>

### Projekt auf einen Blick

| Thema | Details |
|---|---|
| Projekttyp | ST3215 Servo Gripper |
| Mechanik | 3D-gedruckte Baugruppen + Linearfuehrung MGN7H |
| Aktorik | Waveshare ST3215 Serial Bus Servo |
| CAD | STEP-Modell verfuegbar |
| Fertigung | STL-Dateien im Repository |
| Montage | Bebilderte Anleitung mit 25 Schritten |

<a id="de-videos"></a>

### Demovideos

- Gesamtansicht: [Overview.mp4](./Video/Overview.mp4)
- Krafttest: [Force.mp4](./Video/Force.mp4)
- Anwendung mit Flasche: [Beer Bottle.mp4](./Video/Beer%20Bottle.mp4)

![ST3215 Servo Gripper Overview GIF](./Video/Overview.gif)
![ST3215 Servo Gripper Force Test GIF](./Video/Force.gif)
![ST3215 Servo Gripper Beer Bottle GIF](./Video/Beer%20Bottle.gif)

<a id="de-ordner"></a>

### Ordnerstruktur

| Ordner | Inhalt |
|---|---|
| [Assembly](./Assembly/) | Schritt-fuer-Schritt-Montage inkl. Bilder |
| [Material](./Material/) | Materialliste mit Mengen, Kosten und Links |
| [Software](./Software/) | Steuerungs-Software (in Entwicklung) |
| [Step](./Step/) | CAD-Datei im STEP-Format |
| [STL](./STL/) | Druckdateien fuer alle Bauteile |
| [Video](./Video/) | Demo- und Funktionstest-Videos |

<a id="de-bom"></a>

### Materialliste

- [Material/Readme.md](./Material/Readme.md)

<a id="de-stl"></a>

### 3D-Dateien (STL)

- [Baseplate.stl](./STL/Baseplate.stl)
- [Finger_1.stl](./STL/Finger_1.stl)
- [Finger_2.stl](./STL/Finger_2.stl)
- [Motorhousing.stl](./STL/Motorhousing.stl)
- [Motorhousing Cover.stl](./STL/Motorhousing%20Cover.stl)
- [Schwing Arm 1.stl](./STL/Schwing%20Arm%201.stl)
- [Schwing Arm 2.stl](./STL/Schwing%20Arm%202.stl)
- [Turnhead.stl](./STL/Turnhead.stl)

<a id="de-step"></a>

### CAD-Datei (STEP)

- [Gripper.step](./Step/Gripper.step)

<a id="de-assembly"></a>

### Montageanleitung

- [Assembly/Readme.md](./Assembly/Readme.md)

![Assembly Step 01](./Assembly/Step%2001.JPG)
![Assembly Step 12](./Assembly/Step%2012.JPG)
![Assembly Step 25](./Assembly/Step%2025.JPG)

<a id="de-software"></a>

### Software

> **In Entwicklung** — Geplant sind Python- und IEC 61131-3-Implementierungen.
> In der Zwischenzeit kann die Software des SO-101-Projekts direkt verwendet werden — gleicher Servo, gleicher Treiber.

- [Software/Readme.md](./Software/Readme.md)

<a id="de-hinweise"></a>

### Druck- und Setup-Hinweise

- Gewindeeinsaetze sauber und buendig einschmelzen.
- Bewegliche Baugruppen nach Montage auf Leichtgaengigkeit pruefen.
- Schraubenlaengen bei Toleranzabweichungen fein nacharbeiten.
- Erste Funktionstests ohne Last durchfuehren.

<a id="de-roadmap"></a>

### Roadmap

- [ ] Python-Bibliothek fuer direkte Greifer-Steuerung
- [ ] IEC 61131-3 Funktionsbaustein fuer SPS-Steuerungen
- [ ] Parametrische Varianten fuer unterschiedliche Hubwege
- [ ] Standardisierte Test- und Kalibriersequenz
- [ ] Erweiterte Kompatibilitaet mit weiteren Servo-Treibern

<a id="de-contrib"></a>

### Mitwirken

Issues und Pull Requests sind willkommen.

<a id="de-changelog"></a>

### Changelog

Alle Versionen und Änderungen: [CHANGELOG.md](./CHANGELOG.md)

<a id="de-license"></a>

### Lizenz

MIT — siehe [LICENSE](./LICENSE)

[Zur Sprachauswahl](#language-selection)

---

<a id="en-start"></a>

## English

[Back to language selection](#language-selection)

Compact, high-torque ST3215 Servo Gripper with 3D-printed parts, STEP model, detailed assembly guide, and complete bill of materials.

### Table of Contents

- [Project Overview](#en-overview)
- [Demo Videos](#en-videos)
- [Folder Structure](#en-folders)
- [Bill of Materials](#en-bom)
- [3D Files (STL)](#en-stl)
- [CAD File (STEP)](#en-step)
- [Assembly Guide](#en-assembly)
- [Software](#en-software)
- [Print and Setup Notes](#en-notes)
- [Roadmap](#en-roadmap)
- [Contributing](#en-contrib)
- [Changelog](#en-changelog)
- [License](#en-license)

<a id="en-overview"></a>

### Project Overview

| Topic | Details |
|---|---|
| Project Type | ST3215 Servo Gripper |
| Mechanics | 3D-printed assemblies + MGN7H linear rail |
| Actuation | Waveshare ST3215 serial bus servo |
| CAD | STEP model available |
| Manufacturing | STL files included |
| Assembly | Illustrated guide with 25 steps |

<a id="en-videos"></a>

### Demo Videos

- Full overview: [Overview.mp4](./Video/Overview.mp4)
- Force test: [Force.mp4](./Video/Force.mp4)
- Bottle handling demo: [Beer Bottle.mp4](./Video/Beer%20Bottle.mp4)

![ST3215 Servo Gripper Overview GIF](./Video/Overview.gif)
![ST3215 Servo Gripper Force Test GIF](./Video/Force.gif)
![ST3215 Servo Gripper Beer Bottle GIF](./Video/Beer%20Bottle.gif)

<a id="en-folders"></a>

### Folder Structure

| Folder | Content |
|---|---|
| [Assembly](./Assembly/) | Step-by-step build guide with images |
| [Material](./Material/) | Bill of materials with quantities and links |
| [Software](./Software/) | Control software (in development) |
| [Step](./Step/) | CAD source file in STEP format |
| [STL](./STL/) | Printable files for all parts |
| [Video](./Video/) | Demo and test videos |

<a id="en-bom"></a>

### Bill of Materials

- [Material/Readme.md](./Material/Readme.md)

<a id="en-stl"></a>

### 3D Files (STL)

- [Baseplate.stl](./STL/Baseplate.stl)
- [Finger_1.stl](./STL/Finger_1.stl)
- [Finger_2.stl](./STL/Finger_2.stl)
- [Motorhousing.stl](./STL/Motorhousing.stl)
- [Motorhousing Cover.stl](./STL/Motorhousing%20Cover.stl)
- [Schwing Arm 1.stl](./STL/Schwing%20Arm%201.stl)
- [Schwing Arm 2.stl](./STL/Schwing%20Arm%202.stl)
- [Turnhead.stl](./STL/Turnhead.stl)

<a id="en-step"></a>

### CAD File (STEP)

- [Gripper.step](./Step/Gripper.step)

<a id="en-assembly"></a>

### Assembly Guide

- [Assembly/Readme.md](./Assembly/Readme.md)

![Assembly Step 01](./Assembly/Step%2001.JPG)
![Assembly Step 12](./Assembly/Step%2012.JPG)
![Assembly Step 25](./Assembly/Step%2025.JPG)

<a id="en-software"></a>

### Software

> **Work in progress** — Python and IEC 61131-3 implementations are planned.
> Until then, the SO-101 project software works directly — same servo, same driver.

- [Software/Readme.md](./Software/Readme.md)

<a id="en-notes"></a>

### Print and Setup Notes

- Install threaded inserts flush with the surface.
- Verify smooth motion of all moving parts after assembly.
- Adjust screw lengths if tolerances differ between printers.
- Run first functional tests without payload.

<a id="en-roadmap"></a>

### Roadmap

- [ ] Python library for direct gripper control
- [ ] IEC 61131-3 function block for PLC integration
- [ ] Parametric variants for different stroke lengths
- [ ] Standardized calibration and test routine
- [ ] Extended compatibility with additional servo controllers

<a id="en-contrib"></a>

### Contributing

Issues and pull requests are welcome.

<a id="en-changelog"></a>

### Changelog

All versions and changes: [CHANGELOG.md](./CHANGELOG.md)

<a id="en-license"></a>

### License

MIT — see [LICENSE](./LICENSE)

[Back to language selection](#language-selection)
