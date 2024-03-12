document.getElementById("stockForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/serverExample/predictStockData', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        dataObj = JSON.parse(data);
        if ((new Date(dataObj.timestamp)) > new Date()) {
            document.getElementById('result').innerText = dataObj;
        }
        console.log(dataObj);
        const table = document.createElement('table');
        const thead = table.createTHead();
        const headRow = thead.insertRow(0);
        const tbody = table.createTBody();
        const bodyRow = tbody.insertRow(0);
        for (const [key, value] of Object.entries(dataObj)) {
            const th = document.createElement('th');
            th.innerHTML = key.charAt(0).toUpperCase() + key.slice(1);
            headRow.appendChild(th);

            const td = bodyRow.insertCell();
            if (key === 'timestamp') {
                td.innerHTML = (new Date(value[0])).toDateString();
            } else {
                td.innerHTML = value[0];
            }
        }
        document.getElementById('result').innerHTML = '';
        const resultStr = document.createElement('h2');
        resultStr.innerHTML = 'Result:'

        document.getElementById('result').appendChild(resultStr);
        document.getElementById('result').appendChild(table);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});