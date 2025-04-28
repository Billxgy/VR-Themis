# VR-Themis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![.NET](https://img.shields.io/badge/.NET-8.0-blue.svg)](https://dotnet.microsoft.com/download/dotnet/8.0)

A powerful tool for detecting VR application clones using two-stage analysis.

## Features

- Two-stage analysis (coarse-grained and fine-grained)
- Efficient processing for large-scale application dataset
- Accurate clone detection
- Design for VR-Specific features

## Requirements

- Python 3.10
- .NET Core 8.0
- Windows OS


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VR-Themis.git
cd VR-Themis
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install .NET Core 8.0 from [official website](https://dotnet.microsoft.com/download/dotnet/8.0)

4. Download and place required tools:
- AssetStudio.Coarse → `CoarseProcessStage/AssetStudio.Coarse/`
- AssetStudio.Fine → `FineProcessStage/AssetStudio.Fine/`
- dnSpy → `FineProcessStage/dnSpy/`
- Il2CppDumper → `FineProcessStage/IL2CPPDumper/`

## Usage

### Coarse-grained Analysis

1. Extract features:
```bash
python ./CoarseProcessStage/coarseStage.py
```

2. Run clustering:
```bash
python ./CoarseProcessStage/Clustering/DBSCAN.py
```

### Fine-grained Analysis

Run analysis:
```bash
python ./FineProcessStage/fineStage.py APK_DIRECTORY_PATH
```

## Project Structure

```
VR-Themis/
├── CoarseProcessStage/        # Coarse analysis
│   ├── AssetStudio.Coarse/    # Feature extraction tool
│   ├── Clustering/            # Clustering module
│   ├── coarseStage.py         # Main program
│   └── Studio.py              
├── FineProcessStage/          # Fine analysis
│   ├── AssetStudio.Fine/      # Asset extraction tool
│   ├── dnSpy/                 # Decompiler for Mono-based
│   ├── IL2CPPDumper/          # Decompiler for IL2CPP-based
│   ├── fineStage.py           # Main program
│   └── Studio.py              
└── Data/                      # Data storage
```
