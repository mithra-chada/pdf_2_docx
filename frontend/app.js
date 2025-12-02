const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const progressArea = document.getElementById('progressArea');
const progressBar = document.getElementById('progressBar');
const statusText = document.getElementById('statusText');
const resultArea = document.getElementById('resultArea');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');

let currentTaskId = null;

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
});

async function handleFile(file) {
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file.');
        return;
    }

    // Reset UI
    dropZone.classList.add('hidden');
    progressArea.classList.remove('hidden');
    resultArea.classList.add('hidden');
    progressBar.style.width = '0%';
    statusText.textContent = 'Uploading...';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        currentTaskId = data.task_id;
        pollStatus(currentTaskId);

    } catch (error) {
        console.error(error);
        statusText.textContent = 'Error: ' + error.message;
        statusText.classList.add('text-red-500');
    }
}

async function pollStatus(taskId) {
    statusText.textContent = 'Converting...';
    progressBar.style.width = '30%';

    const interval = setInterval(async () => {
        try {
            const response = await fetch(`http://localhost:8000/status/${taskId}`);
            const data = await response.json();

            if (data.status === 'completed') {
                clearInterval(interval);
                progressBar.style.width = '100%';
                statusText.textContent = 'Conversion Complete!';
                setTimeout(() => {
                    progressArea.classList.add('hidden');
                    resultArea.classList.remove('hidden');
                }, 500);
            } else if (data.status === 'failed') {
                clearInterval(interval);
                statusText.textContent = 'Conversion Failed: ' + data.message;
                statusText.classList.add('text-red-500');
            } else {
                // Fake progress for visual feedback
                const currentWidth = parseFloat(progressBar.style.width);
                if (currentWidth < 90) {
                    progressBar.style.width = (currentWidth + 5) + '%';
                }
            }
        } catch (error) {
            clearInterval(interval);
            console.error(error);
        }
    }, 1000);
}

downloadBtn.addEventListener('click', () => {
    if (currentTaskId) {
        window.location.href = `http://localhost:8000/download/${currentTaskId}`;
    }
});

resetBtn.addEventListener('click', () => {
    dropZone.classList.remove('hidden');
    progressArea.classList.add('hidden');
    resultArea.classList.add('hidden');
    fileInput.value = '';
    currentTaskId = null;
    statusText.classList.remove('text-red-500');
});
