// js/services/apiService.js
app.service('apiService', function($http) {
  const BASE_URL = 'http://127.0.0.1:5000/api';

  this.saveStudent = function(studentData) {
    return $http.post(`${BASE_URL}/students`, studentData);
  };

  this.getStudents = function() {
    return $http.get(`${BASE_URL}/students`);
  };
});
