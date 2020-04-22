document.addEventListener('DOMContentLoaded', function () {
   var input = document.getElementById('comp_select');
   if (localStorage['comp_select']) { // if job is set
       input.value = localStorage['comp_select']; // set the value
   }
   input.onchange = function () {
        localStorage['comp_select'] = this.value; // change localStorage on change
    }
});

function submitForm(){
  document.getElementById('myform').submit();
};