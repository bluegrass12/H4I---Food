from enum import Enum


# class ReverseSearchable:
#     _reverse_lookup = None

#     @classmethod
#     def get_name(cls, value):
#         if cls._reverse_lookup is None:
#             cls._reverse_lookup = {v.value: v for v in cls}
#         return cls._reverse_lookup[value]
    
class CTEType(Enum):
    """ This is an enum class to represent the different types of CTEs that can be created.
    """
    HARVEST = "Harvest"
    RECEIVING = "Receiving"
    TRANSFORMATION = "Transformation"


class KDE(Enum):
    """ This is an enum class to represent the different types of Key Data Elements that can be created.
    """
    SUBSEQUENT_RECIPIENT_NAME = "Subsequent Recipient Name"
    SUBSEQUENT_RECIPIENT_ADDRESS = "Subsequent Recipient Address"
    HARVEST_LOCATION_COMPANY_NAME = "Harvest Location Company Name"
    HARVEST_LOCATION_ADDRESS = "Harvest Location Address"
    QUANTITY_HARVESTED = "Quantity Harvested"
    UNIT_OF_MEASURE = "Unit of Measure"
    REFERENCE_DOCUMENT_TYPE = "Reference Document Type"
    REFERENCE_DOCUMENT_NUMBER = "Reference Document Number"
    HARVESTER_BUSINESS_NAME = "Harvester Business Name"
    HARVESTER_PHONE_NUMBER = "Harvester Phone Number"
    RAC_COMMODITY_AND_VARIETY = "RAC Commodity and Variety"
    CONTAINER_NAME_OR_EQUIVALENT = "Container Name or Equivalent"
    HARVEST_DATE = "Harvest Date"
    HARVEST_START_TIME = "Harvest Start Time"
    HARVEST_END_TIME = "Harvest End Time"
    HARVEST_DURATION = "Harvest Duration"
    HARVEST_LOCATION_GPS_LATITUDE = "Harvest Location GPS Latitude"
    HARVEST_LOCATION_GPS_LONGITUDE = "Harvest Location GPS Longitude"
