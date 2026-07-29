async function uploadCSV() {
  const url = document.getElementById('webAppUrl').value.trim();
  const fileInput = document.getElementById('csvFile');
  const statusDiv = document.getElementById('status');

  if (!url) { 
    alert('Please enter your Google Apps Script Web App URL'); 
    return; 
  }
  if (!fileInput.files[0]) { 
    alert('Please select a CSV file'); 
    return; 
  }

  statusDiv.style.color = '#0052cc';
  statusDiv.innerText = 'Reading file & uploading...';

  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.onload = async function(e) {
    const lines = e.target.result.split(/\r\n|\n/);
    let searchTerms = [];
    let searchTermColIndex = -1;

    // Find 'Search term' column dynamically & parse rows
    lines.forEach((line, index) => {
      let cleaned = line.trim();
      if (!cleaned) return;

      let cells = cleaned.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/).map(c => c.replace(/^"|"$/g, '').trim());

      if (searchTermColIndex === -1) {
        let colIdx = cells.findIndex(header => header.toLowerCase() === 'search term');
        if (colIdx !== -1) {
          searchTermColIndex = colIdx;
        }
      } else {
        if (cells[searchTermColIndex]) {
          searchTerms.push(cells[searchTermColIndex]);
        }
      }
    });

    if (searchTerms.length === 0) {
      statusDiv.style.color = '#dc3545';
      statusDiv.innerText = "Error: 'Search term' column not found or file is empty.";
      return;
    }

    try {
      // Sending payload to Google Apps Script
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ searchTerms: searchTerms })
      });

      const result = await response.json();
      if (result.status === 'success') {
        statusDiv.style.color = '#28a745';
        statusDiv.innerText = `Successfully uploaded ${searchTerms.length} terms! Now run script.py locally.`;
      } else {
        throw new Error(result.message);
      }
    } catch (err) {
      statusDiv.style.color = '#dc3545';
      statusDiv.innerText = 'Error: ' + err.message;
    }
  };

  reader.readAsText(file);
}