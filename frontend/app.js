const socket = io("http://localhost:8000");

function join() {
    const username = document.getElementById("username").value;
    socket.emit("join", { username });
}

function sendPrivate() {
    socket.emit("private_message", {
        to: document.getElementById("toUser").value,
        message: document.getElementById("privateMsg").value
    });
}

function joinRoom() {
    socket.emit("join_room", {
        room: document.getElementById("room").value
    });
}

function sendGroup() {
    socket.emit("group_message", {
        room: document.getElementById("room").value,
        message: document.getElementById("groupMsg").value
    });
}

socket.on("private_message", data => {
    addMessage(`(Private) ${data.from}: ${data.message}`);
});

socket.on("group_message", data => {
    addMessage(`(${data.room}) ${data.from}: ${data.message}`);
});

function addMessage(msg) {
    const li = document.createElement("li");
    li.innerText = msg;
    document.getElementById("messages").appendChild(li);
}
