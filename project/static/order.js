/**
 * Created by amrullahzunzunia on 05/05/16.
 */
$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    updater.start();
});


var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/order_socket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(order_object) {
        var stuff_to_append = "<div> Id: " + String(order_object.id) +
            ", Order Id: " + order_object.order_id + ", Status: " + order_object.status +
            "</div>";
        $("#orders").append(stuff_to_append);
    }
};