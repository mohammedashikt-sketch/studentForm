app.controller('FormController', function($scope, apiService, dropdownData, $http) {
  // ===========================================================
  // 🔹 Initialize variables
  // ===========================================================
  $scope.activeCard = null;
  $scope.today = new Date().toISOString().split('T')[0];
  $scope.student = {};
  $scope.academic10 = { subjects: {} };
  $scope.academic12 = {};
  $scope.qualified = {};
  $scope.branchPrefs = {};
  $scope.extra_curricular = "";
  $scope.why_ssn = "";
  $scope.dropdown = dropdownData;

  // ===========================================================
  // 🔹 Parent Section Variables
  // ===========================================================
  $scope.familyBlocks = [{
    father: {},
    mother: {},
    guardian: {},
    guardian_enabled: 'No',
    student_id: ''
  }];

  // ===========================================================
  // 🔹 Collapsible card toggle
  // ===========================================================
  $scope.toggleCard = function(card) {
    $scope.activeCard = ($scope.activeCard === card) ? null : card;
  };

  // ===========================================================
  // 🔹 Country code dropdown label
  // ===========================================================
  $scope.codeDisplay = function(code) {
    if ($scope.student && $scope.student.country_code === code.code) {
      return code.code;
    }
    return code.country + ' (' + code.code + ')';
  };

  // ===========================================================
  // 🔹 FILE UPLOAD SECTION (merged from UploadController)
  // ===========================================================
  $scope.errors = {};
  $scope.message = "";
  $scope.isSubmitting = false;

  $scope.uploadedFiles = {
    photo: false,
    signature: false,
    community: false,
    marksheet_10th: false,
    marksheet_12th: false,
    marksheet_diploma: false,
    marksheet_graduation: false,
    passport: false,
    admitcard: false
  };

  // File validation and preview
  $scope.validateFile = function(file, field) {
    if (!file) {
      $scope.uploadedFiles[field] = false;
      $scope[field + 'Preview'] = null;
      $scope[field] = null;
      return;
    }

    const maxSize = 2 * 1024 * 1024; // 2MB
    const ext = file.name.split('.').pop().toLowerCase();
    const allowedExt = ['jpeg','jpg','png','pdf'];

    if (file.size > maxSize) {
      $scope.errors[field] = "File too large (max 2MB)";
      $scope.uploadedFiles[field] = false;
      return;
    }

    if (!allowedExt.includes(ext)) {
      $scope.errors[field] = "Invalid file type";
      $scope.uploadedFiles[field] = false;
      return;
    }

    $scope.errors[field] = null;
    $scope.uploadedFiles[field] = true;

    $scope[field] = file; 

    const reader = new FileReader();
    reader.onload = function(e) {
      $scope.$apply(() => {
        $scope[field + 'Preview'] = e.target.result;
      });
    };
    reader.readAsDataURL(file);
  };

  $scope.isImage = function(file) {
    if (!file || !file.name) return false;
    const ext = file.name.split('.').pop().toLowerCase();
    return ['jpeg','jpg','png'].includes(ext);
  };

  $scope.allFilesUploaded = function() {
    return Object.values($scope.uploadedFiles).every(v => v);
  };

  $scope.openPDF = function(pdfUrl, fileName) {
    if (!pdfUrl) {
      alert("No PDF available to preview!");
      return;
    }
    const pdfWindow = window.open("", "_blank", "width=900,height=700");
    pdfWindow.document.write(`
      <html><head><title>${fileName || 'PDF Preview'}</title></head>
      <body style="margin:0;"><embed src="${pdfUrl}" type="application/pdf" width="100%" height="100%"></body>
      </html>
    `);
    pdfWindow.document.close();
  };

  // ===========================================================
  // 🔹 FORM SUBMISSION (All Sections + Upload Together)
  // ===========================================================
  $scope.submitForm = function(isValid) {
  if (!isValid) {
    alert("Please check all required fields before submitting.");
    return;
  }
  console.log('familyBlocks[0] =', JSON.stringify($scope.familyBlocks[0], null, 2));
  console.log('parentForm (exists?) =', !!$scope.parentForm, $scope.parentForm);

  // ✅ Check Parent details
  const parent = $scope.familyBlocks[0];
  $scope.student.father_name = parent.father.name;
  $scope.student.father_mobile = parent.father.mobile;
  $scope.student.father_email = parent.father.email;
  $scope.student.father_occupation = parent.father.occupation;
  $scope.student.father_annual_income = parent.father.annual_income;
  $scope.student.father_title = parent.father.title;

// Repeat for mother / guardian
  $scope.student.mother_name = parent.mother.name;
  $scope.student.mother_mobile = parent.mother.mobile;
  $scope.student.mother_email = parent.mother.email;
  $scope.student.mother_occupation = parent.mother.occupation;
  $scope.student.mother_annual_income = parent.mother.annual_income;  
  $scope.student.mother_title = parent.mother.title;

  if(parent.guardian_enabled === 'Yes') {
    $scope.student.has_guardian = true;
    $scope.student.guardian_name = parent.guardian.name;
    $scope.student.guardian_mobile = parent.guardian.mobile;
    $scope.student.guardian_email = parent.guardian.email;
    $scope.student.guardian_occupation = parent.guardian.occupation;
    $scope.student.guardian_designation = parent.guardian.designation;
    $scope.student.guardian_title = parent.guardian.title;
  } else {
      $scope.student.has_guardian = false;
  }
  // Attach parentData as a flat object to student_data
  
  if (!parent.father.title || !parent.father.name || !parent.father.mobile || !parent.father.email || !parent.father.occupation || !parent.father.annual_income) {
    alert("Please complete all mandatory Father's details before submitting.");
    return;
  }
  if (!parent.mother.title || !parent.mother.name || !parent.mother.mobile) {
    alert("Please complete all mandatory Mother's details before submitting.");
    return;
  }
  if (parent.guardian_enabled === 'Yes' && (!parent.guardian || !parent.guardian.name || !parent.guardian.mobile)) {
    alert("Please complete all Guardian's details before submitting.");
    return;
  }
  

   // ✅ Check terms checkbox
  if (!$scope.termsAccepted) {
    alert("You must accept the terms to submit the form.");
    return;
  }

  const requiredFiles = ['photo', 'signature', 'community', 'marksheet_10th', 'marksheet_12th', 'marksheet_diploma','marksheet_graduation','passport','admitcard'];
  for (const file of requiredFiles) {
    if (!$scope.uploadedFiles[file]) {
      alert(`Please upload the required file: ${file.replace(/_/g, ' ')}`);
      return;
    }
  }

  // ===========================================================
  // 🔹 Handle “Other” dropdown options
  // ===========================================================
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

  // ===========================================================
  // 🔹 Format DOB
  // ===========================================================
  if ($scope.student.dob) {
    $scope.student.dob = new Date($scope.student.dob).toISOString().split('T')[0];
  }

  // ===========================================================
  // 🔹 Address
  // ===========================================================
  if ($scope.student.fullAddress && $scope.student.pincode) {
    $scope.student.address = {
      fullAddress: $scope.student.fullAddress,
      pincode: $scope.student.pincode
    };
  }

  // ===========================================================
  // 🔹 Academic Data Merge
  // ===========================================================
  const academic = {
    tenth_school: $scope.academic10.schoolName,
    tenth_board: $scope.academic10.board,
    tenth_roll_number: $scope.academic10.rollNumber,
    tenth_year: $scope.academic10.year,
    tenth_percentage: $scope.academic10.percentage,
    tenth_math_max: $scope.academic10.subjects?.math?.max,
    tenth_math_obt: $scope.academic10.subjects?.math?.obt,
    tenth_math_perc: $scope.academic10.subjects?.math?.perc,
    tenth_sci_max: $scope.academic10.subjects?.science?.max,
    tenth_sci_obt: $scope.academic10.subjects?.science?.obt,
    tenth_sci_perc: $scope.academic10.subjects?.science?.perc,
    twelfth_school: $scope.academic12.schoolName,
    twelfth_board: $scope.academic12.board,
    twelfth_roll_number: $scope.academic12.rollNumber,
    twelfth_year: $scope.academic12.passingYear,
    twelfth_school_code: $scope.academic12.schoolCode,
    twelfth_centre_code: $scope.academic12.centreCode,
    admit_card: $scope.academic12.admitCard,
    cutoff: $scope.academic12.cutoff,
    math_marks: $scope.qualified.math?.obtained,
    physics_marks: $scope.qualified.physics?.obtained,
    chemistry_marks: $scope.qualified.chemistry?.obtained,
    branch_pref_1: $scope.branchPrefs.pref1,
    branch_pref_2: $scope.branchPrefs.pref2,
    extra_curricular: $scope.extra_curricular,
    why_ssn: $scope.why_ssn
  };
  $scope.student.academic = academic;

  $scope.student.parents = $scope.familyBlocks;

  // ===========================================================
  // 🔹 Collect Uploaded Files
  // ===========================================================
  const uploadFiles = {
    photo: $scope.photo,
    signature: $scope.signature,
    community: $scope.community,
    marksheet_10th: $scope.marksheet_10th,
    marksheet_12th: $scope.marksheet_12th,
    marksheet_diploma: $scope.marksheet_diploma,
    marksheet_graduation: $scope.marksheet_graduation,
    passport: $scope.passport,
    admitcard: $scope.admitcard
  };

  $scope.student.applicant_name = $scope.applicant_name;
  $scope.student.parent_name = $scope.parent_name;
  $scope.student.date = $scope.date; // optional


  // ===========================================================
  // 🔹 Send Data + Files to Backend
  // ===========================================================
  $scope.isSubmitting = true;

  apiService.saveStudent($scope.student, uploadFiles)
    .then(function(response) {
      alert(response.data.message || "Student uploaded successfully!");
      console.log("✅ Upload Success:", response.data);

      // Reset form
      $scope.student = {};
      $scope.familyBlocks = [{ father: {}, mother: {}, guardian: {}, guardian_enabled: 'No' }];
      $scope.academic10 = { subjects: {} };
      $scope.academic12 = {};
      $scope.qualified = {};
      $scope.branchPrefs = {};
      $scope.extra_curricular = "";
      $scope.why_ssn = "";
      $scope.isSubmitting = false;

      if ($scope.studentForm) {
        $scope.studentForm.$setPristine();
        $scope.studentForm.$setUntouched();
      }
    })
    .catch(function(error) {
      alert("❌ Upload failed: " + (error.data?.error || "Server error"));
      console.error(error);
      $scope.isSubmitting = false;
    });
  };
});
