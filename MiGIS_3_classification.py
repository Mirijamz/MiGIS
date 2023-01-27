"""
Model exported as python.
Name : MiGIS 3 classification
Group : MiGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Migis3Classification(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('Classificationmodelmodel', 'Classification model (.model)', behavior=QgsProcessingParameterFile.File, fileFilter='Alle Dateien (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('RastergeorefTSscans', 'Clipped multi-band raster (AOI, .tif)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('roival', 'ROI reference layer (.shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classfieldinteger', 'Class field (integer)', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='roival', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classnamefieldstring', 'Class label field (string)', type=QgsProcessingParameterField.Any, parentLayerParameterName='roival', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ClassificationMapTif', 'Classification map (.tif)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ConfidenceMapTif', 'Confidence map (.tif)', optional=True, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ConfusionMatrixCsv', 'Confusion matrix (.csv)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/Mirijama/AppData/Roaming/QGIS/QGIS3/profiles/Mirijam/processing/outputs/.csv'))
        self.addParameter(QgsProcessingParameterFeatureSink('ClassAreaInMClassLabelsInclCsv', 'Class area in m² -  class labels incl. (.csv)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ClassAreaInMCsv', 'Class area in m² (.csv)', optional=True, type=QgsProcessing.TypeVector, createByDefault=False, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # TS classification
        alg_params = {
            'INPUT_MASK': None,
            'INPUT_MODEL': parameters['Classificationmodelmodel'],
            'INPUT_RASTER': parameters['RastergeorefTSscans'],
            'CONFIDENCE_RASTER': parameters['ConfidenceMapTif'],
            'OUTPUT_RASTER': parameters['ClassificationMapTif']
        }
        outputs['TsClassification'] = processing.run('dzetsaka:Predict model (classification map)', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassificationMapTif'] = outputs['TsClassification']['OUTPUT_RASTER']
        results['ConfidenceMapTif'] = outputs['TsClassification']['CONFIDENCE_RASTER']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Class area quantification
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['TsClassification']['OUTPUT_RASTER'],
            'OUTPUT_TABLE': parameters['ClassAreaInMCsv']
        }
        outputs['ClassAreaQuantification'] = processing.run('native:rasterlayeruniquevaluesreport', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassAreaInMCsv'] = outputs['ClassAreaQuantification']['OUTPUT_TABLE']

        feedback.setCurrentStep(2)
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
        outputs['AssessClassificationAccuracyVectorReference'] = processing.run('native:zonalhistogram', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Join class name field
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'Value',
            'FIELDS_TO_COPY': parameters['classnamefieldstring'],
            'FIELD_2': parameters['classfieldinteger'],
            'INPUT': outputs['ClassAreaQuantification']['OUTPUT_TABLE'],
            'INPUT_2': parameters['roival'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['ClassAreaInMClassLabelsInclCsv']
        }
        outputs['JoinClassNameField'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassAreaInMClassLabelsInclCsv'] = outputs['JoinClassNameField']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Dissolve class
        alg_params = {
            'FIELD': parameters['classfieldinteger'],
            'INPUT': outputs['AssessClassificationAccuracyVectorReference']['OUTPUT'],
            'OUTPUT': parameters['ConfusionMatrixCsv']
        }
        outputs['DissolveClass'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ConfusionMatrixCsv'] = outputs['DissolveClass']['OUTPUT']
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
        return """<html><body><p>MiGIS: Classifiy sediment/soil thin sections

MiGIS 3
In this part of the plug-in, a classification map and a confidence map are created based on a trained classification model from part 2. The classification map is the result on which a confusion matrix is created as part of the accuracy assessment. This requires an ROI reference dataset that contains the same classes as the ROI training dataset but is independent of it. Both datasets must be based on the same raster dataset. 
In a further step, area statistics can also be created for the classes based on the classification map.</p>
<h2>Input parameters</h2>
<h3>Classification model (.model)</h3>
<p>Select the classification model trained in (MiGIS 2). However, a model trained on one raster can be applied on another multi-band raster (with the same bands - spectral information) which should then be selected (model file).</p>
<h3>Clipped multi-band raster (AOI, .tif)</h3>
<p>Select the thin section to be classified. Preferably, a clipped multi-band raster containing TL, XPL and RL bands. 
The selected classification model will be applied. Usually, this is the same raster used to train the classification model (in MiGIS 2) on. 
However, a model trained on one raster can be applied on another  multi-band raster (with the same bands - spectral information) which should then be selected (raster file).
It is also recommended to limit the classification area as much as possible by selecting the clipped multiband raster (MiGIS 1), tailored to the section coverage. </p>
<h3>ROI reference layer (.shp)</h3>
<p>2nd ROI dataset used to evaluate the classification result. Serves as input for the accuracy assessment (confusion matrix). Required fields: Id (integer), Class label (string), Class (integer)</p>
<h3>Class field (integer)</h3>
<p>Numeric field containing class identifiers. Used as input for the class area statistics. </p>
<h3>Class label field (string)</h3>
<p>Text field with class description/names (ROI layer). Used to supplement class descriptions to the class area statistics.</p>
<h2>Outputs</h2>
<h3>Classification map (.tif)</h3>
<p>Classification result based on the selected training (model, classes)</p>
<h3>Confidence map (.tif)</h3>
<p>Displays certain vs. uncertain areas of the classification result</p>
<h3>Confusion matrix (.csv)</h3>
<p>Essential for the accuracy assessment. Based on this matrix, classification accuracy statistics as overall accuracy, Kappa Coefficient (Cohen's Kappa), commission and omission errors can be calculated (see Congalton & Green 2019).</p>
<h3>Class area in m² -  class labels incl. (.csv)</h3>
<p>Required output. Class description (labels) inclusive. Produces class-based area statistics to determine the quantity ratio of the classified components and the porosity (if such a class was created). </p>
<h3>Class area in m² (.csv)</h3>
<p>Numeric class identifier only. Produces class-based area statistics to determine the quantity ratio of the classified components and the porosity. Can be skipped if not needed.</p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2022. MiGIS Thin Section Classification. https://github.com/Mirijamz/MiGIS-script, 2022-05-15.

References: 
Breiman, “Random Forests”, Machine Learning, 45(1), 5-32, 2001. 

Karasiak, N., 2016. Dzetsaka Qgis Classification plugin, DOI:10.5281/zenodo.2552284, 2021-04-01.

QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. 

Scikit-learn developers, 2007-2022. User guide: 1.11.2. Forests of randomized trees. https://scikit-learn.org/stable/modules/ensemble.html#forest, 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS-script'

    def createInstance(self):
        return Migis3Classification()
