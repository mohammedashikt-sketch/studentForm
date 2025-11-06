app.controller('FormController', function($scope, apiService, dropdownData) {
  // 🔹 Initialize variables
  $scope.activeCard = null;
  $scope.today = new Date().toISOString().split('T')[0];
  $scope.student = {};               // Personal + Address
  $scope.academic10 = { subjects: {} }; // 10th details
  $scope.academic12 = {};            // 12th details
  $scope.qualified = {};             // Qualified exam
  $scope.branchPrefs = {};           // Branch preferences
  $scope.extra_curricular = "";
  $scope.why_ssn = "";
  $scope.dropdown = dropdownData;

  // 🔹 Toggle collapsible card
  $scope.toggleCard = function(card) {
    $scope.activeCard = ($scope.activeCard === card) ? null : card;
  };

  // 🔹 Country code dropdown label
  $scope.codeDisplay = function(code) {
    if ($scope.student && $scope.student.country_code === code.code) {
      return code.code;
    }
    return code.country + ' (' + code.code + ')';
  };

  // ===========================================================
  // 🔹 FORM SUBMISSION (All Sections Together)
  // ===========================================================
  $scope.submitForm = function(isValid) {
    if (!isValid) {
      alert("Please check all required fields before submitting.");
      return;
    }

    // ✅ Handle custom “Other” dropdown values
    const otherFields = [
      'community', 'religion', 'mother_tongue', 'nationality',
      'state', 'district', 'city', 'country_of_residency'
    ];
    otherFields.forEach(field => {
      const customField = field + '_custom';
      if ($scope.student[field] === 'Other' && $scope.student[customField]) {
        $scope.student[field] = $scope.student[customField];
      }
    });

    // ✅ Format DOB (YYYY-MM-DD)
    if ($scope.student.dob) {
      $scope.student.dob = new Date($scope.student.dob).toISOString().split('T')[0];
    }

    // ✅ Merge Address
    if ($scope.student.fullAddress && $scope.student.pincode) {
      $scope.student.address = {
        fullAddress: $scope.student.fullAddress,
        pincode: $scope.student.pincode
      };
    }

    // ===========================================================
    // 🎓 Merge Academic Data into single JSON structure
    // ===========================================================
    const academic = {
      // 10th details
      tenth_school: $scope.academic10.schoolName,
      tenth_board: $scope.academic10.board,
      tenth_roll_number: $scope.academic10.rollNumber,
      tenth_year: $scope.academic10.year,
      tenth_percentage: $scope.academic10.percentage,

      // 10th subjects
      tenth_math_max: $scope.academic10.subjects?.math?.max,
      tenth_math_obt: $scope.academic10.subjects?.math?.obt,
      tenth_math_perc: $scope.academic10.subjects?.math?.perc,
      tenth_sci_max: $scope.academic10.subjects?.science?.max,
      tenth_sci_obt: $scope.academic10.subjects?.science?.obt,
      tenth_sci_perc: $scope.academic10.subjects?.science?.perc,

      // 12th details
      twelfth_school: $scope.academic12.schoolName,
      twelfth_board: $scope.academic12.board,
      twelfth_roll_number: $scope.academic12.rollNumber,
      twelfth_year: $scope.academic12.passingYear,
      twelfth_school_code: $scope.academic12.schoolCode,
      twelfth_centre_code: $scope.academic12.centreCode,
      admit_card: $scope.academic12.admitCard,
      cutoff: $scope.academic12.cutoff,

      // Qualified exam marks
      math_marks: $scope.qualified.math?.obtained,
      math_perc: $scope.qualified.math?.perc,
      math_attempts: $scope.qualified.math?.attempts,
      math_month_year: $scope.qualified.math?.monthYear,

      physics_marks: $scope.qualified.physics?.obtained,
      physics_perc: $scope.qualified.physics?.perc,
      physics_attempts: $scope.qualified.physics?.attempts,
      physics_month_year: $scope.qualified.physics?.monthYear,

      chemistry_marks: $scope.qualified.chemistry?.obtained,
      chemistry_perc: $scope.qualified.chemistry?.perc,
      chemistry_attempts: $scope.qualified.chemistry?.attempts,
      chemistry_month_year: $scope.qualified.chemistry?.monthYear,

      // Branch preferences
      branch_pref_1: $scope.branchPrefs.pref1,
      branch_pref_2: $scope.branchPrefs.pref2,
      branch_pref_3: $scope.branchPrefs.pref3,
      branch_pref_4: $scope.branchPrefs.pref4,
      branch_pref_5: $scope.branchPrefs.pref5,
      branch_pref_6: $scope.branchPrefs.pref6,

      // Additional particulars
      extra_curricular: $scope.extra_curricular,
      why_ssn: $scope.why_ssn
    };

    // Attach to student
    $scope.student.academic = academic;

    // ===========================================================
    // 🔹 Submit to API (All in one)
    // ===========================================================
    apiService.saveStudent($scope.student)
      .then(function(res) {
        alert(res.data.message || "Student added successfully!");

        // ✅ Reset forms after submit
        /*$scope.student = {};
        $scope.academic10 = { subjects: {} };
        $scope.academic12 = {};
        $scope.qualified = {};
        $scope.branchPrefs = {};
        $scope.extra_curricular = "";
        $scope.why_ssn = "";*/

        if ($scope.studentForm) {
          $scope.studentForm.$setPristine();
          $scope.studentForm.$setUntouched();
        }
        $scope.activeCard = null;
      })
      .catch(function(err) {
        alert("Error: " + (err.data?.error || "Server error"));
      });
  };
});
