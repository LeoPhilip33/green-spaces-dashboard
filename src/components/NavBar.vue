<template>
  <nav class="navbar position-fixed navbar-expand-lg navbar-light bg-light flex-column vh-100">
    <a class="navbar-brand" href="#">
      <img src="../assets/logo.png" class="d-inline-block align-top" alt="">
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav flex-column">
        <li class="nav-item">
          <router-link class="nav-link" to="/" exact>Carte</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/statistics">Statistics</router-link>
        </li>
      </ul>
    </div>
    <small class="mt-auto p-3 text-center">
      <p class="mb-0">philipleopro@mail.com</p>
      <p class="mb-0">06.37.25.99.14</p>
    </small>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
};
</script>

<style scoped>
.navbar {
  width: 10rem;
}

.navbar-brand img {
  width: 100px;
}

.router-link-active {
  font-weight: bold;
  color: #007bff;
}

.mt-auto {
  margin-top: auto;
}
</style>