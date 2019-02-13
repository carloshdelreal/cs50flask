
document.addEventListener('DOMContentLoaded', () => {

    // //Add form-control class to all the forms, styling stuff
    // document.querySelectorAll(".input-group>input").forEach( 
    //     (element) => element.classList.add("form-control") 
    // );

    ///form control forms
    document.querySelectorAll("input[type=text]").forEach((element) => { element.classList.add("form-control")})
    document.querySelectorAll("input[type=email]").forEach((element) => { element.classList.add("form-control")})
    document.querySelectorAll("input[type=password]").forEach((element) => { element.classList.add("form-control")})
    document.getElementById("id_itemGroup").classList.add("form-control")
    document.getElementById("id_item").classList.add("form-control")

    $( document ).ready(function() {
        $('#id_extras').selectpicker();
    });
});
