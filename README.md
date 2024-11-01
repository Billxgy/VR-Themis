# VR-Themis

A Virtual Reality Application Clone Detection Tool

*Download AssetStudio.Coarse and AssetStudio.Fine for VR-Themis from dependents or [link](https://zenodo.org/records/14024433)*


## Requirements

Python 3.10
Dotnet core 8.0

## Coarse-grained process stage

* **Statistical feature extraction**

```
$ python ./CoarseProcessStage/coarseStage.py
```

* **Clustering**

```
$ python ./CoarseProcessStage/Clustering/DBSCAN.py
```

## Fine-grained process Stage

Place `AssetStudio.Fine`, [dnSpy](https://github.com/dnSpy/dnSpy), and [Il2cppDumper](https://github.com/Perfare/Il2CppDumper) in their respective directories.

command line

```
$ python ./FineProcessStage/fineStage.py APK_DIRECTORY_PATH
```

