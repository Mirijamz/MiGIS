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
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterDefinition
import processing


class MigisPart2RoiEvaluationOptional(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # TS - Thin section
        # TL - Transmitted Light; scanned, georeferenced image
        # XPL - Cross Polarized Light;  scanned, georeferenced image
        # RL - Reflected Light; scanned, georeferenced image
        self.addParameter(QgsProcessingParameterRasterLayer('MultibandrasterTLXPLandoptRLbands', 'Multiband raster (TL, XPL and opt. RL bands)', defaultValue=None))
        # Vector polygons required (.shp)m OBLIGATORY FIELDS (attribute table): ID, Class, Class nr
        param = QgsProcessingParameterVectorLayer('ROItrainingareasandclasses', 'ROI (training areas and classes)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand1', 'Zonal statistics band 1', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand2', 'Zonal statistics band 2', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand3', 'Zonal statistics band 3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand4', 'Zonal statistics band 4', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand5', 'Zonal statistics band 5', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand6', 'Zonal statistics band 6', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand7', 'Zonal statistics band 7', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand8', 'Zonal statistics band 8', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ZonalStatisticsBand9', 'Zonal statistics band 9', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
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
        feedback = QgsProcessingMultiStepFeedback(18, model_feedback)
        results = {}
        outputs = {}

        # Band 1: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b1_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 1,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand1']
        }
        outputs['Band1RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand1'] = outputs['Band1RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Band 2: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b2_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 2,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand2']
        }
        outputs['Band2RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand2'] = outputs['Band2RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
            
        # Band 3: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b3_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 3,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand3']
        }
        outputs['Band3RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand3'] = outputs['Band3RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
            
        # Boxplott 1
        # Band 1: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band1RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b1_median',
            'OUTPUT': parameters['RoiBoxplottBand1']
        }
        outputs['Boxplott1'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand1'] = outputs['Boxplott1']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Band 4: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b4_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 4,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand4']
        }
        outputs['Band4RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand4'] = outputs['Band4RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
            
        # Band 5: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b5_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 5,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand5']
        }
        outputs['Band5RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand5'] = outputs['Band5RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Band 6: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b6_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 6,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand6']
        }
        outputs['Band6RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand6'] = outputs['Band6RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
    
        # Band 7: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b7_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 7,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand7']
        }
        outputs['Band7RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand7'] = outputs['Band7RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
            
        # Band 8: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b8_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 8,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand8']
        }
        outputs['Band8RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand8'] = outputs['Band8RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
            
        # Band 9: ROI pixel statistics (median, st.dev.) as a table (.shp file)
        alg_params = {
            'COLUMN_PREFIX': 'b9_',
            'INPUT': parameters['ROItrainingareasandclasses'],
            'INPUT_RASTER': parameters['MultibandrasterTLXPLandoptRLbands'],
            'RASTER_BAND': 9,
            'STATISTICS': [3,4],  # Median,Std. Abw.
            'OUTPUT': parameters['ZonalStatisticsBand9']
        }
        outputs['Band9RoiPixelStatisticsMedianStdevAsATableShpFile'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ZonalStatisticsBand9'] = outputs['Band9RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Boxplott 6
        # Band 6: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band6RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b6_median',
            'OUTPUT': parameters['RoiBoxplottBand6']
        }
        outputs['Boxplott6'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand6'] = outputs['Boxplott6']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Boxplott 4
        # Band 4: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band4RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b4_median',
            'OUTPUT': parameters['RoiBoxplottBand4']
        }
        outputs['Boxplott4'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand4'] = outputs['Boxplott4']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Boxplott 3
        # Band 3: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band3RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b3_median',
            'OUTPUT': parameters['RoiBoxplottBand3']
        }
        outputs['Boxplott3'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand3'] = outputs['Boxplott3']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Boxplott 5
        # Band 5: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band5RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b5_median',
            'OUTPUT': parameters['RoiBoxplottBand5']
        }
        outputs['Boxplott5'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand5'] = outputs['Boxplott5']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Boxplott 2
        # Band 2: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band2RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b2_median',
            'OUTPUT': parameters['RoiBoxplottBand2']
        }
        outputs['Boxplott2'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand2'] = outputs['Boxplott2']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Boxplott 7
        # Band 7: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band7RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b7_median',
            'OUTPUT': parameters['RoiBoxplottBand7']
        }
        outputs['Boxplott7'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand7'] = outputs['Boxplott7']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
            
        # Boxplott 8
        # Band 8: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band8RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b8_median',
            'OUTPUT': parameters['RoiBoxplottBand8']
        }
        outputs['Boxplott8'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand8'] = outputs['Boxplott8']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
            
        # Boxplott 9
        # Band 9: ROI pixel statistics (median, st.dev.), boxplotted per class (.html file)
        alg_params = {
            'INPUT': outputs['Band9RoiPixelStatisticsMedianStdevAsATableShpFile']['OUTPUT'],
            'MSD': 1,  # Standardabweichung anzeigen
            'NAME_FIELD': 'Class',
            'VALUE_FIELD': 'b9_median',
            'OUTPUT': parameters['RoiBoxplottBand9']
        }
        outputs['Boxplott9'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['RoiBoxplottBand9'] = outputs['Boxplott9']['OUTPUT']
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
