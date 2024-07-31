async function submitForm() {
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const income = document.getElementById('income').value;
    const savings = document.getElementById('savings').value;

    const data = { age, gender, income, savings };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_response', {  // Update this URL to your backend's address
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        document.getElementById('response').textContent = result.response;
        document.getElementById('responseContainer').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').textContent = 'An error occurred. Please try again.';
        document.getElementById('responseContainer').style.display = 'block';
    }
}




