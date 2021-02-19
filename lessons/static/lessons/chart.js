const randomChartData = n => {
  let data = []

  for (let i = 0; i < n; i++) {
    data.push(Math.round(Math.random() * 2400))
  }

  return data
}


const monthlyData = n => {
  var result = JSON.parse(monthly_earnings);

  var values = Object.keys(result).map(function(key){
    return result[key];
  });

  return values;

}

const chartColors = {
  default: {
    primary: '#00D1B2',
    info: '#209CEE',
    danger: '#FF3860'
  }
}

const ctx = document.getElementById('big-line-chart').getContext('2d');

new Chart(ctx, {
  type: 'bar',
  data: {
    datasets: [
      {
        fill: false,
        borderColor: chartColors.default.primary,
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: chartColors.default.primary,
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: chartColors.default.primary,
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: monthlyData(12)
      },
    ],
    labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    responsive: true,
    tooltips: {
      backgroundColor: '#f5f5f5',
      titleFontColor: '#333',
      bodyFontColor: '#666',
      bodySpacing: 4,
      xPadding: 12,
      mode: 'nearest',
      intersect: 0,
      position: 'nearest'
    },
    scales: {
      yAxes: [{
        barPercentage: 1.6,
        gridLines: {
          drawBorder: false,
          color: 'rgba(29,140,248,0.0)',
          zeroLineColor: 'transparent'
        },
        ticks: {
          padding: 20,
          fontColor: '#9a9a9a'
        }
      }],

      xAxes: [{
        barPercentage: 1,
        gridLines: {
          drawBorder: false,
          color: 'rgba(225,78,202,0.1)',
          zeroLineColor: 'transparent'
        },
        ticks: {
          padding: 20,
          fontColor: '#9a9a9a'
        }
      }]
    }
  }
})
