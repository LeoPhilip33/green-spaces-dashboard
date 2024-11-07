<template>
  <div>
    <h1>Home</h1>
    <p>Welcome to the Home page!</p>
    <div id="map"></div>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      map: null,
      geojsonData: [],
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
          this.geojsonData.forEach((data, index) => {
            this.map.addSource(`geojsonSource${index}`, {
              type: 'geojson',
              data: data,
            });

            this.map.addLayer({
              id: `geojsonLayer${index}`,
              type: index === 0 ? 'fill' : 'circle',
              source: `geojsonSource${index}`,
              layout: {},
              paint: index === 0 ? {
                'fill-color': '#008000',
                'fill-opacity': 0.5,
              } : {
                'circle-radius': 3,
                'circle-color': '#00FF00',
              },
            });
          });
        });
      })
      .catch(error => {
        console.error('Error loading GeoJSON data:', error);
      });
  },
};
</script>

<style>
#map {
    height: 500px;
    width: 100%;
}
</style>