
document.addEventListener('DOMContentLoaded', () => {

    //Add form-control class to all the forms, styling stuff
    document.querySelectorAll('input.form-control').forEach( 
        (element) => element.addEventListener('input', function (evt) {
            if (evt.srcElement.value >= 0){
                updateItem(evt.srcElement)
            }else{
                evt.srcElement.value = 0;
            }
            updateCart()
        })
    );

    document.querySelectorAll('input.form-control').forEach(
        (element) => updateItem(element)
    );
    updateCart();
    
    function updateItem(element){
        quantity = element.value
        price = element.parentElement.nextElementSibling.nextElementSibling.innerText
        priceDisplay = parseFloat(element.value) * parseFloat(element.parentElement.nextElementSibling.nextElementSibling.innerText)
        element.parentElement.nextElementSibling.innerText = "$ " + priceDisplay.toFixed(2)

    }
    function updateCart(){
        var total = 0.0
        document.querySelectorAll('input.form-control').forEach(
            (element) => {
                total = total + parseFloat(element.parentElement.nextElementSibling.innerText.slice(2))
            }
        );
        document.querySelector('tr:last-child>td:last-child').innerText = "$ " + total.toFixed(2)
    }


    $( document ).ready(function() {
        $('#id_extras').selectpicker();
    });
});
