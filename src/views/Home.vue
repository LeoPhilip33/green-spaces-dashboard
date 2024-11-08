<template>
  <div>
    <div class="position-relative">
      <div class="position-absolute z-1 top-0 start-0 p-3">
        <div class="d-flex flex-wrap gap-2">
          <FilterComponent :filterName="'Parcs'" :color="colors.parks" :icon="'bi bi-bounding-box'" v-model="filters.parks" @change="updateMapLayers" />
          <FilterComponent :filterName="'Jardins'" :color="colors.gardens" :icon="'bi bi-flower1'" v-model="filters.gardens" @change="updateMapLayers" />
          <FilterComponent :filterName="'Terrains de jeux'" :color="colors.playgrounds" :icon="'bi bi-dice-1-fill'" v-model="filters.playgrounds" @change="updateMapLayers" />
          <FilterComponent :filterName="'Emplacements'" :color="colors.pitches" :icon="'bi bi-geo-alt-fill'" v-model="filters.pitches" @change="updateMapLayers" />
          <FilterComponent :filterName="'Forêts'" :color="colors.forests" :icon="'bi bi-signpost-2-fill'" v-model="filters.forests" @change="updateMapLayers" />
          <FilterComponent :filterName="'Bois'" :color="colors.woods" :icon="'bi bi-signpost-fill'" v-model="filters.woods" @change="updateMapLayers" />
          <FilterComponent :filterName="'Arbres'" :color="colors.trees" :icon="'bi bi-tree-fill'" v-model="filters.trees" @change="updateMapLayers" />
          <FilterComponent :filterName="'Arbres à feuilles caduques'" :color="colors.deciduous" v-model="filters.deciduous" @change="updateMapLayers" />
          <FilterComponent :filterName="'Arbres à feuilles larges'" :color="colors.broadleaved" v-model="filters.broadleaved" @change="updateMapLayers" />
          <FilterComponent :filterName="'Arbres à feuilles d\'aiguilles'" :color="colors.needleleaved" v-model="filters.needleleaved" @change="updateMapLayers" />
        </div>
      </div>
      <div id="map"></div>
    </div>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import axios from 'axios';
import FilterComponent from '@/components/FilterComponent.vue';

const COLORS = {
  parks: '#107026',
  gardens: '#ff8c20',
  playgrounds: '#0451d3',
  pitches: '#010a64',
  forests: '#1a9a7a',
  woods: '#904f0b',
  trees: '#049004',
  deciduous: '#049004',
  broadleaved: '#049004',
  needleleaved: '#049004',
};

const FILTERS = [
  { key: 'parks', property: 'leisure', value: 'park' },
  { key: 'gardens', property: 'leisure', value: 'garden' },
  { key: 'playgrounds', property: 'leisure', value: 'playground' },
  { key: 'pitches', property: 'leisure', value: 'pitch' },
  { key: 'forests', property: 'landuse', value: 'forest' },
  { key: 'woods', property: 'natural', value: 'wood' },
];

export default {
  name: 'HomePage',
  components: {
    FilterComponent
  },
  data() {
    return {
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
      colors: COLORS,
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
        this.initializeMap();
      })
      .catch(error => {
        console.error('Error loading GeoJSON data:', error);
      });
  },
  methods: {
    initializeMap() {
      this.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [2.3522, 48.8566],
        zoom: 12,
      });

      this.map.on('load', () => {
        this.updateMapLayers();
      });

      this.map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');
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

      FILTERS.forEach(filter => {
        this.addSourceAndLayer(filter.key, filter.property, filter.value, this.colors[filter.key]);
      });

      this.addClusterLayer('trees', this.colors.trees);
    },
    addSourceAndLayer(filterKey, propertyKey, propertyValue, color) {
      if (this.filters[filterKey]) {
        const data = {
          type: 'FeatureCollection',
          features: this.geojsonData[0].features.filter(feature => feature.properties[propertyKey] === propertyValue)
        };

        this.map.addSource(`${filterKey}Source`, {
          type: 'geojson',
          data: data,
        });

        this.map.addLayer({
          id: `${filterKey}Layer`,
          type: 'fill',
          source: `${filterKey}Source`,
          layout: {},
          paint: {
            'fill-color': color,
            'fill-opacity': 0.5,
          },
        });
      }
    },
    addClusterLayer(filterKey, color) {
      if (this.filters[filterKey]) {
        this.map.addSource('treesSource', {
          type: 'geojson',
          data: this.geojsonData[1],
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
            'circle-color': color,
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
  },
};
</script>

<style scoped>
#map {
  height: 100vh;
  width: 100%;
}
</style>