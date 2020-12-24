var socket = io();
console.log("connecting")


var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vueee!',
      resources: null,
  },
  delimiters: ['[[', ']]'],
  methods: {
    upgrade: function (resource_activity) {
      socket.emit('upgrade', {
        data: resource_activity
      });
    },
  }
});

/* const upgrade_names = ['upgrade_hunting', 'upgrade_chopping', 'upgrade_coal_mining', 'upgrade_metal_mining']

upgrade_names.forEach(upgrade_name => {
  const element = document.getElementById(upgrade_name)
  element.onclick = function () {
    socket.emit('upgrade', {
      data: upgrade_name
    });
  }
})
*/

socket.on("resources", data => {
  console.log(data);
  app.resources = data
})