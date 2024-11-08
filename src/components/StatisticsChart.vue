<template>
  <div>
    <canvas ref="statisticsChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import { COLORS } from '@/config.js';

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
        const ctx = this.$refs.statisticsChart?.getContext('2d');
        if (!ctx) {
          console.error('Canvas context not found');
          return;
        }
        this.chart = new Chart(ctx, {
          type: 'doughnut',
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
                COLORS.parks,
                  COLORS.gardens,
                  COLORS.playgrounds,
                  COLORS.pitches,
                  COLORS.forests,
                  COLORS.woods,
                  COLORS.trees,
                ],
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Répartition des espaces verts',
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
  max-height: 30rem;
}
</style>