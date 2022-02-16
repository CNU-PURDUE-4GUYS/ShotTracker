var circleRadius = 20
var textsize = 15
var user_id = "jisoo"
var set_id = ""
var imageObj = new Image();
var referObj = new Image();
const defaultwidth = 640
const defaultheight = 480
// var c = document.getElementById("myCanvas");
// var referCanvas = document.getElementById("myReferCanvas");
// var context = c.getContext("2d");
// var referContext = referCanvas.getContext("2d");
var canvas = new fabric.Canvas('myCanvas');
canvas.setWidth(defaultwidth);
canvas.setHeight(defaultheight);
var referCanvas = new fabric.Canvas('myReferCanvas');
referCanvas.setWidth(defaultwidth);
referCanvas.setHeight(defaultheight);


function setuserid(){
    user_id = document.getElementById("fname").value
}

function toLoginPage(){
    document.getElementById("loginpage").style.display = "block"
    document.getElementById("newsetpage").style.display = "none"
    document.getElementById("referencepage").style.display = "none"
    document.getElementById("detectpage").style.display = "none"
    document.getElementById("historypage").style.display = "none"
}

function toNewSetPage(){
    
    document.getElementById("loginpage").style.display = "none"
    document.getElementById("newsetpage").style.display = "block"
    document.getElementById("referencepage").style.display = "none"
    document.getElementById("detectpage").style.display = "none"
    document.getElementById("historypage").style.display = "none"
}

function toReferencePage(){
    referCanvas.clear()
    document.getElementById("loginpage").style.display = "none"
    document.getElementById("newsetpage").style.display = "none"
    document.getElementById("referencepage").style.display = "block"
    document.getElementById("detectpage").style.display = "none"
    document.getElementById("historypage").style.display = "none"
}
function toDetectPage(){
    canvas.clear()
    document.getElementById("loginpage").style.display = "none"
    document.getElementById("newsetpage").style.display = "none"
    document.getElementById("referencepage").style.display = "none"
    document.getElementById("detectpage").style.display = "block"
    document.getElementById("historypage").style.display = "none"}
function toHistoryPage(){
    document.getElementById("loginpage").style.display = "none"
    document.getElementById("newsetpage").style.display = "none"
    document.getElementById("referencepage").style.display = "none"
    document.getElementById("detectpage").style.display = "none"
    document.getElementById("historypage").style.display = "block"}



function drawImage(image,canvas){

    canvas.clear();
    canvas.setWidth(image.width);
    canvas.setHeight(image.height);
    var imgInstance = new fabric.Image(image, {
      });
    imgInstance.set('selectable', false);
    canvas.add(imgInstance);
}

function drawBullets(image,canvas){

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

function clientInit(mybutton,websocket) {
    
    mybutton.addEventListener("click",({target})=>{
        setuserid()
        const event = {
            command: "init",
            user_id: user_id,
         };
         websocket.send(JSON.stringify(event));
         alert("hello "+ user_id)
         toNewSetPage()
    })
    
    // const event = {
    //     command: "init",
    //     user_id: user_id,
    //  };
    //  websocket.send(JSON.stringify(event));
    }


function newSet(mybutton, websocket) {



    mybutton.addEventListener("click",({target})=>{
        const event = {
            command: "newSetFromCli",
            user_id: user_id,
            };
        websocket.send(JSON.stringify(event));
        toReferencePage()
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


function toDetectPageButton(mybutton){
    mybutton.addEventListener("click",({target})=>{
        toDetectPage()
    })
}

function toHistoryPageButton(mybutton){
    mybutton.addEventListener("click",({target})=>{
        toHistoryPage()
    })
}

function toSetPageButton(mybutton){
    mybutton.addEventListener("click",({target})=>{
        toNewSetPage()
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
                referObj.src = "data:image/jpg;base64, "+ event.image
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
        drawImage(this,canvas)
        drawBullets(this,canvas)
        drawPaths(this,canvas)
        if(typeof this.bullets !== "undefined"){
            console.log(this.bullets.length)
        }
        
      }


    referObj.onload = function() { 
        drawImage(this,referCanvas)

        
      }
    console.log("before web")
    
     // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8888/");
    listenToWebSocket(websocket)
    clientInit(document.querySelector(".login-button"),websocket)
    newSet(document.querySelector(".newset"),websocket)
    takeRef(document.querySelector(".refer"),websocket)
    toDetectPageButton(document.querySelector(".todetectbutton"))
    takePhoto(document.querySelector(".photo"),websocket)
    toHistoryPageButton(document.querySelector(".tohistorypage"))
    toSetPageButton(document.querySelector(".tosetpage"))
    console.log("after web")
    
    });