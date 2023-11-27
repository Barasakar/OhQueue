document.addEventListener('DOMContentLoaded', function() {
    var ws = new WebSocket('ws://' + window.location.host + '/ws/queue/');
    var joinButton = document.querySelector('.join-queue-container button[value="join"]');
    var leaveButton = document.getElementById('leaveQueue');

    ws.onopen = function(e) {
        console.log('WebSocket connected');
    };

    ws.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var currentUser = document.querySelector('#student_name').value;

        if (data.action === 'join' && data.name === currentUser) {
            joinButton.disabled = true;
            joinButton.style.backgroundColor = 'grey';
            joinButton.style.cursor = 'not-allowed';
            updateQueue(data.queue, currentUser); // Update queue when a user joins
        } else if (data.action === 'leave' && data.name === currentUser) {
            joinButton.disabled = false;
            joinButton.style.backgroundColor = '';
            joinButton.style.cursor = '';
        } else if (data.action === 'update_queue' || data.action === 'initial_state') {
            updateQueue(data.queue, currentUser);
        } else if (data.action === 'update_ta_list') {
            updateTaList(data.tas);
        } else if (data.action === 'user_status') {
            joinButton.disabled = data.in_queue;
            joinButton.style.backgroundColor = data.in_queue ? 'grey' : '';
            joinButton.style.cursor = data.in_queue ? 'not-allowed' : '';
        }
    };

    ws.onclose = function(e) {
        console.error('WebSocket closed unexpectedly', e);
    };

    ws.onerror = function(e) {
        console.error('WebSocket encountered an error:', e);
    };

    var form = document.querySelector('.join-queue-container form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var name = document.querySelector('#student_name').value;
            var question = document.querySelector('#question').value;
            var location = document.querySelector('#location').value;
            ws.send(JSON.stringify({ action: 'join', name: name, question: question, location: location }));
        });
    }

    if (leaveButton) {
        leaveButton.addEventListener('click', function() {
            var name = document.querySelector('#student_name').value;
            ws.send(JSON.stringify({ action: 'leave', name: name }));
        });
    }

    function updateQueue(queue, currentUser) {
        var queueContainer = document.querySelector('.queue-container');
        queueContainer.innerHTML = '';
    
        if (queue && Array.isArray(queue)) { // Check if queue is defined and is an array
            queue.forEach(function(queueItem) {
                var newDiv = document.createElement('div');
                newDiv.id = 'queue-user-' + queueItem.name;
                newDiv.textContent = 'Name: ' + queueItem.name + ', Question: ' + queueItem.question + ', Location: ' + queueItem.location;
                queueContainer.appendChild(newDiv);
    
                if (queueItem.name === currentUser) {
                    joinButton.disabled = true;
                    joinButton.style.backgroundColor = 'grey';
                    joinButton.style.cursor = 'not-allowed';
                }
            });
        } else {
            console.error("Queue data is undefined or not an array");
        }
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
});
