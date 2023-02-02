# MiGIS toolbox for QGIS 3 - digital soil and sediment thin section analysis

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/workflow.png"
alt="MiGIS-Workflow"/>
</p>

## Short version
MiGIS was developed for digital spatial analysis and composition classification of soil and sediment thin sections in QGIS 3 3. The plugin is divided in three main parts to pre-process in [MiGIS 1](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_1_preprocess.py), train [MiGIS 2.1](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_2-1_train_algorithm.py) and classify [MiGIS 3](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_3_classification.py). In addition, training data set validity can be assessed in [MiGIS 2.2](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_2-2_ROI_eval.py). [Detailed processing](https://github.com/Mirijamz/MiGIS/tree/main#detailed-instructions) is described below, but summarised in the following.

### Integrate MiGIS into QGIS
The toolbox can be easily integrated into QGIS as a [Python processing script](https://docs.qgis.org/3.22/en/docs/user_manual/processing/toolbox.html). Besides native QGIS 3 (QGIS Development Team, 2022) and GDAL (GDAL/OGR contributors 2022) geoprocessing algorithms, MiGIS also applies parts of the [Dzetsaka classification plugin for QGIS](https://github.com/nkarasiak/dzetsaka) (see Karasiak 2016). The Dzetsaka plugin must be added separately via the [QGIS extension manager]( https://docs.qgis.org/3.22/en/docs/training_manual/qgis_plugins/fetching_plugins.html). The Random Forest classifier, integrated via Dzetsaka, runs with the Python scipy library, thus scikit-learn (see Pedregosa et al. 2011) must be installed via the OSGeo shell (see [Dzetsaka classification plugin manual](https://github.com/nkarasiak/dzetsaka/blob/master/readme.md).
Commands for QGIS > 3.22:

`o4w_env`

`python3 -m pip install scikit-learn -U --user`

### Imagery aquisition
Up to three high-resolution RGB images of a thin section, for example a transmitted light (TL), cross-polarised (XPL) and reflected light (RL) image are required. The described workflow is adapted to soil and sediment micromorphology, a section size of 6x8 cm and flatbed scan acquired imagery with a resolution of 1200 dpi, but can be adapted to other application areas and section types and sizes.

### Geoeferencing
Before importing the imagery into QGIS, spatial reference points have to be created using image processing software (see Inkscape template file: [MiGIS_TS_ref_temp.svg](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_TS_ref_temp.svg)). These reference points match the dimensions provided by [MiGIS_georef.points](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_georef.points) and are used for straightforward georeferentiation, using QGIS Georeferencer and a metric CRS (coordinate reference system), for example UTM. 

### Classification training
For the semi-supervised classification approach, user defined ROIs (Regions of Interest) should cover the variety of the thin section’s composition: pore space, groundmass, coarse fraction (e.g. sand/gravel), organic remains (e.g. charcoal), pedofeatures such as clay coatings, iron oxide nodules and precipitates (e.g. micrite). To collect ROIs in a training data set, create a new polygon shapefile layer with a numeric class (integer) and a class description/label (string) field.

### Classification and quantification
After creating the classification model in[MiGIS 2.1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-21-train-algorithm) and based on the (cropped) multi-band raster of [MiGIS 1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-1-preprocess-ts-images), it can be classified in [MiGIS 3](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-22-roi-evaluation-optional). For the accuracy assessment, the creation of a confusion matrix, another training dataset with independent reference ROIs must be available. Based on the classification map created with MiGIS 3, class area statistics (in m²) are also generated.

(see [MiGIS 1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-1-preprocess-ts-images)). Based on this data set, training areas (ROI - Regions of Interest) are collected using a costum vector polygon shapefile. Each ROI polygon should include an ID (unique, consecutive number) and be assigned to a user-defined class (one value per class). If necessary, a field with a class description (label) can be added. Each classification process requires at least two classes, each with a minimum of one ROI polygon. The selected area of each ROI polygon determines the number of pixels used for training the respective class. Each class should include approximately equal numbers of ROIs (pixel counts). Also, misclassifications might occur due to abundant similarity of pixel values between separate classes. ROI validity can be estimated before the actual classification by running [MiGIS 2.2](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-22-roi-evaluation-optional). Based on the training dataset a Random Forest classification model can be produced using [MiGIS 2.1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-21-train-algorithm). After running the classification in [MiGIS 3](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-22-roi-evaluation-optional)

### Related publication: 
Zickel, M., Kehl, M., Gröbner, M. o(in prep.). MiGIS: Digital soil and sediment thin sections analyses using an open-source GIS Machine Learning approach. Applied Computing and Geosciences.

### This work is based on:
Breiman, L., 2001. “Random Forests”. Machine Learning, 45 (1), 5-32.

GDAL/OGR contributors, 2022. GDAL/OGR Geospatial Data Abstraction software Library. Open Source Geospatial Foundation. URL https://gdal.org , DOI: 10.5281/zenodo.5884351

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin. https://github.com/nkarasiak/dzetsaka/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, É., 2011. Scikit-learn: Machine Learning in Python, JMLR 12, 2825-2830.

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html


### Cite toolbox: 
Zickel, M., Kehl, M., Gröbner, M., 2023. MiGIS toolbox. https://github.com/Mirijamz/MiGIS

Bibtex reference:
```
@misc{zickel2023MiGIS,
title={MiGIS toolbox},
author={Mirijam Zickel and Martin Kehl and Marie Gröbner},
url={https://github.com/Mirijamz/MiGIS},
year={2023},
doi={XXXX}
}
```


# Detailed instructions
1.	[Hardware](https://github.com/Mirijamz/MiGIS/blob/main/README.md#1-hardware)

2.	[Software](https://github.com/Mirijamz/MiGIS/blob/main/README.md#2-software)

3.	[Required skills](https://github.com/Mirijamz/MiGIS/blob/main/README.md#3-required-skills)

4.	[Micromorphological thin section scans](https://github.com/Mirijamz/MiGIS/blob/main/README.md#4-micromorphological-thin-section-scans)

5.	[MiGIS integration (QGIS 3)](https://github.com/Mirijamz/MiGIS/blob/main/README.md#5-migis-integration-qgis-3)

6.	[Image classification basics & Random Forest classifier](https://github.com/Mirijamz/MiGIS/blob/main/README.md#6-image-classification-basics--random-forest-classifier)

7.	[Preprocessing](https://github.com/Mirijamz/MiGIS/blob/main/README.md#7-preprocessing)

7.1	[Transmitted light scanning (Canon Canoscan 9000F Mark II)](https://github.com/Mirijamz/MiGIS/blob/main/README.md#71-transmitted-light-scanning-canon-canoscan-9000f-mark-ii)

7.2	[Stack images & spatial referencing using image processing software (Inkscape)](https://github.com/Mirijamz/MiGIS/blob/main/README.md#72-stack-images--spatial-referencing-using-image-processing-software-inkscape)

7.3	[Georeference thin section imagery (QGIS Georeferencer)](https://github.com/Mirijamz/MiGIS/blob/main/README.md#73-georeference-thin-section-imagery-qgis-georeferencer)

8.	[MiGIS 1 preprocess TS images](https://github.com/Mirijamz/MiGIS/blob/main/README.md#8-migis-1-preprocess-ts-images)

9.	[MiGIS 2.1 train algorithm](https://github.com/Mirijamz/MiGIS/blob/main/README.md#9-migis-21-train-algorithm)

10.	[MiGIS 2.2 ROI evaluation [optional]](https://github.com/Mirijamz/MiGIS/blob/main/README.md#10-migis-22-roi-evaluation-optional)

11.	[MiGIS 3 classification](https://github.com/Mirijamz/MiGIS/blob/main/README.md#11-migis-3-classification)

12.	[References](https://github.com/Mirijamz/MiGIS/blob/main/README.md#12-references)


### 1. Hardware
•	Transmitted light scanner/ film scanner or similiar hardware to capture thin sections

•	2x polarisation film for XPL imagery, 1x black opaque film for RL imagery

•	QGIS-capable computer (min.: 8GB RAM, 100GB free storage, CPU with 4 cores)

### 2. Software
•	For digital image preprocessing: Inkscape (current: Inkscape 1.1.2)

•	GIS software: QGIS 3 (current: QGIS 3.22)

### 3. Required skills
•	GIS (QGIS) experience: navigate the GUI, Georeference raster data, create and edit vector data (polygons)

•	Basic knowledge of semi-automated image classification and accuracy assessment

•	Basic knowledge about the electromagnetic spectrum, light refraction, spectral signatures

•	Good training in micromorphology

### 4. Micromorphological thin section scans
In micromorphology, different microscope light modes - PPL (Plane Polarized Light), XPL (Cross Polarised Light) and OIL (Oblique Incident Light) - are used to distinguish thin section components (e.g. minerals) by their specific light refraction properties in different polarisation modes. Using transmitted light scanning, the analytical oppurtunities of petrographic microscopy can be obtained for an entire thin section. PPL can be acquired by capturing the plain thin section in transmitted light scanning mode (TL - Transmitted Light). For XPL, two orthogonally aligned polarisation films (90° orientation offset) are added on top and below the thin section. Using ordinary flatbed scanning and a black (isotropic) film on top of the thin section, a RL (Reflected Light) image can be produced which is similar to OIL imagery.

## 5. MiGIS integration (QGIS 3)
1.	Install the Dzetsaka Classification Plugin in QGIS (go to ‘Plugins’ and select ‘Manage and install plugins’).
2.	Install the Python machine learning library ‘scikit-learn’ using OSGeo shell (QGIS command line) typing:

    `o4w_env`
    
    `python3 -m pip install scikit-learn -U --user`

3.  For a detailed instruction check the documentation of [Dzetsaka classification plugin manual](https://github.com/nkarasiak/dzetsaka/blob/master/readme.md)
4.	Import the MiGIS Python scripts to your QGIS Project (Python symbol ([Python processing script](https://docs.qgis.org/3.22/en/docs/user_manual/processing/toolbox.html)) in ‘Processing toolbox’ tab) by ‘Adding Script to Toolbox’.
5.	After importing, all four parts of the toolbox are available in the QGIS ‘Processing toolbox’ (category ‘Scripts’, 'Python').

## 6. Image classification basics & Random Forest classifier
Among others, Machine Learning supported semi-supervised image classification is used to produce remote sensing products such as land cover maps. By the integration of multispectral information, different surface types can be identified, sorted and extracted by the classifier. MiGIS follows a similar approach by using bundled spectral information from TL, XPL and RL imagery (see [Transmitted light scanning](https://github.com/Mirijamz/MiGIS/blob/main/README.md#transmitted-light-scanning-canon-canoscan-9000f-mark-ii)) as classification input. To do this, it is necessary to spatial reference the RGB scan images (see [Stack images & spatial referencing]( https://github.com/Mirijamz/MiGIS/blob/main/README.md#stack-images--spatial-referencing-using-image-processing-software-inkscape)), perform georeferentiation in QGIS (see [Georeference thin section imagery](https://github.com/Mirijamz/MiGIS/blob/main/README.md#georeference-thin-section-imagery-qgis-georeferencer)) and composite them to a multi-band raster (see [MiGIS 1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-1-preprocess-ts-images)). 

Based on this data set, training areas (ROI - Regions of Interest) are collected using a costum vector polygon shapefile. ROI polygons mark a subsample of thin section components, each class should contain a set of exemplars e.g of quartz. The classifier will take this examples to learn and to create a classification model. Each ROI polygon should include an ID (unique, consecutive number) and be assigned to a user-defined class (one value per class). If necessary, a field with a class description (label) can be added. Each classification process requires at least two classes, each with a minimum of one ROI polygon. The selected area of each ROI polygon determines the number of pixels used for training the respective class. Each class should include approximately equal numbers of ROIs (pixel counts). Also, misclassifications might occur due to abundant similarity of pixel values between separate classes. 

ROI validity can be estimated before the actual classification by running [MiGIS 2.2](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-22-roi-evaluation-optional). Based on the training dataset a Random Forest classification model can be produced using [MiGIS 2.1](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-21-train-algorithm). After running the classification in [MiGIS 3](https://github.com/Mirijamz/MiGIS/blob/main/README.md#migis-22-roi-evaluation-optional) its accuracy can be assessed when a reference training data set is provided and accordingly by the evaluation of the confusion matrix. Produced classification models can also be applied to other thin section scans. However, increased variation concerning sediment composition, embedding resin and thin section thickness, and image acquisition may produce misclassifications. 

MiGIS applies Scikit-learn Random Forest classifier with a fixed number of 100 trees. Splitting is performed at each internal tree node using the square root of the number of features e.g. max_features = sqrt(n_features):

When constructing each decision tree of the Random Forest, the Classifier will still use all the given features defined in the training data. But for the node splitting only a defined number (maximum features) is used. These maximum features are randomly selected from the training data (see also Pedregosa et al. 2011, Scikit-learn developers 2007-2022, Breiman 2001).



## 7. Preprocessing

### 7.1 Transmitted light scanning (Canon Canoscan 9000F Mark II)
•	Use the transmitted light mode for TL (Transmitted Light) and XPL (Cross-Polarised Light) thin section scanning. Some flatbed scanner come with stencils (film-holder) to lock the scan object’s position, (e.g. dia slides or film). They can be helpful to keep the thin section in position.

•	XPL scanning: One polarisation film is positioned below the thin section. The polarisation direction of the second film needs to be orthogonal (rotated 90°) to the first film to achieve cross-polarisation.

•	Regular flatbed scanning can be applied to produce RL (Reflected Light) images. Using the film-holder and black (isotropic, non-reflective) film on top of the thin section.

•	Choose high-resolution scanning mode (1200 dpi) without automated image adjustments.

•	If necessary, image brightness and contrast can be adjusted using raster image processing software (e.g. Adobe Photoshop, GIMP).

**NOTE:** Keep the same scanning position for each thin section: the geometry of produced TL/ XPL/ RL imagery can vary according to the scan position on the scan pad. It is recommended to use a stencil (e.g. film holder for transmitted light scans). To avoid reflectance artifacts it could be helpful to turn all thin sections upside down. reflection artefacts will then appear where the sample label is positioned on the glass slide.

### 7.2 Stack images & spatial referencing using image processing software (Inkscape)
1.	Create a new Inkscape project or use the Inkscape project: [MiGIS_TS_ref_temp.svg](https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_TS_ref_temp.svg) and import all thin section images (1200 dpi).

2.	Make sure to create additional layers for XPL and RL image or click on the mentioned layer in the template to import the specific image in the correct layer.

**NOTE:** Do not modify the position of the reference crosses (Reference crosses layer) in the template (see [Fig. 1]( https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Inkscape_reference.png)), they match the georeference points in [MiGIS_georef.points]( https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_georef.points). If a new Inkscape project was created, it is required to create a top layer with reference points.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Inkscape_reference.png"
alt="Inkscape"/>
</p>
Figure 1: Creating a spatial reference (cross layer) for thin sections in Inkscape and setting the TL image visibility to 20-50% to adjust image stack.

3.	Change the transparency of the TL image to 50 - 20% visibility and lock the layer (see [Fig. 1]( https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Inkscape_reference.png)).

4.	Adjust the position/dimensions of the XPL image until it is congruent with the TL image.

5.	Lock and hide the XPL image layer

6.	Repeat the process with the RL image (alike XPL processing). Possibly the RL image will show some distortion as a result of different scan modes and light pass and needs to be stretched. Major distortions can cause artifacts in the classification result, keep them to a minimum.

7.	Set the TL image visibility back to 100%.

8.	Export the seperate images (Tl, XPL and RL layer) including the reference points (cross layer). The other two pictures or layer have to be deactivated (made invisible). 

**NOTE:** Use RGB8 PNG export mode without compression, do not export with alpha channel (RGBA_8).


### 7.3 Georeference thin section imagery (QGIS Georeferencer)
1.	Open a new QGIS project and adjust the project’s CRS: EPSG:32634 - WGS 84 / UTM zone 34N (matches [MiGIS_georef.points]( https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_georef.points)). If the template is not used, another metric CRS – for example the UTM system should be applied.

2.	Open the raster [Georeferencer](https://docs.qgis.org/3.22/en/docs/user_manual/working_with_raster/georeferencer.html) in QGIS.

3.	Import one of the referenced images (see [section above](https://github.com/Mirijamz/MiGIS/blob/main/README.md#stack-images--spatial-referencing-using-image-processing-software-inkscape)).

4.	Import the [MiGIS_georef.points]( https://github.com/Mirijamz/MiGIS/blob/main/MiGIS_georef.points) data set (see [Fig.2](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Georeferencer.png)) or create a costum set of reference points when using a different CRS.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Georeferencer.png"
alt="Georeferencer"/>
</p>

Figure 2: Georeferencing a TL thin section image using reference crosses and the provided POINTS data set.

5.	Adjust settings (see. (see [Fig.2](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Georeferencer.png)): Choose ‘Projective’ as transformation type, ‘Linear’ for Sampling and EPSG:32634 - WGS 84 / UTM zone for ‘CRS’. Do not adjust resolution or transparency of the output, but choose a directory for the georeferenced image.

6.	Run the tool and repeat the process with the second and third image.

7.	Validate georeferentiation output by comparing the georeferenced TL, XPL and RL raster in the QGIS window.


## 8. MiGIS 1 preprocess TS images
In a first step, the multi-band raster is created, by merging the georeferenced thin section images. The bundled spectral information is the target for later classification. To create the image stack or multi-band raster the tool merges the input RGB bands (TL, XPL, and opt. RL). As a result the multi-band raster will contain 6 (TL + XPL RGB image) or 9 (TL + XPL + RL RGB image) bands. The classification area can be narrowed down by using a clipping layer which matches the outlines of the sample section area (see result in [Fig. 3](github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MBR_MBRC.png). This step will enable precise area statistics and minimises the computational effort.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MBR_MBRC.png"
alt="MBRvsMBRC"/>
</p>

Figure 3: Georeferenced and stacked thin section mulit-band raster vs. the clipped version.

A clipping layer can be created by adding a new polygon shapefile to the QGIS project (see [Creating a new shapefile]( github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MBR_MBRC.png)) and using [vector editing]( https://docs.qgis.org/3.22/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html?highlight=editing#). Artificial gaps within the polygon’s area: e.g. dry cracks, and saw marks can be excluded by adding rings (see [Add ring](https://docs.qgis.org/3.22/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html?highlight=editing#add-ring)).

After running the tool, it is recommended to open the ‘Style’ tab of the multi-band raster’s ‘Properties’ and set the sampling method to bilinear. Also, it is possible to switch displayed RGB bands to display TL, XPL, or RL by choosing different band combinations in the dialog.
Note: The order of the band sets in the output data set might defer due to file naming etc. Possibly band 1 to 3 belong to the TL image’s R, G, B bands and band 4 to 6 provides XPL RGB information.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MiGIS_1.png"
alt="MiGIS_1"/>
</p>

Figure 4: MiGIS 1 tool.


## 9. MiGIS 2.1 train algorithm
Based on the created training areas (see Fig. 5 [ROIs](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/ROIs.png) - Regions of Interest) and target raster a Random Forest classification model will created (MODEL file). A training data set can be added by editing (see [vector editing]( https://docs.qgis.org/3.22/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html?highlight=editing#)) a custom polygon shapefile (see [Creating a new shapefile](https://docs.qgis.org/2.18/en/docs/user_manual/managing_data_source/create_layers.html#creating-a-new-shapefile-layer)). 

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/ROIs.png"
alt="Inkscape"/>
</p>
Figure 5: ROI polygon examples.

For straightforward accuracy assessment a second, independent reference data set with ROIs should be created (see [MiGIS 3](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-3-classification )). Ideally, the classification target is a TL/XPL and optional RL multi-band raster (see [section MiGIS 1](https://github.com/Mirijamz/MiGIS-script/blob/main/README.md#migis-1-preprocess-ts-images)).


<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MiGIS_2_1.png"
alt="MiGIS_2.1"/>
</p>

Figure 6: MiGIS 2.1 tool.

**Note:**

•	The component classes and sample observations should be determined under the microscope beforehand. 

•	When collecting ROIs, it is recommendable to switch between the single TL, XPL and RL raster image for verification.

•	The total amount of pixel per class (ROI polygon area) should be approximately equal. 

•	A separate reference training dataset data set should be created by independent ROI collection.

•	ROI validity per class can be estimated by running (see [section MiGIS 2.2](https://github.com/Mirijamz/MiGIS#migis-22-roi-evaluation-optional)).

### Input
**ROI layer (training data set, .shp):** Training data set (SHP format) with numeric (integer) class identification, class label field (text – string), and an ID field (integer) with unique values for the attributes (each ROI polygon). Minimum two classes per training data set.

**Example attribute 1:**

Id (field 1) = 23

Class (field 2) = 1

Class label (field 3) = clay coating


**Example attribute 2:**

Id (field 1) = 45

Class (field 2) = 2

Class label (field 3) = quartz


**Class field (integer):** Select the class identifier field of the training data set. 



## 10. MiGIS 2.2 ROI evaluation [optional]
To facilitate ROI validation the tool computes HTML boxplot diagrams for each input band of the multi-band raster. Thus 1-9 boxplot diagrams are created as output. A maximum of nine bands will be created, if the multi-band raster contains the TL, XPL and RL bands.This illustrates pixel value distribution (polygon area median) and standard deviation of the classes. Classes showing increased similarity to others in most bands, also as classes broadly scattered values are likely to be confused with other classes. In addition, outlier ROIs can be identified in this way. The interactive HTML plot allows detailed data exploration (see [Fig. 6]( https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/ROI_boxplot_exp.png). Raw median pixel values per ROI polygon for each band are stored in a CSV table.

**Note:** The column heads are b[bandnumber]_median and b[bandnumber]_stdev.


<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/ROI_boxplot_exp.png"
alt="ROI band boxplot"/>
</p>

Figure 6: Boxplot showing ROI value distribution of one band per class.

### Additional information
### Input
A vector training data set with ROI polygons (see [MiGIS 2.1]([https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MiGIS_2_1.png](https://github.com/Mirijamz/MiGIS#migis-21-train-algorithm)) and a thin section multi-band raster (see [MiGIS 1](https://github.com/Mirijamz/MiGIS#migis-1-preprocess-ts-images)) is required.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MiGIS_2_2.png"
alt="MiGIS_2.2"/>
</p>

Figure 7: MiGIS 2.1 tool.


## 11. MiGIS 3 classification
Based on a trained classification model from part 2 a classification map (see [Fig. 8](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Class_output.png)), confidence map, confusion matrix, and spatial statistics (see [Fig. 8](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Class_output.png))  will be computed out of the classification result (classification map). The accuracy assessment (confusion matrix) requires an additional reference training data set which contains the same classes as the ROI training data set, but a second set of ROIs (independent collection). 

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Class_output.png"
alt="ClaM"/>
</p>

Figure 8: Exemplary classification map and spatial statistics.

•	In a further step, area statistics can also be created for the classes based on the classification map.

•	To run the prediction and to produce the classification map one of the clipped multi-band raster (including the TL, XPL and optional RL image) is required. 

•	It is also recommended to limit the classification area as much as possible to the sample section extent by using a clipped multi-band raster (see [MiGIS 1](https://github.com/Mirijamz/MiGIS#migis-1-preprocess-ts-images)). 

•	The confusion matrix (see [Fig.9](https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Confusion_exp.png)) requires a second reference (independent) training data set with identical fields as the original training data set e.g. ID, Class, Class No, identical classes and labels, but a second set of ROIs.

<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/Confusion_exp.png"
alt="Confi"/>
</p>

Figure 9: Exemplary confusion matrix and selected accuracy parameters (see Congalton & Green 2019)


<p align="center">
  <img src="https://github.com/Mirijamz/MiGIS/blob/main/Manual_figures/MiGIS_3.png"
alt="MiGIS_3"/>
</p>

Figure 10: MiGIS 3 tool.

### Additional information
### Input
**Classification model (.model):** Select the classification model trained in (MiGIS 2.1). However, a model trained on one raster can be applied on another multi-band raster (with the same bands - spectral information) which should then be selected (model file).

**Clipped multi-band raster (AOI, .tif):** Select the thin section to be classified. Preferably, a clipped multi-band raster containing TL, XPL and RL bands. 

### Output
**Classification map (.tif):** Classification result based on the selected training (model, classes)

**Confidence map (.tif):** Displays certain vs. uncertain areas of the classification result

**Confusion matrix:** Based on the matrix, classification accuracy statistics as overall accuracy, Kappa Coefficient (Cohen's Kappa), producer and user accuracy can be calculated (see Congalton & Green 2019).

**Class area in m² - class labels incl. (.csv):** Required output. Produces class-based area statistics to determine the quantity ratio of the classified components and the porosity (if such a class was created). Class labels (description) are provided in an additional column.

**Class area in m² (.csv):** optional output. Numeric class identifier column only. Produces class-based area statistics to determine the quantity ratio of the classified components and the porosity.


## 12. References
Breiman, L., 2001. “Random Forests”. Machine Learning, 45 (1), 5-32

Congalton, R., Green, K., 2019. Assessing the Accuracy of Remotely Sensed Data. CRS Press, Boca Raton. https://doi.org/10.1201/9780429052729

GDAL/OGR contributors, 2022. GDAL/OGR Geospatial Data Abstraction software Library. Open Source Geospatial Foundation. https://gdal.org , DOI: 10.5281/zenodo.5884351

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin. DOI:10.5281/zenodo.2552284, 2021-04-01

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, É., 2011. Scikit-learn: Machine Learning in Python, JMLR 12, 2825-2830

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04

Scikit-learn developers, 2007-2022. User guide: 1.11.2. Forests of randomized trees. https://scikit-learn.org/stable/modules/ensemble.html#forest, 2022-05-04
