import json
import csv
import matplotlib.pyplot as plt
import numpy as np

from json import loads as json_loads
from pathlib import Path

from ...wtss_plugin.config import Config

class FilesExport:
    def defaultCode(self):
        template = (
            Path(Config.BASE_DIR)
                / 'files_export'
                    / 'examples'
                        / 'times_series_export_template.py'
        )
        return open(template, 'r').read()

    def generateCode(self, file_name, attributes):
        try:
            bands_string = "("
            for band in attributes.get("bands"):
                bands_string = bands_string + "'" + str(band) + "', "
            bands_string = bands_string[:len(bands_string)-2] + ")"
            lat = "{:,.2f}".format(attributes.get("coordinates").get("lat"))
            lon = "{:,.2f}".format(attributes.get("coordinates").get("long"))
            mapping = {
                "service_host": attributes.get("host"),
                "selected_coverage": attributes.get("coverage"),
                "selected_bands": bands_string,
                "latitude" : lat,
                "longitude" : lon,
                "start_date" : attributes.get("time_interval").get("start"),
                "end_date" : attributes.get("time_interval").get("end")
            }
            code_to_save = self.defaultCode().format(**mapping)
            file = open(file_name, "w")
            file.write(code_to_save)
            file.close()
        except FileNotFoundError:
            pass

    def generateCSV(self, file_name, time_series):
        try:
            dates = [str(date_str) for date_str in time_series.timeline]
            with open(file_name, 'w', newline='') as csvfile:
                fieldnames = ['timeline','latitude','longitude']
                for band in list(time_series.attributes.keys()):
                    fieldnames.append(band)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                ind = 0
                for date in dates:
                    line = {
                        'timeline': date,
                        'latitude': time_series.doc.get('query').get('latitude'),
                        'longitude': time_series.doc.get('query').get('longitude')
                    }
                    for band in list(time_series.attributes.keys()):
                        line[band] = time_series.attributes[band][ind]
                    ind += 1
                    writer.writerow(line)
        except FileNotFoundError:
            pass

    def generateJSON(self, file_name, time_series):
        try:
            data = time_series.doc.get('result')
            data['timeline'] = [str(date_str) for date_str in time_series.timeline]
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            pass

    def generatePlotFig(self, time_series):
        try:
            plt.clf()
            plt.cla()
            plt.close()
            plt.title("Coverage " + str(time_series.doc.get('query').get('coverage')), fontsize=14)
            plt.xlabel("Date", fontsize=10)
            plt.ylabel("Value", fontsize=10)
            x = [str(date_str) for date_str in time_series.timeline]
            plt.xticks(np.arange(0, len(x), step=float(len(x) // 5)))
            plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5)
            for band in list(time_series.attributes.keys()):
                y = time_series.attributes[band]
                plt.plot(x, y, label = band)
            plt.legend()
            plt.show()
        except:
            pass
