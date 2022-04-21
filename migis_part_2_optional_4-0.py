"""
Model exported as python.
Name : MiGIS part 2 ROI evaluation [optional]
Group : MicroGIS
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


class MigisPart2RoiEvaluationOptional(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # TL - Transmitted Light; scanned, georeferenced image
        #XPL - Cross Polarized Light;  scanned, georeferenced image
        #RL - Reflected Light; scanned, georeferenced image
        self.addParameter(QgsProcessingParameterRasterLayer('MultibandrasterTLXPLandoptRLbands', 'Multiband raster (TL, XPL and opt. RL bands)', defaultValue=None))
        # Polygon type required (.shp)
        #OBLIGATORY FIELDS (attribute table):
        #ID, Class, Class nr
        self.addParameter(QgsProcessingParameterVectorLayer('ROItrainingareasandclasses', 'ROI (training areas and classes)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classnamefiled', 'Class name field (string)', type=QgsProcessingParameterField.Any, parentLayerParameterName='ROItrainingareasandclasses', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('RoiStatisticsXlsx', 'ROI statistics (.xlsx)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand1', 'ROI boxplott band 1', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand2', 'ROI boxplott band 2', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand3', 'ROI boxplott band 3', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand4', 'ROI boxplott band 4', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand5', 'ROI boxplott band 5', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand6', 'ROI boxplott band 6', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand7', 'ROI boxplott band 7', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand8', 'ROI boxplott band 8', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('RoiBoxplottBand9', 'ROI boxplott band 9', fileFilter='HTML-Dateien (*.html)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(19, model_feedback)
        results = {}
        outputs = {}

        # Band 9: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b9_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 9,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band9RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Band 1: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b1_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 1,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band1RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Band 3: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b3_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 3,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band3RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Band 6: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b6_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 6,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band6RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Band 5: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b5_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 5,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band5RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Band 4: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b4_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 4,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band4RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Band 7: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b7_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 7,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band7RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Band 8: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b8_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 8,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band8RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Band 2: ROI pixel statistics (median, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b2_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 2,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band2RoiPixelStatisticsMedianStdev'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Unite single band statistics
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['Band1RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band2RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band3RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band4RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band5RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band6RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band7RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band8RoiPixelStatisticsMedianStdev']['OUTPUT'],outputs['Band9RoiPixelStatisticsMedianStdev']['OUTPUT']],
            'OUTPUT': parameters['RoiStatisticsXlsx']
        }
        outputs['UniteSingleBandStatistics'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiStatisticsXlsx'] = outputs['UniteSingleBandStatistics']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Boxplott 5
        # Band 5: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b5_median',
            'OUTPUT': parameters['RoiBoxplottBand5']
        }
        outputs['Boxplott5'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand5'] = outputs['Boxplott5']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Boxplott 2
        # Band 2: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b2_median',
            'OUTPUT': parameters['RoiBoxplottBand2']
        }
        outputs['Boxplott2'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand2'] = outputs['Boxplott2']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Boxplott 7
        # Band 7: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b7_median',
            'OUTPUT': parameters['RoiBoxplottBand7']
        }
        outputs['Boxplott7'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand7'] = outputs['Boxplott7']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Boxplott 4
        # Band 4: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b4_median',
            'OUTPUT': parameters['RoiBoxplottBand4']
        }
        outputs['Boxplott4'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand4'] = outputs['Boxplott4']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Boxplott 9
        # Band 9: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b9_median',
            'OUTPUT': parameters['RoiBoxplottBand9']
        }
        outputs['Boxplott9'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand9'] = outputs['Boxplott9']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Boxplott 8
        # Band 8: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b8_median',
            'OUTPUT': parameters['RoiBoxplottBand8']
        }
        outputs['Boxplott8'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand8'] = outputs['Boxplott8']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Boxplott 6
        # Band 6: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b6_median',
            'OUTPUT': parameters['RoiBoxplottBand6']
        }
        outputs['Boxplott6'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand6'] = outputs['Boxplott6']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Boxplott 1
        # Band 1: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b1_median',
            'OUTPUT': parameters['RoiBoxplottBand1']
        }
        outputs['Boxplott1'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand1'] = outputs['Boxplott1']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Boxplott 3
        # Band 3: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['UniteSingleBandStatistics']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b3_median',
            'OUTPUT': parameters['RoiBoxplottBand3']
        }
        outputs['Boxplott3'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand3'] = outputs['Boxplott3']['OUTPUT']
        return results

    def name(self):
        return 'MiGIS part 2 ROI evaluation [optional]'

    def displayName(self):
        return 'MiGIS part 2 ROI evaluation [optional]'

    def group(self):
        return 'MicroGIS'

    def groupId(self):
        return 'MicroGIS'

    def createInstance(self):
        return MigisPart2RoiEvaluationOptional()
