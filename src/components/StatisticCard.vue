<template>
  <div class="col-md-4 mb-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatisticCard',
  props: {
    title: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
  },
};
</script>

<style scoped>
.card {
  margin-bottom: 1rem;
}
</style>