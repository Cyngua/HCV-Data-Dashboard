document.addEventListener('DOMContentLoaded', function() {
    // Function to populate column names dropdown based on hcvData
    function populateColumnNames() {
      const columnNameDropdown = document.getElementById('columnName');
      
      // Clear previous options
      columnNameDropdown.innerHTML = '';
      
      // Get column names from hcvData and populate dropdown
      const columns = Object.keys(hcvData[0]); // Assuming the first element holds column names
      columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.text = column;
        columnNameDropdown.appendChild(option);
      });
    }
  
    function plotGraph() {
        const selectedColumnName = document.getElementById('columnName').value;
        const selectedOtherName = document.getElementById('otherName').value;
      
        // Extract selected column data for plotting
        const xData = hcvData.map(row => row[selectedColumnName]);
        const yData = hcvData.map(row => row[selectedOtherName]);
      
        // Check if both selected columns are the same for histogram creation
        if (selectedColumnName === selectedOtherName) {
          createHistogramPlot(xData);
        } else {
          createScatterPlot(xData, yData, selectedColumnName, selectedOtherName);
        }
        // Add more conditions for other plot types if needed
      }
  
    // Function to create a scatter plot using Plotly
    function createScatterPlot(xData, yData, selectedColumnName, selectedOtherName) {
      const trace = {
        x: xData,
        y: yData,
        mode: 'markers',
        type: 'scatter',
        marker: { size: 8 }
      };
  
      const layout = {
        title: 'Scatter Plot',
        xaxis: { title: selectedColumnName },
        yaxis: { title: selectedOtherName }
        // Additional layout configurations
      };
  
      const plotData = [trace];
      Plotly.newPlot('plot', plotData, layout);
    }
  
    // Function to create a histogram using Plotly
    function createHistogramPlot(data) {
        const trace = {
          x: data,
          type: 'histogram'
        };
    
        const layout = {
          title: 'Histogram',
          xaxis: { title: 'Value' },
          yaxis: { title: 'Frequency' }
          // Additional layout configurations
        };
    
        const plotData = [trace];
        Plotly.newPlot('plot', plotData, layout);
    }
  
    // Initialize the column names dropdown on page load
    populateColumnNames();
  
    // Event listener for the "Plot" button
    const plotButton = document.querySelector('#plotButton');
    if (plotButton) {
      plotButton.addEventListener('click', plotGraph);
    }
  
});
  