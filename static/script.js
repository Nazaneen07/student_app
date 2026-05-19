document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    if (uploadBtn) {
        uploadBtn.addEventListener("click", function () {
            const fileInput = document.getElementById("imageInput");
            const subject = document.getElementById("subjectInput").value;
            const msgEl = document.getElementById("upload_message");

            if (!fileInput.files.length) {
                msgEl.textContent = "Please select an image first.";
                return;
            }

            const formData = new FormData();
            formData.append("image", fileInput.files[0]);
            formData.append("subject", subject);

            fetch("/upload/image", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    msgEl.textContent = data.message;
                    location.reload(); // refresh gallery
                } else {
                    msgEl.textContent = "Error: " + data.error;
                }
            })
            .catch(() => {
                msgEl.textContent = "Upload failed. Try again.";
            });
        });
    }
});