# MiGIS toolbox
MiGIS python script based toolbox for QGIS - analyse and classify soil and sediment thin section in GIS

![MiGIS-Workflow](https://github.com/Mirijamz/MiGIS-script/blob/main/Manual_figures/workflow_v5_low.png)

Info
-Random Forest classifier with 100 trees and splitted at each internal tree note using the square root of the number of features e.g. max_features=sqrt(n_features):
During the construction of each decision tree, RF will still use all the features (n_features), but it only consider number of "max_features" features for node splitting. And the "max_features" features are randomly selected from the entire features.
Cite:
https://scikit-learn.org/stable/about.html#citing-scikit-learn
Breiman, “Random Forests”, Machine Learning, 45(1), 5-32, 2001.

To do examples
-Tob 12 Poren ohne übergroße Hohlräume auswerten
-Tob 5 nochmal mit OIL klassifizieren und ohne große Hohlräume auswerten

Hardware
-Transmitted light scanner
-QGIS capable (runs stable) computer
Micro GIS requirements
For digital image preprocessing:
Install Inkspace or GIMP in your system

MicroGIS integration to QGIS
Install QGIS – OSGEO4W
Install dzetsaka classification tool (install scikit learn using the OSGEO4W command line tool) – dzetsaka see:
https://github.com/nkarasiak/dzetsaka

Install OrfeoToolbox in QGIS – OTB:  see https://www.orfeo-toolbox.org/ ) and https://docs.qgis.org/3.16/en/docs/user_manual/processing/3rdParty.html#otb-applications

Load the MicroGIS python model in your QGIS Project visit Github: XXX

Digital Image Preprocessing
Scanning
Use transmitted light function for TL and XPL thin section images
Normal flatbed scanning for RL. Using the transmitted light scanning frame and a black (isotropic) foil on top of the thin section in the frame (scanner glas – within the frame: thin section – black foil)
Choose high-resolution mode (1200 to 3600 dpi)
It is recommended to adjust the image brightness and contrast after scanning (e.g. in Adobe Photoshop, GIMP etc.).

GIMP/ Inkscape
Open high-resolution thin section scan images (3600 dpi) in GIMP/Inkscape project TS_ref_temp
Create additional layers for XPL and RL image or click on the mentioned layer in the template to import the specific image in the correct layer.
NOTE: Do not modify the position of the reference crosses (Reference crosses layer) in the template. If a new Inkscape/GIMP project was created, it is required to create a new layer with approx. 0,1 pt vector line crosses (important for the georefenciation process)
Change the transparency of the TL image to 50 or 10% visibility
Move/ stretch the XPL image until it is congruent with the visible structures in the TL image
Repeat the process with the RL image (instead of XPL), possibly the RL image will still show some distortion which might depend on the scanning process. Relevant distortions will show up as artifacts in the classification result.
Set the TL image visibility back to 100%
Export the single TL image (layer) with the overlaying cross layers by setting the other XPL and RL image to invisible.
Repeat the export process with the XPL and RL image
NOTE: Use RGB 8 export without compression and be aware to export as RGB8 image without alpha channel (RGBA_8).
Georeferncing
-Open the QGIS project Micro_GIS
-Open the Georeferencer (see also https://docs.qgis.org/3.16/en/docs/user_manual/working_with_raster/georeferencer.html )
-Open the TL image in the Georeferencer window
-Add a georeferencer point to each of the four cross center by taking the correct position from the TS_georef_inkscape layer of the map
OR: Load the MicroGIS_georef POINTS dataset for the Georeferencer
-Goereferencer settings: Choose ‘Projective’ as Transformationtype, ‘Linear’ for Sampling and EPSG:32634 - WGS 84 / UTM zone 34N (the QGIS project template uses this projection, otherwise make sure to use a metric CRS - as UTM – in your QGIS project) for ‘CRS’. Do not change the resolution or transparency of the output, but choose a directory for the georeferenced TL image
-Run the tool and open the georeferenced image in the QGIS main window
-Check if the georeferencing was successful by comparing the position of the TL, XPL and RL image
IF NOT: Repeat the georefenciation process with the .POINTS dataset, but with additionally set reference points (using one image e.g. TL as a reference) grapped from the map window
KOMMENTARE IM MODEL WERDEN NICHT IM TOOL ANGEZEIGT

MicroGIS part 1: Processing the multiband image
REIHENFOLGE DER OUTPUTS CHECKEN
Multiband image (TL, XPL, and opt. RL): Merges the different thin section scan images. The result is a multiband raster image with 6 (TL + XPL RGB image) or 9 (TL + XPL + RL RGB image) bands. 
Note: The order of the band sets in the output dataset might defer due to file naming etc. Possibly band 1 to 3 are equivalent to the TL image’s R, G, B bands and band 4 to 6 keeps the XPL information. ¬
For ‘Clip TS area’: Create or edit the thin section area vector layer.
Create a rectangular polygon which covers the thin section content area
- The polygon borders should be set as close to the sediment cover as possible
AND/ OR
For ‘Clip TS real area’: Create or edit the thin section area vector layer.
Create a polygon by following the actual outlines of the sediment cover. Big empty parts within this area (the polygon), as big cracks which result from unsuitable micromorphological sample storing, can be excluded by the addition of rings (see also https://docs.qgis.org/3.16/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html?highlight=editing#add-ring) 
Run the MicroGIS part 1 tool using the datasets above.
In the Raster Properties ‘Style’ tab: Set sampling method to bilinear
CHANGE OUTPUT ORDER IN PYTHON SCRIPT

MicroGIS Part 2: Train Algorithm
Create training data (vector layer TS_train):
-Use the template layer or create a new vector layer with the fields: Id, Class, Class nr, Area (OTIONAL: to control and equalize the training pixel per class)
-Each object (polygon) needs a single ID and a class assignment
-The total amount of pixel or the area (covered area by the sum of polygons) per class should be more or less equal
-Create a second independent training datasets for later evaluation
NOTE: To gather training polygons, it is recommendable to switch between the TL, XPL and RL image in order to verify the individual content or consistency of components.
-Run the tool
MicroGIS part 2: detailed ROI evaluation [optional
Requires a vector training dataset (ROI) and a multiband raster (merged TS scans).
Zonal statistics: Produces an attribute table with a mean pixel (median) value also as the standard deviation for each ROI polygon and each band. 
Note: The column heads are b[bandnumber]_median and b[bandnumber]_stdev.
Boxplotts: Based on the training classes (Column ‘Class’) and the class-specific ROI median values, a boxplot diagrams is computed for each band.

MicroGIS Plugin Part 3: Classification and validation
To run the prediction and to produce the classification map one of the clipped multiband raster image (including the TL, XPL and optional RL image) is required. 
Note: It depends on the goal of the classification if ‘Clipped multiband image (TS area)’ or ‘Clipped multiband image (TS real area)’ is chosen. For example, ‘Clipped multiband image (TS real area)’ with masked out irrelevant areas is recommended, if later pore space quantification is planned and the sediment sample in the thin section has a very unregular shape, a big saw mark and/ or big postsampling cracks are visible.
Load the classification model, that was created in step 2 (train algorithm)
The classification step produces a classification and a confidence map
Class. area quantification (Area per class): Enables the quantification of the area covered by the different classes. For example the area covered by pore space, if such a class was created.
ROI validation - Confusion matrix: requires a second independent training dataset (.shp) with identical fields as the original training dataset: Id, Class, Class nr and produces a .csv file including the classification matrix.
-Run the tool
