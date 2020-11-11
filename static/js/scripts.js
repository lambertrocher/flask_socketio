var socket = io();
console.log("connecting")

var test = document.getElementById('test');
test.onclick = function () {
    socket.emit('upgrade', {
        data: 'Upgrading mine'
    });
}

mining_speed = document.getElementById('mining_speed');
socket.on('mining_speed', data => {
    console.log(data);
    mining_speed.innerText = data;
  });
  
gold = document.getElementById('gold');
socket.on('gold', data => {
    console.log(data);
    gold.innerText = data;
  });
  
  