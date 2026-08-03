async function uploadAndAnalyze() {
  const fileInput = document.getElementById('csvFileInput');
  if (!fileInput.files[0]) return alert("Select CSV file!");

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const res = await fetch('http://127.0.0.1:5000/analyze', { 
      method: 'POST', 
      body: formData 
    });
    
    const result = await res.json();

    if (result.success) {
      openReportWindow(result.data);
    } else {
      alert("Error: " + result.error);
    }
  } catch (err) {
    alert("Server Error! Make sure Python Flask server is running on port 5000.");
  }
}

function openReportWindow(data) {
  const win = window.open("", "_blank");

  // Dynamically Generate Table Rows
  const tableRows = data.map(item => `
    <tr>
      <td><b>${item["Main Word"] || "-"}</b></td>
      <td>${item["Clicks"] !== undefined ? item["Clicks"] : "-"}</td>
      <td>${item["Impressions"] !== undefined ? item["Impressions"] : "-"}</td>
      <td>${item["Cost"] !== undefined ? Number(item["Cost"]).toFixed(2) : "-"}</td>
    </tr>
  `).join('');

  win.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>One Word Metrics Report</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
        h2 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; max-width: 700px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #dddddd; padding: 10px 14px; text-align: left; }
        th { background-color: #3498db; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
      </style>
    </head>
    <body>
      <h2>One Word Performance Analysis</h2>
      <table>
        <thead>
          <tr>
            <th>Main Word</th>
            <th>Clicks</th>
            <th>Impressions</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows}
        </tbody>
      </table>
    </body>
    </html>
  `);

  win.document.close();
}
