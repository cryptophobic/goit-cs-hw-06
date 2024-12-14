// Send text to all users through the server
const sendText = async () => {
    const message = document.getElementById("floatingTextarea").value;
    const username = document.getElementById("floatingInput").value;

    fetch("/message", {
        method: "POST",
        body: JSON.stringify({
            username,
            message,
        }),
    }).then(async (response) => {
        document.getElementById("floatingTextarea").value = '';
        document.getElementById("floatingInput").value = '';
        if (response.status === 200) {
            const json = await response.json();
            if (json.status === "success") {
                document.getElementById("info").innerHTML =`
                    <p style="color: green">data has been added successfully!</p>
                    User: ${json?.received.username}<br />
                    Message: ${json?.received.message}<br />
                    Date: ${json?.received.date}
                `;
                return;
            }
        }
        document.getElementById("info").innerHTML = '<p style="color: red">ERROR!</p>'
    });
}

document.getElementById('send_message').addEventListener('click', (event) => {
    event.preventDefault();
    sendText();
}, false);
