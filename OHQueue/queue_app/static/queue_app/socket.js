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
        if (data.action === 'user_status') {
            console.log("User status received:", data.in_queue);
            joinButton.disabled = data.in_queue;
            joinButton.style.backgroundColor = data.in_queue ? 'grey' : '';
            joinButton.style.cursor = data.in_queue ? 'not-allowed' : '';
        }
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
        if (data.action === 'answer') {
            displayAssistance(data.studentUsername, data.taUsername);
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
            var name = username;  
            var question = document.querySelector('#question').value;
            var location = document.querySelector('#location').value;
    
            joinButton.disabled = true;
            joinButton.style.backgroundColor = 'grey';
            joinButton.style.cursor = 'not-allowed';
    
            ws.send(JSON.stringify({ action: 'join', name: name, question: question, location: location }));
        });
    }

    if (leaveButton) {
        leaveButton.addEventListener('click', function() {
            var name = username;
            joinButton.disabled = false;
            joinButton.style.backgroundColor = '';
            joinButton.style.cursor = '';
    
            ws.send(JSON.stringify({ action: 'leave', name: name }));
        });
    }

    function updateQueue(queue, currentUser) {
        var queueContainer = document.querySelector('.queue-container');
        queueContainer.innerHTML = '';
        
        queue.forEach(function(queueItem) {
            if (queueItem.in_queue) {
                var newDiv = document.createElement('div');
                newDiv.id = 'queue-user-' + queueItem.name;
                newDiv.innerHTML = 'Name: ' + queueItem.name + ', Question: ' + queueItem.question + ', Location: ' + queueItem.location;

                if (queueItem.assisting_ta) {
                    var assistanceInfo = document.createElement('p');
                    assistanceInfo.textContent = 'You are currently assisted by ' + queueItem.assisting_ta;
                    newDiv.appendChild(assistanceInfo);
                }
                if (isTA) {  // Don't show the button if already assisted
                    if (!queueItem.assisting_ta) {
                        var answerButton = document.createElement('button');
                        answerButton.textContent = 'Answer';
                        answerButton.onclick = function() { answerQueueItem(queueItem.username); };
                        newDiv.appendChild(answerButton);
                    }
                    var deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = function() { deleteQueueItem(queueItem.username); };
                    newDiv.appendChild(deleteButton);
                }
        
                queueContainer.appendChild(newDiv);
            }
        });
    }
    

    function answerQueueItem(username) {
        ws.send(JSON.stringify({ action: 'answer', studentUsername: username }));
    }

    function deleteQueueItem(username) {
        ws.send(JSON.stringify({ action: 'delete', studentUsername: username }));
    }

    function displayAssistance(studentUsername, taUsername) {
        var studentDiv = document.getElementById('queue-user-' + studentUsername);
        console.log("studentDiv: ", studentDiv);
        if (studentDiv) {
            var assistanceInfo = 'You are currently assisted by ' + taUsername;
            studentDiv.innerHTML += '<p>' + assistanceInfo + '</p>';
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
