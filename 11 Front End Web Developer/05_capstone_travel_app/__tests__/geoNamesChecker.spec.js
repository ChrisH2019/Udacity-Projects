import { checkForGeoName } from "../src/client/js/geoNamesChecker"

describe("Testing the geo name functionality", () => {
    test("Testing the checkForGeoName() function", () => {
        expect(checkForGeoName('')).toBe(false);
    });
});