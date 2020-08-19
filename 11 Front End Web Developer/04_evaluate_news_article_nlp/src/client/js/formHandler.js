function handleSubmit(event) {
    event.preventDefault();

    // check what text was put into the form field
    let formText = document.getElementById('text').value;

    console.log(formText);

    // If no text is entered
    if (Client.checkForText(formText)) {
        alert("Please enter text before pressing submit button");
        return;
    };

    console.log("::: Form Submitted :::");
    fetch('http://localhost:8081/analysis', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({formText: formText})
    })
    .then(res => res.json())
    .then(function(res) {
        document.getElementById('agreement').innerHTML = res.agreement;
        document.getElementById('subjectivity').innerHTML = res.subjectivity;
        document.getElementById('confidence').innerHTML = res.confidence;
        document.getElementById('irony').innerHTML = res.irony;
    })
}

export { handleSubmit };
