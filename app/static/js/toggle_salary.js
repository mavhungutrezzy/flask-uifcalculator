document.addEventListener("DOMContentLoaded", function () {
  const sameSalaryCheck = document.getElementById("sameSalaryCheck");
  const singleSalaryGroup = document.getElementById("singleSalaryGroup");
  const multiSalaryGroup = document.getElementById("multiSalaryGroup");
  const singleSalaryInput = document.getElementById("singleSalary");
  const salaryFields = multiSalaryGroup.querySelectorAll("input");

  function toggleSalaryInputs() {
    if (sameSalaryCheck.checked) {
      singleSalaryGroup.style.display = "";
      singleSalaryInput.required = true;
      multiSalaryGroup.style.display = "none";
      salaryFields.forEach((field) => {
        field.required = false;
      });
    } else {
      singleSalaryGroup.style.display = "none";
      singleSalaryInput.required = false;
      multiSalaryGroup.style.display = "";
      salaryFields.forEach((field) => {
        field.required = true;
      });
    }
  }

  sameSalaryCheck.addEventListener("change", toggleSalaryInputs);
  toggleSalaryInputs();

  if (window.jQuery) {
    if (typeof $.fn.datePicker !== "undefined") {
      $('[data-select="datepicker"]').datePicker();
    } else {
      console.error("jQuery datePicker plugin not found.");
    }
  }
});