// Setup empty JS object to act as endpoint for all routes
projectData = {};

// Use environment variables
const dotenv = require('dotenv');
dotenv.config();

var path = require('path');
const express = require('express');
const mockAPIResponse = require('./mockAPI.js');

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

// POST route
app.post('/analysis', getSentiment);

// Callback function to complete POST '/analysis'
function getSentiment(req, res) {
    const https = require('follow-redirects').https;
    const formText = encodeURI(req.body.formText);
    const options = {
        'method': 'POST',
        'hostname': 'api.meaningcloud.com',
        'path': `/sentiment-2.1?key=${process.env.API_KEY}&lang=en&txt=${formText}&model=general`,
        'headers': {
        },
        'maxRedirects': 20
      };
    
      const request = https.request(options, function (response) {
        var chunks = [];
    
        response.on("data", function (chunk) {
          chunks.push(chunk);
        });
    
        response.on("end", function (chunk) {
          let body = Buffer.concat(chunks);
          // Send the response back to client
          res.send(JSON.parse(body));
        });
    
        response.on("error", function (error) {
          console.error(error);
        });
      });
    
      request.end();
}

app.get('/test', function (req, res) {
    res.send(mockAPIResponse)
});
