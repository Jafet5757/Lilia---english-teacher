const checkButton = document.getElementById('check-button');
const observationsContainer = document.getElementById('observations-container');
const levellabel = document.getElementById('level-label');

checkButton.addEventListener('click', () => { 
  const letter = document.getElementById('letter-textarea').value;

  // Enviamos a la api
  if(letter.length > 0 && letter.length < 1000) {
    fetch('/api/writing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ letter })
    })
    .then(response => response.json())
    .then(data => {
      feedback = data.feedback;
      level = data.level;
      observationsContainer.innerHTML = marked.parse(feedback);
      levellabel.innerHTML = `${level}`;
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al enviar la carta');
    });
  } else {
    alert('La carta debe tener entre 1 y 1000 caracteres');
  }
})