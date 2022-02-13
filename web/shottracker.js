/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function menuToggle() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.hamburger-menu-icon')) {
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

//Selector for your <video> element
const video = document.querySelector('#myVidPlayer');

//Core
//function loadCamera() {
window.navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
        };
    })
  //}
//Scroll the page when user clicks arrow icon
// function titleScroll(){
// 	document.getElementById("bodyHeader").scrollIntoView({alignToTop: true, behavior: "smooth"});
// 	console.log("scroll");
// }