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

food = document.getElementById('food');
socket.on('food', data => {
  console.log(data);
  food.innerText = data;
});

wood = document.getElementById('wood');
socket.on('wood', data => {
  console.log(data);
  wood.innerText = data;
});

coal = document.getElementById('coal');
socket.on('coal', data => {
  console.log(data);
  coal.innerText = data;
});

metal = document.getElementById('metal');
socket.on('metal', data => {
  console.log(data);
  metal.innerText = data;
}); I