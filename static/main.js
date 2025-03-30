const form = document.getElementById("FileUploadForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    
    if (!fileInput.files.length) {
        alert("Please select a file before submitting.");
        return;
    }
    try {
        const formData = new FormData(e.target);
        const response = await fetch("/submit", {
            method: "POST",
            // BIG OL' RED ONES!
            body: formData
        });
        if (response.ok) {
            console.log("ok it worked i guess");
        }
        const data = await response.json();
        if (data.code == 200) {
            // We won! I ACTUALLY FUCKING WON!
            alert(data.msg);
        }
    } catch (error) {
        alert(error);
    }
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image')) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result; 
            img.style.maxWidth = '100%'; 
            img.style.height = 'auto';
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.innerHTML = ''; 
            imagePreview.appendChild(img); 
        };
        reader.readAsDataURL(file);
        const lbl = document.getElementById('imglbl');
        lbl.innerHTML = 'Your image: '; 
        lbl.appendChild(text);
    } else {
        alert('Please upload a valid image file.');
    }
});