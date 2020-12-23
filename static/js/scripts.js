var socket = io();
console.log("connecting")

const upgrade_names = ['upgrade_hunting', 'upgrade_chopping', 'upgrade_coal_mining', 'upgrade_metal_mining']

upgrade_names.forEach(upgrade_name => {
  const element = document.getElementById(upgrade_name)
  element.onclick = function () {
    socket.emit('upgrade', {
      data: upgrade_name
    });
  }
})

const speed_names = ['hunting_speed', 'chopping_speed', 'coal_mining_speed', 'metal_mining_speed']

speed_names.forEach(speed_name => {
  const element = document.getElementById(speed_name)
  socket.on(speed_name, data => {
    console.log(data);
    element.innerText = data;
  });
})

const resource_names = ['food', 'wood', 'coal', 'metal']

resource_names.forEach(resource_name =>  {
  const element = document.getElementById(resource_name)
  socket.on(resource_name, data => {
    console.log(data);
    element.innerText = data;
  })
})