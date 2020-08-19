const request = require('supertest');
const express = require('express');
 
const app = express();
 
describe('GET /all', function() {
    it('test all endpoint', function(done) {
      request(app)
        .get('/all')
        .expect(404, done);
    });
});