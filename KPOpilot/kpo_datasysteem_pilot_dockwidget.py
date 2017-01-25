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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'kpo_datasysteem_pilot_dockwidget_base.ui'))


class KPOpilotDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(KPOpilotDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.plugin_dir = os.path.dirname(__file__)
        self.logosLabel.setPixmap(QtGui.QPixmap(self.plugin_dir + '/images/partner_logos.png'))

        # Dictionary containing all language in type/element/naming structure
        self.language = 'dutch'
        self.gui_name_dutch = {
            'vragenTabWidget' : ['Introductie',
                                 'Knooppunten',
                                 'Verstedelijking',
                                 'Koppelingen',
                                 'Bereikbaarheid'],
            'introductionLabel' : 'Project samenvatting',
            'introductionSummaryText' : '',
            'housingDemandBox': 'Huisaanbod',
            'knooppuntenStatusBox': 'Knooppunten status',
            'scenarioSelectBox': ['Huidig scenario',
                                  'WLO Laag 2040',
                                  'WLO Hoog 2040',
                                  'Primus'],
            'knooppuntenAttributeCombo': ['In- en uitstappers',
                                          'fietsstallingen',
                                          'perrons',
                                          'stijgpunten',
                                          'loopstromen']
        }
        # let's not do this for now
        self.gui_naming_english = {}



    '''General'''
    # Updating GUI elements
    def setLanguage(self):
        for widget in self.children():
            name = widget.objectName()
            if name in self.gui_name_dutch.keys():
                # Labels
                if isinstance(widget, QtGui.QLabel):
                    widget.setText(self.gui_name_dutch[name])
                # GroupBox
                elif isinstance(widget, QtGui.QGroupBox):
                    widget.setTitle(self.gui_name_dutch[name])
                # Tabs
                elif isinstance(widget, QtGui.QTabWidget):
                    for index, name in enumerate(self.gui_name_dutch[name]):
                        widget.setTabText(index, name)
                # ComboBox
                elif isinstance(widget, QtGui.QComboBox):
                    widget.addItems(self.gui_name_dutch[name])
                # CheckBox
                elif isinstance(widget, QtGui.QCheckBox):
                    widget.setText(self.gui_name_dutch[name])
                # Button
                elif isinstance(widget, QtGui.QPushButton):
                    widget.setText(self.gui_name_dutch[name])
                # Table
                elif isinstance(widget, QtGui.QTabWidget):
                    widget.setHorizontalHeaderLabels(self.gui_name_dutch[name])



    '''General'''
    def getWidget(self,gui_name):
        for widget in self.children():
            name = widget.objectName()
            if name == gui_name:
                return widget


    def setTextField(self, gui_name, text_list):
        field = self.getWidget(gui_name)
        field.clear()
        for line in text_list:
            field.append(line)


    def setLabelValue(self, gui_name, value):
        label = self.getWidget(gui_name)
        label.clearContent()
        label.setText(value)


    def setDataTableSize(self, gui_name, rows):
        if rows.type() == int:
            table = self.getWidget(gui_name)
            table.setRowCount(rows)


    def setDataTableField(self, gui_name, row, column, value):
        table = self.getWidget(gui_name)
        entry = QTableWidgetItem(value)
        table.setItem(row, column, entry)


    def setSliderRange(self, gui_name, min, max, step):
        slider = self.getWidget(gui_name)
        slider.setRange(min, max)
        slider.setSingleStep(step)


    def showChart(self):
        pass


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


    def ifShow(self):
        pass


    '''Knooppunten'''
    def getScenario(self):
        return self.scenarioSelectCombo.currentText()


    def getKnooppunt(self):
        return self.knooppuntenAttributeCombo.currentText()


    '''Verstedelijking'''
    def getIntensity(self):
        return self.intensitySelectCombo.currentText()


    def getIntensityValue(self):
        return self.intensityValueLabel.text()


    def updateIntensityValue(self):
        value = self.intensityValueSlider.tickPosition()
        self.setLabelValue('intensityValueLabel', value)


    def getLocation(self):
        return self.locationSelectCombo.currentText()


    '''Koppelingen'''
    def getOverbelast(self):
        return self.overbelastAttributeCombo.currentText()


    def getLocations(self):
        return self.importantSelectCombo.currentText()


    '''Mobiliteit'''
    def getPTAL(self):
        return self.ptalSelectCombo.currentText()


    def getLinks(self):
        return self.linkSelectCombo.currentText()


    def getStops(self):
        return self.stopSelectCombo.currentText()


    def getTime(self):
        return self.frequencyTimeCombo.currentText()
