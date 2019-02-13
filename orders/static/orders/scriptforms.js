
document.addEventListener('DOMContentLoaded', () => {

    // //Add form-control class to all the forms, styling stuff
    // document.querySelectorAll(".input-group>input").forEach( 
    //     (element) => element.classList.add("form-control") 
    // );

    ///form control forms
    document.querySelectorAll("input[type=text]").forEach((element) => { element.classList.add("form-control")})
    document.querySelectorAll("input[type=email]").forEach((element) => { element.classList.add("form-control")})
    document.querySelectorAll("input[type=password]").forEach((element) => { element.classList.add("form-control")})
    document.querySelectorAll("input[type=number]").forEach((element) => { element.classList.add("form-control")})
    //document.querySelectorAll("select").forEach((element) => { element.classList.add("form-control")})
    

});
