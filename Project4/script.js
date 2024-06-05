const form = document.getElementById('forecast-form');
const forecastContainer = document.getElementById('forecast-container');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const precipitation = document.getElementById('precipitation').value;
    const temp_max = document.getElementById('temp_max').value;
    const temp_min = document.getElementById('temp_min').value;
    const wind = document.getElementById('wind').value;
    const data = { precipitation, temp_max, temp_min, wind };

    try {
        const response = await fetch('/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const weather = await response.json();
        const forecastHTML = `
            <h2>Weather Forecast</h2>
            <p>Weather: ${weather.weather}</p>
        `;
        forecastContainer.innerHTML = forecastHTML;
    } catch (error) {
        console.error(error);
    }
});
