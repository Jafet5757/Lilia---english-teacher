const topic = "México"

function getQuestions() {
  // Fetch petition to server
  fetch("/api/questions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ topic: topic })
  })
    .then(response => response.json())
    .then(data => {
      json = JSON.parse(data);
      form = json.form;
    })
    .catch(error => {
      alert("Error al obtener las preguntas");
      console.error("Error:", error);
    });
}

//getQuestions();