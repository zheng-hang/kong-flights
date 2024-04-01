# IS213 G7T2 Ais Kachang
# SMOOth Flights
SMOOth Flights is a flight company that offers an interactive web-based application encompassing:
- Flight Search and Booking System: For users to browse available flights from SIA and Lufthansa and make flight bookings
- Payment System: For handling payments 
- Seat Selection System: For users to change seats for their flight.

In this project, SMOOth Flights is able to tackle the following 3 users scenarios:
1. Passenger searching for flight
2. Passenger booking a flight
3. Passenger changes flight seat

## Requirements

## Tools used
- [Vue 3](https://vuejs.org/guide/introduction.html)
- [Bootstrap XX](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Docker](https://www.docker.com/get-started/)
- [Python](https://www.python.org/about/gettingstarted/)
- [MySQL](https://dev.mysql.com/doc/workbench/en/wb-intro.html)

## REST APIs used
- SIA API (https://developer.singaporeair.com/api_flight_schedule)
- Lufthansa API (https://developer.lufthansa.com/docs/read/api_details/flight_schedules) 
- Paypal API (https://developer.paypal.com/api/rest/)

## Beyond The Lab
- Choreography
- Enable communication among microservices running on different physical machines
- Utilising a different coding language

# Description

## Vue
We used `VUE3 cli` for this project. This allowed us to customize configuration. [Configuration Reference](https://cli.vuejs.org/config/).

Most notable portions included the use of 
- VUE Routers

We created `components` that were reused in various places and imported them where needed to streamline the application.  

## Bootstrap and CSS
We made use of the `12-point grid system` to help make our application responsive. 

# API Used
We incorporated `SIA API` (https://developer.singaporeair.com/api_flight_schedule) and `Lufthansa API` (https://developer.lufthansa.com/docs/read/api_details/flight_schedules) into our Scraper complex microservice.

This allows us to obtain all new available flights from SIA and Lufthansa for passengers to view and book. This is done through our Scraper complex microservice through a HTTP GET request. 

We also incorporated `Paypal API` (https://developer.paypal.com/api/rest/) into Payment service.

This enables passengers to do payment through Paypal at the end of their booking process. This is done through our Payment service. 

# Beyond The Lab

## Choreography
To enable asynchronous email notifications, we built a choreography-based system for when passengers make a booking by establishing communication between the two (micro)services - Passenger Bookings and Notifications. This means that whenever a booking is made,  the Passenger Bookings composite microservice sends a message to the Notification service queue via RabbitMQ. Afterwhich, the Notification service consumes the message and sends the email notification to the user. 

## Enable communication among microservices running on different physical machines
Multiple devices communication aka the 2 devices run container, they shld be able to connect to the other container. This is when the devices are on the same hotspot.

## Utilising a different coding language
Our payment page uses Javascript, instead of Vue.

# Project setup
## Access project folder and download dependencies

```sh
cd Kong Flights
npm install
```

### Compiles and hot-reloads for development
```sh
npm run serve
```

### Compiles and minifies for production
```sh
npm run build
```

### Building docker containers
In one terminal, 
```sh
cd dbcontainers
docker-compose up --build
```
In a separate terminal,
```sh
cd microservices
docker-compose -f microsvc.yml up --build
```

# Accessing the application
You may log into our pages using any of the following credentials
```sh
credentials_list = [
    ('emily.jones987@example.org', 'abc123'),
    ('sarah.smith5678@gmail.com', 'efg456'),
    ('johndoe1234@example.com', 'hij789'),
]
```




