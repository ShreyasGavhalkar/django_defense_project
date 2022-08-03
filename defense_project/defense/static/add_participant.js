var video
var canvas
var capture_button

window.onload = function () {
 video  = document.querySelector("#video")
 canvas  = document.querySelector("#video_frame")
 capture_button  = document.querySelector("#get_image")
}	
console.log(video)
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log(err0r)
    });
}

function capture_button_clicked(){
	console.log("capture button clicked")
	ctx = canvas.getContext('2d');
	ctx.drawImage(video,0,0)
	const img = canvas.toDataURL('image/png')
  var form = document.getElementById("form")
  form.photo.value = img
	console.log(form.id.value)
  console.log(form.photo.value)
}
