"""
Model exported as python.
Name : MiGIS part 3 classification
Group : MicroGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterDefinition
import processing


class MigisPart3Classification(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # MiGIS part 2 output (dzetsaka train algorithm output, .model)
        self.addParameter(QgsProcessingParameterFile('Classificationmodelmodel', 'Classification model (.model)', behavior=QgsProcessingParameterFile.File, fileFilter='Alle Dateien (*.*)', defaultValue=None))
        # MiGIS part 1 output (clipped multiband TS image)
        param = QgsProcessingParameterRasterLayer('RastergeorefTSscans', 'Clipped multiband raster (TL,XPL and opt. RL/OIL bands)', defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        # Required fields: Id (integer), Class (string), Class nr (integer)
        self.addParameter(QgsProcessingParameterVectorLayer('roival', 'ROI validation (2nd independent dataset, .shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ClassificationMapTif', 'Classification map (.tif)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ConfidenceMapTif', 'Confidence map (.tif)', optional=True, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ConfusionMatrixXlsx', 'Confusion matrix (.xlsx)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ClassAreaInMAddClassNameXlsx', 'Class area in m² - add class name (.xlsx)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ClassAreaInMClassNrXlsx', 'Class area in m² - Class nr (.xlsx)', optional=True, type=QgsProcessing.TypeVector, createByDefault=False, defaultValue=None))

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

        # Assess classification accuracy (vector reference)
        alg_params = {
            'COLUMN_PREFIX': 'Classified_',
            'INPUT_RASTER': outputs['TsClassification']['OUTPUT_RASTER'],
            'INPUT_VECTOR': parameters['roival'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AssessClassificationAccuracyVectorReference'] = processing.run('native:zonalhistogram', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Aggregieren
        alg_params = {
            'AGGREGATES': [{'aggregate': 'first_value','delimiter': ',','input': '"Class"','length': 150,'name': 'Class','precision': 0,'type': 10},{'aggregate': 'first_value','delimiter': ',','input': '"Class nr"','length': 10,'name': 'Class nr','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_1"','length': 20,'name': 'Classified_1','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_2"','length': 20,'name': 'Classified_2','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_3"','length': 20,'name': 'Classified_3','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_4"','length': 20,'name': 'Classified_4','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_5"','length': 20,'name': 'Classified_5','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_6"','length': 20,'name': 'Classified_6','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_7"','length': 20,'name': 'Classified_7','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_8"','length': 20,'name': 'Classified_8','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_9"','length': 20,'name': 'Classified_9','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_10"','length': 20,'name': 'Classified_10','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_11"','length': 20,'name': 'Classified_11','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_12"','length': 20,'name': 'Classified_12','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': '"Classified_13"','length': 20,'name': 'Classified_13','precision': 0,'type': 4}],
            'GROUP_BY': '"Class nr"',
            'INPUT': outputs['AssessClassificationAccuracyVectorReference']['OUTPUT'],
            'OUTPUT': parameters['ConfusionMatrixXlsx']
        }
        outputs['Aggregieren'] = processing.run('native:aggregate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ConfusionMatrixXlsx'] = outputs['Aggregieren']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Class area quantification
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['TsClassification']['OUTPUT_RASTER'],
            'OUTPUT_TABLE': parameters['ClassAreaInMClassNrXlsx']
        }
        outputs['ClassAreaQuantification'] = processing.run('native:rasterlayeruniquevaluesreport', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassAreaInMClassNrXlsx'] = outputs['ClassAreaQuantification']['OUTPUT_TABLE']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Join class name field
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'Value',
            'FIELDS_TO_COPY': ['Class'],
            'FIELD_2': 'Class nr',
            'INPUT': outputs['ClassAreaQuantification']['OUTPUT_TABLE'],
            'INPUT_2': parameters['roival'],
            'METHOD': 1,  # Nur Attribute des ersten passenden Objekts verwenden (eins-zu-eins)
            'PREFIX': '',
            'OUTPUT': parameters['ClassAreaInMAddClassNameXlsx']
        }
        outputs['JoinClassNameField'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClassAreaInMAddClassNameXlsx'] = outputs['JoinClassNameField']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS part 3 classification'

    def displayName(self):
        return 'MiGIS part 3 classification'

    def group(self):
        return 'MicroGIS'

    def groupId(self):
        return 'MicroGIS'

    def createInstance(self):
        return MigisPart3Classification()
