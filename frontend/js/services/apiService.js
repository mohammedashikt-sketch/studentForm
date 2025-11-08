// js/services/apiService.js
app.service('apiService', function($http) {
  const BASE_URL = 'http://127.0.0.1:5000/api';

  // ✅ Save student + upload files
  this.saveStudent = function(studentData, files) {
    const formData = new FormData();

    // Convert JS object to JSON string
    formData.append('student_data', JSON.stringify(studentData));

    // Append all file fields if present
    if (files) {
      for (const key in files) {
        if (files[key]) {
          formData.append(key, files[key]);
        }
      }
    }

    // Send multipart/form-data request
    return $http.post(`${BASE_URL}/students/upload`, formData, {
      transformRequest: angular.identity,
      headers: { 'Content-Type': undefined }
    });
  };

  // ✅ Fetch all students
  this.getStudents = function() {
    return $http.get(`${BASE_URL}/students`);
  };
});
