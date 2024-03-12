document.getElementById("stockForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/serverExample/predictStockData', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Error getting stock information due to invalid ticker
        if (data === 'Invalid stock ticker') {
            document.getElementById('result').innerHTML = '';
            document.getElementById('result').innerText = 'Error: ' + data;
            return;
        }
        dataObj = JSON.parse(data);
        // The output for a future date is an array with the following information:
        // symbol, timestamp, open price, high price, low price, close price, volume, and trade count 
        if (dataObj instanceof Array) {
            const headings = ['Symbol', 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trade Count'];

            // Create a table with the information
            const table = document.createElement('table');
            const thead = table.createTHead();
            const headRow = thead.insertRow(0);

            const tbody = table.createTBody();
            const bodyRow = tbody.insertRow(0);

            document.getElementById('result').innerText = dataObj;
            for (let i = 0; i < dataObj.length; i++) {
                const th = document.createElement('th');
                th.innerHTML = headings[i];
                headRow.appendChild(th);

                const td = bodyRow.insertCell();
                if (i === 0) {
                    td.innerHTML = dataObj[i].toUpperCase();
                } else if (i === 1) {
                    let startDate = new Date(dataObj[i]);
                    startDate = new Date(startDate.getTime() + (startDate.getTimezoneOffset() * 60000));
                    td.innerHTML = startDate.toDateString();
                } else {
                    td.innerHTML = Math.round(dataObj[i] * 100) / 100;
                }
            }
            document.getElementById('result').innerHTML = '';
            document.getElementById('result').innerText = '';
            const resultStr = document.createElement('h2');
            resultStr.innerHTML = 'Result:'

            document.getElementById('result').appendChild(resultStr);
            document.getElementById('result').appendChild(table);
            return;
        }
        // Create a table with the data from the Alpaca API
        const table = document.createElement('table');
        const thead = table.createTHead();
        const headRow = thead.insertRow(0);
        const tbody = table.createTBody();
        const bodyRow = tbody.insertRow(0);
        for (const [key, value] of Object.entries(dataObj)) {
            const th = document.createElement('th');
            if (key === 'trade_count') {
                th.innerHTML = 'Trade Count';
            } else {
                th.innerHTML = key.charAt(0).toUpperCase() + key.slice(1);
            }
            headRow.appendChild(th);

            const td = bodyRow.insertCell();
            if (key === 'timestamp') {
                td.innerHTML = (new Date(value[0])).toDateString();
            } else {
                td.innerHTML = value[0];
            }
        }
        document.getElementById('result').innerHTML = '';
        document.getElementById('result').innerText = '';
        const resultStr = document.createElement('h2');
        resultStr.innerHTML = 'Result:'

        document.getElementById('result').appendChild(resultStr);
        document.getElementById('result').appendChild(table);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});