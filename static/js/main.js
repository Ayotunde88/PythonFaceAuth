document.getElementById('basicButton').addEventListener('click', function() {

    const message = document.querySelector('.message');
    const otherDetails = document.getElementById('otherDetails');
    const basicInfoForm = document.getElementById('basicInfoForm');
    // Get form data
    const formData = new FormData();
    formData.append('firstName', document.getElementById('firstName').value);
    formData.append('lastName', document.getElementById('lastName').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('phonenumber', document.getElementById('phonenumber').value);

    // Send the data using Fetch API
    fetch('/api/basicinfo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success' ) {
        
            basicInfoForm.style.display = 'none';
            basicInfoForm.style.width = '0';
            otherDetails.style.display = 'block';

        } else {
           
            message.className = `${data.messageclass}`;
            var newmessage = document.querySelector(`.${message.className}`);
            newmessage.innerHTML = `
                <div class='alert alert-danger' role='alert' style='padding:5px; border-radius:5px;'>
                    ${data.message}
                </div>`;

        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('goToBiometric').addEventListener('click', function() {

    const message = document.querySelector('.message');
    const biodetails = document.getElementById('biodetails');
    const otherDetails = document.getElementById('otherDetails');
    const basicInfoForm = document.getElementById('basicInfoForm');
    // Get form data
    const formData = new FormData();
    formData.append('purposeOfVisit', document.getElementById('purposeOfVisit').value);
    formData.append('visitingWhom', document.getElementById('visitingWhom').value);

    // Send the data using Fetch API
    fetch('/api/otherdetails', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success' ) {
            basicInfoForm.style.display = 'none';
            otherDetails.style.display = 'none';
            biodetails.style.display = 'block';
        
        } else {
            message.className = `${data.messageclass}`;
            var newmessage = document.querySelector(`.${message.className}`);
            newmessage.innerHTML = `
                <div class='alert alert-danger' role='alert' style='padding:5px; border-radius:5px;'>
                    ${data.message}
                </div>`;

          
        }
    })
    .catch(error => console.error('Error:', error));
});




var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var countdownText = document.getElementById('countdown-text');
var progressCircle = document.getElementById('progress-circle');
var successModal = document.getElementById('successModal');
var goToBiometric = document.getElementById('goToBiometric');
var biodetails = document.getElementById('biodetails');
var otherDetails = document.getElementById('otherDetails');
var basicInfoForm = document.getElementById('basicInfoForm');
// var countdownTime = 10; // Countdown time in seconds

// Ensure that face-api.js models are loaded before starting the countdown
async function loadFaceApiModels() {
    try {
        await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        console.log('Face-api.js models loaded successfully.');
    } catch (error) {
        console.error('Error loading face-api.js models:', error);
    }
}

// Start the countdown and capture photo when time is up
function startCountdown() {
    countdownTime = 10; // Reset countdown time
    var interval = setInterval(function () {
        countdownText.textContent = countdownTime;
        countdownTime--;

        if (countdownTime < 0) {
            clearInterval(interval);
            capturePhoto();
        }
    }, 1000);
}

// Capture photo from video stream and send to the server
function capturePhoto() {
    video.style.display = 'none';
    canvas.style.display = 'block';
    var context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(function(blob) {
        var formData = new FormData();
        formData.append('face_image', blob, 'face_image.jpg');

        fetch('/api/biometric', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);  // Ensure you see the response in the console
            if (data.status === 'success') {
                biodetails.style.display = 'none';
                basicInfoForm.style.display = 'none';
                otherDetails.style.display = 'none';
                successModal.style.display = 'block';
            } else {
                alert('Failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the image.');
        });
    }, 'image/jpeg');
}

// Set up the video stream and start the countdown when the page loads
navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
    video.srcObject = stream;
    video.play();
    console.log('Video stream started successfully.');
})
.catch(function(err) {
    console.error('An error occurred while accessing the camera: ', err);
});

// Add event listener to start countdown on button click
goToBiometric.addEventListener('click', function() {
    loadFaceApiModels().then(() => startCountdown());
});

const startAgain = document.getElementById('startAgain');
startAgain.addEventListener('click',function(){
    successModal.style.display = 'none';
    basicInfoForm.style.display = 'block';
    alert("Hello")
})


$(document).ready(function(){
    $('#successModal').modal('hide');
   
})