const offButton = document.getElementById('offButton');
let randomButton = document.getElementById("randomButton")
let downloadButton = document.getElementById("GetTemplateButton")

let gridColor = document.getElementById("GridColorSelector")
let colorBoxes = document.querySelectorAll(".boxColor")


downloadButton.addEventListener("click", () => {fetch("/GetTemplate")})

let sendRandom = () => {
    fetch("/SinglePixelRandom"      )

}
randomButton.addEventListener("click", () => {sendRandom()})



let setBoxColor = (row, col, color) => {
    let params = new URLSearchParams(
            {
                row:row,
                column:col,
                color:color
            }
    )
    fetch(`/SetBoxColor?${params}`)
}



// Initialize Iro.js color picker
const colorPicker = document.getElementById("colorPicker")

function sendColor(colorValue) {
    fetch('/colors', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ colordata: colorValue }),
    })
    .then(response => response.json())
    .then(data => {
    console.log('Server responded:', data);
    })
    .catch(error => {
    console.error('Error sending color:', error);
    });
}

// Send color when user picks a new one
colorPicker.addEventListener('change', (e) => {
    sendColor(colorPicker.value);
});

// Send black (#000000) when "Off" button is pressed
offButton.addEventListener('click', () => {
    sendColor('#000000');
});


colorBoxes.forEach(box => {
    box.addEventListener("click", function (e) {
        setBoxColor(
            this.parentNode.dataset.row,
            this.dataset.col,
            gridColor.value
        )
    })
});