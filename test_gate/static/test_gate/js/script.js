const videoElement = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const uploadButton = document.getElementById('uploadButton');
const statusMessage = document.getElementById('statusMessage');

let mediaRecorder;
let recordedChunks = [];
let stream;
let recordingTimeout;

const API_URL = '/api/test-gate/upload/video-recordings/';

startButton.addEventListener('click', async () => {
    recordedChunks = [];
    statusMessage.textContent = '';
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        videoElement.srcObject = stream;
        videoElement.play();

        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            videoElement.srcObject = null;
            videoElement.src = URL.createObjectURL(blob);
            videoElement.controls = true;
            uploadButton.disabled = false;
            clearTimeout(recordingTimeout);
        };

        mediaRecorder.start();
        startButton.disabled = true;
        stopButton.disabled = false;
        uploadButton.disabled = true;
        statusMessage.textContent = 'Recording started... (Max 1 minute)';

        // Set a timeout for 1 minute (60000 milliseconds)
        recordingTimeout = setTimeout(() => {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                statusMessage.textContent = 'Recording stopped automatically after 1 minute.';
            }
        }, 60000);

    } catch (error) {
        console.error('Error accessing media devices:', error);
        statusMessage.textContent = 'Error accessing webcam. Please ensure it is connected and permissions are granted.';
    }
});

stopButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        stream.getTracks().forEach(track => track.stop()); // Stop all tracks in the stream
        startButton.disabled = false;
        stopButton.disabled = true;
        statusMessage.textContent = 'Recording stopped.';
        clearTimeout(recordingTimeout);
    }
});

uploadButton.addEventListener('click', async () => {
    if (recordedChunks.length === 0) {
        statusMessage.textContent = 'No video to upload.';
        return;
    }

    statusMessage.textContent = 'Uploading video...';
    uploadButton.disabled = true;

    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const formData = new FormData();
    formData.append('video_file', blob, `video-${Date.now()}.webm`);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
            // Django REST Framework handles CSRF for multipart/form-data automatically
            // if session authentication is used. For token auth, no CSRF token is needed.
        });

        if (response.ok) {
            const data = await response.json();
            statusMessage.textContent = 'Video uploaded successfully!';
            console.log('Upload successful:', data);
            // Optionally, reset the video element or show a success message
            videoElement.src = '';
            videoElement.controls = false;
            recordedChunks = [];
        } else {
            const errorData = await response.json();
            statusMessage.textContent = `Upload failed: ${errorData.detail || response.statusText}`;
            console.error('Upload failed:', response.status, errorData);
        }
    } catch (error) {
        statusMessage.textContent = `An error occurred during upload: ${error.message}`;
        console.error('Network error or other issue:', error);
    } finally {
        uploadButton.disabled = false;
    }
});