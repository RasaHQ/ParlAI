import api

#apt, count = api.call_api(
#    "apartment_search", 
#     constraints={
#         "HasBalcony": True,
#         "NumRooms": api.is_greater_than(2),
#         "NumRooms": api.is_less_than(5),
#     },
#)
#
#msg  = api.call_api(
#    "book_apartment_viewing",
#    constraints={
#        "Name": apt["Name"],
#        "RenterName": "Shikib",
#        "StartTimeHour": 5,
#        "EndTimeHour": 7,
#        "Day": "Tuesday",
#        "ApplicationFeePaid": True
#    },
#)
#I
#print(msg)

msg = api.call_api(
    "plane_search",
    constraints=[{
        "DepartureCity": "New York City",
        "ArrivalCity": "San Francisco",
        "Date": 13,
    }],
)
print(msg)
