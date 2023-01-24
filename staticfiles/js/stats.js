const renderChart =(data, labels) => {
    const ctx = document.getElementById('myChart');
  
    new Chart(ctx, {
        type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            label: 'Amount spent',
            data: data,
            backgroundColor: //[]
            [
                'teal',
                'green',
                'yellow',
                'blue',
                'red',
                'magenta',
            ],
           
            borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          },
          title:{
            display:true,
            text:'Expenses sorted by Category'
          }
      }
    });
}               
const getChartData=() => {
    fetch('/stats')
    .then((res)=>res.json())
    .then((results) => {
        const category_data = results.final_data;
        console.log(category_data)
        const [labels, data] = [
            Object.keys(category_data),
            Object.values(category_data)
        ]
        renderChart(data, labels)
    })
}
document.onload=getChartData()