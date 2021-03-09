
DUMMY_FORM_DESCRIPTION = {
    "apartment_search": {
        "input": [
            {
                "Name": "Level",
                "Type": "Integer",
                "Min": 0,
                "Max": 15,
                "ReadableName": "Level",
            },
            {
                "Name": "MaxLevel",
                "Type": "Integer",
                "Min": 0,
                "Max": 15,
                "ReadableName": "Max Level",
            },
            {"Name": "HasBalcony", "Type": "Boolean", "ReadableName": "Has Balcony"},
            {
                "Name": "BalconySide",
                "Type": "Categorical",
                "Categories": ["east", "north", "south", "west"],
                "ReadableName": "Balcony Side",
            },
            {"Name": "HasElevator", "Type": "Boolean", "ReadableName": "Has Elevator"},
            {
                "Name": "NumRooms",
                "Type": "Integer",
                "Min": 1,
                "Max": 7,
                "ReadableName": "Num Rooms",
            },
            {
                "Name": "FloorSquareMeters",
                "Type": "Integer",
                "Min": 10,
                "Max": 350,
                "ReadableName": "Floor Square Meters",
            },
            {
                "Name": "NearbyPOIs",
                "Type": "CategoricalMultiple",
                "Categories": ["School", "TrainStation", "Park"],
                "ReadableName": "Nearby POIs",
            },
            {
                "Name": "Name",
                "Type": "Categorical",
                "Categories": [
                    "One on Center Apartments",
                    "Shadyside Apartments",
                    "North Hill Apartments",
                ],
                "ReadableName": "Name",
            },
        ],
        "output": [
            {
                "Name": "Level",
                "Type": "Integer",
                "Min": 0,
                "Max": 15,
                "ReadableName": "Level",
            },
            {
                "Name": "MaxLevel",
                "Type": "Integer",
                "Min": 0,
                "Max": 15,
                "ReadableName": "Max Level",
            },
            {"Name": "HasBalcony", "Type": "Boolean", "ReadableName": "Has Balcony"},
            {
                "Name": "BalconySide",
                "Type": "Categorical",
                "Categories": ["east", "north", "south", "west"],
                "ReadableName": "Balcony Side",
            },
            {"Name": "HasElevator", "Type": "Boolean", "ReadableName": "Has Elevator"},
            {
                "Name": "NumRooms",
                "Type": "Integer",
                "Min": 1,
                "Max": 7,
                "ReadableName": "Num Rooms",
            },
            {
                "Name": "FloorSquareMeters",
                "Type": "Integer",
                "Min": 10,
                "Max": 350,
                "ReadableName": "Floor Square Meters",
            },
            {
                "Name": "NearbyPOIs",
                "Type": "CategoricalMultiple",
                "Categories": ["School", "TrainStation", "Park"],
                "ReadableName": "Nearby POIs",
            },
            {
                "Name": "Name",
                "Type": "Categorical",
                "Categories": [
                    "One on Center Apartments",
                    "Shadyside Apartments",
                    "North Hill Apartments",
                ],
                "ReadableName": "Name",
            },
        ],
        "required": [],
        "db": "apartment",
        "function": "generic_sample",
        "returns_count": True,
        "schema_url": "https://upload.wikimedia.org/wikipedia/commons/6/65/Difficult_editor_-_flow_chart.png",
    },
    "ride_status": {
        "input": [
            {
                "Name": "id",
                "Type": "Integer",
                "Min": 1,
                "Max": 1000,
                "ReadableName": "id",
            }
        ],
        "output": [
            {
                "Name": "Price",
                "Type": "Integer",
                "Min": 5,
                "Max": 50,
                "ReadableName": "Price",
            },
            {
                "Name": "AllowsChanges",
                "Type": "Boolean",
                "ReadableName": "Allows Changes",
            },
            {
                "Name": "DurationMinutes",
                "Type": "Integer",
                "Min": 5,
                "Max": 30,
                "ReadableName": "Duration Minutes",
            },
            {
                "Name": "ServiceProvider",
                "Type": "Categorical",
                "Categories": ["Uber", "Lyft", "Taxi"],
                "ReadableName": "Service Provider",
            },
            {
                "Name": "DriverName",
                "Type": "Categorical",
                "Categories": ["Mark", "John", "Dave", "Connor", "Alex"],
                "ReadableName": "Driver Name",
            },
            {
                "Name": "CarModel",
                "Type": "Categorical",
                "Categories": ["Honda", "Toyota", "Corolla", "Tesla", "BMW", "Ford"],
                "ReadableName": "Car Model",
            },
            {
                "Name": "LicensePlate",
                "Type": "Categorical",
                "Categories": ["432 LSA", "313 EA9", "901 FSA", "019 EAS", "031 NGA"],
                "ReadableName": "License Plate",
            },
            {
                "Name": "id",
                "Type": "Integer",
                "Min": 1,
                "Max": 1000,
                "ReadableName": "id",
            },
            {
                "Name": "RideStatus",
                "Type": "ShortString",
                "ReadableName": "Ride Status",
            },
            {"Name": "RideWait", "Type": "ShortString", "ReadableName": "Ride Wait"},
        ],
        "required": ["id"],
        "db": "ride",
        "function": "ride_status",
        "returns_count": False,
        "schema_url": "http://www.texample.net/media/tikz/examples/PNG/simple-flow-chart.png",
    }
}