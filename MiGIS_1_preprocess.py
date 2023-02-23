"""
Model exported as python. #modified
Name : MiGIS 1 preprocess TS images
Group : MiGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterMultipleLayers
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class Migis1PreprocessTsImages(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterMultipleLayers('Georefthinsectionscans', 'Thin section scans (georef., .tif)', layerType=QgsProcessing.TypeRaster, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('TSareabeingclassified (2)', 'Area of interest (to be classified, .shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('MultibandRasterTlXplAndOptRlImageStackTif', 'Multi-band raster (TL, XPL and opt. RL image stack, .tif)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('ClippedMultibandRasterAoiTif', 'Clipped multi-band raster (AOI, .tif)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Merge (TS multi-band raster)
        alg_params = {
            'DATA_TYPE': 2,  # UInt16
            'EXTRA': '',
            'INPUT': parameters['Georefthinsectionscans'],
            'NODATA_INPUT': None,
            'NODATA_OUTPUT': 9999,
            'OPTIONS': '',
            'PCT': False,
            'SEPARATE': True,
            'OUTPUT': parameters['MultibandRasterTlXplAndOptRlImageStackTif']
        }
        outputs['MergeTsMultibandRaster'] = processing.run('gdal:merge', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MultibandRasterTlXplAndOptRlImageStackTif'] = outputs['MergeTsMultibandRaster']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # TS mutli-band image clip
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['MergeTsMultibandRaster']['OUTPUT'],
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
            'OUTPUT': parameters['ClippedMultibandRasterAoiTif']
        }
        outputs['TsMutlibandImageClip'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ClippedMultibandRasterAoiTif'] = outputs['TsMutlibandImageClip']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS 1 preprocess TS images'

    def displayName(self):
        return 'MiGIS 1 preprocess TS images'

    def group(self):
        return 'MiGIS'

    def groupId(self):
        return 'MiGIS'

    def shortHelpString(self):
        return """<html><body><p>MiGIS: Classify rock, sediment & soil thin sections

MiGIS 1
Creates a multi-band raster by merging the georeferenced thin section scans.
The multi-band raster will be used for classification training in (MiGIS 2). 
In addition, the classification area (sample section coverage) can be cropped using a clip layer.
This method enables class related spatial statistics (MiGIS 3) and minimises the computational effort.</p>
<h2>Input parameters</h2>
<h3>Thin section imagery (georef., .tif)</h3>
<p>Georeferenced thin section scans (max. three RGB images or 9 bands):
TL - transmitted light scanned image
XPL - cross polarized scanned image
RL - reflected light scanned image</p>
<h3>Area of interest (to be classified, .shp)</h3>
<p>Single polygon covering the sample section (or relevant parts) which needs to be classified. 
Should be sharply delimited to allow precise pore space volume calculation (MiGIS 3). 
Also, major artefacts of sample collection, storage, or production should be excluded here.</p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2023. MiGIS Thin Section Classification. https://github.com/Mirijamz/MiGIS, 2022-05-15.

References:
QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS'

    def createInstance(self):
        return Migis1PreprocessTsImages()
