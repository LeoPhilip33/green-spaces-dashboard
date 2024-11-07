<template>
    <div>
        <h1>Statistics</h1>
        <p>Total Parks: {{ statistics.totalParks }}</p>
        <p>Total Gardens: {{ statistics.totalGardens }}</p>
        <p>Total Playgrounds: {{ statistics.totalPlaygrounds }}</p>
        <p>Total Pitches: {{ statistics.totalPitches }}</p>
        <p>Total Forests: {{ statistics.totalForests }}</p>
        <p>Total Woods: {{ statistics.totalWoods }}</p>
        <p>Total Trees: {{ statistics.totalTrees }}</p>
        <p>Percentage of Deciduous Trees: {{ statistics.percentageDeciduous }}%</p>
        <p>Percentage of Broadleaved Trees: {{ statistics.percentageBroadleaved }}%</p>
        <p>Percentage of Needleleaved Trees: {{ statistics.percentageNeedleleaved }}%</p>
    </div>

    <StatisticsChart :statistics="statistics" />
</template>

<script>
import axios from 'axios';
import StatisticsChart from '@/components/StatisticsChart.vue';

export default {
  name: 'StatisticsPage',
  components: {
    StatisticsChart,
  },
  data() {
    return {
      map: null,
      geojsonData: null,
      filters: {
        parks: false,
        gardens: false,
        playgrounds: false,
        pitches: false,
        forests: false,
        woods: false,
        trees: false,
        deciduous: false,
        broadleaved: false,
        needleleaved: false,
      },
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
  }
};
</script>

<style scoped></style>