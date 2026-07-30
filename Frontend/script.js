function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Word Analysis')
    .addItem('Run One Word Analysis', 'runOneWordAnalysis')
    .addToUi();
}

function runOneWordAnalysis() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var data = sheet.getDataRange().getValues();
  
  if (data.length <= 1) return;
  
  var wordMap = {};
  
  for (var i = 1; i < data.length; i++) {
    var searchTerm = String(data[i][0]).toLowerCase().trim();
    var impressions = Number(data[i][1]) || 0;
    var clicks = Number(data[i][2]) || 0;
    var conversions = Number(data[i][3]) || 0;
    var cost = Number(data[i][4]) || 0;
    var convValue = Number(data[i][5]) || 0;
    
    if (!searchTerm) continue;
    
    var words = searchTerm.split(/\s+/);
    var uniqueWordsInRow = {};
    
    for (var j = 0; j < words.length; j++) {
      var word = words[j].replace(/[^a-zA-Z0-9]/g, '');
      if (word.length > 0 && !uniqueWordsInRow[word]) {
        uniqueWordsInRow[word] = true;
        
        if (!wordMap[word]) {
          wordMap[word] = {
            impressions: 0,
            clicks: 0,
            conversions: 0,
            cost: 0,
            convValue: 0
          };
        }
        
        wordMap[word].impressions += impressions;
        wordMap[word].clicks += clicks;
        wordMap[word].conversions += conversions;
        wordMap[word].cost += cost;
        wordMap[word].convValue += convValue;
      }
    }
  }
  
  var headers = [
    "#", "SEARCH TERM", "IMPRESSIONS", "CLICKS", "CONVERSIONS", 
    "COST", "CONVERSION VALUE", "ROAS", "CTR", "CPC", "COST PER CONVERSION"
  ];
  
  var outputData = [headers];
  var index = 1;
  
  for (var w in wordMap) {
    var item = wordMap[w];
    var roas = item.cost > 0 ? (item.convValue / item.cost) : 0;
    var ctr = item.impressions > 0 ? (item.clicks / item.impressions) : 0;
    var cpc = item.clicks > 0 ? (item.cost / item.clicks) : 0;
    var costPerConv = item.conversions > 0 ? (item.cost / item.conversions) : 0;
    
    outputData.push([
      index++,
      w,
      item.impressions,
      item.clicks,
      item.conversions,
      item.cost,
      item.convValue,
      roas,
      ctr,
      cpc,
      costPerConv
    ]);
  }
  
  var newSS = SpreadsheetApp.create("Word_Part_Analysis_Report");
  var newSheet = newSS.getActiveSheet();
  
  newSheet.getRange(1, 1, outputData.length, headers.length).setValues(outputData);
  
  newSheet.getRange(2, 3, outputData.length - 1, 3).setNumberFormat("#,##0");
  newSheet.getRange(2, 6, outputData.length - 1, 2).setNumberFormat("$#,##0.00");
  newSheet.getRange(2, 8, outputData.length - 1, 1).setNumberFormat("0.00");
  newSheet.getRange(2, 9, outputData.length - 1, 1).setNumberFormat("0.00%");
  newSheet.getRange(2, 10, outputData.length - 1, 2).setNumberFormat("$#,##0.00");
  
  newSheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
  
  var htmlOutput = HtmlService
    .createHtmlOutput('<p>Original data se fetch karke nayi file bana di gayi hai:</p><p><a href="' + newSS.getUrl() + '" target="_blank"><b>Open New Analysis File</b></a></p>')
    .setWidth(350)
    .setHeight(120);
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, 'Analysis Complete');
}
