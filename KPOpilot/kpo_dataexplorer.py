# -*- coding: utf-8 -*-
"""
/***************************************************************************
 KPOpilotDockWidget
                                 A QGIS plugin
 Knooppunten Datasysteem
                             -------------------
        begin                : 2016-12-19
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Jorge Gil
        email                : gil.jorge@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtCore, QtGui, uic

from qgis.core import *
from qgis.gui import *

import os.path

from . import utility_functions as uf

class KPOExplorer():

    def __init__(self, iface, dockwidget, plugin_dir):

        self.iface = iface
        self.dlg = dockwidget
        self.plugin_dir = plugin_dir
        self.canvas = self.iface.mapCanvas()
        self.legend = self.iface.legendInterface()

        self.dlg.visibilityChanged.connect(self.onShow)

        # Knooppunten
        self.dlg.scenarioSelectCombo.activated.connect(self.updateScenarioSummaryText)
        self.dlg.scenarioSelectCombo.activated.connect(self.showScenario)
        self.dlg.scenarioShowCheck.stateChanged.connect(self.showScenario)
        self.dlg.knooppuntenAttributeCombo.activated.connect(self.updateKnooppuntenSummaryTable)
        self.dlg.knooppuntenAttributeCombo.activated.connect(self.showKnooppunten)
        self.dlg.knooppuntenShowCheck.stateChanged.connect(self.showKnooppunten)
        self.dlg.knooppuntenChartButton.clicked.connect(self.showKnooppuntenChart)

        # Verstedelijking
        self.dlg.intensitySelectCombo.activated.connect(self.setIntensityValueSlider)
        self.dlg.intensitySelectCombo.activated.connect(self.setAccessibilityValueSlider)
        self.dlg.intensitySelectCombo.activated.connect(self.showIntensity)
        self.dlg.intensityShowCheck.stateChanged.connect(self.showIntensity)
        self.dlg.intensityValueSlider.valueChanged.connect(self.setIntensityValueSlider)
        self.dlg.accessibilityValueSlider.valueChanged.connect(self.setAccessibilityValueSlider)
        self.dlg.locationSelectCombo.activated.connect(self.updateLocationSummaryText)
        self.dlg.locationSelectCombo.activated.connect(self.updateLocationAttributeTable)
        self.dlg.locationSelectCombo.activated.connect(self.showLocations)
        self.dlg.locationShowCheck.stateChanged.connect(self.showLocations)
        self.dlg.locationChartButton.clicked.connect(self.showLocationChart)

        # Koppelingen
        self.dlg.overbelastAttributeCombo.activated.connect(self.showOverbelast)
        self.dlg.overbelastShowCheck.stateChanged.connect(self.showOverbelast)
        self.dlg.routesShowCheck.stateChanged.connect(self.showRoutes)
        self.dlg.routesShowCheck.stateChanged.connect(self.updateOverlapAttributeTable)
        self.dlg.importantSelectCombo.activated.connect(self.updateImportantAttributeTable)
        self.dlg.importantSelectCombo.activated.connect(self.showImportant)
        self.dlg.importantShowCheck.stateChanged.connect(self.showImportant)
        self.dlg.importantChartButton.clicked.connect(self.showImportantChart)

        # Mobiliteit
        self.dlg.isochroneWalkCheck.stateChanged.connect(self.showWalk)
        self.dlg.isochroneWalkCheck.stateChanged.connect(self.showCycling)
        self.dlg.isochroneWalkCheck.stateChanged.connect(self.showOV)
        self.dlg.ptalSelectCombo.activated.connect(self.showPTAL)
        self.dlg.ptalShowCheck.stateChanged.connect(self.showPTAL)
        self.dlg.linkSelectCombo.activated.connect(self.showLinkFrequency)
        self.dlg.linkFrequencyCheck.stateChanged.connect(self.showLinkFrequency)
        self.dlg.stopSelectCombo.activated.connect(self.showStopFrequency)
        self.dlg.stopFrequencyCheck.stateChanged.connect(self.showStopFrequency)
        self.dlg.frequencyTimeCombo.activated.connect(self.updateStopSummaryTable)


    def onShow(self):
        self.dlg.clearScenarioSummary()
        self.dlg.clearLocationSummary()
        self.dlg.updateIntensityValue()
        self.dlg.updateAccessibilityValue()

    def readDataModel(self):
        self.iface.project.read(QFileInfo(self.plugin_dir +'data/project.qgs'))


    def getModelLayers(self, geom='all', provider='all'):
        """Return list of valid QgsVectorLayer in QgsMapCanvas, with specific geometry type and/or data provider"""
        layers_list = []
        for layer in iface.mapCanvas().layers():
            add_layer = False
            if layer.isValid() and layer.type() == QgsMapLayer.VectorLayer:
                if layer.hasGeometryType() and (geom is 'all' or layer.geometryType() in geom):
                    if provider is 'all' or layer.dataProvider().name() in provider:
                        add_layer = True
            if add_layer:
                layers_list.append(layer)
        return layers_list


    '''Knooppunten'''
    def updateScenarioSummaryText(self):
        scenario = self.dlg.getScenario()
        scenario_summary = {'Current scenario':{'total':45324, 'walking':100, 'cycling':30, 'outside':10},
                            'WLO Hoog 2040': {'total':100, 'walking':90, 'cycling':325, 'outside':10},
                            'WLO Laag 2040': {'total':200, 'walking':100, 'cycling':60, 'outside':10},
                            'Primus': {'total':3430, 'walking':100, 'cycling':88, 'outside':10}}

        if self.dlg.language == 'dutch':
            summary_text = ['%i  totaal huishoudens' % scenario_summary[scenario]['total'],
                            '%i  huishoudens op loopafstand' % scenario_summary[scenario]['walking'],
                            '%i  huishoudens op loopafstand' % scenario_summary[scenario]['cycling'],
                            '%i  huishoudens op loopafstand' % scenario_summary[scenario]['outside']]

        self.setTextField('scenarioSummaryText', summary_text)


    def showScenario(self):
        if self.dlg.scenarioShowCheck.isChecked():
            scenario = self.dlg.getScenario()
            scenario_layers = {'Current scenario': ['ov_stops', 'station_isochrones'],
                               'WLO Hoog 2040': ['ov_stops'],
                               'WLO Laag 2040': ['station_isochrones'],
                               'Primus': []}
            layers = scenario_layers[scenario]
            self.showLayersInCanvas(layers)
        else:
            self.showLayersInCanvas([])


    def updateKnooppuntenSummaryTable(self):
        self.updateTable('ov_stops', 'knooppuntenSummaryTable')


    def showKnooppunten(self):
        if self.dlg.knooppuntenShowCheck.isChecked():
            knooppunten = self.dlg.getKnooppunt()
            knooppunten_layers = {'in- en uitstappers': ['ov_stops', 'station_isochrones'],
                                  'fietsenstallingen': ['ov_stops'],
                                  'perrons': ['station_isochrones'],
                                  'stijgpunten': [],
                                  'loopstromen': ['ov_stops', 'station_isochrones']}
            layers = knooppunten_layers[knooppunten]
            self.showLayersInCanvas(layers)
        else:
            self.showLayersInCanvas([])


    def showKnooppuntenChart(self):
        pass


    '''Verstedelijking'''
    def showIntensity(self):
        if self.dlg.intensityShowCheck.isChecked():
            intensity = self.dlg.getIntensity()
            intensity_layers = {'all population': ['ov_stops', 'station_isochrones'],
                                'residents': ['ov_stops'],
                                'workers': ['station_isochrones'],
                                'students': [],
                                'property value (WOZ)': [],
                                'built density': []}
            layers = intensity_layers[intensity]
            self.showLayersInCanvas(layers)
        else:
            self.showLayersInCanvas([])


    def setIntensityValueSlider(self):
        self.dlg.setSliderRange('intensityValueSlider', 0, 100, 10)
        self.dlg.updateIntensityValue()


    def setAccessibilityValueSlider(self):
        self.dlg.setSliderRange('accessibilityValueSlider', 0, 8, 1)
        self.dlg.updateAccessibilityValue()


    def updateLocationSelectCombo(self):
        pass


    def showLocations(self):
        pass


    def updateLocationSummaryText(self):
        pass


    def updateLocationAttributeTable(self):
        self.updateTable('ov_stops', 'locationAttributeTable')


    def showLocationChart(self):
        pass


    '''Koppelingen'''
    def showOverbelast(self):
        pass


    def showRoutes(self):
        pass


    def updateOverlapAttributeTable(self):
        pass


    def showImportant(self):
        pass


    def updateImportantAttributeTable(self):
        self.updateTable('ov_stops', 'importantAttributeTable')


    def showImportantChart(self):
        pass


    '''Bereikbaarheid'''
    def showWalk(self):
        pass


    def showCycling(self):
        pass


    def showOV(self):
        pass


    def showPTAL(self):
        pass


    def showLinkFrequency(self):
        pass


    def showStopFrequency(self):
        pass


    def updateStopSummaryTable(self):
        self.updateTable('ov_stops', 'stopSummaryTable')


    '''General'''
    # MapTip setup
    def createMapTip(self, layer, fields, mouse_location):
        self.tip = QgsMapTip()


    def changeMapTip(self):
        pass

    def showMapTip(self):
        if self.canvas.underMouse():
            pointQgs = self.lastMapPosition
            pointQt = self.canvas.mouseLastXY()
            self.canvas.showMapTip(self.layer, pointQgs, pointQt, self.canvas)

    # Selecting
    def setFeatureSelection(self, features, layer):
        if features:
            if layer.isValid():
                layer.setSelectedFeatures(features)

    # Canvas control
    def setExtentToLayer(self,layer):
        if layer.isValid():
            self.canvas.setExtent(layer.extent())
            self.canvas.refresh()

    def setExtentToSelection(self,layer):
        if layer.isValid():
            if layer.selectedFeatures():
                self.canvast.setExtent(layer.boundingBoxOfSelected())
                self.canvas.refresh()


    def showLayersInCanvas(self, layers):
        current_layers = self.legend.layers()
        for layer in current_layers:
            if layer.name() in layers:
                self.legend.setLayerVisible(layer, True)
            else:
                self.legend.setLayerVisible(layer, False)

    # Data reading
    def getLayerByName(self, name):
        layer = None
        for i in QgsMapLayerRegistry.instance().mapLayers().values():
            if i.name() == name:
                layer = i
        return layer

    def getFeatureValue(self, layer, id_field, id, value_field):
        exp = QgsExpression('%s = %s' % (id_field, id))
        request = QgsFeatureRequest(exp)
        fet = layer.getFeatures(request)
        value = fet[value_field]

        return value


    def setTextField(self, gui_name, text_list):
        self.dlg.setTextField(gui_name, text_list)


    def setLabelValue(self, gui_name, value):
        self.dlg.setLabelValue(gui_name, value)


    def setDataTable(self, gui_name, row, column, entry):
        self.dlg.setDataTableField(gui_name, row, column, entry)


    def updateTable(self, data_layer, gui_name):
        layer = self.getLayerByName(data_layer)
        layer_fields = layer.fields()
        self.dlg.setDataTableSize(gui_name, layer.featureCount())

        table_headers = self.dlg.getDataTableHeaders(gui_name)

        for row, fet in enumerate(layer.getFeatures()):
            for name in table_headers:
                if name in layer_fields:
                    self.dlg.setDataTableField(gui_name, row, column, QtGui.QTableWidgetItem(fet[name]))

