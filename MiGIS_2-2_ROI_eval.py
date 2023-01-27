"""
Model exported as python.
Name : MiGIS 2.2 ROI evaluation [optional]
Group : MiGIS
With QGIS : 32201
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
import processing


class Migis22RoiEvaluationOptional(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('MultibandrasterTLXPLandoptRLbands', 'Clipped multi-band raster (AOI, .tif)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('ROItrainingareasandclasses', 'ROI layer (training dataset, .shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classnamefiled', 'Class label field (string)', type=QgsProcessingParameterField.Any, parentLayerParameterName='ROItrainingareasandclasses', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('RoiStatisticsCsv', 'ROI statistics (.csv)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand1Html', 'ROI boxplot band 1 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand2Html', 'ROI boxplot band 2 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand3Html', 'ROI boxplot band 3 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand4Html', 'ROI boxplot band 4 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand5Html', 'ROI boxplot band 5 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand6Html', 'ROI boxplot band 6 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand7Html', 'ROI boxplot band 7 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand8Html', 'ROI boxplot band 8 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplotBand9Html', 'ROI boxplot band 9 (.html)', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(19, model_feedback)
        results = {}
        outputs = {}

        # Band 4: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b4_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 4,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band4RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Band 1: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b1_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 1,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band1RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Band 7: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b7_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 7,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band7RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Band 2: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b2_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 2,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band2RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Band 8: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b8_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 8,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band8RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Band 5: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b5_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 5,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band5RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Band 3: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b3_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 3,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band3RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Band 9: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b9_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 9,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band9RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Band 6: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b6_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 6,
            'STATISTICS': [3,4],  # Median,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band6RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Unite single band statistics
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['Band1RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band2RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band3RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band4RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band5RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band6RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band7RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band8RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band9RoiPixelStatisticsMedianStdev']['OUTPUT']],
            'OUTPUT': parameters['RoiStatisticsCsv']
        }
        outputs['UniteSingleBandStatistics'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiStatisticsCsv'] = outputs['UniteSingleBandStatistics']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Boxplot 8
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b8_median',
            'OUTPUT': parameters['RoiBoxplotBand8Html']
        }
        outputs['Boxplot8'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand8Html'] = outputs['Boxplot8']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Boxplot 7
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b7_median',
            'OUTPUT': parameters['RoiBoxplotBand7Html']
        }
        outputs['Boxplot7'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand7Html'] = outputs['Boxplot7']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Boxplot 5
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b5_median',
            'OUTPUT': parameters['RoiBoxplotBand5Html']
        }
        outputs['Boxplot5'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand5Html'] = outputs['Boxplot5']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Boxplot 2
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b2_median',
            'OUTPUT': parameters['RoiBoxplotBand2Html']
        }
        outputs['Boxplot2'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand2Html'] = outputs['Boxplot2']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Boxplot 4
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b4_median',
            'OUTPUT': parameters['RoiBoxplotBand4Html']
        }
        outputs['Boxplot4'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand4Html'] = outputs['Boxplot4']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Boxplot 1
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b1_median',
            'OUTPUT': parameters['RoiBoxplotBand1Html']
        }
        outputs['Boxplot1'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand1Html'] = outputs['Boxplot1']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Boxplot 9
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b9_median',
            'OUTPUT': parameters['RoiBoxplotBand9Html']
        }
        outputs['Boxplot9'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand9Html'] = outputs['Boxplot9']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Boxplot 6
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b6_median',
            'OUTPUT': parameters['RoiBoxplotBand6Html']
        }
        outputs['Boxplot6'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand6Html'] = outputs['Boxplot6']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Boxplot 3
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b3_median',
            'OUTPUT': parameters['RoiBoxplotBand3Html']
        }
        outputs['Boxplot3'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplotBand3Html'] = outputs['Boxplot3']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS 2.2 ROI evaluation [optional]'

    def displayName(self):
        return 'MiGIS 2.2 ROI evaluation [optional]'

    def group(self):
        return 'MiGIS'

    def groupId(self):
        return 'MiGIS'

    def shortHelpString(self):
        return """<html><body><p>MiGIS: Classifiy sediment/soil thin sections

MiGIS 2 [optional]
This part offers the possibility to check the class-internal consistency of the generated training data (ROI- Regions of Interest). For this purpose, a boxplot diagram is created for each band which shows the pixel value distribution (polygon area median) of the class and the standard deviation. The raw data for the plots is provided in aCSV table.</p>
<h2>Input parameters</h2>
<h3>Clipped multi-band raster (AOI, .tif)</h3>
<p>Select the thin section to be classified. Preferably, a clipped multi-band raster containing TL, XPL and RL bands.</p>
<h3>ROI layer (training dataset, .shp)</h3>
<p>Training dataset (SHP format) with numeric (integer) class identification and class label field (text - string). Besides an ID field (integer) with unique value for each attribute (ROI polygon), there should always be at least two classes identified by different values in the attribute table.

Example attribute 1:
 Id (field 1) = 23
Class (field 2) = 1
Class label (field 3) = clay coating

Example attribute 2:
 Id (field 1) = 45
Class (field 2) = 2
Class label (field 3) = quarz</p>
<h3>Class label field (string)</h3>
<p>Text field with class description/names (ROI layer). Used as input for the class area statistics.</p>
<h2>Outputs</h2>
<h3>ROI statistics (.csv)</h3>
<p>Mean pixel values per ROI and standard deviation for each band, stored in a CSV table. </p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2022. MiGIS Thin Section Classification. https://github.com/Mirijamz/MiGIS-script, 2022-05-15.

References:
QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS-script'

    def createInstance(self):
        return Migis22RoiEvaluationOptional()
