const form = document.getElementById("upload-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const files = document.getElementById("file-input").files;

    const formData = new FormData();
    for (const file of files) {
        formData.append("files", file);
    }

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    result.innerHTML = "<h3>Imagens corrigidas:</h3>";
    for (const filename of data.arquivos) {
        const link = document.createElement("a");
        link.href = `/download/${filename}`;
        link.innerText = `Baixar ${filename}`;
        link.download = filename;
        result.appendChild(link);
    }
});
