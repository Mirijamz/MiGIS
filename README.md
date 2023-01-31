# MiGIS toolbox manual
MiGIS toolbox for QGIS 3 - digital soil and sediment thin section analysis

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS-script/blob/main/Manual_figures/workflow.png"
alt="MiGIS-Workflow"/>
</p>

## Short version
MiGIS was developed for digital spatial analysis and composition classification of soil and sediment thin sections in QGIS 3 3. The plugin is divided in three main parts to pre-process in [MiGIS 1](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_1_preprocess.py), train [MiGIS 2.1](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_2-1_train_algorithm.py) and classify [MiGIS 3](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_3_classification.py). In addition, training data set validity can be assessed in [MiGIS 2.2](https://github.com/Mirijamz/MiGIS-script/blob/main/MiGIS_2-2_ROI_eval.py). [Detailed processing](https://github.com/Mirijamz/MiGIS-script/tree/main#detailed-instructions) is described below, but summarised in the following.

### Integrate MiGIS into QGIS
The toolbox can be easily integrated into QGIS as a [Python processing script](https://docs.qgis.org/3.22/en/docs/user_manual/processing/toolbox.html). Besides native QGIS and GDAL geoprocessing algorithms, MiGIS also applies parts of the [Dzetsaka classification plugin for QGIS](https://github.com/nkarasiak/dzetsaka) (see Karasiak 2016). The Dzetsaka plugin must separately be added via the [QGIS extension manager]( https://docs.qgis.org/3.22/en/docs/training_manual/qgis_plugins/fetching_plugins.html). The Random Forest classifier, integrated via Dzetsaka, runs with the Python scipy library, thus scikit-learn (see Pedregosa et al. 2011) must be installed via the OSGeo shell (see [Dzetsaka classification plugin manual](https://github.com/nkarasiak/dzetsaka/blob/master/readme.md).
Commands for QGIS > 3.22:

`o4w_env`

`python3 -m pip install scikit-learn -U --user`

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


# Detailed instructions

### Required hardware
•	Transmitted light scanner/ film scanner or similiar hardware to capture thin sections

•	2x polarisation film for XPL imagery, 1x black opaque film for RL imagery

•	QGIS-capable computer (min.: 8GB RAM, 100GB free storage, CPU with 4 cores)

### Software
•	For digital image preprocessing: Inkscape (current: Inkscape 1.1.2)

•	GIS software: QGIS 3 (current: QGIS 3.22)

### Skills
•	GIS (QGIS) experience: navigate the GUI, Georeference raster data, create and edit vector data (polygons)

•	Basic knowledge of semi-automated image classification and accuracy assessment

•	Basic knowledge about the electromagnetic spectrum, light refraction, spectral signatures

•	Good training in micromorphology

### Micromorphological thin section scans
In micromorphology, different microscope light modes - PPL (Plane Polarized Light), XPL (Cross Polarised Light) and OIL (Oblique Incident Light) - are used to distinguish thin section components (e.g. minerals) by their specific light refraction properties in different polarisation modes. Using transmitted light scanning, the analytical oppurtunities of petrographic microscopy can be obtained for an entire thin section. PPL can be acquired by capturing the plain thin section in transmitted light scanning mode (TL - Transmitted Light). For XPL, two orthogonally aligned polarisation films (90° orientation offset) are added on top and below the thin section. Using ordinary flatbed scanning and a black (isotropic) film on top of the thin section, a RL (Reflected Light) image can be produced which is similar to OIL imagery.

## MiGIS integration (QGIS)
1.	Install the Dzetsaka Classification Plugin in QGIS (go to ‘Plugins’ and select ‘Manage and install plugins’).
2.	Install the Python machine learning library ‘scikit-learn’ using OSGeo shell (QGIS command line) typing:

    `o4w_env`
    
    `python3 -m pip install scikit-learn -U --user`

3.  For a detailed instruction check the documentation of [Dzetsaka classification plugin manual](https://github.com/nkarasiak/dzetsaka/blob/master/readme.md)
4.	Import the MiGIS Python scripts to your QGIS Project (Python symbol ([Python processing script](https://docs.qgis.org/3.22/en/docs/user_manual/processing/toolbox.html)) in ‘Processing toolbox’ tab) by ‘Adding Script to Toolbox’.
5.	After importing, all four parts of the toolbox are available in the QGIS ‘Processing toolbox’ (category ‘Scripts’, 'Python').

## Image classification basics & Random Forest Classifier
Among others, Machine Learning supported semi-supervised image classification is used to produce remote sensing products such as land cover maps. By the integration of multispectral information, different surface types can be identified, sorted and extracted by the classifier. MiGIS follows a similar approach by using bundled spectral information from TL, XPL and RL imagery (see [Transmitted light scanning](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#transmitted-light-scanning-canon-canoscan-9000f-mark-ii)) as classification input. To do this, it is necessary to spatial reference the RGB scan images (see [Stack images & spatial referencing]( https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#stack-images--spatial-referencing-using-image-processing-software-inkscape)), perform georeferentiation in QGIS (see [Georeference thin section imagery] (https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#georeference-thin-section-imagery-qgis-georeferencer)) and composite them to a multi-band raster ([see MiGIS 1](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-1-preprocess-ts-images)). Based on this data set, training areas (ROI - Regions of Interest) are collected using a costum vector polygon shapefile. Each ROI polygon should include an ID (unique, consecutive number) and be assigned to a user-defined class (one value per class). If necessary, a field with a class description (label) can be added. Each classification process requires at least two classes, each with a minimum of one ROI polygon. The selected area of each ROI polygon determines the number of pixels used for training the respective class. Each class should include approximately equal numbers of ROIs (pixel counts). Also, misclassifications might occur due to abundant similarity of pixel values between separate classes. ROI validity can be estimated before the actual classification by running [MiGIS 2.2](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-22-roi-evaluation-optional). Based on the training dataset a Random Forest classification model can be produced using [MiGIS 2.1](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-21-train-algorithm). After running the classification in [MiGIS 3](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-22-roi-evaluation-optional) its accuracy can be assessed when a reference training data set is provided and accordingly by the evaluation of the confusion matrix. Produced classification models can also be applied to other thin section scans. However, increased variation concerning sediment composition, embedding resin and thin section thickness, and image acquisition may produce misclassifications. 

MiGIS applies Scikit-learn Random Forest classifier with a fixed number of 100 trees. Splitting is performed at each internal tree node using the square root of the number of features e.g. max_features = sqrt(n_features):

When constructing each decision tree of the Random Forest, the Classifier will still use all the given features defined in the training data. But for the node splitting only a defined number (maximum features) is used. These maximum features are randomly selected from the training data (see also Pedregosa et al. 2011, Scikit-learn developers 2007-2022, Breiman 2001).



## Preprocessing

### Transmitted light scanning (Canon Canoscan 9000F Mark II)
•	Use the transmitted light mode for TL (Transmitted Light) and XPL (Cross-Polarised Light) thin section scanning. Some flatbed scanner come with stencils (film-holder) to lock the scan object’s position, (e.g. dia slides or film). They can be helpful to keep the thin section in position.

•	XPL scanning: One polarisation film is positioned below the thin section. The polarisation direction of the second film needs to be orthogonal (rotated 90°) to the first film to achieve cross-polarisation.

•	Regular flatbed scanning can be applied to produce RL (Reflected Light) images. Using the film-holder and black (isotropic, non-reflective) film on top of the thin section.

•	Choose high-resolution scanning mode (1200 dpi) without automated image adjustments.

•	If necessary, image brightness and contrast can be adjusted using raster image processing software (e.g. Adobe Photoshop, GIMP).

NOTE: Keep the same scanning position for each thin section: the geometry of produced TL/ XPL/ RL imagery can vary according to the scan position on the scan pad. It is recommended to use a stencil (e.g. film holder for transmitted light scans). To avoid reflectance artifacts it could be helpful to turn all thin sections upside down. reflection artefacts will then appear where the sample label is positioned on the glass slide.

### Stack images & spatial referencing using image processing software (Inkscape)

### Georeference thin section imagery (QGIS Georeferencer)


## MiGIS 1 preprocess TS images

## MiGIS 2.1 train algorithm

## MiGIS 2.2 ROI evaluation [optional]

## MiGIS 3 classification


