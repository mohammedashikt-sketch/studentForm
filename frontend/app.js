/*var app = angular.module('studentApp', []);

app.controller('FormController', function($scope, $http) {
    $scope.student = {};
    $scope.students = [];

    $scope.loadStudents = function() {
        $http.get('http://127.0.0.1:5000/api/students').then(function(res) {
            $scope.students = res.data;
        });
    };

    $scope.submitForm = function(isValid) {
        if (!isValid) {
            alert("Please correct the errors before submitting.");
            return;
        }

        // Convert DOB to correct date format
        const dob = new Date($scope.student.dob).toISOString().split('T')[0];
        $scope.student.dob = dob;

        $http.post('http://127.0.0.1:5000/api/students', $scope.student)
        .then(function(res) {
            alert(res.data.message);
            $scope.student = {};
            $scope.studentForm.$setPristine();
            $scope.studentForm.$setUntouched();
            $scope.loadStudents();
        }, function(err) {
            alert("Error: " + err.data.error);
        });
    };

    $scope.loadStudents();
});
    */