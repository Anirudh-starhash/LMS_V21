<template>
    <div class="scatter-plot">
      <canvas ref="scatterChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Scatter } from 'vue-chartjs';
  import { Chart, ScatterController, LinearScale, PointElement, Tooltip, Legend } from 'chart.js';
  
  Chart.register(ScatterController, LinearScale, PointElement, Tooltip, Legend);
  
  export default {
    name: 'ScatterPlot',
    props: {
      sectionInfo: {
        type: Object,
        required: true,
      },
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const data = {
          datasets: [
            {
              label: 'Books per Section',
              data: Object.keys(this.sectionInfo).map((key, index) => {
                return { x: index, y: this.sectionInfo[key] };
              }),
              backgroundColor: '#FF6384',
              pointBorderColor: '#36A2EB',
              pointBackgroundColor: '#FFCE56',
              pointBorderWidth: 2,
              pointRadius: 5,
            },
          ],
        };
  
        const options = {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
            },
            tooltip: {
              enabled: true,
            },
          },
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
            },
            y: {
              beginAtZero: true,
            },
          },
        };
  
        new Chart(this.$refs.scatterChart, {
          type: 'scatter',
          data: data,
          options: options,
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .scatter-plot {
    background-color: aliceblue;
    background-size: cover;
    background-position: center;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  }
  </style>
  