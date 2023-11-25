document.addEventListener('DOMContentLoaded', function() {
    // Open a WebSocket connection
    var ws = new WebSocket('ws://' + window.location.host + '/ws/queue/');
    var joinButton = document.querySelector('.join-queue-container button[value="join"]');


    ws.onopen = function(e) {
        console.log('WebSocket connected');
    };
    
    ws.onmessage = function(e) {
        console.log('Message received:', e.data); // Log received message
        var data = JSON.parse(e.data);
        
        if (data.action === 'join' && data.name === document.querySelector('#student_name').value) {
            joinButton.disabled = true;
            joinButton.style.backgroundColor = 'grey';
            joinButton.style.cursor = 'not-allowed';
        }
        var queueContainer = document.querySelector('.queue-container');
        var newDiv = document.createElement('div');
        newDiv.textContent = 'Name: ' + data.name + ', Question: ' + data.question + ', Location: ' + data.location;
        
        queueContainer.appendChild(newDiv);
        
    };

    ws.onclose = function(e) {
        console.error('WebSocket closed unexpectedly', e);
    };

    ws.onerror = function(e) {
        console.error('WebSocket encountered an error:', e);
    };

    // Handle form submission
    var form = document.querySelector('.join-queue-container form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submission intercepted'); // Log form submission

            var name = document.querySelector('#student_name').value;
            var question = document.querySelector('#question').value;
            var location = document.querySelector('#location').value;
            var action = e.submitter.value; // Using 'value' since it's the button's value

            console.log('Sending message via WebSocket'); // Log WebSocket send
            ws.send(JSON.stringify({ action: action, name: name, question: question, location: location }));
        });
    } else {
        console.error('Form not found');
    }
});
