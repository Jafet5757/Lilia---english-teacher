const messageInput = document.getElementById('message-input');
const messageButton = document.getElementById('message-button');
const chatMessagesContainer = document.getElementById('chat-messages');
const modalButton = document.getElementById('modal-button');
const addContextButton = document.getElementById('add-context-button');
let context = '';

// When the DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
  modalButton.click(); // Open the modal
})

/**
 * Show user message when the user press enter
 */
messageInput.addEventListener('keyup', function (event) {
  if (event.key === 'Enter') {
    showMessage();
    getNextMessage();
  }
});

/**
 * Show user message when the user press the button
 */
messageButton.addEventListener('click', function () {
  showMessage();
  getNextMessage();
});

/**
 * Add the context to the conversation
 */
addContextButton.addEventListener('click', function () {
  contextInput = document.getElementById('context-input'); // Get the context
  context = contextInput.value; // Set the context
  contextInput.value = ''; // Clear the input
  document.getElementById('close-modal-button').click(); // Close the modal
});

/**
 * Show the message in the chat
 */
function showMessage(msg = null, userType = 'user') {
  const message = msg == null ? messageInput.value : msg;
  const card = `
    <div class="alert alert-${userType == 'user' ? 'light' : 'primary'}" role="alert">
      ${message}
    </div>
  `;
  chatMessagesContainer.innerHTML += card;
  // Clear the input
  messageInput.value = '';
}

function getNextMessage() {
  let conversation = getConversation();
  
  // Do a petition to the server to get the next message
  fetch('/api/speaking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ conversation, context })
  })
    .then(response => response.json())
    .then(data => {
      showMessage(data.next_message, 'bot');
    });
}

/**
 * Get all messages in the conversation (showed in the chat) and return like a string
 * @returns The conversation in the format (role: user, content: message), (role: bot, content: message)
 */
function getConversation() {
  // Get all divs with the class alert
  const messages = document.querySelectorAll('.alert');
  let conversation = '';

  for (let message of messages) {
    const content = message.innerHTML;
    const userType = message.classList.contains('alert-light') ? 'user' : 'bot';
    conversation += `(role: ${userType}, content: ${content}),`;
  }
  return conversation;
}