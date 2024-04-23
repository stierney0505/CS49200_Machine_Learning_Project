document.getElementById("stockForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/serverExample/predictStockData', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data)
        // Error getting stock information due to invalid ticker
        if (data === 'Invalid stock ticker') {
            document.getElementById('result').innerHTML = '';
            document.getElementById('result').innerText = 'Error: ' + data;
            return;
        } else if (data === 'Invalid date: Must be a weekend') {
            document.getElementById('result').innerHTML = '';
            document.getElementById('result').innerText = 'Error: ' + data;
            return;
        }
        dataObj = JSON.parse(data);
        // The output for a future date is an array with the following information:
        // symbol, predicted close price 
        if (dataObj instanceof Array) {
            const headings = ['Symbol']
            if (dataObj[0] === 'Today') {
                headings.push('Predicted Close Price for ' + dataObj[0]);
            } else {
                headings.push('Predicted Close Price in ' + dataObj[0]);
            }

            // Create a table with the information
            const table = document.createElement('table');
            const thead = table.createTHead();
            const headRow = thead.insertRow(0);

            const tbody = table.createTBody();
            const bodyRow = tbody.insertRow(0);

            for (let i = 0; i < headings.length; i++) {
                const th = document.createElement('th');
                th.innerHTML = headings[i];
                headRow.appendChild(th);

                const td = bodyRow.insertCell();
                if (i === 0) {
                    td.innerHTML = dataObj[i+1];
                } else {
                    td.innerHTML = Math.round(dataObj[i+1] * 100) / 100;
                }
            }
            document.getElementById('result').innerHTML = '';
            document.getElementById('result').innerText = '';
            const resultStr = document.createElement('h2');
            resultStr.innerHTML = 'Result:'

            document.getElementById('result').appendChild(resultStr);
            document.getElementById('result').appendChild(table);

            // Getting data plot
            fetch('/serverExample/make-plot', {
                method: 'POST',
                body: formData
            })
            .then(() => {
                let img = new Image();
                img.src = '/client/static/plot.png'
                document.getElementById('result').appendChild(img)
            })

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

        fetch('/serverExample/make-plot', {
            method: 'POST',
            body: formData
        })
        .then(() => {
            let img = new Image();
            img.src = '/client/static/plot.png'
            document.getElementById('result').appendChild(img)
        })
    })
    .catch(error => {
        console.error('Error:', error);
    });
});