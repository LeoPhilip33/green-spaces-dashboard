<template>
  <div>
    <div class="d-flex gap-2">
      <FilterComponent :filterName="'Parks'" :color="'#084298'" v-model="filters.parks" @change="updateMapLayers" />
      <FilterComponent :filterName="'Gardens'" :color="'#084298'" v-model="filters.gardens" @change="updateMapLayers" />
      <FilterComponent :filterName="'Playgrounds'" :color="'#084298'" v-model="filters.playgrounds" @change="updateMapLayers" />
      <FilterComponent :filterName="'Pitches'" :color="'#084298'" v-model="filters.pitches" @change="updateMapLayers" />
      <FilterComponent :filterName="'Forests'" :color="'#084298'" v-model="filters.forests" @change="updateMapLayers" />
      <FilterComponent :filterName="'Woods'" :color="'#084298'" v-model="filters.woods" @change="updateMapLayers" />
      <FilterComponent :filterName="'Trees'" :color="'#084298'" v-model="filters.trees" @change="updateMapLayers" />
      <FilterComponent :filterName="'Deciduous Trees'" :color="'#084298'" v-model="filters.deciduous" @change="updateMapLayers" />
      <FilterComponent :filterName="'Broadleaved Trees'" :color="'#084298'" v-model="filters.broadleaved" @change="updateMapLayers" />
      <FilterComponent :filterName="'Needleleaved Trees'" :color="'#084298'" v-model="filters.needleleaved" @change="updateMapLayers" />
    </div>
    <div id="map"></div>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import axios from 'axios';
import FilterComponent from '@/components/FilterComponent.vue';

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

<style scoped>
#map {
  height: 100vh;
  width: 100%;
}
</style>