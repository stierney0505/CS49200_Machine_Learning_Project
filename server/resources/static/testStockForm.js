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
        if (dataObj instanceof Array) {
            const headings = ['Symbol', 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trade Count'];
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
                if (i === 1) {
                    td.innerHTML = (new Date(dataObj[1])).toDateString();
                } else {
                    td.innerHTML = Math.round(dataObj[i] * 100) / 100;
                }
            }
            document.getElementById('result').innerHTML = '';
            const resultStr = document.createElement('h2');
            resultStr.innerHTML = 'Result:'

            document.getElementById('result').appendChild(resultStr);
            document.getElementById('result').appendChild(table);
            return;
        }
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