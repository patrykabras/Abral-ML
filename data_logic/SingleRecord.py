from db_tables import Postcode_Table
from data_logic.Utils import Utils


class SingleRecord:
    def __init__(self, postcode_table: Postcode_Table, shipment_identicode: str, shipment_createdate: str, first_event: str,
                 last_event: str, receiver_zip: str, receiver_country_code: str, sender_zip: str,
                 sender_country_code: str, contract_type: str, xlidentifier: str):
        self.receiver_zip_found = True
        self.sender_zip_found = True
        self.shipment_identicode = shipment_identicode
        self.shipment_createdate = shipment_createdate
        self.unix_shipment_createdate = Utils.convert_to_unix_time(shipment_createdate)
        self.first_event = first_event
        self.unix_first_event = Utils.convert_to_unix_time(first_event)
        self.last_event = last_event
        self.unix_last_event = Utils.convert_to_unix_time(last_event)
        # Calculate difference between two extreme unix time values
        if self.unix_shipment_createdate < self.unix_first_event:
            self.unix_difference = \
                Utils.get_difference_between_unix_time(self.unix_shipment_createdate, self.unix_last_event)
        else:
            self.unix_difference = \
                Utils.get_difference_between_unix_time(self.unix_first_event, self.unix_last_event)

        # Translate receiver zip code into coordinates
        receiver_coord = postcode_table.get_coordinates(receiver_country_code, receiver_zip)
        self.receiver_zip = receiver_zip
        self.receiver_country_code = receiver_country_code

        if receiver_coord.get("empty"):
            # No zip code found in dictionary table
            self.receiver_zip_found = False
        else:
            self.receiver_city_name = receiver_coord.get('placeName')
            self.receiver_latitude = receiver_coord.get('latitude')
            self.receiver_longitude = receiver_coord.get('longitude')

        # Translate sender zip code into coordinates
        sender_coord = postcode_table.get_coordinates(sender_country_code, sender_zip)
        self.sender_zip = sender_zip
        self.sender_country_code = sender_country_code

        if sender_coord.get("empty"):
            # No zip code found in dictionary table
            self.sender_zip_found = False
        else:
            self.sender_city_name = sender_coord.get('placeName')
            self.sender_latitude = sender_coord.get('latitude')
            self.sender_longitude = sender_coord.get('longitude')

        # if both zip codes found in dictionary, calculate distance between them
        if self.receiver_zip_found and self.sender_zip_found:
            self.distance = Utils.convert_cords_to_distance(receiver_coord.get('latitude'),
                                                            receiver_coord.get('longitude'),
                                                            sender_coord.get('latitude'),
                                                            sender_coord.get('longitude'))
        self.contract_type = contract_type
        self.xlidentifier = xlidentifier

    def print(self) -> None:
        print("\nshipment_identicode: " + self.shipment_identicode +
              "\nshipment_createdate: " + self.shipment_createdate +
              "\nunix_shipment_createdate: " + str(self.unix_shipment_createdate) +
              "\nfirst_event: " + self.first_event +
              "\nunix_first_event: " + str(self.unix_first_event) +
              "\nlast_event: " + self.last_event +
              "\nunix_last_event: " + str(self.unix_last_event) +
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
