document.addEventListener('DOMContentLoaded', function() {

    // Get the chatername from the localstorage
    if (!localStorage.getItem('chatername')){
        $("#myModal").modal({
            backdrop: 'static',
            keyboard: false
        })
    }
    if (localStorage.getItem('chatchannel')){
        sval = localStorage.getItem('chatchannel')
        document.querySelector('#schannels').value = sval;
        getChatMesssages();
    }

    document.querySelector('#idspan').innerHTML = localStorage.getItem('chatername')
    
    // By default, chatername button and msg button are disabled
    document.querySelector('#submitChaterName').disabled = true;
    document.querySelector('#msgbtn').disabled = true;
    document.querySelector('#newchbtn').disabled = true;
    document.querySelector('#msg-delete-btn').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#chaterName').onkeyup = (e) => {
        if (document.querySelector('#chaterName').value.length > 0){
            document.querySelector('#submitChaterName').disabled = false;
            if (13 == e.keyCode){
                document.querySelector('#submitChaterName').click()
            }
        }
        else
            document.querySelector('#submitChaterName').disabled = true;
    };
    // Enable button only if there is text in the input field
    document.querySelector('#msg').onkeyup = (e) => {
        if (document.querySelector('#msg').value.length > 0 && document.querySelector('#schannels').value != "none"){

            document.querySelector('#msgbtn').disabled = false;
            if (13 == e.keyCode){
                document.querySelector('#msgbtn').click()
            }
        }
        else
            document.querySelector('#msgbtn').disabled = true;
    };


    // Enable button only if there is text in the input field channel
    document.querySelector('#newchannel').onkeyup = (e) => {
        if (document.querySelector('#newchannel').value.length > 0){
            document.querySelector('#newchbtn').disabled = false;
            if (13 == e.keyCode){
                document.querySelector('#newchbtn').click()
            }
        }
        else
            document.querySelector('#newchbtn').disabled = true;
    };

    //Get the chatername
    document.querySelector('#submitChaterName').onclick = registerChater; 

    //Get the chatmessages
    document.querySelector('#schannels').onchange = getChatMesssages;

    //Delete selected messages
    document.querySelector("#msg-delete-btn").onclick = () =>{
        document.querySelectorAll(".msg-selected").forEach( element => {
            element.style.animationPlayState = 'running';
            element.addEventListener('animationend', (element) => {
                const msgid = element.srcElement.firstElementChild.innerText;
                element.srcElement.remove();
                //when a message is deleted
                data = {"channel": localStorage.getItem("chatchannel"), 
                        "msgid": msgid }
                socket.emit('msg delete', data );
                
            });
        });
    };

    // Log out
    document.querySelector("#logoutbtn").onclick = () =>{
        localStorage.removeItem('chatername')
    }

    //--------------------------------------------------------
    // connect to the websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        //--------------------------------------------------------
        // Create New Channel
        document.querySelector("#newchbtn").onclick = () =>{
            channel = document.querySelector("#newchannel").value;
            socket.emit('new channel', { 'channel': channel });
            // Clear input fiel and disable button again
            document.querySelector("#newchannel").value = "";
            document.querySelector("#newchbtn").disabled =true;
        }

        // emit a "new msg" event
        document.querySelector('#msgbtn').onclick = () => {
            const msg = document.querySelector('#msg').value;
            const chan = document.querySelector('#schannels').value;
            t = new Date();
            const timestamp = t.toTimeString().slice(0,8);
            socket.emit('new msg', {'chaterName': localStorage.getItem('chatername'),
                                    'msg': msg,
                                    "channel": chan,
                                    "timestamp": timestamp });
            
            // Clear input field and disable button again
            document.querySelector('#msg').value = '';
            document.querySelector('#msgbtn').disabled = true;
        }
    });

    // When a new channel is created
    socket.on('newChannel', data => {
        //show the channels in the selector
        const selec = document.createElement("option")
        selec.value = data['channel']
        selec.innerHTML = data['channel']
        document.querySelector("#schannels").append(selec)
        //show the channels in the table
        const tabl = document.createElement('tr')
        tabl.innerHTML = "<td>" + data['channel'] + "</td>"
        document.querySelector('tbody').append(tabl);
    });

    // When a new message is added
    socket.on('msg', data => addMessage(data));

});

function registerChater() {
    chaterName = document.querySelector('#chaterName').value;
    localStorage.setItem('chatername',chaterName);
    document.querySelector('#idspan').innerHTML = localStorage.getItem('chatername');
    $("#myModal").modal('hide');
}


 
function getChatMesssages(){
    svalue = document.querySelector('#schannels').value;
    localStorage.setItem('chatchannel', svalue);

    // Clean the values
    document.querySelector('#msgs').innerHTML = "";

    // Initialize new request
    const request = new XMLHttpRequest();
    request.open('POST', '/chatmsgs');

    request.onload = () => {

        const data = JSON.parse(request.responseText);

        if (data.success) {
            data.msgs.forEach(element => {
                
                addMessage({ "chaterName": element[0], 
                            "msg": element[1],
                            "timestamp": element[2],
                            "msgIndex": element[3]
                         })
            
        });
        }
        else{
            console.log("no messages or there was an error");
        }
    }

    // Add data to send with request
    const data = new FormData();
    
    data.append('channel', svalue);

    request.send(data);
    return false;
}

const template = Handlebars.compile(document.getElementById("entry-template").innerHTML);

function addMessage(data){
    //Delete the no msg
    nomsgelm = document.querySelector("#nomsg")
    if (nomsgelm)
        nomsgelm.parentElement.removeChild(nomsgelm)

        
        const msgcontent = template(data);
        const msgcontainer = document.createElement('div')
        msgcontainer.className = 'msg-entry'
        if (localStorage.getItem('chatername') === data["chaterName"]){
            msgcontainer.className = 'msg-local';
        }
        else{
            msgcontainer.className = 'msg-remote';
        }
        msgcontainer.innerHTML = msgcontent
        msgcontainer.onclick = selectedMsg;
    //append the messages to the row
    document.querySelector('#msgs').prepend(msgcontainer);
}

function selectedMsg(){
    if ( this.classList.contains("msg-selected")){
        this.classList.remove("msg-selected")
    }else if (this.children[1].innerText === localStorage.getItem('chatername')){
        this.classList.add("msg-selected")
    }

    //delete msgs button enable or disable
    if( document.querySelector('.msg-selected')){
        document.querySelector("#msg-delete-btn").disabled = false;
    }else{
        document.querySelector("#msg-delete-btn").disabled = true;
    }
}