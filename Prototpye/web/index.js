window.addEventListener("DOMContentLoaded", () => {
    // variables
    var circleRadius = 20
    var textsize = 15
    var user_id = "jisoo"
    var set_id = ""
    var imageObj = new Image();
    var referObj = new Image();
    var pointcount = 0
    var temppoint;
    var defaultMeasure = 1
    var calculatedPixel = 1
    function myRatio(){
        return defaultMeasure/calculatedPixel
    }
    const defaultwidth = 640
    const defaultheight = 480
    // make canvas for displaying bullet images
    var canvas = new fabric.Canvas('myCanvas');
    canvas.setWidth(defaultwidth);
    canvas.setHeight(defaultheight);
    // make canvas for displaying refer images
    var referCanvas = new fabric.Canvas('myReferCanvas');
    referCanvas.setWidth(defaultwidth);
    referCanvas.setHeight(defaultheight);
    
    // set user id
    function setuserid(){
        user_id = document.getElementById("fname").value
    }
    // loginpage mode
    function toLoginPage(){
        document.getElementById("loginpage").style.display = "block"
        document.getElementById("newsetpage").style.display = "none"
        document.getElementById("referencepage").style.display = "none"
        document.getElementById("detectpage").style.display = "none"
        document.getElementById("historypage").style.display = "none"
    }
    // newsetpage mode
    function toNewSetPage(){
        
        document.getElementById("loginpage").style.display = "none"
        document.getElementById("newsetpage").style.display = "block"
        document.getElementById("referencepage").style.display = "none"
        document.getElementById("detectpage").style.display = "none"
        document.getElementById("historypage").style.display = "none"
    }
    // refernecepage mode
    function toReferencePage(){
        referCanvas.clear()
        document.getElementById("loginpage").style.display = "none"
        document.getElementById("newsetpage").style.display = "none"
        document.getElementById("referencepage").style.display = "block"
        document.getElementById("detectpage").style.display = "none"
        document.getElementById("historypage").style.display = "none"
    }
    // detection page mode
    function toDetectPage(){
        canvas.clear()
        document.getElementById("loginpage").style.display = "none"
        document.getElementById("newsetpage").style.display = "none"
        document.getElementById("referencepage").style.display = "none"
        document.getElementById("detectpage").style.display = "block"
        document.getElementById("historypage").style.display = "none"}
    // history page mode
    function toHistoryPage(){
        document.getElementById("loginpage").style.display = "none"
        document.getElementById("newsetpage").style.display = "none"
        document.getElementById("referencepage").style.display = "none"
        document.getElementById("detectpage").style.display = "none"
        document.getElementById("historypage").style.display = "block"}
    
    
    // draw image on canvas
    function drawImage(image,canvas){
    
        canvas.clear();
        canvas.setWidth(image.width);
        canvas.setHeight(image.height);
        var imgInstance = new fabric.Image(image, {
          });
        imgInstance.set('selectable', false);
        canvas.add(imgInstance);
    }
    // draw bullet traces on canvas
    function drawBullets(image,canvas){
    
        if (image.bullets){
            for (var i = 0; i < image.bullets.length; i++) {
                console.log(image.bullets[i]);
                var bullet = image.bullets[i];
                var stroke = "#33FF33"
                if (bullet.isnew){
                    stroke = "red"
                }
                var circlePatrol = new fabric.Circle({
                    originX: "center",
                    originY: "center",
                    top: bullet.yposition,
                    left: bullet.xposition,
                    radius: circleRadius,
                    stroke: stroke,
                    strokeWidth: 2,
                    fill: 'rgba(0,0,0,0)'
                  });
                canvas.add(circlePatrol);
    
            }       
        }
    
    }
    
    // draw paths between image's bullet traces with their lenght
    // draw the longest path for each bullet
    function drawPaths(image,canvas){
        if (image.bullets){
            for (var i = 0; i < image.bullets.length; i++) {
                var max = 0
                var mainbullet1;
                var mainbullet2;
                for(var j = 0; j<image.bullets.length;j++){
                    var bullet1 = image.bullets[i];
                    var bullet2 = image.bullets[j];
                    var len = (myRatio()*((bullet1.xposition-bullet2.xposition)**2+
                    (bullet1.yposition-bullet2.yposition)**2)**0.5).toFixed(2)
                    if (len>max){
                        max = len
                        mainbullet1 = bullet1
                        mainbullet2 = bullet2
                    }
                }
    
                if (typeof mainbullet2 !== 'undefined' && max!= 0){
                    var stroke = "#33FF33"
                    if (mainbullet1.isnew || mainbullet2.isnew){
                        stroke = 'red'
                    }
                    var line = new fabric.Line([mainbullet1.xposition, mainbullet1.yposition, mainbullet2.xposition, mainbullet2.yposition], {
                        stroke: "#FEFF3E"
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
    
    
    
    // send init message to server
    
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
        

        }
    
    // send new set message to server
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
    // send takeRef message to server
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
    
    // go to detect page
    function toDetectPageButton(mybutton){
        mybutton.addEventListener("click",({target})=>{
            defaultMeasure = document.getElementById("referdistance").value
            toDetectPage()
        })
    }
    // go to history page
    function toHistoryPageButton(mybutton){
        mybutton.addEventListener("click",({target})=>{
            toHistoryPage()
        })
    }
    // go to set page
    function toSetPageButton(mybutton){
        mybutton.addEventListener("click",({target})=>{
            toNewSetPage()
        })
    }
    // send takephoto message
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

    //listen to websocket server
    function listenToWebSocket(websocket){
        websocket.addEventListener("message",({data})=>{
            const event = JSON.parse(data);
            switch(event.command){
                
                case "newSet":
                    // new set inited. set set_id 
                    set_id = event.set_id;
                    console.log("new set id detected"+set_id)
                    break;
                case "refer":
                    // get reference image. add it to page
                    referObj.src = "data:image/jpg;base64, "+ event.image
                    break;
                case "warp":
                    // get warped image. add it to page
                    imageObj.bullets = event.bullets
                    imageObj.src = "data:image/jpg;base64, "+ event.image
                    
                    console.log(event)
                    break;
                default:
                    console.log(event)
            }
        })
    }
    
    

    imageObj.onload = function() { 
        // when image loads, update that to canvas
        drawImage(this,canvas)
        // and draw bullets
        drawBullets(this,canvas)
        // and draw paths
        drawPaths(this,canvas)
        if(typeof this.bullets !== "undefined"){
            console.log(this.bullets.length)
        }
        
      }


    referObj.onload = function() { 
        // when refer image loads, update that to canvas
        drawImage(this,referCanvas)
        // let user mark points for measuring.
        referCanvas.on("mouse:down", function(event) {
            var pointer = referCanvas.getPointer(event.e);
            var positionX = pointer.x;
            var positionY = pointer.y;
            // Add small circle as an indicative point
            var circlePoint = new fabric.Circle({
                radius: 4,
                fill: "blue",
                left: positionX ,
                top: positionY,
                selectable: false,
                originX: "center",
                originY: "center",
                hoverCursor: "auto"
            });
            referCanvas.add(circlePoint);
            
            if(pointcount == 0){
                temppoint = [positionX,positionY]
                pointcount = 1
            }else if (pointcount == 1){
                calculatedPixel = (((positionX-temppoint[0])**2+
                    (positionY-temppoint[1])**2)**0.5)
                pointcount = 0
            }

        })
        
      }
    console.log("before web")
    
     // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8888/");
    // listen to websocket
    listenToWebSocket(websocket)
    // make buttons functionable
    clientInit(document.querySelector(".login-button"),websocket)
    newSet(document.querySelector(".newset"),websocket)
    takeRef(document.querySelector(".refer"),websocket)
    toDetectPageButton(document.querySelector(".todetectbutton"))
    takePhoto(document.querySelector(".photo"),websocket)
    toHistoryPageButton(document.querySelector(".tohistorypage"))
    toSetPageButton(document.querySelector(".tosetpage"))
    console.log("after web")
    
// One day... lets do react and display results & history.
// const e = React.createElement;

// class LikeButton extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = { liked: false };
//   }

//   render() {
//     if (this.state.liked) {
//       return 'You liked this.';
//     }

//     return e(
//       'button',
//       { onClick: () => this.setState({ liked: true }) },
//       'Like'
//     );
//   }
// }

// const domContainer = document.querySelector('#like_button_container');
// ReactDOM.render(e(LikeButton), domContainer);
    });