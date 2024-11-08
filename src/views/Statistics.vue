<template>
  <div class="container mt-4">
    <div class="row">
      <StatisticCard
        v-for="(value, key) in formattedStatistics"
        :key="key"
        :title="key"
        :value="value"
      />
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Statistics Chart</h5>
            <StatisticsChart :statistics="statistics" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import StatisticsChart from '@/components/StatisticsChart.vue';
import StatisticCard from '@/components/StatisticCard.vue';

export default {
  name: 'StatisticsPage',
  components: {
    StatisticsChart,
    StatisticCard,
  },
  data() {
    return {
      geojsonData: null,
      statistics: {
        totalParks: 0,
        totalGardens: 0,
        totalPlaygrounds: 0,
        totalPitches: 0,
        totalForests: 0,
        totalWoods: 0,
        totalTrees: 0,
        percentageDeciduous: 0,
        percentageBroadleaved: 0,
        percentageNeedleleaved: 0,
      },
    };
  },
  computed: {
    formattedStatistics() {
      return {
        'Parcs': this.statistics.totalParks,
        'Jardins': this.statistics.totalGardens,
        'Terrains de jeux': this.statistics.totalPlaygrounds,
        'Terrains': this.statistics.totalPitches,
        'Forêts': this.statistics.totalForests,
        'Bois': this.statistics.totalWoods,
        'Arbres': this.statistics.totalTrees,
        'Arbres à feuilles caduques': `${this.statistics.percentageDeciduous}%`,
        'Arbres à feuilles larges': `${this.statistics.percentageBroadleaved}%`,
        'Arbres à feuilles d\'aiguilles': `${this.statistics.percentageNeedleleaved}%`,
      };
    },
  },
  mounted() {
    this.loadGeojsonData();
  },
  methods: {
    async loadGeojsonData() {
      try {
        const responses = await Promise.all([
          axios.get('/geojson/green_spaces_paris.geojson'),
          axios.get('/geojson/trees_paris.geojson'),
        ]);
        this.geojsonData = responses.map(response => response.data);
        this.calculateStatistics();
      } catch (error) {
        console.error('Error loading GeoJSON data:', error);
      }
    },
    calculateStatistics() {
      if (!this.geojsonData) {
        return;
      }

      const parks = this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'park').length;
      const gardens = this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'garden').length;
      const playgrounds = this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'playground').length;
      const pitches = this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'pitch').length;
      const forests = this.geojsonData[0].features.filter(feature => feature.properties.landuse === 'forest').length;
      const woods = this.geojsonData[0].features.filter(feature => feature.properties.natural === 'wood').length;
      const trees = this.geojsonData[1].features.length;
      const deciduousTrees = this.geojsonData[1].features.filter(feature => feature.properties.leaf_cycle === 'deciduous').length;
      const broadleavedTrees = this.geojsonData[1].features.filter(feature => feature.properties.leaf_type === 'broadleaved').length;
      const needleleavedTrees = this.geojsonData[1].features.filter(feature => feature.properties.leaf_type === 'needleleaved').length;

      this.statistics.totalParks = parks;
      this.statistics.totalGardens = gardens;
      this.statistics.totalPlaygrounds = playgrounds;
      this.statistics.totalPitches = pitches;
      this.statistics.totalForests = forests;
      this.statistics.totalWoods = woods;
      this.statistics.totalTrees = trees;
      this.statistics.percentageDeciduous = ((deciduousTrees / trees) * 100).toFixed(2);
      this.statistics.percentageBroadleaved = ((broadleavedTrees / trees) * 100).toFixed(2);
      this.statistics.percentageNeedleleaved = ((needleleavedTrees / trees) * 100).toFixed(2);
    },
  },
};
</script>

<style scoped>
.card {
  margin-bottom: 1rem;
}
</style>