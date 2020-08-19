function checkForDate(inputDate) {
    if (!inputDate) {
        return false;
    } else if ((new Date(inputDate)).getUTCDate() < (new Date()).getUTCDate()) {
        return false;
    } else {
        return true;
    }
}

export { checkForDate };