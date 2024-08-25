<template>
  <div class="chart-container">
    <canvas ref="pieChart"></canvas>
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';

Chart.register(ArcElement, Tooltip, Legend);

export default {
  name: 'PieChart',
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
      if (this.chart) {
        this.chart.destroy(); // Destroy previous chart instance
      }

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
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 20,
              padding: 15,
            },
          },
        },
      };

      this.chart = new Chart(this.$refs.pieChart, {
        type: 'pie',
        data: data,
        options: options,
      });
    },
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.destroy(); // Clean up chart instance
    }
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
