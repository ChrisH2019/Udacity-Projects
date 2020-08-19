/* Global Variables */
// User name for GeoNames API
const USER_NAME = '';

// Weatherbit API key
const WEATHERBIT_API_KEY = '';

// Pixaby API key
const PIXABAY_API_KEY = '';

// Create a new timestamp instance dynamically with JS
const currentDate = new Date();
const currentTimestamp = currentDate.getTime() / 1000.0;

// Event listener to add function to the print button element
const printBtn = document.getElementById('print-button')
printBtn.addEventListener('click', function(e) {
    window.print();
})

// Event listener to add function to existing delete button element
const deleteBtn = document.getElementById("delete-button");
deleteBtn.addEventListener('click', function(e) {
    document.getElementById('results').style.display = 'none';
});

// Event listener to add function to existing search button element
const searchBtn = document.getElementById("search-button");
searchBtn.addEventListener('click', performAction);

// Function called by click event listener
function performAction(e) {
    e.preventDefault();

    const city = document.getElementById("city").value;
    if (!Client.checkForGeoName(city)) {
        alert("Please enter a valid city name");
        return;
    };

    const departureDate = document.getElementById("departure-date").value;
    if (!Client.checkForDate(departureDate)) {
        alert("Please enter a valid date");
        return;
    }

    const departureTimestamp = (new Date(departureDate).getTime()) / 1000.0;
    const dayDelta = Math.ceil((departureTimestamp - currentTimestamp) / 86400.0);

    // An empty object to store travel planner data
    const travelData = {};

    getGeonames(encodeURI(city))
    .then((geoData) => {
        const weatherData = getWeatherbit(geoData.lat, geoData.lng, dayDelta);
        return weatherData;
    })
    .then((weatherData) => {
        const pixabayData = getPixabay(encodeURI(weatherData.city));

        travelData.city = weatherData.city;
        let reformattedDate = departureDate.split("-");
        reformattedDate = reformattedDate[1] + "/" + reformattedDate[2] + "/" + reformattedDate[0];
        travelData.date = reformattedDate;
        travelData.days = dayDelta < 1 ? 0 : dayDelta;
        travelData.temp = weatherData.temp;
        travelData.weather = weatherData.weather;

        return pixabayData;
    })
    .then((pixabayData) => {
        travelData.imgURL = pixabayData.imgURL;
        postData('http://localhost:8081/addTravelPlan', travelData);
    })
    .then(() => {
        updateUI();
    })
};

/* Function to GET Geonames API Data (latitude, longitude & counry) */
export const getGeonames = async (city) => {

    const geonamesURL = 'http://api.geonames.org/' +
        `searchJSON?formatted=true&q=${city}` +
        `&username=${USER_NAME}` +
        '&style=full';

    const res = await fetch(geonamesURL);
    try {
        if (!res.ok) {
            alert(`Nonexistent city name: ${city}!`);
            return;
        }
        const geoData = {};
        const data = await res.json();
        geoData.lat = data.geonames[0].lat;
        geoData.lng = data.geonames[0].lng;
        geoData.countryCode = data.geonames[0].countryCode;
        console.log(`${city} info: ${geoData.lat} ${geoData.lng} ${geoData.countryCode}`);
        return geoData;
    } catch (error) {
        console.log('getGeonames error', error);
    }
};

/* Function to GET Weatherbit API Data (weather forecast) */
export const getWeatherbit = async (lat, lon, days) => {
    // Weatherbit only provides 16 days forecast plus 1 current weather data
    if (days > 17) {
        days = 17;
    } else if (days < 1) {
        days = 1;
    }

    const weatherbitURL = 'https://cors-anywhere.herokuapp.com/' +
        'http://api.weatherbit.io/v2.0' +
        `/forecast/daily?lat=${lat}&lon=${lon}` +
        `&days=${days}` +
        `&key=${WEATHERBIT_API_KEY}`;

    const res = await fetch(weatherbitURL);
    try {
        const data = await res.json();
        const weatherData =  {
            city: data.city_name,
            temp: Math.round(data.data[days-1].temp * 9 / 5 + 32),
            weather: data.data[days-1].weather.description
        };
        console.log(weatherData);
        return weatherData;
    } catch (error) {
        console.log('getWeatherbit error', error);
    }
};

/* Function to GET Pixabay API Data (image) */
export const getPixabay = async(city) => {
    const pixabayURL = 'https://pixabay.com/api/' +
        `?key=${PIXABAY_API_KEY}` +
        `&q=${city}&image_type=photo` +
        '&category=places&editors_choice=true';

    const res = await fetch(pixabayURL);
    try {
        const data = await res.json();

        const pixabayData = {};
        if (data.totalHits === 0) {
            pixabayData.imgURL = 'https://cdn.browshot.com/static/images/not-found.png';
        } else {
            pixabayData.imgURL = data.hits[0].webformatURL;
        }
        console.log(pixabayData);

        return pixabayData;
    } catch (error) {
        console.log('getPixabay error', error);
    }
};

/* Function to POST travel planner data to local server */
const postData = async (url='', data={}) => {
    console.log(data);
    const res = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    try {
        const newData = await res.json();
        return newData;
    } catch (error) {
        console.log('postData error', error);
    }
};

/* Function to update travel planner data to index.html */
const updateUI = async () => {
    const request = await fetch('http://localhost:8081/all');
    try {
        const data = await request.json();
        console.log(data);
        document.getElementById('city_name').innerHTML = data.city;
        document.getElementById('date').innerHTML = data.date;
        document.getElementById('days').innerHTML = data.days;
        document.getElementById('temp').innerHTML = data.temp;
        document.getElementById('weather').innerHTML = data.weather;
        document.getElementById('city_image').src = data.imgURL;
        document.getElementById('results').style.display = 'grid';
    } catch (error) {
        console.log('updateUI error', error);
    }
};

export { performAction };