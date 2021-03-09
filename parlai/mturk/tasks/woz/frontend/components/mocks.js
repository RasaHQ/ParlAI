// Copied from https://github.com/RasaHQ/data-collection-2020/blob/master/apis/apis/apartment_search.json
export const apartmentJson = {
  input: [
    { Name: "Level", Type: "Integer", Min: 0, Max: 15 },
    {
      Name: "MaxLevel",
      Type: "Integer",
      Min: 0,
      Max: 15
    },
    { Name: "HasBalcony", Type: "Boolean" },
    {
      Name: "BalconySide",
      Type: "Categorical",
      Categories: ["east", "north", "south", "west"]
    },
    {
      Name: "HasElevator",
      Type: "Boolean"
    },
    { Name: "NumRooms", Type: "Integer", Min: 1, Max: 7 },
    {
      Name: "FloorSquareMeters",
      Type: "Integer",
      Min: 10,
      Max: 350
    },
    {
      Name: "NearbyPOIs",
      Type: "CategoricalMultiple",
      Categories: ["School", "TrainStation", "Park"]
    },
    {
      Name: "Name",
      Type: "Categorical",
      Categories: [
        "One on Center Apartments",
        "Shadyside Apartments",
        "North Hill Apartments"
      ]
    }
  ],
  output: [
    { Name: "Level", Type: "Integer", Min: 0, Max: 15 },
    {
      Name: "MaxLevel",
      Type: "Integer",
      Min: 0,
      Max: 15
    },
    { Name: "HasBalcony", Type: "Boolean" },
    {
      Name: "BalconySide",
      Type: "Categorical",
      Categories: ["east", "north", "south", "west"]
    },
    {
      Name: "HasElevator",
      Type: "Boolean"
    },
    { Name: "NumRooms", Type: "Integer", Min: 1, Max: 7 },
    {
      Name: "FloorSquareMeters",
      Type: "Integer",
      Min: 10,
      Max: 350
    },
    {
      Name: "NearbyPOIs",
      Type: "CategoricalMultiple",
      Categories: ["School", "TrainStation", "Park"]
    },
    {
      Name: "Name",
      Type: "Categorical",
      Categories: [
        "One on Center Apartments",
        "Shadyside Apartments",
        "North Hill Apartments"
      ]
    }
  ],
  required: ["NumRooms"],
  db: "apartment",
  function: "generic_sample",
  returns_count: true
};

const hotelSearch = {
  input: [
    {
      Name: "Name",
      Type: "Categorical",
      Categories: [
        "Shadyside Inn",
        "Hilton Hotel",
        "Hyatt Hotel",
        "Old Town Inn"
      ]
    },
    {
      Name: "Cost",
      Type: "Categorical",
      Categories: ["Cheap", "Moderate", "Expensive"]
    },
    { Name: "TakesReservations", Type: "Boolean" },
    { Name: "Service", Type: "Boolean" },
    { Name: "AverageRating", Type: "Integer", Min: 1, Max: 5 },
    {
      Name: "ServiceStartHour",
      Type: "Integer",
      Min: 6,
      Max: 10,
      Enabled: '!lambda p: p["Service"]'
    },
    {
      Name: "ServiceStopHour",
      Type: "Integer",
      Min: 15,
      Max: 23,
      Enabled: '!lambda p: p["Service"]'
    },
    {
      Name: "Location",
      Type: "Categorical",
      Categories: ["South", "West", "East", "North", "Center"]
    }
  ],
  output: [
    {
      Name: "Name",
      Type: "Categorical",
      Categories: [
        "Shadyside Inn",
        "Hilton Hotel",
        "Hyatt Hotel",
        "Old Town Inn"
      ]
    },
    {
      Name: "Cost",
      Type: "Categorical",
      Categories: ["Cheap", "Moderate", "Expensive"]
    },
    { Name: "TakesReservations", Type: "Boolean" },
    { Name: "Service", Type: "Boolean" },
    { Name: "AverageRating", Type: "Integer", Min: 1, Max: 5 },
    {
      Name: "ServiceStartHour",
      Type: "Integer",
      Min: 6,
      Max: 10,
      Enabled: '!lambda p: p["Service"]'
    },
    {
      Name: "ServiceStopHour",
      Type: "Integer",
      Min: 15,
      Max: 23,
      Enabled: '!lambda p: p["Service"]'
    },
    {
      Name: "Location",
      Type: "Categorical",
      Categories: ["South", "West", "East", "North", "Center"]
    }
  ],
  required: [],
  db: "hotel",
  function: "generic_sample",
  returns_count: true
};
