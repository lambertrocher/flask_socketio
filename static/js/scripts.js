var socket = io();
console.log("connecting")

var test = document.getElementById('test');
test.onclick = function () {
    socket.emit('my event', {
        data: 'I\'m connected!'
    });
}

speed = document.getElementById('speed');
socket.on('my event', data => {
    console.log(data);
    speed.innerText = data;
  });
  
  