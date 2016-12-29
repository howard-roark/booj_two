# Required parent tags
CONST_LISTING = 'Listing'
CONST_LISTING_DETAILS = 'ListingDetails'
CONST_LOCATION = 'Location'
CONST_BASIC_DETAILS = 'BasicDetails'
CONST_RICH_DETAILS = 'RichDetails'
# Indices for table headers
CONST_DATE_INDEX = 0
CONST_ID_INDEX = 1
CONST_NAME_INDEX = 2
CONST_PRICE_INDEX = 3
CONST_BEDR_INDEX = 4
CONST_BATHR_INDEX = 5
CONST_ADDR_INDEX = 6
CONST_ROOMS_INDEX = 7
CONST_APPS_INDEX = 8
CONST_DESC_INDEX = 9
# Required fields to parse; tuples to hold index, tag name
#  and path to the tag
CONST_DATE_LISTED = (
    CONST_DATE_INDEX, 'DateListed')
CONST_MLS_ID = (CONST_ID_INDEX, 'MlsId')
CONST_MLS_NAME = (CONST_NAME_INDEX, 'MlsName')
CONST_PRICE = (CONST_PRICE_INDEX, 'Price')
CONST_BEDROOMS = (CONST_BEDR_INDEX, 'Bedrooms')
CONST_BATHROOMS = (CONST_BATHR_INDEX, 'Bathrooms')
CONST_ADDRESS = (CONST_ADDR_INDEX, 'StreetAddress')
CONST_ROOMS = (CONST_ROOMS_INDEX, 'Rooms')
CONST_APPLIANCES = (CONST_APPS_INDEX, 'Appliances')
CONST_DESC = (CONST_DESC_INDEX, 'Description')

CONST_REQ_FIELDS = (
    CONST_DATE_LISTED,
    CONST_MLS_ID,
    CONST_MLS_NAME,
    CONST_PRICE,
    CONST_BEDROOMS,
    CONST_BATHROOMS,
    CONST_ADDRESS,
    CONST_ROOMS,
    CONST_APPLIANCES,
    CONST_DESC)

CONST_REQS_SUBNODES = (CONST_APPLIANCES, CONST_ROOMS)
# Dict for holding listing requirements, key is Element / Tag and
# value is the condition that needs to be met for the listing to be
# written to the CSV.
CONST_LISTING_REQUIREMENTS = {CONST_DATE_LISTED: '2016-',
                              CONST_DESC: ' and '}

CONST_REM_DUPS = (('Office', 'StreetAddress'),
                  ('Neighborhood', 'Description'))
