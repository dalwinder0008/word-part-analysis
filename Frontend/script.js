async function uploadAndAnalyze() {
  const fileInput = document.getElementById('csvFileInput');
  if (!fileInput || !fileInput.files[0]) {
    alert("csv file not select");
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const response = await fetch('http://127.0.0.1:5000/analyze', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
      openNewPage(result.data);
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    alert("Server Error! Check if Flask is running on port 5000.");
  }
}

function openNewPage(data) {
  const newWin = window.open("", "_blank");

  const tableRows = data.map(item => `
    <tr>
      <td>${item["Main Word"] || "-"}</td>
      <td>${item["Impr."] !== undefined ? item["Impr."] : 0}</td>
      <td>${item["Clicks"] !== undefined ? item["Clicks"] : 0}</td>
      <td>${item["Cost"] !== undefined ? item["Cost"] : 0}</td>
      <td>${item["Conv. rate"] !== undefined ? item["Conv. rate"] : (item["Conversions"] || 0)}</td>
    </tr>
  `).join('');
  newWin.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Extracted One Word Analysis</title>
    </head>
    <body>
      <h3>Search Term Analysis Table</h3>
      <table>
        <thead>
          <tr>
            <th>Main Word</th>
            <th>Impr.</th>
            <th>Clicks</th>
            <th>Cost</th>
            <th>Conv. rate</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows}
        </tbody>
      </table>
    </body>
    </html>
  `);

  newWin.document.close();
}
