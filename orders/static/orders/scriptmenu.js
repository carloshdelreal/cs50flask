var order;
document.addEventListener('DOMContentLoaded', () => {

    if (localStorage.getItem('order')){
        order = JSON.parse(localStorage.getItem('order'));
        if (!(JSON.stringify(order) === JSON.stringify({}) )){
            for (var key in order){
                var i = 1;
                if (i > 0){
                    updatechar(key, order[key]);
                    i--;
                }
                document.getElementById(key).value = order[key];
            }
        }
        
    }else{
        order = {};
    }

    //Add form-control class to all the forms, styling stuff, spinner
    document.querySelectorAll(".input-group>input").forEach( 
        (element) => element.classList.add("form-control") 
    );

    // Add Event listener to the spinner
    document.querySelectorAll('.spinner .btn:first-of-type').forEach( 
        (element) => element.addEventListener ('click', (e)=> {
            inputElement = e.srcElement.parentElement.parentElement.previousElementSibling
            if (inputElement){
                let itemNumber = parseInt(inputElement.value);
                let identifier = parseInt(inputElement.id)
                inputElement.value = itemNumber + 1;
                updatechar(identifier, itemNumber+1);
            }
        })
    );

    document.querySelectorAll('.spinner .btn:last-of-type').forEach( 
        (element) => element.addEventListener ('click', (e)=> {
            let itemNumber = parseInt(e.srcElement.parentElement.parentElement.previousElementSibling.value);
            if (itemNumber >= 1){
                inputElement = e.srcElement.parentElement.parentElement.previousElementSibling
                if (inputElement){
                    let itemNumber = parseInt(inputElement.value);
                    let identifier = parseInt(inputElement.id)
                    inputElement.value = itemNumber - 1;
                    updatechar(identifier, itemNumber - 1);
                }
            }
        })
    );
    
    
    function updatechar(id, value){      
        order[id] = value;
        
        var count = 0;
        for (var key in order){
            if (order[key] == 0){
                delete order[key]
                document.getElementById(key).parentElement.parentElement.parentElement.classList.remove("table-warning")
            }else{
                count = count + order[key];
                document.getElementById(key).parentElement.parentElement.parentElement.classList.add("table-warning")
            }
        }
        localStorage.setItem("order", JSON.stringify(order))
        if(count > 0){
            document.querySelector("span.num").innerText = count;
            document.querySelector(".navbar-right").children[1].style.display = ""
            document.getElementById("confirmOrder").style.display = ""
        }else{
            document.querySelector(".navbar-right").children[1].style.display = "none"
            document.getElementById("confirmOrder").style.display = "none"
        }
        document.getElementById("id_orderString").value = JSON.stringify(order)
    }

    document.getElementById("confirmOrder").addEventListener("click", chargeItems);
    //document.getElementById("cart").addEventListener("click", chargeItems);

    function chargeItems (){
        document.querySelectorAll("input[type=submit]")[0].click()
    }
});



