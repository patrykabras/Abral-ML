from data_logic.Utils import Utils


class SingleRecord:
    def __init__(self, shipment_identicode: str, shipment_createdate: str, first_event: str, last_event: str,
                 receiver_zip: str, receiver_country_code: str, sender_zip: str, sender_country_code: str,
                 contract_type: str, xlidentifier: str):
        self.shipment_identicode = shipment_identicode
        self.shipment_createdate = shipment_createdate
        self.unix_shipment_createdate = Utils.convert_to_unix_time(shipment_createdate)
        self.first_event = first_event
        self.unix_first_event = Utils.convert_to_unix_time(first_event)
        self.last_event = last_event
        self.unix_last_event = Utils.convert_to_unix_time(last_event)

        self.receiver_zip = receiver_zip
        self.receiver_country_code = receiver_country_code
        receiver_latitude, receiver_longitude = Utils.get_cords_from_zip_code(receiver_zip)
        self.receiver_latitude = receiver_latitude
        self.receiver_longitude = receiver_longitude

        self.sender_zip = sender_zip
        self.sender_country_code = sender_country_code
        sender_latitude, sender_longitude = Utils.get_cords_from_zip_code(sender_zip)
        self.sender_latitude = sender_latitude
        self.sender_longitude = sender_longitude

        self.distance = Utils.convert_cords_to_distance(receiver_latitude, receiver_longitude,
                                                        sender_latitude, sender_longitude)

        self.contract_type = contract_type
        self.xlidentifier = xlidentifier

    def __print(self):
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
