<template>
  <div class="chart-container">
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: 'BarChart',
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
          },
        ],
      };

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      };

      new Chart(this.$refs.barChart, {
        type: 'bar',
        data: data,
        options: options,
      });
    },
  },
};
</script>

<style scoped>
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
