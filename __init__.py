from modules import cbpi
from modules.core.hardware import ActorBase
from modules.core.props import Property
import httplib2
import urllib
from flask import request
from modules import cbpi
from modules.core.controller import KettleController, FermenterController
from modules.core.props import Property
import requests

@cbpi.fermentation_controller
class SendToWebserver(FermenterController):
    dummy_device_number = Property.Select("Easy ESP dummy Device Task", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ], description="On the left side you can see a number of the device, this one we need here to set the Mode with HTTP Request")
    dummy_target_id = Property.Select("Easy ESP dummy Device Target - ID", [1, 2, 3, 4], description="On the right side we need the row number of target ")
    dummy_mode_id = Property.Select("Easy ESP dummy Device Mode - ID", [1, 2, 3, 4], description="On the right side we need the row number of mode ")

    url_fridge = Property.Text("FrideAPI-Adress", configurable=True, default_value="http://192.168.180.61", description="Adress of the EasyESP device.")

    def send_webserver(self, automatic):
        attempts = 0
        while attempts < 5 :
            url_target = self.url_fridge + '/control?cmd=TaskValueSet,' + str(self.dummy_device_number) + ',' + str(self.dummy_target_id) + ',' + str(self.get_target_temp())
            url_mode = self.url_fridge + '/control?cmd=TaskValueSet,' + str(self.dummy_device_number) + ',' + str(self.dummy_mode_id) + ',' + str(automatic)

            
            try:
                target = requests.get(url_target)
                self.sleep(4)
                mode = requests.get(url_mode)

                if (str(target.text) == 'OK' and str(mode.text) == 'OK'):
                    cbpi.notify("Fridge", "Suggessfully startet Fridge", timeout=None, type="success")
                    return True
                
            except:
                attempts += 1
                cbpi.notify("Fridge", "Can't send request", timeout=5000, type="danger")

	
    def run (self):
        send = self.send_webserver(1)
        while self.is_running():
            self.sleep(5) 

    def stop(self):
        self.send_webserver(0)
