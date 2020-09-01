import json
from json import loads as json_loads
from pathlib import Path
from pyproj import Proj, transform

from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox

from .wtss_client.wtss_client import wtss
from .config import Config

class Controlls:

    def alert(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def addItemsMenuServices(self, parent, elements):
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItemsMenuServices(item, children)

    def formatForQDate(self, date_string):
        # Return a QDate format yyyy-mm-dd
        return QDate(
            int(date_string[:4]),
            int(date_string[5:-3]),
            int(date_string[8:])
        )

    def transformProjection(self, projection, latitude, longitude):
        # transform any projection to EPSG: 4326
        lat, lon = transform(
            Proj(init=projection),
            Proj(init='epsg:4326'),
            latitude, longitude
        )
        return {
            "lat": lat,
            "long": lon,
            "crs": "EPSG: 4326"
        }

    def getDescription(self, name = "Null", host = "Null", coverage = "Null"):
        return (
            "Service name: " + name + "\n" +
            "Host: " + host + "\n" +
            "Active coverage: " + coverage + "\n"
        )

class Services:

    def getPath(self):
        return (
            Path(Config.BASE_DIR)
                / 'json-schemas'
                    / 'services_storage.json'
        )

    def getServices(self):
        with self.getPath().open() as f:
            return json_loads(f.read())

    def getServiceNames(self):
        try:
            service_names = []
            for server in self.getServices().get('services'):
                service_names.append(server.get('name'))
            return service_names
        except (FileNotFoundError, FileExistsError):
            return None

    def loadServices(self):
        servers = []
        for server in self.getServices().get('services'):
            try:
                client_wtss = wtss(server.get('host'))
                coverage_tree = []
                for coverage in client_wtss.list_coverages().get('coverages', []):
                    coverage_tree.append((coverage, []))
                servers.append((server.get('name'), coverage_tree))
            except (ConnectionRefusedError, RuntimeError):
                self.deleteService(server.get('name'))
                pass
        return [('Services', servers)]

    def findServiceByName(self, service_name):
        try:
            service = None
            for server in self.getServices().get('services'):
                if str(server.get('name')) == str(service_name):
                    service = server
            return service
        except (FileNotFoundError, FileExistsError):
            return None

    def listProducts(self, service_name):
        try:
            client_wtss = wtss(self.findServiceByName(service_name).get('host'))
            return client_wtss.list_coverages().get('coverages',[])
        except (ConnectionRefusedError, RuntimeError):
            return []

    def productDescription(self, service_name, product):
        try:
            client_wtss = wtss(self.findServiceByName(service_name).get('host'))
            return client_wtss.describe_coverage(product)
        except (ConnectionRefusedError, RuntimeError):
            return {}

    def productTimeSeries(self, service_name, product, bands, lon, lat, start_date, end_date):
        try:
            client_wtss = wtss(self.findServiceByName(service_name).get('host'))
            time_series = client_wtss.time_series(product, bands, lon, lat, start_date, end_date)
            if len(time_series.doc.get("result").get("attributes")[0].get("values")):
                return time_series
            else:
                return None
        except (ConnectionRefusedError, RuntimeError):
            return {}

    def addService(self, name, host):
        try:
            client_wtss = wtss(host).list_coverages()
            server_to_save = self.findServiceByName(name)
            if server_to_save == None:
                to_save = self.getServices()
                to_save.get('services').append({
                    "name": str(name),
                    "host": str(host)
                })
                with open(str(self.getPath()), 'w') as outfile:
                    json.dump(to_save, outfile)
            return server_to_save
        except (ConnectionRefusedError, FileNotFoundError, FileExistsError):
            return None

    def deleteService(self, server_name):
        try:
            server_to_delete = self.findServiceByName(server_name)
            if server_to_delete != None:
                to_delete = self.getServices()
                to_delete.get('services').pop(
                    to_delete.get('services').index(server_to_delete)
                )
                with open(str(self.getPath()), 'w') as outfile:
                    json.dump(to_delete, outfile)
            return server_to_delete
        except (FileNotFoundError, FileExistsError):
            return None

    def editService(self, server_name, server_host):
        server_to_edit = self.findServiceByName(server_name)
        if server_to_edit != None:
            self.deleteService(server_name)
        return self.addService(
            server_name,
            server_host
        )
