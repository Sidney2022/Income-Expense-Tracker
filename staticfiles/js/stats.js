const selectIncomeRange = document.getElementById('income-form')
const IncomeForm = document.getElementById('form-field')
const expenseForm = document.getElementById('expense-form')
const  selectExpenseRange = document.getElementById('expense-select-field')


const renderChart1 = (data, labels) => {
  const ctx = document.getElementById('myChart1');

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Amount Earned",
          data: data,
          //[]
          backgroundColor: [
            "teal",
            "green",
            "yellow",
            "blue",
            "red",
            "magenta",
          ],

          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      title: {
        display: true,
        text: "Income sorted by Sources",
      },
    },
  });
};

const renderChart2 = (data, labels) => {
  const ctx = document.getElementById('myChart2');

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Amount spent",
          data: data,
          //[]
          backgroundColor: [
            "teal",
            "green",
            "yellow",
            "blue",
            "red",
            "magenta",
          ],

          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      title: {
        display: true,
        text: "Expenses sorted by Category",
      },
    },
  });
};
const getChartData = () => {
  fetch("/income/stats")
    .then((res) => res.json())
    .then((results) => {
      const category_data = results.final_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      renderChart1(data, labels);
    });

  fetch("/expense/stats")
    .then((res) => res.json())
    .then((results) => {
      const category_data = results.final_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      renderChart2(data, labels);
    });
};
document.onload = getChartData();


IncomeForm.addEventListener('submit',  (e) => {
  e.preventDefault()
  fetch('/income/stats', {
    headers : { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
     },
    body : JSON.stringify({ time_range : selectIncomeRange.value }),
    method : 'POST'
  })
  .then(res => res.json()) 
  .then((results) => {
    console.log(results)
        const category_data = results.final_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
        renderChart1(data, labels);
      });      
    
})

expenseForm.addEventListener('submit',  (e) => {
  e.preventDefault()
  fetch('/expense/stats', {
    headers : { 
      'Content-Type': 'application/json',
      'Accept': 'application/json'
     },
    body : JSON.stringify({ time_range : selectExpenseRange.value }),
    method : 'POST'
  })
  .then(res => res.json()) 
  .then((results) => {
    console.log(results)
        const category_data = results.final_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
        renderChart2(data, labels);
      });      
    
})
