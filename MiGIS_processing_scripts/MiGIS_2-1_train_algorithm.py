"""
Model exported as python. #modified
Name : MiGIS 2.1 train algorithm
Group : MiGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFileDestination
import processing


class Migis21TrainAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('ClippedmultibandTSimageTLXPLRL', 'Clipped multi-band raster (AOI, .tif)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('ROItrainingdata', 'ROI layer (training dataset, .shp)', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classfieldint', 'Class field (integer)', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='ROItrainingdata', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RandomForestClassificationModelModel', 'Random Forest classification model (.model)', fileFilter='All files (*.*)', createByDefault=True, defaultValue=''))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Train algorithm (dzetsaka)
        alg_params = {
            'INPUT_COLUMN': parameters['classfieldint'],
            'INPUT_LAYER': parameters['ROItrainingdata'],
            'INPUT_RASTER': parameters['ClippedmultibandTSimageTLXPLRL'],
            'OUTPUT_MATRIX': 'TEMPORARY_OUTPUT',
            'PARAMGRID': '',
            'SPLIT_PERCENT': 0, #Do not split the ROI data set to validate, apply independent ROI collection as reference data set in MiGIS 3
            'TRAIN': 1,  # Random-Forest
            'OUTPUT_MATRIX': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT_MODEL': parameters['RandomForestClassificationModelModel']
        }
        outputs['TrainAlgorithmDzetsaka'] = processing.run('dzetsaka:Train algorithm', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RandomForestClassificationModelModel'] = outputs['TrainAlgorithmDzetsaka']['OUTPUT_MODEL']
        return results

    def name(self):
        return 'MiGIS 2.1 train algorithm'

    def displayName(self):
        return 'MiGIS 2.1 train algorithm'

    def group(self):
        return 'MiGIS'

    def groupId(self):
        return 'MiGIS'

    def shortHelpString(self):
        return """<html><body><p>MiGIS: Classify rock, sediment & soil thin sections

MiGIS 2
Trains Random Forest algorithm based on the created training data set (ROIs - Regions Of Interest) and creates a classification model. 
Optimally, the classification target is a multi-band raster dataset, consisting of the stacked TL (transmitted light), XPL (cross-polarised light) and RL (reflected light) images/bands. Also, to obtain a meaningful classification, it is recommended to first delimit the area to be classified (see MiGIS 1 - Create a classification area) and use the clipped raster as input to the model. Optionally, an ROI evaluation can be performed before creating the model (see MiGIS 2 - ROI evaluation).
</p>
<h2>Input parameters</h2>
<h3>Clipped multi-band raster (AOI, .tif)</h3>
<p>Select the thin section to be classified. Preferably, a clipped multi-band raster containing TL, XPL and RL bands.
</p>
<h3>ROI layer (training dataset, .shp)</h3>
<p>Training dataset (SHP format) with numeric (integer) class identification and class label field (text - string). 
Add an ID field (integer) with a unique value for each attribute (ROI polygon).
Also, create a mimimum of at least two ROI classes, identified by different values in the attribute table.

Example attribute 1:
 Id (field 1) = 23
Class (field 2) = 1
Class label (field 3) = clay coating

Example attribute 2:
 Id (field 1) = 45
Class (field 2) = 2
Class label (field 3) = quarz</p>
<h3>Class field (integer)</h3>
<p>Select the class identifier field of the training dataset. </p>
<h2>Outputs</h2>
<h3>Random Forest classification model (.model)</h3>
<p>MODEL file containing the trained classification scheme according to Random Forest algorithm.</p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2023. MiGIS Thin Section Classification. https://github.com/Mirijamz/MiGIS, 2022-05-15.

References: 
Breiman, “Random Forests”, Machine Learning, 45(1), 5-32, 2001. 

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin, DOI:10.5281/zenodo.2552284, 2021-04-01.

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. 

Scikit-learn developers, 2007-2022. User guide: 1.11.2. Forests of randomized trees. https://scikit-learn.org/stable/modules/ensemble.html#forest, 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS'

    def createInstance(self):
        return Migis21TrainAlgorithm()
