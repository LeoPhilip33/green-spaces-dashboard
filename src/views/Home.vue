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
          <div v-if="filters.trees" class="ms-3">
            <FilterComponent :filterName="'Arbres à feuilles caduques'" :color="colors.deciduous" v-model="filters.deciduous" @change="updateMapLayers" />
            <FilterComponent :filterName="'Arbres à feuilles larges'" :color="colors.broadleaved" v-model="filters.broadleaved" @change="updateMapLayers" />
            <FilterComponent :filterName="'Arbres à feuilles d\'aiguilles'" :color="colors.needleleaved" v-model="filters.needleleaved" @change="updateMapLayers" />
          </div>
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
import { COLORS, FILTERS } from '@/config.js';

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
      geojsonData: null,
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
          style: 'mapbox://styles/philipleo/cm37lqs4w00gd01pd29tg4txb',
          center: [2.3522, 48.8566],
          zoom: 12,
        });

        this.map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

        this.map.on('load', () => {
          this.updateMapLayers();

          const layers = ['parksLayer', 'gardensLayer', 'playgroundsLayer', 'pitchesLayer', 'forestsLayer', 'woodsLayer', 'unclustered-point'];
          layers.forEach(layer => {
            this.map.on('click', layer, (e) => {
              this.showPopup(e);
            });
          });
        });
            })
            .catch(error => {
        console.error('Error loading GeoJSON data:', error);
            });
  },
  methods: {
    updateMapLayers() {
      if (!this.geojsonData) {
        return;
      }

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
            'circle-color': this.colors.trees,
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
            'circle-color': this.colors.trees,
            'circle-radius': 10,
          },
        });
      } else {
        FILTERS.forEach(filter => {
          if (this.filters[filter.key]) {
            const data = {
              type: 'FeatureCollection',
              features: this.geojsonData[0].features.filter(feature => feature.properties[filter.property] === filter.value)
            };

            this.map.addSource(`${filter.key}Source`, {
              type: 'geojson',
              data: data,
            });

            this.map.addLayer({
              id: `${filter.key}Layer`,
              type: 'fill',
              source: `${filter.key}Source`,
              layout: {},
              paint: {
                'fill-color': this.colors[filter.key],
                'fill-opacity': 0.5,
              },
            });
          }
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