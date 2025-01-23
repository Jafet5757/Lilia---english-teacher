const cancelButton = document.getElementById("cancel-button");
const acceptButton = document.getElementById("accept-button");
const textCard = document.getElementById("text-card");
const visibleButtons = document.getElementById("visible-button");
const addCardButton = document.getElementById("add-card-button");
const translationText = document.getElementById("translation-text");
let visibility = false;
let indexCard = 0;

let cards = [
  {
    'word': 'long',
    'traduction': 'Grande',
    'sentence': 'The long table',
    'score': 0
  },
  {
    'word': 'little',
    'traduction': 'Pequeño',
    'sentence': 'The little horse',
    'score': 0
  },
  {
    'word': 'house',
    'traduction': 'Casa',
    'sentence': 'The house is big',
    'score': 0
  }
]

function loadCards() { 
  textCard.innerHTML = cards[indexCard].word;
  translationText.innerHTML = cards[indexCard].traduction;
}

loadCards();
  
function nextCard(score) {
  cards[indexCard].score += score;
  indexCard = (indexCard + 1) % cards.length;
  loadCards();
}

cancelButton.addEventListener("click", () => { 
  nextCard(-1);
})

acceptButton.addEventListener("click", () => { 
  nextCard(1);
})

/**
 * Change the visibility of the translation
 */
visibleButtons.addEventListener("click", () => { 
  visibility = !visibility;
  if (visibility) {
    // add visible class
    translationText.classList.add("visible");
    // delete class invisible
    translationText.classList.remove("invisible");
    // Change text of the button
    visibleButtons.innerHTML = '<i class="bi bi-eye"></i>';
  } else {
    // add invisible class
    translationText.classList.add("invisible");
    // delete class visible
    translationText.classList.remove("visible");
    // Change text of the button
    visibleButtons.innerHTML = '<i class="bi bi-eye-slash"></i>';
  }
})

/**
 * Add a new card to the list of cards
 */
function addCard() {
  const wordInput = document.getElementById("word-input").value;
  const translationInput = document.getElementById("translation-input").value;
  const exampleInput = document.getElementById("example-input").value;

  cards.push({
    word: wordInput,
    traduction: translationInput,
    sentence: exampleInput,
    score: 0
  })

  // Clean the inputs
  document.getElementById("word-input").value = "";
  document.getElementById("translation-input").value = "";
  document.getElementById("example-input").value = "";
  // close the modal
  document.getElementById("model-close-button").click();
}

addCardButton.addEventListener("click", () => {
  addCard();
})

document.getElementById("generate-card-button").addEventListener("click", () => {
  const topic = document.getElementById("topic-input");
  const description = document.getElementById("description-input");
  // send a petition to the server
  fetch('/api/generate-vocabulary', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({topic: topic.value, description: description.value})
  })
    .then(response => response.json())
    .then(data => {
      cards = data.vocabulary;
      console.log(cards);
      // Reemplazar comillas simples por comillas dobles
      cards = cards.replace(/'/g, '"');
      cards = JSON.parse(cards);
      indexCard = 0;
      loadCards();
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al enviar la carta');
    });
})