#WISHLIST:
#input: set band order for TS raster input files
#output: multiband image before clipped multiband images (order in tool frontend), set output von 'clipped section' and clipped - to be classified' to OPTIONAL

"""
Model exported as python.
Name : MiGIS part 1 preprocess the TS image (create clipped multiband image)
Group : MicroGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterMultipleLayers
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class MigisPart1PreprocessTheTsImageCreateClippedMultibandImage(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # TL - Transmitted Light; scanned, georeferenced image
        #XPL - Cross Polarized Light;  scanned, georeferenced image
        #RL - Reflected Light; scanned, georeferenced image

        self.addParameter(QgsProcessingParameterMultipleLayers('Georefthinsectionscans', 'Georef. thin section scans TL (PPL), XPL & opt.  RL (OIL)', layerType=QgsProcessing.TypeRaster, defaultValue=None))
        # Rectangular polygon which approx. covers the sediment section
        self.addParameter(QgsProcessingParameterVectorLayer('TSareabeingclassified', 'TS section cover (rectangular polygon)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # Single polygon which covers relevant parts of the sediment section only
        self.addParameter(QgsProcessingParameterVectorLayer('TSareabeingclassified (2)', 'TS section to be classified (relevant section part only, amorphous polygon)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('BMultibandImageClipSectionCover', 'B Multiband image clip  (section cover)', createByDefault=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterDestination('MultibandImageClipToBeClassified', 'Multiband image clip (to be classified)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('MultibandImageTlXplAndOptRl', 'Multiband image (TL, XPL and opt. RL)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Merge (TS multiband image)
        alg_params = {
            'DATA_TYPE': 2,  # UInt16
            'EXTRA': '',
            'INPUT': parameters['Georefthinsectionscans'],
            'NODATA_INPUT': None,
            'NODATA_OUTPUT': 9999,
            'OPTIONS': '',
            'PCT': False,
            'SEPARATE': True,
            'OUTPUT': parameters['MultibandImageTlXplAndOptRl']
        }
        outputs['MergeTsMultibandImage'] = processing.run('gdal:merge', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MultibandImageTlXplAndOptRl'] = outputs['MergeTsMultibandImage']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Clip (TS section to be classified)
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Eingabelayerdatentyp verwenden
            'EXTRA': '',
            'INPUT': outputs['MergeTsMultibandImage']['OUTPUT'],
            'KEEP_RESOLUTION': True,
            'MASK': parameters['TSareabeingclassified (2)'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': None,
            'TARGET_CRS': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['MultibandImageClipToBeClassified']
        }
        outputs['ClipTsSectionToBeClassified'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MultibandImageClipToBeClassified'] = outputs['ClipTsSectionToBeClassified']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Clip (TS section)
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Eingabelayerdatentyp verwenden
            'EXTRA': '',
            'INPUT': outputs['MergeTsMultibandImage']['OUTPUT'],
            'KEEP_RESOLUTION': True,
            'MASK': parameters['TSareabeingclassified'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': None,
            'TARGET_CRS': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['BMultibandImageClipSectionCover']
        }
        outputs['ClipTsSection'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BMultibandImageClipSectionCover'] = outputs['ClipTsSection']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS part 1 preprocess the TS image (create clipped multiband image)'

    def displayName(self):
        return 'MiGIS part 1 preprocess the TS image (create clipped multiband image)'

    def group(self):
        return 'MicroGIS'

    def groupId(self):
        return 'MicroGIS'

    def createInstance(self):
        return MigisPart1PreprocessTheTsImageCreateClippedMultibandImage()
