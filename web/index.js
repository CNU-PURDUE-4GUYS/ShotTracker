const circleRadius = 20
var user_id = "jisoo"
var set_id = ""
var imageObj = new Image();
var c = document.getElementById("myCanvas");
var context = c.getContext("2d");
var canvas = new fabric.Canvas('myCanvas');

function drawBullets(image,canvas){
    canvas.clear();
    var imgInstance = new fabric.Image(image, {
      });
    canvas.add(imgInstance);
    if (image.bullets){
        for (var i = 0; i < image.bullets.length; i++) {
            console.log(image.bullets[i]);
            var bullet = image.bullets[i];
            var circlePatrol = new fabric.Circle({
                top: toDrawPoint(bullet.yposition),
                left: toDrawPoint(bullet.xposition),
                radius: circleRadius,
                stroke: "#33FF33",
                strokeWidth: circleRadius/5,
                fill: 'rgba(0,0,0,0)'
              });
            canvas.add(circlePatrol);

        }       
    }

    console.log(image.width,image.height)
}

function toDrawPoint(point){
    return point-circleRadius
}
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
                imageObj.src = "data:image/jpg;base64, "+ event.image
                break;
            case "warp":
                imageObj.src = "data:image/jpg;base64, "+ event.image
                imageObj.bullets = event.bullets
                console.log(event)
                break;
            default:
                console.log(event)
        }
    })
}


window.addEventListener("DOMContentLoaded", () => {


    imageObj.onload = function() { 
        drawBullets(this,canvas)
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