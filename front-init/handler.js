const exampleSocket = new WebSocket("wss://localhost:6000");

exampleSocket.onmessage = (event) => {
  console.log(event.data);
};

// Send text to all users through the server
const sendText = () => {
  // Construct a msg object containing the data the server needs to process the message from the chat client.
  const msg = {
      username: "username",
      message: "message",
    //message: document.getElementById("text").value,
  };

  // Send the msg object as a JSON-formatted string.
  exampleSocket.send(JSON.stringify(msg));

  // Blank the text input element, ready to receive the next line of text from the user.
  document.getElementById("text").value = "";
}

document.getElementById('send_message').addEventListener('click', (event) => {
    event.preventDefault();
    sendText();
}, false);
