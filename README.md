# MiGIS toolbox manual
MiGIS toolbox for QGIS 3 - digital soil and sediment thin section analysis

![MiGIS-Workflow](https://github.com/Mirijamz/MiGIS-script/blob/main/Manual_figures/workflow.png)

## Short version
This toolbox was developed for the digital spatial analysis and composition classification of soil and sediment thin sections in QGIS 3. The plugin is divided in three main parts to pre-process in [MiGIS 1](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_1_preprocess.py), train [MiGIS 2.1](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_2-1_train_algorithm.py) and classify [MiGIS 3](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_3_classification.py). In addition, training data set validity can be assessed in [MiGIS 2.2](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_2-2_ROI_eval.py). Detailed processing are described below and summarised in the following.

### Integrate MiGIS into QGIS
MiGIS Toolbox is based on the QGIS Graphical Modeler (see [QGIS documentation](https://docs.qgis.org/3.22/en/docs/index.html)) and can therefore be easily integrated into QGIS as a [Python processing script](https://docs.qgis.org/3.22/en/docs/user_manual/processing/toolbox.html). Besides native QGIS and GDAL geoprocessing algorithms, MiGIS also applies parts of the [Dzetsaka classification plugin for QGIS](https://github.com/nkarasiak/dzetsaka) (see Karasiak 2016). The Dzetsaka plugin must separately be added via the [QGIS extension manager]( https://docs.qgis.org/3.22/en/docs/training_manual/qgis_plugins/fetching_plugins.html). The Random Forest classifier, integrated via Dzetsaka, runs with the Python scipy library, thus scikit-learn (see Pedregosa et al. 2011) must therefore be installed via the OSGeo shell (see [Dzetsaka classification plugin manual](https://github.com/nkarasiak/dzetsaka/blob/master/readme.md).

### Imagery aquisition
Up to three high-resolution RGB images of a thin section, for example a transmitted light (TL), cross-polarised (XPL) and reflected light (RL) image are required. The described workflow is adapted to soil and sediment micromorphology, a section size of 6x8 cm and flatbed scan acquired imagery with a resolution of 1200 dpi, but can be adapted to other application areas and section types and sizes.

### Geoeferencing
Before importing the imagery into QGIS, spatial reference points have to be created using image processing software (see Inkscape template file: [MiGIS_TS_ref_temp.svg](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_TS_ref_temp.svg)). These reference points match the dimensions provided by [MiGIS_georef.points](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_georef.points) and are used for straightforward georeferentiation, using QGIS Georeferencer and a metric CRS (coordinate reference system), for example UTM. 

### Classification training
For the semi-supervised classification approach, user defined ROIs (Regions of Interest) should cover the variety of the thin section’s composition: pore space, groundmass, coarse fraction (e.g. quartz), organic remains (e.g. charcoal), pedofeatures such as clay coatings, iron oxide nodules and precipitates (e.g. micrite). Create a new polygon shapefile and add numeric class (integer) and a class description/label (string) field to the ROIs.

### Classification and quantification
After creating the classification model in MiGIS 2.1 and based on the cropped multi-band raster of MiGIS 1, it can be classified in MiGIS 3. For the accuracy assessment, the creation of a confusion matrix, another training dataset with independent reference ROIs must be available. Based on the classification map created by MiGIS 3, class area statistics (in m²) are also generated.

### Related publication: 
Zickel, M., Kehl, M., Gröbner, M. o(in prep.). MiGIS: Digital soil and sediment thin sections analyses using an open-source GIS Machine Learning approach. Applied Computing and Geosciences.

### This work is based on:
Breiman, L., 2001. “Random Forests”. Machine Learning, 45 (1), 5-32.

GDAL/OGR contributors, 2022. GDAL/OGR Geospatial Data Abstraction software Library. Open Source Geospatial Foundation. URL https://gdal.org , DOI: 10.5281/zenodo.5884351

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin. https://github.com/nkarasiak/dzetsaka/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, É., 2011. Scikit-learn: Machine Learning in Python, JMLR 12, 2825-2830.

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html


### Cite toolbox: 
Zickel, M., Kehl, M., Gröbner, M., 2023. MiGIS toolbox. https://github.com/Mirijamz/MiGIS-script

Bibtex reference:
```
@misc{zickel2023MiGIS,
title={MiGIS toolbox},
author={Mirijam Zickel and Martin Kehl and Marie Gröbner},
url={https://github.com/Mirijamz/MiGIS-script},
year={2023},
doi={XXXX}
}
```

## Detailed instructions

### Required hardware
•	Transmitted light scanner
•	Polarisation film, black opaque film
•	QGIS-capable computer (min.: 8GB RAM, 100GB free storage, CPU with 4 cores)

### Software
•	For digital image preprocessing: Inkscape (current: Inkscape 1.1.2)
•	GIS software: QGIS 3 (current: QGIS 3.22)

### Skills
•	Basic GIS (QGIS) experience: Georeference raster data, create and edit vector data (polygons)
•	Basic knowledge of semi-automated image classification and accuracy assessment
•	Basic knowledge about the electromagnetic spectrum, light refraction, spectral signatures
•	Good training in micromorphology

## MiGIS integration (QGIS)
1.	Install the Dzetsaka Classification Plugin in QGIS (go to ‘Plugins’ and select ‘Manage and install plugins’). If SAGA GIS is not installed yet, please add the current version using the OSGEO setup.
2.	Install the Python machine learning library ‘scikit-learn’ using the OSGeo shell (QGIS command line). For a detailed instruction check the documentation of Karasiak 2021: https://github.com/nkarasiak/dzetsaka
3.	Import the MiGIS Python scripts to your QGIS Project (Python symbol in ‘Processing toolbox’ tab) by ‘Adding Script to Toolbox’.
4.	After importing, all four parts of the toolbox are available in the QGIS ‘Processing toolbox’ (category ‘Scripts’).



### Micromorphological thin section scans
In micromorphology, different microscope light modes - PPL (Plane Polarized Light), XPL (Cross Polarised Light) and OIL (Oblique Incident Light) - are used to distinguish thin section components (e.g. minerals) by their specific light refraction properties in different polarisation modes. Using transmitted light scanning, the analytical oppurtunities of petrographic microscopy can be obtained for an entire thin section. PPL can be acquired by capturing the plain thin section in transmitted light scanning mode (TL - Transmitted Light). For XPL, two orthogonally aligned polarisation films (90° orientation offset) are added on top and below the thin section. Using ordinary flatbed scanning and a black (isotropic) film on top of the thin section, a RL (Reflected Light) image can be produced which is similar to OIL imagery.


