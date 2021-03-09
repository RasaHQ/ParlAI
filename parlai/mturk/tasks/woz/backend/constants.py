DEFAULT_RASA_NLU_SERVER_ADDRESS = "http://localhost:5005/model/parse"
RASA_NLU_SERVER_ADDRESS_TEMPLATE = "http://localhost:{port:s}/model/parse"
RASA_NLU_SERVER_ADDRESS_KEY = 'rasa_nlu_server_address'
INTENT_TO_REPLY_KEY = 'intent2reply'
INTENT_TO_REPLY_FILE_NAME = 'intent2reply.json'
INSTRUCTION_LIST_FILE_NAME = 'instructions.txt'
SCENARIO_ADDITIONAL_RESOURCES_KEY = 'additional_resources'
START_NLU_SERVER_SCRIPT_PATH_KEY = 'start_nlu_server_script_path'
START_NLU_SERVER_SCRIPT_FILE_NAME = 'start_nlu_server.sh'
RASA_NLU_SERVER_PROCESS_KEY = 'nlu_server_process'
MIN_FUZZYWUZZY_RATIO = 80

# Common Intent Names
INTENT_HELLO = 'hello'
INTENT_ASK_NAME = 'ask_name'
INTENT_OUT_OF_SCOPE = 'out_of_scope'
INTENT_ANYTHING_ELSE = 'anything_else'

# Intent Names for book_ride, ride_status, ride_change
INTENT_RIDE_ASK_DESTINATION = 'ride_ask_destination'
INTENT_RIDE_ASK_DEPARTURE = 'ride_ask_departure'
INTENT_RIDE_ASK_CONFIRM_BOOKING = 'ride_ask_confirm_booking'
INTENT_RIDE_BYE = 'ride_bye'
INTENT_RIDE_CONFIRM_BOOKING = 'ride_confirm_booking'
INTENT_RIDE_PROVIDE_DRIVER_DETAILS = 'ride_provide_driver_details'
INTENT_RIDE_PROVIDE_RIDE_DETAILS = 'ride_provide_ride_details'
INTENT_RIDE_INFORM_SEARCH_CRITERIA = 'ride_inform_search_criteria'
INTENT_RIDE_ASK_CHANGE = 'ride_ask_change'
INTENT_RIDE_ASK_BOOKING_NUMBER = 'ride_ask_booking_number'
INTENT_RIDE_INFORM_CHANGES_SUCCESSFUL = 'ride_inform_changes_successful'
INTENT_RIDE_INFORM_CHANGES_FAILED = 'ride_inform_changes_failed'
INTENT_RIDE_PROVIDE_BOOKING_STATUS = 'ride_provide_booking_status'
INTENT_RIDE_PROVIDE_BOOKING_STATUS_UPDATE = 'ride_provide_booking_status_update'
INTENT_RIDE_INFORM_NOTHING_FOUND = 'ride_inform_nothing_found'

# Intent names for hotel_reserve, hotel_search, hotel_service_request
INTENT_HOTEL_INFORM_SEARCH_CRITERIA = 'hotel_inform_search_criteria'
INTENT_HOTEL_ASK_NAME = 'hotel_ask_name'
INTENT_HOTEL_INFORM_NAME = 'hotel_inform_name'
INTENT_HOTEL_ASK_LOCATION = 'hotel_ask_location'
INTENT_HOTEL_INFORM_LOCATION = 'hotel_inform_location'
INTENT_HOTEL_ASK_PRICE = 'hotel_ask_price'
INTENT_HOTEL_INFORM_PRICE = 'hotel_inform_price'
INTENT_HOTEL_ASK_RATING = 'hotel_ask_rating'
INTENT_HOTEL_INFORM_RATING = 'hotel_inform_rating'
INTENT_HOTEL_PROVIDE_SEARCH_RESULT = 'hotel_provide_search_result'
INTENT_HOTEL_ASK_SEARCH_MORE = 'hotel_ask_search_more'
INTENT_HOTEL_BYE = 'hotel_bye'
INTENT_HOTEL_ASK_HOTEL = 'hotel_ask_hotel'
INTENT_HOTEL_ASK_DATE_FROM = 'hotel_ask_date_from'
INTENT_HOTEL_ASK_DATE_TO = 'hotel_ask_date_to'
INTENT_HOTEL_ASK_CUSTOMER_REQUEST = 'hotel_ask_customer_request'
INTENT_HOTEL_UNAVAILABLE = 'hotel_unavailable'
INTENT_HOTEL_ASK_CONFIRM_BOOKING = 'hotel_ask_confirm_booking'
INTENT_HOTEL_RESERVATION_SUCCEEDED = 'hotel_reservation_succeeded'
INTENT_HOTEL_RESERVATION_FAILED = 'hotel_reservation_failed'
INTENT_HOTEL_ASK_ROOM_NUMBER = 'hotel_ask_room_number'
INTENT_HOTEL_ASK_SERVICE_REQUEST = 'hotel_ask_service_request'
INTENT_HOTEL_ASK_TIME = 'hotel_ask_time'
INTENT_HOTEL_INFORM_SERVICE_REQUEST_SUCCESSFUL = 'hotel_inform_service_request_successful'
INTENT_HOTEL_INFORM_SERVICE_REQUEST_FAILED = 'hotel_inform_service_request_failed'
INTENT_HOTEL_INFORM_NOTHING_FOUND = 'hotel_inform_nothing_found'

# Intent names for plane_search, plane_reserve
INTENT_PLANE_ASK_FLIGHT_ID = 'plane_ask_flight_id'
INTENT_PLANE_FLIGHT_AVAILABLE = 'plane_flight_available'
INTENT_PLANE_FLIGHT_UNAVAILABLE = 'plane_flight_unavailable'
INTENT_PLANE_RESERVATION_SUCCEEDED = 'plane_reservation_succeeded'
INTENT_PLANE_RESERVATION_FAILED = 'plane_reservation_failed'
INTENT_PLANE_BYE = 'plane_bye'
INTENT_PLANE_ASK_DEPARTURE_CITY = 'plane_ask_departure_city'
INTENT_PLANE_ASK_ARRIVAL_CITY = 'plane_ask_arrival_city'
INTENT_PLANE_ASK_DATE = 'plane_ask_date'
INTENT_PLANE_REQUEST_OPTIONAL = 'plane_request_optional'
INTENT_PLANE_INFORM_FLIGHT_DETAILS = 'plane_inform_flight_details'
INTENT_PLANE_ASK_MORE_QUESTIONS = 'plane_ask_more_questions'
INTENT_PLANE_INFORM_NOTHING_FOUND = 'plane_inform_nothing_found'

# Intent names for party_plan, party_rsvp
INTENT_PARTY_ASK_VENUE = 'party_ask_venue'
INTENT_PARTY_ASK_NUMBER_OF_GUESTS = 'party_ask_number_of_guests'
INTENT_PARTY_ASK_STARTING_TIME = 'party_ask_starting_time'
INTENT_PARTY_ASK_END_TIME = 'party_ask_end_time'
INTENT_PARTY_ASK_DAY = 'party_ask_day'
INTENT_PARTY_ASK_FOOD = 'party_ask_food'
INTENT_PARTY_ASK_DRINKS = 'party_ask_drinks'
INTENT_PARTY_VENUE_NOT_AVAILABLE = 'party_venue_not_available'
INTENT_PARTY_ASK_CONFIRM_BOOKING = 'party_ask_confirm_booking'
INTENT_PARTY_BOOKING_SUCCESSFUL = 'party_booking_successful'
INTENT_PARTY_BOOKING_FAILED = 'party_booking_failed'
INTENT_PARTY_ASK_HOST = 'party_ask_host'
INTENT_PARTY_ASK_ARRIVAL_TIME = 'party_ask_arrival_time'
INTENT_PARTY_ASK_DIETARY_RESTRICTIONS = 'party_ask_dietary_restrictions'
INTENT_PARTY_CONFIRM_RSVP = 'party_confirm_rsvp'
INTENT_PARTY_NO_VENUE_AVAILABLE = 'party_no_venue_available'
INTENT_PARTY_INFORM_FOOD_DRINK_CRITERIA = 'party_inform_food_drink_criteria'
INTENT_PARTY_ASK_PARKING_NEEDED = 'party_ask_parking_needed'
INTENT_PARTY_BYE = 'party_bye'
INTENT_PARTY_INFORM_NOTHING_FOUND = 'party_inform_nothing_found'

# Intent names for restaurant_reserve, restaurant_search
INTENT_RESTAURANT_ASK_RESTAURANT = 'restaurant_ask_restaurant'
INTENT_RESTAURANT_ASK_TIME = 'restaurant_ask_time'
INTENT_RESTAURANT_ASK_SIZE = 'restaurant_ask_size'
INTENT_RESTAURANT_INFORM_UNAVAILABLE = 'restaurant_inform_unavailable'
INTENT_RESTAURANT_ASK_CONFIRM_BOOKING = 'restaurant_ask_confirm_booking'
INTENT_RESTAURANT_INFORM_BOOKING_SUCCESSFUL = 'restaurant_inform_booking_successful'
INTENT_RESTAURANT_INFORM_BOOKING_FAILED = 'restaurant_inform_booking_failed'
INTENT_RESTAURANT_BYE = 'restaurant_bye'
INTENT_RESTAURANT_ASK_LOCATION = 'restaurant_ask_location'
INTENT_RESTAURANT_ASK_FOOD_TYPE = 'restaurant_ask_food_type'
INTENT_RESTAURANT_ASK_RATING = 'restaurant_ask_rating'
INTENT_RESTAURANT_ASK_DELIVERY = 'restaurant_ask_delivery'
INTENT_RESTAURANT_ASK_TAKES_RESERVATIONS = 'restaurant_ask_takes_reservations'
INTENT_RESTAURANT_INFORM_SEARCH_RESULTS = 'restaurant_inform_search_results'
INTENT_RESTAURANT_ASK_CONTINUE_SEARCHING = 'restaurant_ask_continue_searching'
INTENT_RESTAURANT_INFORM_NOTHING_FOUND = 'restaurant_inform_nothing_found'
INTENT_RESTAURANT_INFORM_SEARCH_CRITERIA = 'restaurant_inform_search_criteria'

# Intent names for apartment_search and book_apartment_viewing
INTENT_APARTMENT_INFORM_SEARCH_CRITERIA = 'apartment_inform_search_criteria'
INTENT_APARTMENT_ASK_NUM_BEDROOMS = 'apartment_ask_num_bedrooms'
INTENT_APARTMENT_ASK_PRICE = 'apartment_ask_price'
INTENT_APARTMENT_ASK_FLOOR = 'apartment_ask_floor'
INTENT_APARTMENT_ASK_BALCONY = 'apartment_ask_balcony'
INTENT_APARTMENT_ASK_ELEVATOR = 'apartment_ask_elevator'
INTENT_APARTMENT_ASK_NEARBY_POIS = 'apartment_ask_nearby_pois'
INTENT_APARTMENT_INFORM_SEARCH_RESULT = 'apartment_inform_search_result'
INTENT_APARTMENT_ASK_SEARCH_MORE = 'apartment_ask_search_more'
INTENT_APARTMENT_BYE = 'apartment_bye'
INTENT_APARTMENT_ASK_APARTMENT_NAME = 'apartment_ask_apartment_name'
INTENT_APARTMENT_ASK_DAY = 'apartment_ask_day'
INTENT_APARTMENT_ASK_START_TIME = 'apartment_ask_start_time'
INTENT_APARTMENT_ASK_END_TIME = 'apartment_ask_end_time'
INTENT_APARTMENT_ASK_APPLICATION_FEE_PAID = 'apartment_ask_application_fee_paid'
INTENT_APARTMENT_ASK_CUSTOM_MESSAGE = 'apartment_ask_custom_message'
INTENT_APARTMENT_INFORM_VIEWING_UNAVAILABLE = 'apartment_inform_viewing_unavailable'
INTENT_APARTMENT_INFORM_VIEWING_AVAILABLE = 'apartment_inform_viewing_available'
INTENT_APARTMENT_INFORM_BOOKING_SUCCESSFUL = 'apartment_inform_booking_successful'
INTENT_APARTMENT_INFORM_NOTHING_FOUND = 'apartment_inform_nothing_found'

# Intents for book_doctor_appointment, followup_doctor_appointment
INTENT_DOCTOR_ASK_DOCTOR_NAME = 'doctor_ask_doctor_name'
INTENT_DOCTOR_ASK_DAY = 'doctor_ask_day'
INTENT_DOCTOR_ASK_START_TIME = 'doctor_ask_start_time'
INTENT_DOCTOR_ASK_END_TIME = 'doctor_ask_end_time'
INTENT_DOCTOR_ASK_SYMPTOMS = 'doctor_ask_symptoms'
INTENT_DOCTOR_INFORM_BOOKING_UNAVAILABLE = 'doctor_inform_booking_unavailable'
INTENT_DOCTOR_INFORM_BOOKING_AVAILABLE = 'doctor_inform_booking_available'
INTENT_DOCTOR_INFORM_BOOKING_SUCCESSFUL = 'doctor_inform_booking_successful'
INTENT_DOCTOR_INFORM_DOCTORS_INSTRUCTIONS = 'doctor_inform_doctors_instructions'
INTENT_DOCTOR_BYE = 'doctor_bye'
INTENT_DOCTOR_INFORM_NOTHING_FOUND = 'doctor_inform_nothing_found'

# Intents for spaceship_access_codes, spaceship_life_support
INTENT_SPACESHIP_ASK_RANK = 'spaceship_ask_rank'
INTENT_SPACESHIP_ASK_CODE = 'spaceship_ask_code'
INTENT_SPACESHIP_ASK_CODE_TYPE = 'spaceship_ask_code_type'
INTENT_SPACESHIP_INFORM_OUTCOME = 'spaceship_inform_outcome'
INTENT_SPACESHIP_ASK_LOCK_MANUFACTURER = 'spaceship_ask_lock_manufacturer'
INTENT_SPACESHIP_ASK_COLOUR_TOP_CABLE = 'spaceship_ask_colour_top_cable'
INTENT_SPACESHIP_ASK_COLOUR_SECOND_CABLE = 'spaceship_ask_colour_second_cable'
INTENT_SPACESHIP_BYE = 'spaceship_bye'
INTENT_SPACESHIP_INFORM_NOTHING_FOUND = 'spaceship_inform_nothing_found'

# Intents for bank_balance, bank_fraud_report
INTENT_BANK_ASK_ACCOUNT_NUMBER = 'bank_ask_account_number'
INTENT_BANK_ASK_PIN = 'bank_ask_pin'
INTENT_BANK_ASK_DOB = 'bank_ask_dob'
INTENT_BANK_ASK_MOTHERS_MAIDEN_NAME = 'bank_ask_mothers_maiden_name'
INTENT_BANK_ASK_CHILDHOOD_PETS_NAME = 'bank_ask_childhood_pets_name'
INTENT_BANK_INFORM_CANNOT_AUTHENTICATE = 'bank_inform_cannot_authenticate'
INTENT_BANK_INFORM_BALANCE = 'bank_inform_balance'
INTENT_BANK_ASK_FRAUD_DETAILS = 'bank_ask_fraud_details'
INTENT_BANK_INFORM_FRAUD_REPORT_SUBMITTED = 'bank_inform_fraud_report_submitted'
INTENT_BANK_BYE = 'bank_bye'
INTENT_BANK_INFORM_NOTHING_FOUND = 'bank_inform_nothing_found'

# Intents for schedule_meeting
INTENT_MEETING_ASK_GUEST_NAME = 'meeting_ask_guest_name'
INTENT_MEETING_ASK_DAY = 'meeting_ask_day'
INTENT_MEETING_ASK_START_TIME = 'meeting_ask_start_time'
INTENT_MEETING_ASK_END_TIME = 'meeting_ask_end_time'
INTENT_MEETING_ASK_REASON = 'meeting_ask_reason'
INTENT_MEETING_INFORM_CONFIRMED = 'meeting_inform_confirmed'
INTENT_MEETING_INFORM_UNAVAILABLE_ASK_DIFFERENT_TIME = 'meeting_inform_unavailable_ask_different_time'
INTENT_MEETING_BYE = 'meeting_bye'
INTENT_MEETING_INFORM_NOTHING_FOUND = 'meeting_inform_nothing_found'

# Intents for trip_directions
INTENT_TRIP_ASK_TRAVEL_MODE = 'trip_ask_travel_mode'
INTENT_TRIP_ASK_DEPARTURE_LOCATION = 'trip_ask_departure_location'
INTENT_TRIP_ASK_ARRIVAL_LOCATION = 'trip_ask_arrival_location'
INTENT_TRIP_ASK_DEPARTURE_TIME = 'trip_ask_departure_time'
INTENT_TRIP_INFORM_SIMPLE_STEP_ASK_PROCEED = 'trip_inform_simple_step_ask_proceed'
INTENT_TRIP_INFORM_DETAILED_STEP = 'trip_inform_detailed_step'
INTENT_TRIP_INFORM_LAST_STEP_AND_DONE = 'trip_inform_last_step_and_done'
INTENT_TRIP_BYE = 'trip_bye'
INTENT_TRIP_INFORM_NOTHING_FOUND = 'trip_inform_nothing_found'
INTENT_TRIP_INFORM_INSTRUCTIONS_DONE = 'trip_instructions_done'

# Intents for trivia
INTENT_TRIVIA_ASK_QUESTION_NUMBER = 'trivia_ask_question_number'
INTENT_TRIVIA_ASK_QUESTION = 'trivia_ask_question'
INTENT_TRIVIA_INFORM_ANSWER_CORRECT_ASK_NEXT = 'trivia_inform_answer_correct_ask_next'
INTENT_TRIVIA_INFORM_ANSWER_INCORRECT_ASK_NEXT = 'trivia_inform_answer_incorrect_ask_next'
INTENT_TRIVIA_INFORM_ANSWER_2_ASK_NEXT = 'trivia_inform_answer_2_ask_next'
INTENT_TRIVIA_BYE = 'trivia_bye'
INTENT_TRIVIA_INFORM_NOTHING_FOUND = 'trivia_inform_nothing_found'

# Intents for weather
INTENT_WEATHER_ASK_DAY = 'weather_ask_day'
INTENT_WEATHER_ASK_LOCATION = 'weather_ask_location'
INTENT_WEATHER_INFORM_FORECAST = 'weather_inform_forecast'
INTENT_WEATHER_BYE = 'weather_bye'
INTENT_WEATHER_INFORM_NOTHING_FOUND = 'weather_inform_nothing_found'

SCENARIO_PORT_MAP = {
    'book_ride': '5005',
    'ride_change': '5006',
    'ride_status': '5007',
    'hotel_search': '5008',
    'hotel_reserve': '5009',
    'party_plan': '5010',
    'party_rsvp': '5011',
    'plane_reserve': '5012',
    'plane_search': '5013',
    'restaurant_reserve': '5014',
    'restaurant_search': '5015',
    'apartment_search': '5016',
    'book_apartment_viewing': '5017',
    'book_doctor_appointment': '5018',
    'followup_doctor_appointment': '5019',
    'spaceship_access_codes': '5020',
    'spaceship_life_support': '5021',
    'bank_balance': '5022',
    'bank_fraud_report': '5023',
    'hotel_service_request': '5024',
    'schedule_meeting': '5025',
    'trip_directions': '5026',
    'trivia': '5027',
    'weather': '5028'
}