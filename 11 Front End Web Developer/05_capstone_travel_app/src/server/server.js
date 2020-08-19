// Setup empty JS object to act as endpoint for all routes
const projectData = {};

// Provide utilities for working with file and directory paths
var path = require('path');

// Require Express to run server and routes
const express = require('express');

// Start up an instance of app
const app = express();

//Here we are configuring express to use body-parser as middle-ware.
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cors for cross origin allowance
const cors = require('cors');
app.use(cors());

// Initialize the main project folder
app.use(express.static('dist'));
console.log(__dirname);

// designates what port the app will listen to for incoming requests
const port = 8081;
app.listen(port, function () {
    console.log('server is running')
    console.log(`running on localport: ${port}!`)
});

// GET route
app.get('/', function (req, res) {
    res.sendFile('dist/index.html')
});

app.get('/all', function (req, res) {
    res.send(projectData);
});

// POST route
app.post('/addTravelPlan', function (req, res) {
    projectData.city = req.body.city;
    projectData.temp = req.body.temp;
    projectData.weather = req.body.weather;
    projectData.date = req.body.date;
    projectData.days = req.body.days;
    projectData.imgURL = req.body.imgURL;
    console.log(projectData);
});