<template>
  <div>
    <canvas ref="statisticsChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'StatisticsChart',
  props: {
    statistics: Object,
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.renderChart();
  },
  watch: {
    statistics: {
      deep: true,
      handler() {
        if (this.chart) {
          this.chart.destroy();
        }
        this.renderChart();
      },
    },
  },
  methods: {
    renderChart() {
      this.$nextTick(() => {
        if (!this.statistics || !this.statistics.totalParks) {
          console.error('Statistics not available');
          return;
        }

        const ctx = this.$refs.statisticsChart?.getContext('2d');
        if (!ctx) {
          console.error('Canvas context not found');
          return;
        }

        this.chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Parks', 'Gardens', 'Playgrounds', 'Pitches', 'Forests', 'Woods', 'Trees'],
            datasets: [
              {
                label: 'Count',
                data: [
                  this.statistics.totalParks,
                  this.statistics.totalGardens,
                  this.statistics.totalPlaygrounds,
                  this.statistics.totalPitches,
                  this.statistics.totalForests,
                  this.statistics.totalWoods,
                  this.statistics.totalTrees,
                ],
                backgroundColor: [
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                  'rgba(75, 192, 192, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(255, 99, 132, 1)',
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
          },
        });
      });
    },
  },
};
</script>

<style scoped>
canvas {
  max-width: 100%;
}
</style>