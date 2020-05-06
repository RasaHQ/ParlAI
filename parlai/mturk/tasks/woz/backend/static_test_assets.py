
def get_book_ride_item():
    kb_item =  {
        "id": 660,
        "Price": 22,
        "AllowsChanges": False,
        "MinutesTillPickup": 20,
        "ServiceProvider": "Uber",
        "DriverName": "Ella",
        "CarModel": "Ford",
        "LicensePlate": "432 LSA",
        "DepartureLocation": "Tegel Airport, International Arrivals",
        "ArrivalLocation": "Hyatt Alexanderplatz",
    }

    utterances = [
        'Right, Could you provide your name?',
        'No problem, where can the driver pick you up from?',
        'whats your name?',
        'where do you like to go, sir?',
        'thats all booked for you now.',
        'Your car will arrive in 34 minutes and your driver will be Carl in some old car. He is from Uber btw.',
        'i can filter for another service provider if you want',
        'What else can I help you with?',
        'Want anything else?'
    ]

    return kb_item, utterances, 'book_ride'


def get_ride_status_item():
    kb_item = {
        "RideStatus": "Your Driver is arriving",
        "RideWait": 12,
    }

    utterances = [
        "Your driver Jack will arrive shortly. He got held up due to traffic.",
        "Your ride will arrive in about 7 minutes.",
        "Can I have your name?",
        "Whats your booking id?",
        "hi",
        "Bye"
    ]

    return kb_item, utterances, 'ride_status'


def get_ride_change_item():
    kb_item = {

    }

    utterances = [
        "howdy cowboy",
        "What do you want changed?",
        "Whats your confirmation code?",
        "You need to to tell me your name",
        "Yes, successfully changed the ride for you",
        "Sorry, changes are not possible",
        "cya"
    ]

    return kb_item, utterances, 'ride_change'


def get_hotel_search_item():
    kb_item_1 = {
        "Name": "Old Town Inn",
        "Cost": "Cheap",
        "TakesReservations": True,
        "Service": False,
        "Location": "North",
        "AverageRating": 3,
        "ServiceStartHour": 10,
        "ServiceStopHour": 4
    }

    kb_item_2 = {
        "Name": "The Fake Hyatt",
        "Cost": "Cheap",
        "TakesReservations": True,
        "Service": True,
        "Location": "East",
        "AverageRating": 2,
        "ServiceStartHour": 10,
        "ServiceStopHour": 4
    }

    utterances = [
        "hohoho",
        "I can search for other things such as cost or location",
        "What hotel do you want?",
        "Its the Marriott",
        "Where do you want to go?",
        "In the North",
        "How much money do you want to spend?",
        "The hotel is a moderately priced place",
        "What rating should the place have?",
        "The hotel has an average rating of 3.3",
        "Great, I found a hotel in the south that matches your search criterea.",
        "Anything else you want to search for?",
        "bybo"
    ]

    return kb_item_2, utterances, 'hotel_search'


def get_hotel_reserve_item():
    kb_item = {
        "Name": "Old Town Inn",
        "StartDate": 12,
        "EndDate": 27,
        "CustomerName": "Ben",
        "CustomerRequest": "vegan breakfast"
    }

    utterances = [
        "hohoho",
        "howdy partner",
        "Hello, what can I do for you today?",
        "Whats your name, please?",
        "When are you going to checkin?",
        "And checkout is when?",
        "Anything special the hotel should provide you with?",
        "Oh no, I'm sorry, but there doesn't seem to be a room available.",
        "Great, I found a hotel that matches your criteria, can I book this for you now?",
        "Yay, booking completed successfully!",
        "Sorry, but the booking request failed.",
        "Bye"
    ]

    return kb_item, utterances, 'hotel_reserve'


def get_plane_reserve_item():
    kb_item = {
        "id": 666,
        "CustomerName": "Sally"
    }

    utterances = [
        "Heyho partner",
        "Whats your name?",
        "Find your flight ID for me please",
        "That flight, however, is not available any more",
        "Got that, can i reserve that for you?",
        "Alright, your reservation is done!",
        "Sorry, but your reservation failed for some reason",
        "cheers and bye"
    ]

    return kb_item, utterances, 'plane_reserve'


def get_party_plan_item():
    kb_item = {
        "Name": "The Awesome Party Venue",
        "HostName": "Joni",
        "Day": "Saturday",
        "StartTimeHour": 16,
        "EndTimeHour": 22,
        "NumberGuests": 12
    }

    utterances = [
        'Heyho, whats up?',
        'Where do you want to get hammered?',
        'Whos hosting this?',
        'How many of you will be dancing and drinking?',
        'When do you want to start?',
        'When should we shove you out of the door again?',
        'What day of the week are you thinkging of?',
        'Any spefific food wishes?',
        'Any drinks prefs you\'ve got?',
        'Sorry mate, but this is not going to work out.',
        'Right, they are happy to have you, can I book this now?',
        'Cool, all booked and all done!',
        'Oops, something went horribly wrong.',
        'Sorry, everything is fully booked on Friday night.',
        'Do you want to optionally book any specific type of food or drink for your party?'
    ]

    return kb_item, utterances, 'party_plan'


def get_party_rsvp_item():
    kb_item = {
        "Name": "John",
        "HostName": "Joanne",
        "GuestName": "Mike",
        "ArrivalTime": 20,
        "NumberGuests": 12,
        "NeedParking": False
    }

    utterances = [
        'Howdie buddy',
        'Your name?',
        'Where is shit going down?',
        'Who is hosting this?',
        'Whats your ETA?',
        'How many of your lads will come with you?',
        'Any of you vegan or got a food allergy?',
        'Your rsvp is done.'
    ]

    return kb_item, utterances, 'party_rsvp'


def get_plane_search_item():
    kb_item = {
        "DepartureCity": "Vienna",
        "ArrivalCity": "New York",
        "Price": 300,
        "Date": 12,
        "Class": "Economy",
        "Duration": 6,
        "Airline": "Virgin"
    }

    utterances = [
        'Hey, whats up?',
        'What did they call you when you were born?',
        'From where are you going?',
        'Going to where?',
        'When do you want to go?',
        'I can filter for other things such as price or duration if you want.',
        'Great, I found an American flight in business class for 500 bucks. Takes 8 hours though.',
        'Want to search for anything else?',
        'Cheers and see you.',
    ]

    return kb_item, utterances, 'plane_search'


def get_restaurant_reserve_item():
    kb_item = {
        "Name": "Cactus Club",
        "Time": 21,
        "PartySize": 4,
        "CustomerName": "Jane"
    }

    utterances = [
        'Hi',
        'Can you give me your esteemed name sir?',
        'What shed to you want to eat at?',
        'When do you want to stuff yourselves?',
        'How many of you are going to be there?',
        'Sorry but this place doesnt want you.',
        'Great, the Cactus Club is delighted to take your booking.',
        'Booking successful',
        'Booking failed!',
        'Bye'
    ]

    return kb_item, utterances, 'restaurant_reserve'


def get_restaurant_search_item():
    kb_item = {
        "Name": "Harmonium",
        "Cost": "Moderate",
        "TakesReservations": True,
        "DoesDelivery": False,
        "AverageRating": 5,
        "Food": "Burgers",
        "AverageWaitMinutes": 32,
        "OpenTimeHour": 11,
        "CloseTimeHour": 23,
        "MaxPartySize": 12,
        "Location": "North"
    }

    utterances = [
        'Hello my friend, what can I do for you today?',
        'Whats your name?',
        'Any restaurant you have in mind?',
        'What district do you want to go to?',
        'Any wishes cuisinewise?',
        'Whats your rating criteria?',
        'Do you need a delivery service?',
        'Do you need a place where you can reserve a table?',
        'Right, there is the Hove Kitchen that serves great food and its in the West part of town. Its average rating is 4 and its in the Expensive price category.',
        'Do you want to search for any more eateries?'
    ]

    return kb_item, utterances, 'restaurant_search'


def get_apartment_search_item():
    kb_item = {
        "Level": 3,
        "MaxLevel": 4,
        "HasBalcony": True,
        "BalconySide": "east",
        "HasElevator": False,
        "NumRooms": 4,
        "FloorSquareMeters": 90,
        "NearbyPOIs": ["Park", "School"],
        "Name": "North Hill Apartments",
        "Price": 1600
    }

    utterances = [
        "Hello",
        "Hello, I love you. Could you tell me your name.",
        "I can search for a lot of things, including, but not limited to, price and floor.",
        "How much money do you want to spend?",
        "Whats your favourite level?",
        "Need a balcony?",
        "Want an elevator?",
        "Looking to live near a park or the station?",
        "Right, got a free flat at Shadyside apartments, no elevator, no windows, no balconly, 600 a month, you in?",
        "Wanna search for more?",
        "Cheerio and byeio"
    ]

    return kb_item, utterances, 'apartment_search'


def get_book_apartment_viewing_item():
    kb_item = {
        "Name": "Shadyside Apartments",
        "Day": "Wednesday",
        "StartTimeHour": 8,
        "EndTimeHour": 10,
        "RenterName": "Jason",
        "ApplicationFeePaid": "Yes",
    }

    utterances = [
        "Heyo, listen what I sayo",
        "Tell me your name.",
        "And now the name of the apartment",
        "Whats a good day to see the place?",
        "And whats a good time to see it?",
        "For how long?",
        "Paid the fee?",
        "Leave a message?",
        "Sorry, there is no viewing available then.",
        "Great, there is a viewing available then. Can I book this for you?",
        "Alright, you're all booked in."
    ]

    return kb_item, utterances, 'book_apartment_viewing'


def get_book_doctor_appointment_item():
    kb_item = {
        "Name": "Dr. Morgan",
        "Day": "Thursday",
        "StartTimeHour": 9,
        "EndTimeHour": 11,
        "PatientName": "Jenny",
        "Symptoms": "Covid-19"
    }

    utterances = [
        "Hey, what can I do for you today?",
        "Your name please",
        "Which doctor do you see typically?",
        "Whats your favourite day for surgery?",
        "When do you want it to start?",
        "And when do you want it to end?",
        "Tell me all teh symptons you have.",
        "Sorry, the doctor is busy then.",
        "Alright, doctor's got time. Can I book it for you?",
        "Cool, all booked with the doc."
    ]

    return kb_item, utterances, 'book_doctor_appointment'


def get_followup_doctor_appointment_item():
    kb_item = {
        "Name": "Dr. Alexis",
        "PatientName": "Mandy",
        "Message": "Dr. Dr. PLEEEEEASE!!! Look at the mess I'm in!"
    }

    utterances = [
        "Hello, this is doctors follow up appointements fully automated speaking."
        "Please give me your name.",
        "Tell me the name of your doctor."
        "Doctor tells you to sit still and relax."
    ]

    return kb_item, utterances, 'followup_doctor_appointment'


def get_spaceship_access_codes_item():
    kb_item = {
        "UserRank": "Bartender",
        "CodeType": "Clearance",
        "Code": "CC 308",
        "UserName": "Johnny",
        "Message": "All your base are belong to us!"
    }

    utterances = [
        "What do you want?",
        "Whats your name?",
        "What rank are you?",
        "Give me the code.",
        "Give me the type of the code",
        "Everything failed."
    ]

    return kb_item, utterances, 'spaceship_access_codes'


def get_spaceship_life_support_item():
    kb_item = {
        "LockManufacturer": "Microsoft",
        "ColorOfTopCable": "Green",
        "ColorOfSecondCable": "Red",
        "Message": "Operation failed. You are doomed."
    }

    utterances = [
        "Hey waddup",
        "Your name, sir",
        "I'd really appreciate if you give me the colour of the top cable.",
        "I'd even more so appreciate you telling me the colour of the other cable.",
        "Thats all sorted again."
    ]

    return kb_item, utterances, 'spaceship_life_support'


def get_bank_balance_item():
    kb_item = {
        'BankName': 'Wells Fargo',
        'BankBalance': 1200
    }

    utterances = [
        'Hi, what cna I do for you?',
        'Whats your name?',
        'And your account number?',
        'I also need your PIN please.',
        'And your date of birth.',
        'First security question is your mother\'s maiden name',
        'Second sec q concerns the name of some pet you had as a kid',
        'Sorry, but I cannot authenticate you.',
        'Your balance is 789 credits.',
        'Do you want anything else?'
    ]

    return kb_item, utterances, 'bank_balance'


def get_bank_fraud_report_item():
    kb_item = {

    }

    utterances = [
        'Hi, what cna I do for you?',
        'Whats your name?',
        'And your account number?',
        'I also need your PIN please.',
        'And your date of birth.',
        'First security question is your mother\'s maiden name',
        'Second sec q concerns the name of some pet you had as a kid',
        'Sorry, but I cannot authenticate you.',
        'Right, your report was submitted, we\'ll be in touch shortly!',
        'Can you provide your fraud report now, please?',
        'Do you want anything else?'
    ]

    return kb_item, utterances, 'bank_fraud_report'


def get_hotel_service_request_item():
    kb_item = {
        'RoomNumber': 123,
        'Time': 14
    }

    utterances = [
        'Hey, what do you want?',
        'Can you give me your name?',
        'Where are you staying?',
        'Whats your room number?',
        'What do you want?',
        'When do you want it?',
        'Thats all done for you!',
        'Sorry, but that is not going to work.',
        'Anything else you want?'
    ]

    return kb_item, utterances, 'hotel_service_request'


def get_schedule_meeting_item():
    kb_item = {
        'Day': 'Tuesday',
        'StartTimeHour': 10,
        'EndTimeHour': 12,
        'Name': 'Fred'
    }

    utterances = [
        'Howdy, whats going on?',
        'Whats your name?',
        'Who would you like to meet?',
        'When do you want to meet?',
        'When do you want to start?',
        'When do you want to finish?',
        'Why do you want to meet?',
        'Your meeting with John has been successfully scheduled.',
        'Jane does not have any time on Tuesday, do you want to pick another day?',
        'Bye.',
        'Anybody else you want to bother for a meeting?'
    ]

    return kb_item, utterances, 'schedule_meeting'


def get_trip_directions_item():
    kb_item = {

    }

    utterances = [

    ]

    return kb_item, utterances, 'trip_directions'


def get_trivia_item():
    kb_item_correct = {
        'Question': 'What is the average air speed velocity of a laden swallow?',
        'CorrectAnswer': '42',
        'UserAnswer': '42'
    }

    kb_item_incorrect = {
        'Question': 'What is the average air speed velocity of a laden swallow?',
        'CorrectAnswer': '42',
        'UserAnswer': '54'
    }

    utterances = [
        'Hi, waddup?!',
        'Where do you want to start?',
        'What is the meaning of life, the universe and everything?',
        'Thats right, well done. Want another one?',
        'Thats wrong unfortunately. Do you want to try another question?',
        'Right, bye.',
        'Anything else you want?'
    ]

    return kb_item_correct, utterances, 'trivia'


def get_weather_item():
    kb_item = {
        'City': 'Detroit',
        'Weather': 'Snowing',
        'TemperatureCelsius': -2,
        'Day': 'Sunday'
    }

    utterances = [
        'Hohoho, what are your hopes and dreams today?',
        'For when would you like a weather report?',
        'Any particular place we should guess the weather for?',
        'Its going to be snowing with temperatures of around -2 all day.',
        'Anything else I can help you with?'
    ]

    return kb_item, utterances, 'weather'