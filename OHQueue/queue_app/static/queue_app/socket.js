document.addEventListener('DOMContentLoaded', function() {
    // Open a WebSocket connection
    var ws = new WebSocket('ws://' + window.location.host + '/ws/queue/');

    ws.onopen = function(e) {
        console.log('WebSocket connected');
    };

    ws.onmessage = function(e) {
        var data = JSON.parse(e.data);
        // Handle incoming message (update DOM)
        console.log('Message from server: ', data);
    };

    ws.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };

    // Example: Sending data to the server
    document.querySelector('.join-leave-queue form').onsubmit = function(e) {
        e.preventDefault();;

        var name = document.querySelector('#student_name').value;
        var question = document.querySelector('#question').value;
        var location = document.querySelector('#location').value;
        var action = e.submitter.value; // either join or leave action

        ws.send(JSON.stringify({ action: action, name: name, question: question, location: location }));
    };
});
