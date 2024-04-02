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
- [MySQL](https://dev.mysql.com/doc/workbench/en/wb-intro.html)
- [Flask](https://flask.palletsprojects.com/en/latest/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/api/)
- [Flask_CORS](https://flask-cors.readthedocs.io/en/latest/)

## REST APIs used
- [SIA API](https://developer.singaporeair.com/api_flight_schedule)
- [Lufthansa API](https://developer.lufthansa.com/docs/read/api_details/flight_schedules) 
- [Paypal API](https://developer.paypal.com/api/rest/)
- [Email API]

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

## Flask
We used `Flask` as a micro web framework written in Python, which we used to build our websites and web applications.  This allowed us Python functions to be called using URLs within HTTP clients such as web browsers and especially by other applications using HTTP methods. We could also use Flask's app.route decorator to map the URL route to a specific function. 

## Flask-SQLAlchemy
We used `Flask-SQLAlchemy` as a Python SQL toolkit and Object Relational Mapper (ORM). This allowed us to easily store objects into a relational database.

## Flask-CORS
We used `Flask-CORS` to explicitly allowing cross-origins access to our microservices to prepare for the web pages.

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

## Useful docker commands
### Check the running containers
```sh
docker ps a
```
### Stop and Remove containers
To stop a specific container,
```sh
docker stop <containerid>
```
To remove a specific container,
```sh
docker rm <containerid>
```
To bring down everything,
```sh
docker compose down
```

### Start the container
```sh
docker start <containerid>
```

### Start a service
```sh
docker compose up <service_name>
```

### Show the logs of the container
```sh
docker logs <containerid>
```

### Creating a custom Docker network
```sh
docker network create <network>
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
