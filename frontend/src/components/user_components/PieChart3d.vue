<template>
    <div class="chart-container">
      <canvas ref="pieChart3D"></canvas>
    </div>
  </template>
  
  <script>
  import { Pie } from 'vue-chartjs';
  import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
  
  Chart.register(ArcElement, Tooltip, Legend);
  
  export default {
    name: 'PieChart3D',
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
          labels: Object.keys(this.sectionInfo),
          datasets: [
            {
              label: 'Books per Section',
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
              data: Object.values(this.sectionInfo),
              borderWidth: 1,
              borderColor: '#333',
              hoverBorderColor: '#000',
              hoverOffset: 20, // This increases the hover effect to give a 3D-like pop effect
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
          elements: {
            arc: {
              borderWidth: 2,
              borderColor: 'rgba(0,0,0,0.1)',
              hoverBorderColor: 'rgba(0,0,0,0.3)',
              hoverOffset: 10, // Increase the shadow effect on hover
            },
          },
        };
  
        new Chart(this.$refs.pieChart3D, {
          type: 'pie',
          data: data,
          options: options,
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .pie-chart-3d {
    background-color: aliceblue;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Adding shadow for 3D effect */
  }
  .chart-container {
    position: relative;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }
  
  canvas {
    display: block;
    width: 100%;
    height: auto;
  }
  
  /* Additional styling for better appearance */
  .chart-container {
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  </style>
  