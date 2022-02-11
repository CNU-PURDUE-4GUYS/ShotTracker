var user_id = "jisoo"
var set_id = ""
var imageObj = new Image();



function clientInit(mybutton, websocket) {
    mybutton.addEventListener("click",({target})=>{
        const event = {
            command: "init",
            user_id: user_id,
         };
         websocket.send(JSON.stringify(event));
    })
    }


function newSet(mybutton, websocket) {
    mybutton.addEventListener("click",({target})=>{
        const event = {
            command: "newSetFromCli",
            user_id: user_id,
            };
        websocket.send(JSON.stringify(event));
    })

}

function takeRef(mybutton, websocket) {
    mybutton.addEventListener("click",({target})=>{
        const event = {
            command: "takeRef",
            user_id: user_id,
            set_id: set_id
            };
        websocket.send(JSON.stringify(event));
    })

}
function takePhoto(mybutton, websocket) {
    mybutton.addEventListener("click",({target})=>{
        const event = {
            command: "takePhoto",
            user_id: user_id,
            set_id: set_id
            };
        websocket.send(JSON.stringify(event));
    })

}
function listenToWebSocket(websocket){
    websocket.addEventListener("message",({data})=>{
        const event = JSON.parse(data);
        switch(event.command){
            case "newSet":
                set_id = event.set_id;
                console.log("new set id detected"+set_id)
                break;
            case "refer":

                document.getElementById("img").src ="data:image/jpg;base64, "+ event.image
                imageObj.src = "data:image/jpg;base64, "+ event.image
            case "warp":
                document.getElementById("img").src ="data:image/jpg;base64, "+ event.image
            default:
                console.log(event)
        }
    })
}


window.addEventListener("DOMContentLoaded", () => {
    var c = document.getElementById("myCanvas");
    var context = c.getContext("2d");

    imageObj.onload = function() { 
        context.drawImage(imageObj, 0,0);  
      }
    console.log("before web")
    
     // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8888/");
    listenToWebSocket(websocket)
    clientInit(document.querySelector(".init"),websocket)
    newSet(document.querySelector(".newset"),websocket)
    takeRef(document.querySelector(".refer"),websocket)
    takePhoto(document.querySelector(".photo"),websocket)
    console.log("after web")
    });