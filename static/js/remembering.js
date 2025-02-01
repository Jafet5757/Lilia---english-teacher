const cancelButton = document.getElementById("cancel-button");
const acceptButton = document.getElementById("accept-button");
const textCard = document.getElementById("text-card");
const visibleButtons = document.getElementById("visible-button");
const addCardButton = document.getElementById("add-card-button");
const translationText = document.getElementById("translation-text");
const textSentence = document.getElementById("text-sentence");
let visibility = false;
let indexCard = 0;

let hiddentCards = [];
let cards = [
  {
    'word': 'long',
    'translation': 'Grande',
    'sentence': 'The long table',
    'score': 0
  },
  {
    'word': 'little',
    'translation': 'Pequeño',
    'sentence': 'The little horse',
    'score': 0
  },
  {
    'word': 'house',
    'translation': 'Casa',
    'sentence': 'The house is big',
    'score': 0
  }
]

function loadCards() { 
  textCard.innerHTML = cards[indexCard].word;
  textSentence.innerHTML = cards[indexCard].sentence;
  translationText.innerHTML = cards[indexCard].translation;
}

loadCards();
  
/**
 * Prepare the next card to be shown and reorder the cards
 * @param {Number} score Points to add to the card
 */
function nextCard(score) {
  cards[indexCard].score += score;
  indexCard = (indexCard + 1) % cards.length;
  if (indexCard === 0) {
    reorderCards();
  }
  if (cards.length === 0) {
    cards = hiddentCards;
    hiddentCards = [];
  }
  loadCards();
}

function reorderCards() {
  cards.sort((a, b) => a.score - b.score);
  // Hide cards over the threshold
  const threshold = 2;
  cards = cards.filter(card => {
    if (card.score <= threshold) {
      return true;
    } else {
      hiddentCards.push(card);
      return false;
    }
  });
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
    translation: translationInput,
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

/***
 * Generate new cards with IA
 */
document.getElementById("generate-card-button").addEventListener("click", () => {
  const topic = document.getElementById("topic-input");
  const description = document.getElementById("description-input");
  const loadingSpinner = document.getElementById("loading-label-genereate-modal")
  const button = document.getElementById("generate-card-button");

  // start loading
  loadingSpinner.classList.add("spinner-grow");
  loadingSpinner.classList.add("spinner-grow-sm");
  button.disabled = true;
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
      cards = JSON.parse(cards);
      indexCard = 0;
      loadCards();
      // close the modal
      document.getElementById("model-close-button-generate").click();
      // clean the inputs
      topic.value = "";
      description.value = "";
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al generar las tarjetas');
    })
    .finally(() => {
      // stop loading
      loadingSpinner.classList.remove("spinner-grow");
      loadingSpinner.classList.remove("spinner-grow-sm");
      button.disabled = false;
    })
})