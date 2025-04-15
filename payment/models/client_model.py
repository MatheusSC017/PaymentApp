class ClientModel:
    email = None
    first_name = None
    last_name = None
    phone_area_code = None
    phone_number = None
    identification_type = None
    identification_number = None
    default_address = None
    address_id = None
    address_zip_code = None
    address_street_name = None
    address_street_number = None
    address_city = None
    date_registered = None
    description = None
    default_card = None

    def __init__(self, email, first_name, last_name, phone_area_code, phone_number, identification_type,
                 identification_number, default_address, address_id, address_zip_code, address_street_name,
                 address_street_number, address_city, date_registered, description, default_card):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_area_code = phone_area_code
        self.phone_number = phone_number
        self.identification_type = identification_type
        self.identification_number = identification_number
        self.default_address = default_address
        self.address_id = address_id
        self.address_zip_code = address_zip_code
        self.address_street_name = address_street_name
        self.address_street_number = address_street_number
        self.address_city = address_city
        self.date_registered = date_registered
        self.description = description
        self.default_card = default_card

    def get_formatted_data(self, include_email=True):
        formatted_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": {
                "area_code": self.phone_area_code,
                "number": self.phone_number
            },
            "identification": {
                "type": self.identification_type,
                "number": self.identification_number
            },
            "default_address": self.default_address,
            "address": {
                "id": self.address_id,
                "zip_code": self.address_zip_code,
                "street_name": self.address_street_name,
                "street_number": self.address_street_number,
                "city": self.address_city
            },
            "date_registered": self.date_registered,
            "description": self.description,
            "default_card": self.default_card
        }
        if include_email:
            formatted_data["email"] = self.email
        return formatted_data
