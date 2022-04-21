"""
Model exported as python.
Name : MiGIS part 2 train algorithm
Group : MicroGIS
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


class MigisPart2TrainAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # TL - Transmitted Light; scanned, georeferenced image
        #XPL - Cross Polarized Light;  scanned, georeferenced image
        #RL - Reflected Light; scanned, georeferenced image

        self.addParameter(QgsProcessingParameterRasterLayer('ClippedmultibandTSimageTLXPLRL', 'Clipped multiband TS image (TL, XPL, RL)', defaultValue=None))
        # OBLIGATORY FIELDS (attribute table): ID, Class, Class nr
        self.addParameter(QgsProcessingParameterVectorLayer('ROItrainingdata', 'ROI (vector training data with target classes)', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classfieldint', 'Class field (integer e.g. 1=pore space, 2=quarz etc.)', type=QgsProcessingParameterField.Any, parentLayerParameterName='ROItrainingdata', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RandomForestClassificationModelModel', 'Random Forest classification model (.model)', fileFilter='Alle Dateien (*.*)', createByDefault=True, defaultValue=None))

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
            'SPLIT_PERCENT': 0,
            'TRAIN': 1,  # Random-Forest
            'OUTPUT_MATRIX': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT_MODEL': parameters['RandomForestClassificationModelModel']
        }
        outputs['TrainAlgorithmDzetsaka'] = processing.run('dzetsaka:Train algorithm', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RandomForestClassificationModelModel'] = outputs['TrainAlgorithmDzetsaka']['OUTPUT_MODEL']
        return results

    def name(self):
        return 'MiGIS part 2 train algorithm'

    def displayName(self):
        return 'MiGIS part 2 train algorithm'

    def group(self):
        return 'MicroGIS'

    def groupId(self):
        return 'MicroGIS'

    def createInstance(self):
        return MigisPart2TrainAlgorithm()
