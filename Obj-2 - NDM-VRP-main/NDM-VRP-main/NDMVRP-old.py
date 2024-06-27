# # -*- coding: utf-8 -*-
# """
# /***************************************************************************
#  NDMVRP
#                                  A QGIS plugin
#  this plugin creates VRP strategies for NDM
#  Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
#                               -------------------
#         begin                : 2023-06-14
#         git sha              : $Format:%H$
#         copyright            : (C) 2023 by AEM
#         email                : sid.mpadhyay@gmail.com
#  ***************************************************************************/

# /***************************************************************************
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  ***************************************************************************/
# """
# from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
# from qgis.PyQt.QtGui import QIcon
# from qgis.PyQt.QtWidgets import QAction
# from qgis.core import QgsField, QgsFields, QgsVectorLayer, QgsWkbTypes, QgsProject
# from PyQt5.QtCore import QVariant
# from qgis.core import QgsField, QgsFields, QgsVectorLayer, QgsWkbTypes, QgsProject, QgsCoordinateReferenceSystem
# from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject
# from qgis.PyQt.QtCore import Qt
# from qgis.utils import iface
# from qgis.utils import iface
# from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QMessageBox
# from PyQt5.QtWidgets import QMessageBox
# # Initialize Qt resources from file resources.py
# from .resources import *
# # Import the code for the dialog
# from .NDMVRP_dialog import NDMVRPDialog
# import os.path
# import pandas as pd


# class NDMVRP:
#     """QGIS Plugin Implementation."""

#     def __init__(self, iface):
#         """Constructor.

#         :param iface: An interface instance that will be passed to this class
#             which provides the hook by which you can manipulate the QGIS
#             application at run time.
#         :type iface: QgsInterface
#         """
#         # Save reference to the QGIS interface
#         self.iface = iface
#         # initialize plugin directory
#         self.plugin_dir = os.path.dirname(__file__)
#         # initialize locale
#         locale = QSettings().value('locale/userLocale')[0:2]
#         locale_path = os.path.join(
#             self.plugin_dir,
#             'i18n',
#             'NDMVRP_{}.qm'.format(locale))

#         if os.path.exists(locale_path):
#             self.translator = QTranslator()
#             self.translator.load(locale_path)
#             QCoreApplication.installTranslator(self.translator)

#         # Declare instance attributes
#         self.actions = []
#         self.menu = self.tr(u'&NDMVRP')

#         # Check if plugin was started the first time in current QGIS session
#         # Must be set in initGui() to survive plugin reloads
#         self.first_start = None
#         self.depot_layer = None
#         self.df = None

#     # noinspection PyMethodMayBeStatic
#     def tr(self, message):
#         """Get the translation for a string using Qt translation API.

#         We implement this ourselves since we do not inherit QObject.

#         :param message: String for translation.
#         :type message: str, QString

#         :returns: Translated version of message.
#         :rtype: QString
#         """
#         # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
#         return QCoreApplication.translate('NDMVRP', message)


#     def add_action(
#         self,
#         icon_path,
#         text,
#         callback,
#         enabled_flag=True,
#         add_to_menu=True,
#         add_to_toolbar=True,
#         status_tip=None,
#         whats_this=None,
#         parent=None):
#         """Add a toolbar icon to the toolbar.

#         :param icon_path: Path to the icon for this action. Can be a resource
#             path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
#         :type icon_path: str

#         :param text: Text that should be shown in menu items for this action.
#         :type text: str

#         :param callback: Function to be called when the action is triggered.
#         :type callback: function

#         :param enabled_flag: A flag indicating if the action should be enabled
#             by default. Defaults to True.
#         :type enabled_flag: bool

#         :param add_to_menu: Flag indicating whether the action should also
#             be added to the menu. Defaults to True.
#         :type add_to_menu: bool

#         :param add_to_toolbar: Flag indicating whether the action should also
#             be added to the toolbar. Defaults to True.
#         :type add_to_toolbar: bool

#         :param status_tip: Optional text to show in a popup when mouse pointer
#             hovers over the action.
#         :type status_tip: str

#         :param parent: Parent widget for the new action. Defaults None.
#         :type parent: QWidget

#         :param whats_this: Optional text to show in the status bar when the
#             mouse pointer hovers over the action.

#         :returns: The action that was created. Note that the action is also
#             added to self.actions list.
#         :rtype: QAction
#         """

#         icon = QIcon(icon_path)
#         action = QAction(icon, text, parent)
#         action.triggered.connect(callback)
#         action.setEnabled(enabled_flag)

#         if status_tip is not None:
#             action.setStatusTip(status_tip)

#         if whats_this is not None:
#             action.setWhatsThis(whats_this)

#         if add_to_toolbar:
#             # Adds plugin icon to Plugins toolbar
#             self.iface.addToolBarIcon(action)

#         if add_to_menu:
#             self.iface.addPluginToMenu(
#                 self.menu,
#                 action)

#         self.actions.append(action)

#         return action

#     def initGui(self):
#         """Create the menu entries and toolbar icons inside the QGIS GUI."""

#         icon_path = ':/plugins/NDMVRP/icon.png'
#         self.add_action(
#             icon_path,
#             text=self.tr(u'vrp for ndm'),
#             callback=self.run,
#             parent=self.iface.mainWindow())

#         # will be set False in run()
#         self.first_start = True


#     def unload(self):
#         """Removes the plugin menu item and icon from QGIS GUI."""
#         for action in self.actions:
#             self.iface.removePluginMenu(
#                 self.tr(u'&NDMVRP'),
#                 action)
#             self.iface.removeToolBarIcon(action)

#     def fill_table(self):
#         self.dlg.table.clear()
#         depot_id_li = []
#         depot_lat_li = []
#         depot_lon_li = []
#         depot_loading_li = []
#         depot_unloading_li = []
#         for feature in self.depot_layer.getFeatures():
#             depot_id_li.append(feature['depot_id'])
#             depot_lat_li.append(feature['depot_lat'])
#             depot_lon_li.append(feature['depot_lon'])
#             depot_loading_li.append(feature['loading'])
#             depot_unloading_li.append(feature['unloading'])

#         self.dlg.table.setRowCount(len(depot_id_li))
#         for row in range(len(depot_id_li)):
#             depot_id = QTableWidgetItem(str(depot_id_li[row]))
#             depot_lat = QTableWidgetItem(str(round(depot_lat_li[row], 6)))
#             depot_lon = QTableWidgetItem(str(round(depot_lon_li[row], 6)))
#             depot_loading = QTableWidgetItem(str(depot_loading_li[row]))
#             depot_unloading = QTableWidgetItem(str(depot_unloading_li[row]))

#             self.dlg.table.setItem(row, 0, depot_id)
#             self.dlg.table.setItem(row, 1, depot_lat)
#             self.dlg.table.setItem(row, 2, depot_lon)
#             self.dlg.table.setItem(row, 3, depot_loading)
#             self.dlg.table.setItem(row, 4, depot_unloading)

#         self.df = pd.DataFrame(list(zip(depot_id_li, depot_lat_li, depot_lon_li, depot_loading_li, depot_unloading_li)),
#                           columns=['Depot_ID', 'Depot_latitude', 'Depot_longitude', 'Depot_loading', 'Depot_unloading'])

#     def on_add_new_depot_feature(self, featureId):
#         layer = self.depot_layer
#         feature = layer.getFeature(featureId)
#         depot_latitude = feature.geometry().asPoint().y()
#         depot_longitude = feature.geometry().asPoint().x()
#         if layer.featureCount() == 1:
#             depot_id = 1
#         else:
#             depot_id = int(layer.maximumValue(layer.fields().indexFromName('depot_id'))) + 1

#         # FOR UPDATING THE ATTRIBUTE TABLE
#         self.stopFile_field_dict = {}
#         fields = layer.dataProvider().fields()
#         for i in range(fields.count()):
#             field = fields.field(i)
#             self.stopFile_field_dict[field.name()] = i
#         feature.setAttribute(self.stopFile_field_dict['depot_id'], depot_id)
#         feature.setAttribute(self.stopFile_field_dict['depot_lat'], depot_latitude)
#         feature.setAttribute(self.stopFile_field_dict['depot_lon'], depot_longitude)
#         feature.setAttribute(self.stopFile_field_dict['loading'], feature['loading'])
#         feature.setAttribute(self.stopFile_field_dict['unloading'], feature['unloading'])
#         layer.updateFeature(feature)
#         layer.updateExtents()
#         self.fill_table()

#     def save_depot_data(self):
#         if self.depot_layer.isEditable():
#             self.depot_layer.featureAdded.disconnect(self.on_add_new_depot_feature)
#             self.depot_layer.commitChanges()
#             self.dlg.table.clear()

#     def select_depot(self):
#         if self.depot_layer == None:
#             fields = QgsFields()
#             fields.append(QgsField("depot_id", QVariant.String))
#             fields.append(QgsField("depot_lat", QVariant.Double))
#             fields.append(QgsField("depot_lon", QVariant.Double))
#             fields.append(QgsField("loading", QVariant.Int))
#             fields.append(QgsField("unloading", QVariant.Int))

#             crs = QgsCoordinateReferenceSystem('EPSG:4326')

#             layer_name = "Depot_Layer"
#             layer = QgsVectorLayer(
#                 f"Point?crs={crs.authid()}&field=depot_id:string&field=depot_lat:double&field=depot_lon:double&field=loading:integer&field=unloading:integer",
#                 layer_name,
#                 "memory"
#             )

#             layer_provider = layer.dataProvider()
#             layer_provider.addAttributes(fields)
#             layer.updateFields()

#             QgsProject.instance().addMapLayer(layer)
#             self.depot_layer = layer

#         if not self.depot_layer.isEditable():
#             self.depot_layer.startEditing()
#             iface.setActiveLayer(self.depot_layer)
#             self.depot_layer.featureAdded.connect(self.on_add_new_depot_feature)

#     def extract_csv(self):
#         vehicle_capacity = [self.dlg.vehicle_capacity_le.text()]
#         df = pd.DataFrame(list(zip(vehicle_capacity)),
#                                columns=['vehicle capacity'])
#         df.to_csv("C:\\Users\\Rahul\\Downloads\\NDMVRP_Data\\Vehicle.csv", index=False)
#         self.df.to_csv("C:\\Users\\Rahul\\Downloads\\NDMVRP_Data\\Depot.csv", index=False)
#         QMessageBox.information(None, "Success", "Files has been extracted to output path.")

#     def run(self):
#         """Run method that performs all the real work"""

#         # Create the dialog with elements (after translation) and keep reference
#         # Only create GUI ONCE in callback, so that it will only load when the plugin is started
#         if self.first_start == True:
#             self.first_start = False
#             self.dlg = NDMVRPDialog()
#             self.dlg.select_depot_pb.clicked.connect(self.select_depot)
#             self.dlg.save_depot_data.clicked.connect(self.save_depot_data)
#             self.dlg.extract_csv_pb.clicked.connect(self.extract_csv)


#         # show the dialog
#         self.dlg.show()
#         # Run the dialog event loop
#         result = self.dlg.exec_()
#         # See if OK was pressed
#         if result:
#             # Do something useful here - delete the line containing pass and
#             # substitute with your code.
#             pass