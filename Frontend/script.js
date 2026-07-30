async function uploadAndAnalyze() {
  const fileInput = document.getElementById('csvFileInput');
  const file = fileInput.files[0];

  if (!file) {
    alert("Kripya pehle ek CSV file select karein!");
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    // 💡 LIVE SERVER SE FLASK PAR BHEJNE KE LIYE POORA ADDRESS LAGAYEIN
    const response = await fetch('http://127.0.0.1:5000/analyze', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.success) {
      openNewPage(data.words);
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("Server Response Error! Make sure Flask server is running on port 5000.");
  }
}

function openNewPage(words) {
  const newWin = window.open("", "_blank");
  
  const tableRows = words.map(w => `<tr><td>${w}</td></tr>`).join('');

  newWin.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Extracted One Word Data</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h3 { color: #333; }
        p { color: #666; font-size: 13px; }
        table { border-collapse: collapse; width: 250px; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #eeeeee; }
      </style>
    </head>
    <body>
      <h3>Extracted One Word Analysis</h3>
      <p><i>Temporary file saved on local server: <b>temp_one_word_analysis.csv</b></i></p>
      <table>
        <thead>
          <tr><th>Main Word</th></tr>
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
