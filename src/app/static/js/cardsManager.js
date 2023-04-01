async function deleteImage(imageId) {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch(`/home/images/delete/${imageId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("An error occurred while deleting the image.");
        }

        (`Image with ID: ${imageId} deleted successfully.`);
        await displayImages(); // Refresh the image grid after successful deletion
    } catch (error) {
        console.error("Error:", error);
    }
}


async function getImages() {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('/home/images', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const images = await response.json();
            return images.map(image => ({
                src: `data:image/jpeg;base64,${image.image_data}`,
                caption: image.description,
                timestamp: new Date(image.creation_date).toLocaleString(),
                image_data: image.image_data,
                image_id: image._id,
            }));
        } else {
            console.error('Failed to fetch images');
            return [];
        }
    } catch (error) {
        console.error('Error fetching images:', error);
        return [];
    }
}

function createImageCard(image) {
    return `
  <div class="col">
    <div class="card shadow-sm">
      <img src="${image.src}" class="card-img-top card-img-fixed" alt="${image.caption}">
      <div class="card-body">
        <p class="card-text">${image.caption}</p>
        <div class="d-flex justify-content-between align-items-center">
          <div class="btn-group">
            <button type="button" class="btn btn-sm btn-outline-secondary">Infer</button>
            <button type="button" class="btn btn-sm btn-outline-secondary delete-btn" data-image-id="${image.image_id}">Delete</button>
          </div>
          <small class="text-muted">${image.timestamp}</small>
        </div>
      </div>
    </div>
  </div>
`;
}


function attachDeleteEventListeners(deleteButtons) {
    deleteButtons.forEach((deleteButton) => {
        deleteButton.addEventListener("click", () => {
            const imageId = deleteButton.getAttribute("data-image-id");
            deleteImage(imageId);
        });
    });
}

async function displayImages() {
    const images = await getImages();
    const imageGrid = document.querySelector(".album .container .row");
    imageGrid.innerHTML = images.map(createImageCard).join("");
    const deleteButtons = document.querySelectorAll(".delete-btn");
    attachDeleteEventListeners(deleteButtons);
}


document.addEventListener('DOMContentLoaded', async () => {
    await displayImages();
});

document.getElementById('refresh').addEventListener('click', async () => {
    await displayImages();
});