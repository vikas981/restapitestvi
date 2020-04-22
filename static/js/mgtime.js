window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 2000);

function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
};
 $("#file-picker").change(function(){

        var input = document.getElementById('file-picker');

        for (var i=0; i<input.files.length; i++)
        {
        //koala.jpg, koala.JPG substring(index) lastIndexOf('a') koala.1.jpg
            var ext= input.files[i].name.substring(input.files[i].name.lastIndexOf('.')+1).toLowerCase()

            if ((ext == 'jpg') || (ext == 'png'))
            {
                $("#msg").text("Files are supported")
            }
            else
            {
                $("#msg").text("Files are NOT supported")
                document.getElementById("file-picker").value ="";
            }

        }


    } );