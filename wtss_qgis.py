# -*- coding: utf-8 -*-
"""
/***************************************************************************
 wtss_qgis
                                 A QGIS plugin
 Python Client Library for Web Time Series Service
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-04
        git sha              : $Format:%H$
        copyright            : (C) 2020 by INPE
        email                : brazildatacube@dpi.inpe.br
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject
from qgis.gui import QgsMapToolEmitPoint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .wtss_qgis_dialog import wtss_qgisDialog

# Import the controlls for the plugin
from .wtss_plugin.wtss_qgis_controller import Services, Controlls

# Import files exporting controlls
from .wtss_plugin.files_export import FilesExport

from .wtss_plugin.config import Config

import os.path
from pathlib import Path
from datetime import datetime, date

class wtss_qgis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'wtss_qgis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&WTSS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('wtss_qgis', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = str(Path(Config.BASE_DIR) / 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'WTSS'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&WTSS'),
                action)
            self.iface.removeToolBarIcon(action)

    def initControlls(self):
        # Init Controlls
        self.basic_controlls = Controlls()
        self.server_controlls = Services(user = "application")
        self.files_controlls = FilesExport()

    def initButtons(self):
        self.dlg.save_service.clicked.connect(self.saveService)
        self.dlg.delete_service.clicked.connect(self.deleteService)
        self.dlg.edit_service.clicked.connect(self.editService)
        self.dlg.export_as_python.clicked.connect(self.exportPython)
        self.dlg.export_as_csv.clicked.connect(self.exportCSV)
        self.dlg.export_as_json.clicked.connect(self.exportJSON)

    def initHistory(self):
        self.dlg.history_list.clear()
        self.selected_location = None
        try:
            self.dlg.history_list.addItems(list(self.locations.keys()))
        except AttributeError:
            self.locations = {}
        self.dlg.history_list.itemActivated.connect(self.getFromHistory)
        self.getLayers()
        self.addCanvasControlPoint()

    def initServices(self):
        self.dlg.service_selection.addItems(self.server_controlls.getServiceNames())
        self.dlg.service_selection.activated.connect(self.selectCoverage)
        self.data = self.server_controlls.loadServices()
        self.model = QStandardItemModel()
        self.basic_controlls.addItemsMenuServices(self.model, self.data)
        self.dlg.data.setModel(self.model)

    def saveService(self):
        name_to_save = str(self.dlg.service_name.text())
        host_to_save = str(self.dlg.service_host.text())
        try:
            self.server_controlls.editService(name_to_save, host_to_save)
            self.selected_service = host_to_save
            self.dlg.service_name.clear()
            self.dlg.service_host.clear()
            self.updateServicesList()
        except (ValueError, AttributeError, ConnectionRefusedError) as error:
            self.basic_controlls.alert("(ValueError, AttributeError)", str(error))

    def deleteService(self):
        host_to_delete = self.dlg.service_selection.currentText()
        try:
            self.server_controlls.deleteService(host_to_delete)
            self.updateServicesList()
        except (ValueError, AttributeError) as error:
            self.basic_controlls.alert("(ValueError, AttributeError)", str(error))

    def editService(self):
        self.dlg.service_name.setText(self.dlg.service_selection.currentText())
        self.dlg.service_host.setText(
            self.server_controlls.findServiceByName(self.dlg.service_selection.currentText()).get("host")
        )

    def updateServicesList(self):
        self.data = self.server_controlls.loadServices()
        self.model = QStandardItemModel()
        self.basic_controlls.addItemsMenuServices(self.model, self.data)
        self.dlg.data.setModel(self.model)
        self.dlg.service_selection.clear()
        self.dlg.service_selection.addItems(self.server_controlls.getServiceNames())
        self.dlg.service_selection.activated.connect(self.selectCoverage)

    def selectCoverage(self):
        self.dlg.service_metadata.setText(
            self.basic_controlls.getDescription(
                name=str(self.dlg.service_selection.currentText()),
                host=str(self.server_controlls.findServiceByName(
                    self.dlg.service_selection.currentText()
                ).get("host")),
            )
        )
        self.dlg.coverage_selection.clear()
        self.dlg.coverage_selection.addItems(
            self.server_controlls.listProducts(
                str(self.dlg.service_selection.currentText())
            )
        )
        self.dlg.coverage_selection.activated.connect(self.selectAtributtes)

    def selectAtributtes(self):
        self.dlg.service_metadata.setText(
            self.basic_controlls.getDescription(
                name=self.dlg.service_selection.currentText(),
                host=str(self.server_controlls.findServiceByName(
                    self.dlg.service_selection.currentText()
                ).get("host")),
                coverage=str(self.dlg.coverage_selection.currentText())
            )
        )
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        description = self.server_controlls.productDescription(
            str(self.dlg.service_selection.currentText()),
            str(self.dlg.coverage_selection.currentText())
        )
        bands = description.get("attributes",{})
        timeline = description.get("timeline",[])
        self.bands_checks = {}
        for band in list(bands.keys()):
            self.bands_checks[bands.get(band).get("name")] = QCheckBox(str(bands.get(band).get("name")))
            self.vbox.addWidget(self.bands_checks.get(bands.get(band).get("name")))
        self.widget.setLayout(self.vbox)
        self.dlg.bands_scroll.setWidgetResizable(True)
        self.dlg.bands_scroll.setWidget(self.widget)
        # Update dates for start and end to coverage selection
        self.dlg.start_date.setDate(self.basic_controlls.formatForQDate(timeline[0]))
        self.dlg.end_date.setDate(self.basic_controlls.formatForQDate(timeline[len(timeline) - 1]))

    def loadAtributtes(self):
        selected_attributes = []
        for band in list(self.bands_checks.keys()):
            if self.bands_checks.get(band).isChecked():
                selected_attributes.append(band)
        return selected_attributes

    def loadTimeSeries(self):
        return self.server_controlls.productTimeSeries(
            str(self.dlg.service_selection.currentText()),
            str(self.dlg.coverage_selection.currentText()),
            tuple(self.loadAtributtes()),
            self.transformSelectedLocation().get('long', 0),
            self.transformSelectedLocation().get('lat', 0),
            str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
            str(self.dlg.end_date.date().toString('yyyy-MM-dd'))
        )

    def exportPython(self):
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as python code',
                directory=('{coverage}.{end}.py').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.py'
            )
            attributes = {
                "host": str(self.server_controlls.findServiceByName(
                    self.dlg.service_selection.currentText()
                ).get("host")),
                "coverage": str(self.dlg.coverage_selection.currentText()),
                "bands": tuple(self.loadAtributtes()),
                "coordinates": {
                    "crs": self.selected_location.get('crs'),
                    "lat": self.selected_location.get('lat'),
                    "long": self.selected_location.get('long')
                },
                "time_interval": {
                    "start": str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
                    "end": str(self.dlg.end_date.date().toString('yyyy-MM-dd'))
                }
            }
            self.files_controlls.generateCode(name[0], attributes)
        except AttributeError as error:
            self.basic_controlls.alert("AttributeError", str(error))

    def exportCSV(self):
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as CSV',
                directory=('{coverage}.{end}.csv').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.csv'
            )
            time_series = self.loadTimeSeries()
            self.files_controlls.generateCSV(name[0], time_series)
        except AttributeError as error:
            self.basic_controlls.alert("AttributeError", str(error))

    def exportJSON(self):
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as JSON',
                directory=('{coverage}.{end}.json').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.json'
            )
            time_series = self.loadTimeSeries()
            self.files_controlls.generateJSON(name[0], time_series)
        except AttributeError as error:
            self.basic_controlls.alert("AttributeError", str(error))

    def plotTimeSeries(self):
        time_series = self.loadTimeSeries()
        if time_series != None:
            self.files_controlls.generatePlotFig(time_series)
        else:
            self.basic_controlls.alert("AttributeError", "The times series service returns empty, no data to show!")

    def getLayers(self):
        self.layers = QgsProject.instance().layerTreeRoot().children()
        self.layer_names = [layer.name() for layer in self.layers] # Get all layer names
        self.layer = self.iface.activeLayer() # QVectorLayer QRasterFile

    def getFromHistory(self, item):
        self.selected_location = self.locations.get(item.text(), {})

    def display_point(self, pointTool):
        try:
            self.selected_location = {
                'layer_name' : str(self.layer.name()),
                'lat' : float(pointTool.x()),
                'long' : float(pointTool.y()),
                'crs' : str(self.layer.crs().authid())
            }
            history_key = str(
                (
                    "({lat:,.2f},{long:,.2f}) {crs}"
                ).format(
                    crs = self.selected_location.get('crs'),
                    lat = self.selected_location.get('lat'),
                    long = self.selected_location.get('long')
                )
            )
            self.locations[history_key] = self.selected_location
            self.dlg.history_list.clear()
            self.dlg.history_list.addItems(list(self.locations.keys()))
            self.dlg.history_list.itemActivated.connect(self.getFromHistory)
            self.plotTimeSeries()
        except AttributeError:
            pass

    def addCanvasControlPoint(self):
        self.canvas = self.iface.mapCanvas()
        self.point_tool = QgsMapToolEmitPoint(self.canvas)
        self.point_tool.canvasClicked.connect(self.display_point)
        self.canvas.setMapTool(self.point_tool)
        self.display_point(self.point_tool)

    def transformSelectedLocation(self):
        transformed = self.selected_location
        if self.selected_location.get("crs"):
            transformed = self.basic_controlls.transformProjection(
                self.selected_location.get("crs"),
                self.selected_location.get("lat"),
                self.selected_location.get("long")
            )
        return transformed

    def run(self):
        """Run method that performs all the real work"""
        # Init Application
        self.dlg = wtss_qgisDialog()
        # Init Controlls
        self.initControlls()
        # Description
        self.dlg.service_metadata.setText(self.basic_controlls.getDescription())
        # Services
        self.initServices()
        # History
        self.initHistory()
        # Add functions to buttons
        self.initButtons()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
