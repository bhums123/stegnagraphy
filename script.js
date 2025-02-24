document.getElementById('encryptForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/encrypt', {
        method: 'POST',
        body: formData
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'encoded_image.png';
    link.click();
};

document.getElementById('decryptForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/decrypt', {
        method: 'POST',
        body: formData
    });
    const result = await response.text();
    document.getElementById('result').innerText = result;
};
