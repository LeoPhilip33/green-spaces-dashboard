<template>
  <div class="d-flex">
    <NavBar />
    <div class="app-content flex-grow-1">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar
  },
}
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

.app-content{
  margin-left: 7rem;
}
</style>