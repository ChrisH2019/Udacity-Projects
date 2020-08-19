function checkForGeoName(geoName) {
    // The shortest length of city name in the world is 1 and the longest one is 85
    let geoNameRegex = /^[a-zA-Z\s]{1,85}$/;
    if (geoNameRegex.test(geoName)) {
        return true;
    } else {
        return false;
    }
}

export { checkForGeoName };