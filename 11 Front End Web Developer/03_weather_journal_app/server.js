// Setup empty JS object to act as endpoint for all routes
projectData = {};

// Require Express to run server and routes
const express = require('express');

// Start up an instance of app
const app = express();

/* Middleware*/
//Here we are configuring express to use body-parser as middle-ware.
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cors for cross origin allowance
const cors = require('cors');
app.use(cors());

// Initialize the main project folder
app.use(express.static('website'));

// Setup Server
const port = 8000

// Spin up the server
const server = app.listen(port, listening);

// Callback to debug
function listening() {
    console.log('server is running');
    console.log(`running on localport: ${port}`);
}

// GET route
app.get('/all', sendWeather);

// Callback function to complete GET '/all'
function sendWeather(req, res) {
    res.send(projectData);
}

// Post Route
app.post('/addWeather', addWeather);

// Callback function to complete POST '/addWeather'
function addWeather(req, res) {
    projectData.date = req.body.date;
    projectData.temp = req.body.temp;
    projectData.feelings = req.body.feelings;
    // console.log(projectData);
}