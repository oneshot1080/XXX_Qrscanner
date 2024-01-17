document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const messageDiv = document.getElementById('message');
    let mediaStream = null;
    let delayNextRequest = false;

    // Open rear camera on page load
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then((stream) => {
            video.srcObject = stream;
            mediaStream = stream;
            startStreaming();
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });

    // Function to start streaming and capture frames
    function startStreaming() {
        const captureFrame = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const imageDataUrl = canvas.toDataURL('image/jpeg');
            sendDataToServer(imageDataUrl);
        };

        // Capture a frame every 1 second (adjust as needed)
        setInterval(() => {
            if (!delayNextRequest) {
                captureFrame();
            }
        }, 1000);
    }

    // Function to send data to the Flask server
    function sendDataToServer(imageDataUrl) {
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_data: imageDataUrl }),
        })
            .then(response => response.json())
            .then(data => handleServerResponse(data))
            .catch(error => console.error('Error sending data to server:', error));
    }

    // Function to handle server response
    function handleServerResponse(data) {
        if (data.message === 'granted') {
            showMessage('Access Granted', 'green');
        } else if (data.message === 'denied') {
            showMessage('Access Denied', 'red');
        }
        video.stop();
    // Delay the next request for 2 seconds
    delayNextRequest = true;
    setTimeout(() => {
        delayNextRequest = false;
    }, 1000);
    }
    // Function to display a message on the page for a limited time
    function showMessage(message, color) {
        messageDiv.innerText = message;
        messageDiv.style.color = color;
        messageDiv.style.display = 'block';

        setTimeout(() => {
            messageDiv.style.display = 'none';
            messageDiv.innerText = ''; // Clear the message
        }, 2000);
    }

    // Cleanup resources when the page is closed
    window.addEventListener('beforeunload', () => {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }
    });
});
