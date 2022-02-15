const circleRadius = 20
const textsize = 15
var user_id = "jisoo"
var set_id = ""
var imageObj = new Image();
var c = document.getElementById("myCanvas");
var context = c.getContext("2d");
var canvas = new fabric.Canvas('myCanvas');

function drawBullets(image,canvas){

    canvas.clear();
    canvas.setWidth(image.width);
    canvas.setHeight(image.height);
    var imgInstance = new fabric.Image(image, {
      });
    imgInstance.set('selectable', false);
    canvas.add(imgInstance);
    if (image.bullets){
        for (var i = 0; i < image.bullets.length; i++) {
            console.log(image.bullets[i]);
            var bullet = image.bullets[i];
            var stroke = "#33FF33"
            if (bullet.isnew){
                stroke = "#FEFF3E"
            }
            var circlePatrol = new fabric.Circle({
                top: toDrawPoint(bullet.yposition),
                left: toDrawPoint(bullet.xposition),
                radius: circleRadius,
                stroke: stroke,
                strokeWidth: 2,
                fill: 'rgba(0,0,0,0)'
              });
            canvas.add(circlePatrol);

        }       
    }

}


function drawPaths(image,canvas){
    if (image.bullets){
        for (var i = 0; i < image.bullets.length; i++) {
            var max = 0
            var mainbullet1;
            var mainbullet2;
            for(var j = 0; j<image.bullets.length;j++){
                var bullet1 = image.bullets[i];
                var bullet2 = image.bullets[j];
                var len = Math.ceil(((bullet1.xposition-bullet2.xposition)**2+
                (bullet1.yposition-bullet2.yposition)**2)**0.5)
                if (len>max){
                    max = len
                    mainbullet1 = bullet1
                    mainbullet2 = bullet2
                }
            }

            if (typeof mainbullet2 !== 'undefined' && max!= 0){
                var stroke = "#33FF33"
                if (mainbullet1.isnew || mainbullet2.isnew){
                    stroke = "#FEFF3E"
                }
                var line = new fabric.Line([mainbullet1.xposition, mainbullet1.yposition, mainbullet2.xposition, mainbullet2.yposition], {
                    stroke: 'red'
                });
                line.set('selectable', false);
                canvas.add(line);
                var text = new fabric.Text(
                    max.toString()
                    , { 
                    left: (mainbullet1.xposition+mainbullet2.xposition)/2, 
                    top: (mainbullet1.yposition+mainbullet2.yposition)/2,
                    fontSize: textsize,
                    stroke:stroke
                });
                text.set('selectable', false);
                canvas.add(text);
            }
        }       
    }

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
                imageObj.bullets = event.bullets
                imageObj.src = "data:image/jpg;base64, "+ event.image
                
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
        drawPaths(this,canvas)
        if(typeof this.bullets !== "undefined"){
            console.log(this.bullets.length)
        }
        
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