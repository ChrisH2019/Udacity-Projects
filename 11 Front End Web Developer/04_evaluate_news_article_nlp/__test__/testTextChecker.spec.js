// Import the js file to test
import { checkForText } from "../src/client/js/textChecker"

// The describe() function takes two arguments - a string description, and a test suite as a callback function.  
// A test suite may contain one or more related tests    
describe("Testing the check input text functionality", () => {
    // The test() function has two arguments - a string description, and an actual test as a callback function.  
    test("Testing the checkForText() function", () => {
           // Define the input for the function, if any, in the form of variables/array
           // Define the expected output, if any, in the form of variables/array
           // The expect() function, in combination with a Jest matcher, is used to check if the function produces the expected output
           // The general syntax is `expect(myFunction(arg1, arg2, ...)).toEqual(expectedValue);`, where `toEqual()` is a matcher
           expect(checkForText('')).toBe(true);
    });
});