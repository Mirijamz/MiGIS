"""
Model exported as python. #modified
Name : MiGIS_3_classification
Group : MiGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
import processing


class Migis3Classification(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('RastergeorefTSscans', 'Clipped multi-band raster (AOI, .tif)', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('classification_model_model', 'Classification model (.model)', behavior=QgsProcessingParameterFile.File, fileFilter='Alle Dateien (*.*)', defaultValue=None))        
        self.addParameter(QgsProcessingParameterVectorLayer('roival', 'ROI reference layer (.shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classfieldinteger', 'Class field (integer)', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='roival', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classnamefieldstring', 'Class label field (string)', type=QgsProcessingParameterField.Any, parentLayerParameterName='roival', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ClassificationMapTif', 'Classification map (.tif)', createByDefault=True, defaultValue=None))
        #self.addParameter(QgsProcessingParameterRasterDestination('ConfidenceMapTif', 'Confidence map (.tif)', optional=True, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ConfusionMatrixCsv', 'Confusion matrix (.csv)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ClassAreaLabelsCsv', 'Class area in m² with labels (.csv)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('Cal_plot', 'Class area plot (.html)', fileFilter='HTML files (*.html)', optional=True, createByDefault=True, defaultValue=None))


    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # TS classification
        alg_params = {
            'INPUT_MASK': None,
            'INPUT_MODEL': parameters['classification_model_model'],
            'INPUT_RASTER': parameters['RastergeorefTSscans'],
            #'CONFIDENCE_RASTER': parameters['ConfidenceMapTif'],
            'OUTPUT_RASTER': parameters['ClassificationMapTif']
        }
        outputs['TsClassification'] = processing.run('dzetsaka:Predict model (classification map)', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassificationMapTif'] = outputs['TsClassification']['OUTPUT_RASTER']
        #results['ConfidenceMapTif'] = outputs['TsClassification']['CONFIDENCE_RASTER']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Assess classification accuracy (vector reference)
        alg_params = {
            'COLUMN_PREFIX': 'Classified_',
            'INPUT_RASTER': outputs['TsClassification']['OUTPUT_RASTER'],
            'INPUT_VECTOR': parameters['roival'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClassAccuracyVecRef'] = processing.run('native:zonalhistogram', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Dissolve class
        alg_params = {
            'FIELD': parameters['classfieldinteger'],
            'INPUT': outputs['ClassAccuracyVecRef']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': parameters['ConfusionMatrixCsv']
        }
        outputs['DissolveClass'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ConfusionMatrixCsv'] = outputs['DissolveClass']['OUTPUT']
        
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
        # Spatial statistics
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['TsClassification']['OUTPUT_RASTER'],
            'OUTPUT_TABLE': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SpatialStatistics'] = processing.run('native:rasterlayeruniquevaluesreport', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"value"','length': 100,'name': 'value','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'expression': '"count"','length': 100,'name': 'count','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'expression': '"m2"','length': 100,'name': 'm2','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'}],
            'INPUT': outputs['SpatialStatistics']['OUTPUT_TABLE'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'value',
            'FIELDS_TO_COPY': parameters['classnamefieldstring'],
            'FIELD_2': parameters['classfieldinteger'],
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'INPUT_2': parameters['roival'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'NON_MATCHING': None,
            'PREFIX': '',
            'OUTPUT': parameters['ClassAreaLabelsCsv']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassAreaLabelsCsv'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Bar plot
        alg_params = {
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'NAME_FIELD': parameters['classnamefieldstring'],
            'VALUE_FIELD': 'm2',
            'OUTPUT': parameters['Cal_plot']
        }
        outputs['BarPlot'] = processing.run('qgis:barplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cal_plot'] = outputs['BarPlot']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS 3 classification'

    def displayName(self):
        return 'MiGIS 3 classification'

    def group(self):
        return 'MiGIS'

    def groupId(self):
        return 'MiGIS'

    def shortHelpString(self):
        return """<html><body><p>MiGIS: Classify rock, sediment & soil thin sections

MiGIS 3
Creates a classification map based on a trained classification model (MiGIS 2) and a (clipped) multi-band raster with TL, XPL and RL bands (see MiGIS 1). 
The classification map is the main result on which a confusion matrix is calculated, as a first step of accuracy assessment. 
This requires an ROI reference dataset that contains the same classes as the ROI training dataset, but an independent ROI collection. 
Optionally, class specific spatial statistics will be calculated based on the classification map.</p>
<h2>Input parameters</h2>
<h3>Clipped multi-band raster (AOI, .tif)</h3>
<p>Select the thin section to be classified. Preferably, a clipped multi-band raster containing TL, XPL and RL bands.
It is also recommended to limit the classification area as much as possible by selecting the clipped multiband raster (MiGIS 1), cropped to the sample section coverage. 
The selected model (see MiGIS 2) will be applied to the input raster. 
In general, a classification model trained on one raster can be applied to another (with similar properties - bands etc.). 
However, due to high variation in thin section quality this is not recommended.</p>
<h3>Classification model (.model)</h3>
<p>Select the classification model trained in (MiGIS 2). 
However, a model trained on one raster can be applied on another multi-band raster (with the same bands - spectral information) which should then be selected (model file).</p>
<h3>ROI reference layer (.shp)</h3>
<p>2nd ROI dataset used to evaluate the classification result. Serves as input for the accuracy assessment (confusion matrix). Required fields: Id (integer), Class label (string), Class (integer)</p>
<h3>Class field (integer)</h3>
<p>Numeric field containing class identifiers. Used as input for the confusion matrix and spatial statistics (Class area in m² with class labels). </p>
<h3>Class label field (string)</h3>
<p>Text field with class description/names (ROI layer). Used to supplement class descriptions to the spatial statistics (Class area in m² with class labels).</p>
<h2>Outputs</h2>
<h3>Classification map (.tif)</h3>
<p>Classification result based on the selected training data (model, ROI classes).</p>
<h3>Confidence map (.tif)</h3>
<p>Displays certain vs. uncertain areas of the classification result</p>
<h3>Confusion matrix (.csv)</h3>
<p>To assess classification accuracy. Based on this matrix, classification accuracy statistics as overall accuracy, Kappa Coefficient (Cohen's Kappa), commission and omission errors can be calculated (see Congalton & Green 2019).</p>
<h3>Class area in m² with class labels (.csv)</h3>
<p>Produces class related pixel area statistics, to determine quantities and area ratios of classified components, such as pore space volume (if such a class was created). 
The output unit is m², it is helpful to calculate class percentages in relation to the total classified area from the output values. 
Class descriptions (labels) are automatically added from the class labels (class label field) stored in the reference training data set (ROI reference layer). </p>
<h3>Class area plot (.html)</h3>
<p>Illustrates the area ratio of the input classes in a bar plot</p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2023. MiGIS toolbox - Thin Section Classification. https://github.com/Mirijamz/MiGIS, 2023-02-09.

References: 
Breiman, “Random Forests”, Machine Learning, 45(1), 5-32, 2001. 

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin, DOI:10.5281/zenodo.2552284, 2021-04-01.

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. 

Scikit-learn developers, 2007-2022. User guide: 1.11.2. Forests of randomized trees. https://scikit-learn.org/stable/modules/ensemble.html#forest, 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS'

    def createInstance(self):
        return Migis3Classification()
