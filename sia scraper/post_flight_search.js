const url = "https://apigw.singaporeair.com/api/uat/v1/commercial/flightavailability/get";
// const headers = {
//     "Accept": "application/json",
//     "Authorization": "Bearer YOUR_ACCESS_TOKEN",  // Only if needed
// };

// fetch(url, {
//     method: "GET",
//     headers: headers
// })
// .then(response => {
//     if (response.ok) {
//         return response.json();
//     }
//     throw new Error("Network response was not ok.");
// })
// .then(data => console.log(data))
// .catch(error => console.error("Error:", error));


// const url = "YOUR_API_ENDPOINT";
const data = {

  "clientUUID": "05b2fa78-a0f8-4357-97fe-d18506618c3f",
  "request": {
    "itineraryDetails": [
      {
        "originAirportCode": "SIN",
        "destinationAirportCode": "SPK",
        "departureDate": "2024-11-01",
        "returnDate": "2024-11-10"
      }
    ],
    "cabinClass": "Y",
    "adultCount": 1,
    "childCount": 0,
    "infantCount": 0
  }

};
const headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer uuabey8rvxfbvznqqhtqt6je",  // Only if needed
};

fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data)
})
.then(response => {
    if (response.ok) {
        console.log(response)
        return response.json();
    }
    throw new Error("Network response was not ok.");
})
.then(data => console.log(data))
.catch(error => console.error("Error:", error));
