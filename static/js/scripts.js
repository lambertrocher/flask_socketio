var socket = io();
console.log("connecting")

var upgrade_hunting = document.getElementById('upgrade_hunting');
upgrade_hunting.onclick = function () {
  socket.emit('upgrade_hunting', {
    data: 'Upgrading'
  });
}

var upgrade_chopping = document.getElementById('upgrade_chopping');
upgrade_chopping.onclick = function () {
  socket.emit('upgrade_chopping', {
    data: 'Upgrading'
  });
}

var upgrade_coal_mining = document.getElementById('upgrade_coal_mining');
upgrade_coal_mining.onclick = function () {
  socket.emit('upgrade_coal_mining', {
    data: 'Upgrading'
  });
}

var upgrade_metal_mining = document.getElementById('upgrade_metal_mining');
upgrade_metal_mining.onclick = function () {
  socket.emit('upgrade_metal_mining', {
    data: 'Upgrading'
  });
}

hunting_speed = document.getElementById('hunting_speed');
socket.on('hunting_speed', data => {
  console.log(data);
  hunting_speed.innerText = data;
});

chopping_speed = document.getElementById('chopping_speed');
socket.on('chopping_speed', data => {
  console.log(data);
  chopping_speed.innerText = data;
});

coal_mining_speed = document.getElementById('coal_mining_speed');
socket.on('coal_mining_speed', data => {
  console.log(data);
  coal_mining_speed.innerText = data;
});

metal_mining_speed = document.getElementById('metal_mining_speed');
socket.on('metal_mining_speed', data => {
  console.log(data);
  metal_mining_speed.innerText = data;
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
});