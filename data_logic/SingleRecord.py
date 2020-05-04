from data_logic.Utils import Utils
from db_tables.Postcode_Table import Postcode_Table


class SingleRecord:
    def __init__(self, shipment_identicode: str, shipment_createdate: str, first_event: str, last_event: str,
                 receiver_zip: str, receiver_country_code: str, sender_zip: str, sender_country_code: str,
                 contract_type: str, xlidentifier: str):
        self.ready = True
        self.shipment_identicode = shipment_identicode
        self.shipment_createdate = shipment_createdate
        self.unix_shipment_createdate = Utils.convert_to_unix_time(shipment_createdate)
        self.first_event = first_event
        self.unix_first_event = Utils.convert_to_unix_time(first_event)
        self.last_event = last_event
        self.unix_last_event = Utils.convert_to_unix_time(last_event)

        receiver_coord = Postcode_Table.getCoordinates(receiver_country_code, receiver_zip)
        self.receiver_zip = receiver_zip
        self.receiver_country_code = receiver_country_code

        if receiver_coord.get("empty"):
            self.ready = False
            print("ready ustawiam na false")
        else:
            self.receiver_city_name = receiver_coord.get('placeName')
            self.receiver_latitude = receiver_coord.get('latitude')
            self.receiver_longitude = receiver_coord.get('longitude')

        sender_coord = Postcode_Table.getCoordinates(sender_country_code, sender_zip)
        self.sender_zip = sender_zip
        self.sender_country_code = sender_country_code

        if sender_coord.get("empty"):
            self.ready = False
        else:
            self.sender_city_name = sender_coord.get('placeName')
            self.sender_latitude = sender_coord.get('latitude')
            self.sender_longitude = sender_coord.get('longitude')

        if self.ready:
            self.distance = Utils.convert_cords_to_distance(receiver_coord.get('latitude'),
                                                            receiver_coord.get('longitude'),
                                                            sender_coord.get('latitude'),
                                                            sender_coord.get('longitude'))
        self.contract_type = contract_type
        self.xlidentifier = xlidentifier

    def print(self):
        print("\nshipment_identicode: " + self.shipment_identicode +
              "\nshipment_createdate: " + self.shipment_createdate +
              "\nunix_shipment_createdate: " + self.unix_shipment_createdate +
              "\nfirst_event: " + self.first_event +
              "\nunix_first_event: " + self.unix_first_event +
              "\nlast_event: " + self.last_event +
              "\nunix_last_event: " + self.unix_last_event +
              "\nreceiver_zip: " + self.receiver_zip +
              "\nreceiver_country_code: " + self.receiver_country_code +
              "\nreceiver_latitude: " + self.receiver_latitude +
              "\nreceiver_longitude: " + self.receiver_longitude +
              "\nsender_zip: " + self.sender_zip +
              "\nsender_country_code: " + self.sender_country_code +
              "\nsender_latitude: " + self.sender_latitude +
              "\nsender_longitude: " + self.sender_longitude +
              "\ncontract_type: " + self.contract_type +
              "\nxlidentifier: " + self.xlidentifier)
