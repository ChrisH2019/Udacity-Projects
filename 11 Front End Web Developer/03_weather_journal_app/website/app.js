/* Global Variables */
// Personal API Key for OpenWeatherMap API
const baseURL = 'http://api.openweathermap.org/data/2.5/weather?zip=';
const apiKey = '&appid=';

// Create a new date instance dynamically with JS
let d = new Date();
let newDate = d.getMonth()+'.'+ d.getDate()+'.'+ d.getFullYear();

// Event listener to add function to existing HTML DOM element
document.getElementById('generate').addEventListener('click', performAction);

/* Function called by event listener */
function performAction(e) {
    const newZipcode = document.getElementById('zip').value + ',us';
    const feelings = document.getElementById('feelings').value;

    getWeather(baseURL, newZipcode, apiKey)
    .then(function(data) {
        console.log(data);
        // Convert temp to Farenheight scale
        let temp = data.main.temp;
        temp = (temp - 273.15) * 9 / 5 + 32;
        temp = temp.toFixed(0) + ' \xB0F';
        // Entry to be posted
        newData = {
            date: newDate,
            temp: temp,
            feelings: feelings
        };
        postWeather('http://localhost:8000/addWeather', newData);
        updateUI();
    });
}

/* Function to GET Web API Data*/
const getWeather = async (baseURL, zipcode, key) => {
    const res = await fetch(baseURL + zipcode + key);
    try {
        const data = await res.json();
        return data;
    } catch(error) {
        console.log('error', error);
    }
};

/* Function to POST data */
const postWeather = async (url='', data={}) => {
    const response = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    try {
        const newData = await response.json();
        return newData;
    } catch(error) {
        console.log('error', error);
    }
};

/* Function to GET Project Data */
const updateUI = async () => {
    const request = await fetch('http://localhost:8000/all');
    try {
        const data = await request.json();
        document.getElementById('date').innerHTML = data.date;
        document.getElementById('temp').innerHTML = data.temp;
        document.getElementById('content').innerHTML = data.feelings;
    } catch(error) {
        console.log('error', error);
    }
}
