# -*- coding: utf-8 -*-
"""
/***************************************************************************
 KPOpilotDockWidget
                                 A QGIS plugin
 Knooppunten Datasysteem
                             -------------------
        begin                : 2016-12-19
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Jorge Gil
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
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'kpo_datasysteem_pilot_dockwidget_base.ui'))


class KPOpilotDockWidget(QtGui.QDockWidget, FORM_CLASS):
    # set dialog user signals
    closingPlugin = pyqtSignal()
    tabChanged = pyqtSignal(int)
    # knooppunten
    scenarioChanged = pyqtSignal(str)
    scenarioShow = pyqtSignal(bool)
    isochronesShow = pyqtSignal(bool)
    todLevelChanged = pyqtSignal(int)
    knooppuntChanged = pyqtSignal(str)
    knooppuntShow = pyqtSignal(bool)
    knooppuntSelected = pyqtSignal(str)
    knooppuntDeselected = pyqtSignal(str)
    # verstedelijking
    onderbenutShow = pyqtSignal(bool)
    intensityTypeChanged = pyqtSignal(str)
    intensityShow = pyqtSignal(bool)
    intensityLevelChanged = pyqtSignal(int)
    accessibilityShow = pyqtSignal(bool)
    accessibilityLevelChanged = pyqtSignal(int)
    planTypeChanged = pyqtSignal(str)
    planShow = pyqtSignal(bool)
    planSelected = pyqtSignal(str)
    planDeselected = pyqtSignal(str)
    # afvangstations
    stationAttributeChanged = pyqtSignal(str)
    stationShow = pyqtSignal(bool)
    stationSelected = pyqtSignal(str)
    stationDeselected = pyqtSignal(str)
    locationTypeChanged = pyqtSignal(str)
    locationShow = pyqtSignal(bool)
    locationSelected = pyqtSignal(str)
    locationDeselected = pyqtSignal(str)
    # mobiliteit
    isochroneWalkShow = pyqtSignal(bool)
    isochroneBikeShow = pyqtSignal(bool)
    isochroneOVShow = pyqtSignal(bool)
    ptalChanged = pyqtSignal(str)
    ptalShow = pyqtSignal(bool)
    frequencyChanged = pyqtSignal(str)
    stopsChanged = pyqtSignal(str)
    stopsShow = pyqtSignal(bool)
    stopsSelected = pyqtSignal(str)
    stopsDeselected = pyqtSignal(str)

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

        # set-up dialog defaults
        self.resetDefaults()

        # set-up UI interaction signals
        self.vragenTabWidget.currentChanged.connect(self.__changeQuestionTab__)

        #  Knooppunten
        self.scenarioSelectCombo.currentIndexChanged.connect(self.__setScenario__)
        self.scenarioShowCheck.stateChanged.connect(self.__showScenario__)
        self.isochronesShowCheck.stateChanged.connect(self.__showIsochrones__)
        self.todPolicySlider.valueChanged.connect(self.__updateTODLevel__)
        self.knooppuntenAttributeCombo.currentIndexChanged.connect(self.__setKnooppuntKenmerk__)
        self.knooppuntenShowCheck.stateChanged.connect(self.__showKnooppunt__)
        self.knooppuntenSummaryTable.itemClicked.connect(self.__setKnooppunt__)
        self.knooppuntenSummaryTable.horizontalHeader().sortIndicatorChanged.connect(self.__updateKnooppunt__)
        # Verstedelijking
        self.locatiesShowCheck.stateChanged.connect(self.__showOnderbenutLocaties__)
        self.intensitySelectCombo.currentIndexChanged.connect(self.__setIntensity__)
        self.intensityShowCheck.stateChanged.connect(self.__showIntensity__)
        self.intensityValueSlider.valueChanged.connect(self.__updateIntensityLevel__)
        self.accessibilityShowCheck.stateChanged.connect(self.__showAccessibility__)
        self.accessibilityValueSlider.valueChanged.connect(self.__updateAccessibilityLevel__)
        self.planSelectCombo.currentIndexChanged.connect(self.__setPlan__)
        self.planShowCheck.stateChanged.connect(self.__showPlan__)
        self.planAttributeTable.itemClicked.connect(self.__setPlanLocation__)
        self.planAttributeTable.horizontalHeader().sortIndicatorChanged.connect(self.__updatePlanLocation__)
        # Verbindingen
        self.overbelastAttributeCombo.currentIndexChanged.connect(self.__setStationKenmerk__)
        self.overbelastShowCheck.stateChanged.connect(self.__showStations__)
        self.overbelastAttributeTable.itemClicked.connect(self.__setStation__)
        self.overbelastAttributeTable.horizontalHeader().sortIndicatorChanged.connect(self.__updateStation__)
        self.locationSelectCombo.currentIndexChanged.connect(self.__setLocationType__)
        self.locationShowCheck.stateChanged.connect(self.__showLocations__)
        self.locationAttributeTable.itemClicked.connect(self.__setLocation__)
        self.locationAttributeTable.horizontalHeader().sortIndicatorChanged.connect(self.__updateLocation__)
        # Mobiliteit
        self.isochroneWalkCheck.stateChanged.connect(self.__showWalk__)
        self.isochroneBikeCheck.stateChanged.connect(self.__showBike__)
        self.isochroneOvCheck.stateChanged.connect(self.__showOV__)
        self.ptalSelectCombo.activated.connect(self.__setPTAL__)
        self.ptalShowCheck.stateChanged.connect(self.__showPTAL__)
        self.frequencyTimeCombo.currentIndexChanged.connect(self.__setTimePeriod__)
        self.stopSelectCombo.currentIndexChanged.connect(self.__setStopType__)
        self.stopFrequencyCheck.stateChanged.connect(self.__showStops__)
        self.stopSummaryTable.itemClicked.connect(self.__setStops__)
        self.stopSummaryTable.horizontalHeader().sortIndicatorChanged.connect(self.__updateStops__)

        # some globals
        self.current_tab = 0
        self.locatiesShowCheck.hide()
        self.current_knooppunt = -1
        self.current_plan = -1
        self.current_station = -1
        self.current_location = -1
        self.current_stop = -1

    #####
    # Main
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def __changeQuestionTab__(self, tab_id):
        # make changes if not visiting the introduction
        # and if not returning to the same tab as before
        if tab_id > 0 and tab_id != self.current_tab:
            self.current_tab = tab_id
            self.tabChanged.emit(self.current_tab)

    def resetQuestionTab(self):
        self.vragenTabWidget.setCurrentIndex(0)
        self.current_tab = 0

    def resetDefaults(self):
        #  Knooppunten
        self.scenarioSelectCombo.setCurrentIndex(1)
        self.scenarioShowCheck.setChecked(True)
        self.isochronesShowCheck.setChecked(True)
        self.__activateTODLevel__(True)
        self.todPolicyValueLabel.hide()
        self.todPolicySlider.setValue(0)
        self.knooppuntenAttributeCombo.setCurrentIndex(0)
        self.knooppuntenShowCheck.setChecked(True)

        # Verstedelijking
        self.locatiesShowCheck.setChecked(True)
        self.intensitySelectCombo.setCurrentIndex(0)
        self.intensityShowCheck.setChecked(False)
        self.intensityValueSlider.setValue(0)
        self.accessibilityShowCheck.setChecked(False)
        self.accessibilityValueSlider.setValue(5)
        self.planSelectCombo.setCurrentIndex(0)
        self.planShowCheck.setChecked(True)

        # Verbindingen
        self.overbelastAttributeCombo.setCurrentIndex(0)
        self.overbelastShowCheck.setChecked(True)
        self.locationSelectCombo.setCurrentIndex(0)
        self.locationShowCheck.setChecked(True)

        # Mobiliteit
        self.isochroneWalkCheck.setChecked(True)
        self.isochroneBikeCheck.setChecked(True)
        self.isochroneOvCheck.setChecked(True)
        self.ptalSelectCombo.setCurrentIndex(0)
        self.ptalShowCheck.setChecked(False)
        self.frequencyTimeCombo.setCurrentIndex(0)
        self.stopSelectCombo.setCurrentIndex(0)
        self.stopFrequencyCheck.setChecked(False)

    #####
    # Knooppunten
    # Methods for Woonscenario
    def __setScenario__(self):
        scenario_name = self.scenarioSelectCombo.currentText()
        self.scenarioChanged.emit(scenario_name)
        if scenario_name == 'Huidige situatie':
            self.__activateTODLevel__(False)
        else:
            self.__activateTODLevel__(True)

    def getScenario(self):
        return self.scenarioSelectCombo.currentText()

    def isScenarioVisible(self):
        return self.scenarioShowCheck.isChecked()

    def __showScenario__(self, state):
        self.scenarioShow.emit(state)

    def isIsochronesVisible(self):
        return self.isochronesShowCheck.isChecked()

    def __showIsochrones__(self, state):
        self.isochronesShow.emit(state)

    # Methods for TOD level
    def __activateTODLevel__(self, onoff):
        self.todPolicyLabel.setEnabled(onoff)
        self.todPolicySlider.setEnabled(onoff)
        self.todPolicyValueLabel.setEnabled(onoff)
        if not onoff:
            self.todPolicySlider.setValue(0)

    def getTODLevel(self):
        value = self.todPolicySlider.value()
        if value == 1:
            tod_level = 50
        elif value == 2:
            tod_level = 100
        else:
            tod_level = 0
        return tod_level

    def __updateTODLevel__(self, value):
        tod_level = 0
        if value == 1:
            tod_level = 50
        elif value == 2:
            tod_level = 100
        self.todPolicyValueLabel.setText('%d%%' % tod_level)
        self.todLevelChanged.emit(tod_level)

    def updateScenarioSummary(self, data_values):
        text_list = []
        if len(data_values) == 4:
            text_list.append('%s  totaal huishoudens' % '{:,}'.format(data_values[0]).replace(',','.'))
            text_list.append('%s  op loopafstand van knooppunten' % '{:,}'.format(data_values[1]).replace(',','.'))
            text_list.append('%s  op fietsafstand van knooppunten' % '{:,}'.format(data_values[2]).replace(',','.'))
            text_list.append('%s  buiten invloedsgebied van knooppunten' % '{:,}'.format(data_values[3]).replace(',','.'))
            self.__setTextField__('scenarioSummaryText', text_list)

    # Methods for Knooppunten
    def __setKnooppuntKenmerk__(self):
        attribute = self.knooppuntenAttributeCombo.currentText()
        self.knooppuntChanged.emit(attribute)

    def getKnooppuntKenmerk(self):
        return self.knooppuntenAttributeCombo.currentText()

    def isKnooppuntVisible(self):
        return self.knooppuntenShowCheck.isChecked()

    def __showKnooppunt__(self, state):
        self.knooppuntShow.emit(state)

    def updateKnooppuntenTable(self, headers, data_values):
        if self.current_knooppunt >= 0:
            # get the current selection
            current_row = self.knooppuntenSummaryTable.currentRow()
            current_item = self.knooppuntenSummaryTable.item(current_row, 0)
            station_name = current_item.text()
            # update the table
            self.__populateDataTable__('knooppuntenSummaryTable', headers, data_values)
            # reselect the current selection (can be in a different row)
            for row in xrange(self.knooppuntenSummaryTable.rowCount()):
                item = self.knooppuntenSummaryTable.item(row, 0)
                text = item.text()
                if text == station_name:
                    self.knooppuntenSummaryTable.selectRow(row)
                    self.current_knooppunt = row
                    break
        else:
            # simply update the table
            self.__populateDataTable__('knooppuntenSummaryTable', headers, data_values)

    def __setKnooppunt__(self):
        current_row = self.knooppuntenSummaryTable.currentRow()
        current_item = self.knooppuntenSummaryTable.item(current_row, 0)
        station_name = current_item.text()
        if self.current_knooppunt != current_row:
            self.current_knooppunt = current_row
            self.knooppuntSelected.emit(station_name)
        elif self.current_knooppunt >= 0 and self.current_knooppunt == current_row:
            self.current_knooppunt = -1
            self.knooppuntDeselected.emit(station_name)
            self.knooppuntenSummaryTable.clearSelection()
            print self.isKnooppuntSelected()

    def isKnooppuntSelected(self):
        if self.current_knooppunt >= 0:
            return True
        else:
            return False

    def __updateKnooppunt__(self):
        current_row = self.knooppuntenSummaryTable.currentRow()
        if current_row >= 0:
            self.current_knooppunt = current_row
        else:
            self.current_knooppunt = -1

    #####
    # Verstedelijking
    # Methods for opportunities
    def __showOnderbenutLocaties__(self, state):
        self.onderbenutShow.emit(state)

    def isLocatiesVisible(self):
        return self.locatiesShowCheck.isChecked()

    def __showIntensity__(self, state):
        self.intensityShow.emit(state)

    def isIntensityVisible(self):
        return self.intensityShowCheck.isChecked()

    def __setIntensity__(self):
        attribute = self.intensitySelectCombo.currentText()
        self.intensityTypeChanged.emit(attribute)

    def getIntensityType(self):
        return self.intensitySelectCombo.currentText()

    def getIntensityLevel(self):
        value = self.intensityValueSlider.value()
        return value

    def __updateIntensityLevel__(self, value):
        self.intensityLevelChanged.emit(value)

    def updateIntensityLabel(self, intensity_label):
        self.intensityValueLabel.setText('%s' % intensity_label)

    def __showAccessibility__(self, state):
        self.accessibilityShow.emit(state)

    def isAccessibilityVisible(self):
        return self.accessibilityShowCheck.isChecked()

    def getAccessibilityLevel(self):
        value = self.accessibilityValueSlider.value()
        return value

    def __updateAccessibilityLevel__(self, value):
        self.accessibilityLevelChanged.emit(value)

    def updateAccessibilityLabel(self, ptal_label):
        self.accessibilityValueLabel.setText('%s' % ptal_label)

    # Methods for plans
    def __showPlan__(self, state):
        self.planShow.emit(state)

    def isPlanVisible(self):
        return self.planShowCheck.isChecked()

    def __setPlan__(self):
        attribute = self.planSelectCombo.currentText()
        self.planTypeChanged.emit(attribute)

    def getPlanType(self):
        return self.planSelectCombo.currentText()

    def updatePlanSummary(self, data_values):
        text_list = []
        if len(data_values) == 3:
            text_list.append('%s  totaal woningen' % '{:,}'.format(data_values[0]).replace(',','.'))
            text_list.append('%s  in onderbenute bereikbaare locaties' % '{:,}'.format(data_values[1]).replace(',','.'))
            text_list.append('%s  buiten onderbenute bereikbaare locaties' % '{:,}'.format(data_values[2]).replace(',','.'))
            self.__setTextField__('planSummaryText', text_list)

    def updatePlanTable(self, headers, data_values):
        if self.current_plan >= 0:
            # get the current selection
            current_row = self.planAttributeTable.currentRow()
            current_item = self.planAttributeTable.item(current_row, 0)
            location_name = current_item.text()
            # update the table
            self.__populateDataTable__('planAttributeTable', headers, data_values)
            # reselect the current selection (can be in a different row)
            for row in xrange(self.planAttributeTable.rowCount()):
                item = self.planAttributeTable.item(row, 0)
                text = item.text()
                if text == location_name:
                    self.planAttributeTable.selectRow(row)
                    self.current_plan = row
                    break
        else:
            # simply update the table
            self.__populateDataTable__('planAttributeTable', headers, data_values)

    def __setPlanLocation__(self):
        current_row = self.planAttributeTable.currentRow()
        current_item = self.planAttributeTable.item(current_row, 0)
        location_name = current_item.text()
        if self.current_plan != current_row:
            self.current_plan = current_row
            self.planSelected.emit(location_name)
        elif self.current_plan >=0 and self.current_plan == current_row:
            self.planAttributeTable.clearSelection()
            self.current_plan = -1
            self.planDeselected.emit(location_name)

    def isPlanLocationSelected(self):
        if self.current_plan >= 0:
            return True
        else:
            return False

    def __updatePlanLocation__(self):
        current_row = self.planAttributeTable.currentRow()
        if current_row >= 0:
            self.current_plan = current_row
        else:
            self.current_plan = -1

    #####
    # Verbindingen
    # Methods for Overbelast stations
    def __showStations__(self, state):
        self.stationShow.emit(state)

    def isStationVisible(self):
        return self.overbelastShowCheck.isChecked()

    def __setStationKenmerk__(self):
        attribute = self.overbelastAttributeCombo.currentText()
        self.stationAttributeChanged.emit(attribute)

    def getSationAttribute(self):
        return self.overbelastAttributeCombo.currentText()

    def updateStationsTable(self, headers, data_values):
        # get the current selection
        if self.current_station >= 0:
            current_row = self.overbelastAttributeTable.currentRow()
            current_item = self.overbelastAttributeTable.item(current_row, 0)
            station_name = current_item.text()
            # update the table
            self.__populateDataTable__('overbelastAttributeTable', headers, data_values)
            # reselect the current selection (can be in a different row)
            for row in xrange(self.overbelastAttributeTable.rowCount()):
                item = self.overbelastAttributeTable.item(row, 0)
                text = item.text()
                if text == station_name:
                    self.overbelastAttributeTable.selectRow(row)
                    self.current_station = row
                    break
        else:
            # simply update the table
            self.__populateDataTable__('overbelastAttributeTable', headers, data_values)

    def __setStation__(self):
        current_row = self.overbelastAttributeTable.currentRow()
        current_item = self.overbelastAttributeTable.item(current_row, 0)
        station_name = current_item.text()
        if self.current_station != current_row:
            self.current_station = current_row
            self.stationSelected.emit(station_name)
        elif self.current_station >= 0 and self.current_station == current_row:
            self.current_station = -1
            self.stationDeselected.emit(station_name)
            self.overbelastAttributeTable.clearSelection()

    def isStationSelected(self):
        if self.current_station >= 0:
            return True
        else:
            return False

    def __updateStation__(self):
        current_row = self.overbelastAttributeTable.currentRow()
        if current_row >= 0:
            self.current_station = current_row
        else:
            self.current_station = -1

    # Methods for Locaties
    def __showLocations__(self, state):
        self.locationShow.emit(state)

    def isLocationVisible(self):
        return self.locationShowCheck.isChecked()

    def __setLocationType__(self):
        attribute = self.locationSelectCombo.currentText()
        self.locationTypeChanged.emit(attribute)
        if self.current_location >= 0:
            self.locationAttributeTable.clearSelection()
            self.current_location = -1

    def getLocationType(self):
        return self.locationSelectCombo.currentText()

    def updateLocationsTable(self, headers, data_values):
        # get the current selection
        if self.current_location >= 0:
            current_row = self.locationAttributeTable.currentRow()
            current_item = self.locationAttributeTable.item(current_row, 0)
            location_name = current_item.text()
            # update the table
            self.__populateDataTable__('locationAttributeTable', headers, data_values)
            # reselect the current selection (can be in a different row)
            for row in xrange(self.locationAttributeTable.rowCount()):
                item = self.locationAttributeTable.item(row, 0)
                text = item.text()
                if text == location_name:
                    self.locationAttributeTable.selectRow(row)
                    self.current_location = row
                    break
        else:
            # simply update the table
            self.__populateDataTable__('locationAttributeTable', headers, data_values)

    def __setLocation__(self):
        current_row = self.locationAttributeTable.currentRow()
        current_item = self.locationAttributeTable.item(current_row, 0)
        location_name = current_item.text()
        if self.current_location != current_row:
            self.current_location = current_row
            self.locationSelected.emit(location_name)
        elif self.current_location >= 0 and self.current_location == current_row:
            self.current_location = -1
            self.locationDeselected.emit(location_name)
            self.locationAttributeTable.clearSelection()

    def isLocationSelected(self):
        if self.current_location >= 0:
            return True
        else:
            return False

    def __updateLocation__(self):
        row = self.locationAttributeTable.currentRow()
        if row >= 0:
            self.current_location = row
        else:
            self.current_location = -1

    #####
    # Mobiliteit
    # Methods for Isochronen
    def __showWalk__(self, state):
        self.isochroneWalkShow.emit(state)

    def isWalkVisible(self):
        return self.isochroneWalkCheck.isChecked()

    def __showBike__(self, state):
        self.isochroneBikeShow.emit(state)

    def isBikeVisible(self):
        return self.isochroneBikeCheck.isChecked()

    def __showOV__(self, state):
        self.isochroneOVShow.emit(state)

    def isOvVisible(self):
        return self.isochroneOvCheck.isChecked()

    # Methods for Bereikbaarheid
    def __showPTAL__(self, state):
        self.ptalShow.emit(state)

    def isPTALVisible(self):
        return self.ptalShowCheck.isChecked()

    def __setPTAL__(self):
        attribute = self.ptalSelectCombo.currentText()
        self.ptalChanged.emit(attribute)

    def getPTAL(self):
        return self.ptalSelectCombo.currentText()

    # Methods for stops frequency
    def __showStops__(self, state):
        self.stopsShow.emit(state)

    def __setStopType__(self):
        attribute = self.stopSelectCombo.currentText()
        self.stopsChanged.emit(attribute)
        self.stopSummaryTable.clearSelection()

    def isStopsVisible(self):
        return self.stopFrequencyCheck.isChecked()

    def getStops(self):
        return self.stopSelectCombo.currentText()

    def __setTimePeriod__(self):
        attribute = self.frequencyTimeCombo.currentText()
        self.frequencyChanged.emit(attribute)

    def getTimePeriod(self):
        return self.frequencyTimeCombo.currentText()

    def updateStopsTable(self, headers, data_values):
        # get the current selection
        if self.current_stop >= 0:
            current_row = self.stopSummaryTable.currentRow()
            current_item = self.stopSummaryTable.item(current_row, 0)
            stop_name = current_item.text()
            # update the table
            self.__populateDataTable__('stopSummaryTable', headers, data_values)
            # reselect the current selection (can be in a different row)
            self.current_stop = -1
            for row in xrange(self.stopSummaryTable.rowCount()):
                item = self.stopSummaryTable.item(row, 0)
                text = item.text()
                if text == stop_name:
                    self.stopSummaryTable.selectRow(row)
                    self.current_stop = row
                    break
            # if the stop type changes there might be a different list
            if self.current_stop == -1:
                self.stopSummaryTable.clearSelection()
                self.stopsDeselected.emit(stop_name)
        else:
            # simply update the table
            self.__populateDataTable__('stopSummaryTable', headers, data_values)

    def __setStops__(self):
        current_row = self.stopSummaryTable.currentRow()
        current_item = self.stopSummaryTable.item(current_row, 0)
        stop_name = current_item.text()
        if self.current_stop != current_row:
            self.current_stop = current_row
            self.stopsSelected.emit(stop_name)
        elif self.current_stop >= 0 and self.current_stop == current_row:
            self.stopSummaryTable.clearSelection()
            self.current_stop = -1
            self.stopsDeselected.emit(stop_name)

    def isStopSelected(self):
        if self.current_stop >= 0:
            return True
        else:
            return False

    def __updateStops__(self):
        current_row = self.stopSummaryTable.currentRow()
        if current_row >= 0:
            self.current_stop = current_row
        else:
            self.current_stop = -1

    #####
    # General functions
    def __setTextField__(self, gui_name, text_list):
        field2 = self.findChild(QtGui.QTextEdit, gui_name)
        field2.clear()
        for line in text_list:
            field2.append(line)

    def __populateDataTable__(self, gui_name, headers, values):
        table = self.findChild(QtGui.QTableWidget, gui_name)
        table.clear()
        columns = len(headers)
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        table.verticalHeader().setVisible(False)
        table.setSortingEnabled(False)
        rows = len(values)
        table.setRowCount(rows)
        for i, feature in enumerate(values):
            for j in range(columns):
                entry = QtGui.QTableWidgetItem()
                # this way of adding values allows sorting numbers numerically, not as text
                entry.setData(QtCore.Qt.EditRole, feature[j])
                table.setItem(i, j, entry)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.horizontalHeader().setResizeMode(columns - 1, QtGui.QHeaderView.Stretch)

    def __setSliderRange__(self, gui_name, minimum, maximum, step):
        slider = self.findChild(QtGui.QSlider, gui_name)
        slider.setRange(minimum, maximum)
        slider.setSingleStep(step)

    # check if a text string is of numeric type
    def isNumeric(self, txt):
        if txt != QtCore.QNULL:
            try:
                int(txt)
                return True
            except ValueError:
                try:
                    long(txt)
                    return True
                except ValueError:
                    try:
                        float(txt)
                        return True
                    except ValueError:
                        return False
        else:
            return False