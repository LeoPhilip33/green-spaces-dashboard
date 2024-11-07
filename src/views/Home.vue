<template>
  <div>
    <h1>Home</h1>
    <p>Welcome to the Home page!</p>
    <div>
      <label>
        <input type="checkbox" v-model="filters.parks" @change="updateMapLayers"> Parks
      </label>
      <label>
        <input type="checkbox" v-model="filters.gardens" @change="updateMapLayers"> Gardens
      </label>
      <label>
        <input type="checkbox" v-model="filters.playgrounds" @change="updateMapLayers"> Playgrounds
      </label>
      <label>
        <input type="checkbox" v-model="filters.pitches" @change="updateMapLayers"> Pitches
      </label>
      <label>
        <input type="checkbox" v-model="filters.forests" @change="updateMapLayers"> Forests
      </label>
      <label>
        <input type="checkbox" v-model="filters.woods" @change="updateMapLayers"> Woods
      </label>
      <label>
        <input type="checkbox" v-model="filters.trees" @change="updateMapLayers"> Trees
      </label>
      <label>
        <input type="checkbox" v-model="filters.deciduous" @change="updateMapLayers"> Deciduous Trees
      </label>
      <label>
        <input type="checkbox" v-model="filters.broadleaved" @change="updateMapLayers"> Broadleaved Trees
      </label>
      <label>
        <input type="checkbox" v-model="filters.needleleaved" @change="updateMapLayers"> Needleleaved Trees
      </label>
    </div>
    <div id="map" style="height: 500px; width: 100%;"></div>
    <div>
      <h2>Statistics</h2>
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
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import axios from 'axios';
import StatisticsChart from '@/components/StatisticsChart.vue';

export default {
  name: 'HomePage',
  components: {
    StatisticsChart,
  },
  data() {
    return {
      map: null,
      geojsonData: [],
      filters: {
        parks: true,
        gardens: true,
        playgrounds: true,
        pitches: true,
        forests: true,
        woods: true,
        trees: true,
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
    mapboxgl.accessToken = 'pk.eyJ1IjoicGhpbGlwbGVvIiwiYSI6ImNtMzc4NGI0bjBldzEybXNmN2ltb2F3ZDEifQ._Zl6AnfQY1xmGDIsTTihMA';

    const geojsonFiles = [
      '/geojson/green_spaces_paris.geojson',
      '/geojson/trees_paris.geojson'
    ];

    const geojsonPromises = geojsonFiles.map(file => axios.get(file));

    Promise.all(geojsonPromises)
      .then(responses => {
        this.geojsonData = responses.map(response => response.data);

        this.calculateStatistics();

        this.map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/mapbox/light-v10',
          center: [2.3522, 48.8566],
          zoom: 12,
        });

        this.map.addControl(new mapboxgl.NavigationControl());

        this.map.on('load', () => {
          this.updateMapLayers();
        });

        this.map.on('click', 'parksLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'gardensLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'playgroundsLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'pitchesLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'forestsLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'woodsLayer', (e) => {
          this.showPopup(e);
        });

        this.map.on('click', 'unclustered-point', (e) => {
          this.showPopup(e);
        });
      })
      .catch(error => {
        console.error('Error loading GeoJSON data:', error);
      });
  },
  methods: {
    calculateStatistics() {
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
    updateMapLayers() {
      const layers = ['parksLayer', 'gardensLayer', 'playgroundsLayer', 'pitchesLayer', 'forestsLayer', 'woodsLayer', 'clusters', 'cluster-count', 'unclustered-point'];
      const sources = ['parksSource', 'gardensSource', 'playgroundsSource', 'pitchesSource', 'forestsSource', 'woodsSource', 'treesSource'];

      layers.forEach(layer => {
        if (this.map.getLayer(layer)) {
          this.map.removeLayer(layer);
        }
      });

      sources.forEach(source => {
        if (this.map.getSource(source)) {
          this.map.removeSource(source);
        }
      });

      if (this.filters.parks) {
        const parksData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'park')
        };

        this.map.addSource('parksSource', {
          type: 'geojson',
          data: parksData,
        });

        this.map.addLayer({
          id: 'parksLayer',
          type: 'fill',
          source: 'parksSource',
          layout: {},
          paint: {
            'fill-color': '#008000',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.gardens) {
        const gardensData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'garden')
        };

        this.map.addSource('gardensSource', {
          type: 'geojson',
          data: gardensData,
        });

        this.map.addLayer({
          id: 'gardensLayer',
          type: 'fill',
          source: 'gardensSource',
          layout: {},
          paint: {
            'fill-color': '#FFD700',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.playgrounds) {
        const playgroundsData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'playground')
        };

        this.map.addSource('playgroundsSource', {
          type: 'geojson',
          data: playgroundsData,
        });

        this.map.addLayer({
          id: 'playgroundsLayer',
          type: 'fill',
          source: 'playgroundsSource',
          layout: {},
          paint: {
            'fill-color': '#FF4500',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.pitches) {
        const pitchesData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.leisure === 'pitch')
        };

        this.map.addSource('pitchesSource', {
          type: 'geojson',
          data: pitchesData,
        });

        this.map.addLayer({
          id: 'pitchesLayer',
          type: 'fill',
          source: 'pitchesSource',
          layout: {},
          paint: {
            'fill-color': '#1E90FF',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.forests) {
        const forestsData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.landuse === 'forest')
        };

        this.map.addSource('forestsSource', {
          type: 'geojson',
          data: forestsData,
        });

        this.map.addLayer({
          id: 'forestsLayer',
          type: 'fill',
          source: 'forestsSource',
          layout: {},
          paint: {
            'fill-color': '#228B22',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.woods) {
        const woodsData = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties.natural === 'wood')
        };

        this.map.addSource('woodsSource', {
          type: 'geojson',
          data: woodsData,
        });

        this.map.addLayer({
          id: 'woodsLayer',
          type: 'fill',
          source: 'woodsSource',
          layout: {},
          paint: {
            'fill-color': '#8B4513',
            'fill-opacity': 0.5,
          },
        });
      }

      if (this.filters.trees) {
        let treesData = this.geojsonData[1].features;

        if (this.filters.deciduous) {
          treesData = treesData.filter(feature => feature.properties.leaf_cycle === 'deciduous');
        }

        if (this.filters.broadleaved) {
          treesData = treesData.filter(feature => feature.properties.leaf_type === 'broadleaved');
        }

        if (this.filters.needleleaved) {
          treesData = treesData.filter(feature => feature.properties.leaf_type === 'needleleaved');
        }

        this.map.addSource('treesSource', {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: treesData,
          },
          cluster: true,
          clusterMaxZoom: 14,
          clusterRadius: 50,
        });

        this.map.addLayer({
          id: 'clusters',
          type: 'circle',
          source: 'treesSource',
          filter: ['has', 'point_count'],
          paint: {
            'circle-color': '#51bbd6',
            'circle-radius': [
              'step',
              ['get', 'point_count'],
              20,
              100,
              30,
              750,
              40
            ],
          },
        });

        this.map.addLayer({
          id: 'cluster-count',
          type: 'symbol',
          source: 'treesSource',
          filter: ['has', 'point_count'],
          layout: {
            'text-field': '{point_count_abbreviated}',
            'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
            'text-size': 12,
          },
        });

        this.map.addLayer({
          id: 'unclustered-point',
          type: 'circle',
          source: 'treesSource',
          filter: ['!', ['has', 'point_count']],
          paint: {
            'circle-color': '#00FF00',
            'circle-radius': 3,
          },
        });
      }
    },
    showPopup(e) {
      const coordinates = e.features[0].geometry.coordinates;
      const properties = e.features[0].properties;

      let lngLat;
      if (Array.isArray(coordinates[0])) {
        lngLat = coordinates[0][0];
      } else {
        lngLat = coordinates;
      }

      if (lngLat.length === 2 && !isNaN(lngLat[0]) && !isNaN(lngLat[1])) {
        let description = '<strong>Details:</strong><br>';
        for (const key in properties) {
          description += `${key}: ${properties[key]}<br>`;
        }

        new mapboxgl.Popup()
          .setLngLat(lngLat)
          .setHTML(description)
          .addTo(this.map);
      } else {
        console.error('Invalid coordinates:', lngLat);
      }
    },
  },
};
</script>

<style>
#map {
  height: 500px;
  width: 100%;
}
</style>