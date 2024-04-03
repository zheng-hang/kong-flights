// Import required modules
const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const cors = require('cors');

// Create an Express.js application
const app = express();

app.use(cors());

// Middleware setup
app.use(bodyParser.json());
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

app.use(cors({
    origin: 'http://localhost:8080/login', // Allow requests only from example.com
    methods: ['GET', 'POST'], // Allow only GET and POST requests
    allowedHeaders: ['Content-Type'], // Allow only Content-Type header
  }));

// Define an API endpoint to store data in session
app.post('/storeDataInSession', (req, res) => {
    const { key, value } = req.body;
  
    // Check if the key is valid and value is a string
    if (typeof value === 'string') {
      req.session[key] = value;
      res.send('Data stored in session successfully');
    } else {
      res.status(400).send('Invalid data type for session storage');
    }
  });

// Define an API endpoint to retrieve session data
app.get('/api/getSessionData', (req, res) => {
    // Retrieve the data from the session
    const email = req.session.email; // Assuming email is stored in session
    res.json({ email }); // Send the data back to the client
  });

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});