document.addEventListener('DOMContentLoaded', function() {
    // Open a WebSocket connection
    var ws = new WebSocket('ws://' + window.location.host + '/ws/queue/');
    var joinButton = document.querySelector('.join-queue-container button[value="join"]');
    var leaveButton = document.getElementById('leaveQueue'); // Get the leave button

    ws.onopen = function(e) {
        console.log('WebSocket connected');
    };
    
    ws.onmessage = function(e) {
        console.log('Message received:', e.data); // Log received message
        var data = JSON.parse(e.data);
        var currentUser = document.querySelector('#student_name').value;

        if (data.action === 'join') {
            var queueContainer = document.querySelector('.queue-container');
            var newDiv = document.createElement('div');
            newDiv.id = 'queue-user-' + data.name;
            newDiv.textContent = 'Name: ' + data.name + ', Question: ' + data.question + ', Location: ' + data.location;
            queueContainer.appendChild(newDiv);

            if (data.name === currentUser) {
                joinButton.disabled = true;
                joinButton.style.backgroundColor = 'grey';
                joinButton.style.cursor = 'not-allowed';
            }
        }
        
        if (data.action === 'leave') {
            var userDiv = document.getElementById('queue-user-' + data.name);
            if (userDiv) {
                userDiv.remove();
            }

            if (data.name === currentUser) {
                joinButton.disabled = false;
                joinButton.style.backgroundColor = ''; 
                joinButton.style.cursor = '';
            }
        }
        if (data.action === 'update_queue') {
            console.log("Received updated queue:", data.queue);
            updateQueue(data.queue);
        }

        if (data.action === 'initial_state') {
            updateTaList(data.tas);
            updateQueue(data.queue);
        }

        if (data.action === 'update_ta_list') {
            var taListContainer = document.querySelector('.TA-list');
            taListContainer.innerHTML = ''; 
        
            // Add each TA to the list
            data.tas.forEach(function(taUsername) {
                var taElement = document.createElement('p');
                taElement.textContent = taUsername;
                taListContainer.appendChild(taElement);
            });
        }

        function updateTaList(tas) {
            var taListContainer = document.querySelector('.TA-list');
            taListContainer.innerHTML = ''; 
            tas.forEach(function(taUsername) {
                var taElement = document.createElement('p');
                taElement.textContent = taUsername;
                taListContainer.appendChild(taElement);
            });
        }
        
        function updateQueue(queue) {
            var queueContainer = document.querySelector('.queue-container');
            queueContainer.innerHTML = '';
            queue.forEach(function(queueItem) {
                var newDiv = document.createElement('div');
                newDiv.textContent = 'Name: ' + queueItem.name + ', Question: ' + queueItem.question + ', Location: ' + queueItem.location;
                queueContainer.appendChild(newDiv);
            });
        }
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
            console.log('Form submission intercepted'); 

            var name = document.querySelector('#student_name').value;
            var question = document.querySelector('#question').value;
            var location = document.querySelector('#location').value;
            var action = e.submitter.value; 

            console.log('Sending message via WebSocket');
            ws.send(JSON.stringify({ action: action, name: name, question: question, location: location }));
        });
    } else {
        console.error('Form not found');
    }

    if (leaveButton) {
        leaveButton.addEventListener('click', function() {
            var name = document.querySelector('#student_name').value; // Assuming the name is still needed for leave
            ws.send(JSON.stringify({ action: 'leave', name: name }));
        });
    } else {
        console.error('Leave button not found');
    }
});
