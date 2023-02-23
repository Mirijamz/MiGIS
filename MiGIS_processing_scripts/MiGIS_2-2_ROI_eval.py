
"""
Model exported as python. #modified
Name : MiGIS 2.2 ROI evaluation [optional]
Group : MiGIS
With QGIS : 32201
"""
import os
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsExpression
import processing


class Migis22RoiEvaluationOptional(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('multibandraster', 'Clipped multi-band raster (AOI, .tif)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('rois', 'ROI layer (training dataset, .shp)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classnamefiled', 'Class label field (string)', type=QgsProcessingParameterField.Any, parentLayerParameterName='rois', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('roistats', 'ROI/band statistics (.csv)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('boxplotoutput', 'ROI/band box plots directory', behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(19, model_feedback)
        results = {}
        outputs = {}
        
        # Set variable for output directory
        BP_output = parameters['boxplotoutput']

        # Band 1: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b1_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band1roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}  

        # Band 2: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b2_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 2,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band2roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Band 3: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b3_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 3,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band3roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Band 4: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b4_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 4,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band4roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
 
        # Band 5: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b5_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 5,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band5roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Band 6: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b6_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 6,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band6roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Band 7: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b7_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 7,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band7roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Band 8: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b8_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 8,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band8roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Band 9: ROI pixel statistics (mean, st.dev.)
        alg_params = {
            'COLUMN_PREFIX': 'b9_',
            'INPUT': parameters['rois'],
            'INPUT_RASTER': parameters['multibandraster'],
            'RASTER_BAND': 9,
            'STATISTICS': [2,4],  # Mean,St dev
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Band9roipixelstats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Unite single band statistics
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['Band1roipixelstats']['OUTPUT'],outputs['Band2roipixelstats']['OUTPUT'],outputs['Band3roipixelstats']['OUTPUT'],outputs['Band4roipixelstats']['OUTPUT'],outputs['Band5roipixelstats']['OUTPUT'],outputs['Band6roipixelstats']['OUTPUT'],outputs['Band7roipixelstats']['OUTPUT'],outputs['Band8roipixelstats']['OUTPUT'],outputs['Band9roipixelstats']['OUTPUT']],
            'OUTPUT': parameters['roistats']
        }
        outputs['unitesinglebandstats'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['roistats'] = outputs['unitesinglebandstats']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Box plot 1
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b1_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b1.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            
        }
        outputs['Boxplot1'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Box plot 2
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b2_mean',           
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b2.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot2'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Box plot 3
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b3_mean',           
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b3.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot3'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

 
        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Box plot 4
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b4_mean',   
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b4.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot4'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Box plot 5
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b5_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b5.html")    
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot5'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Box plot 6
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b6_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b6.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot6'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}
        
        # Box plot 7
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b7_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b7.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot7'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
        
        # Box plot 8
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b8_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b8.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot8'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Box plot 9
        alg_params = {
            'INPUT': outputs['unitesinglebandstats']['OUTPUT'],
            'MSD': 1,  # Show Standard Deviation
            'NAME_FIELD': parameters['classnamefiled'],
            'VALUE_FIELD': 'b9_mean',
            'OUTPUT': os.path.join(BP_output, "ROI_BP_b9.html")
            #'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Boxplot9'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
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
        return """<html><body><p>MiGIS: Classify rock, sediment & soil thin sections

MiGIS 2 [optional]
Enables training class and raster band specific ROI (Regions of Interest) validation. 
For this purpose, a box plot diagram (.html file) for each input raster band will be created (ROI/band box plots directory output). 
This implies pixel value distribution (polygon area mean) within each class and related standard deviation. 
Raw pixel values (ROI/polygon mean) per class and for each band are provided in a CSV table (ROI/band statistics output).</p>
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
<h3>ROI/band statistics (.csv)</h3>
<p>Mean pixel values per ROI and class standard deviation for each band, stored in a CSV table. </p>
<h3>ROI/band box plots directory</h3>
<p>Box plot diagrams (.html files) for each single band, showing mean pixel values per ROI and class standard deviation. </p>
<br><p align="right">Algorithm author: 

Compilation: 
Mirijam Zickel, 2023. MiGIS Thin Section Classification. https://github.com/Mirijamz/MiGIS, 2022-05-15.

References:
QGIS Development Team, 2022. QGIS Geographic Information System, Version 3.22. Open Source Geospatial Foundation. https://www.qgis.org/en/site/index.html , 2022-05-04. </p><p align="right">Help author: Mirijam Zickel, 2022</p><p align="right">Algorithm version: MiGIS 1.0</p></body></html>"""

    def helpUrl(self):
        return 'https://github.com/Mirijamz/MiGIS'

    def createInstance(self):
        return Migis22RoiEvaluationOptional()
