<template>
  <button
    class="container-filter p-2 border rounded"
    :class="{ active: isActive }"
    @click="toggleActive"
    :style="{ backgroundColor: isActive ? color : '' }"
  >
    <p class="mb-0">{{ filterName }}</p>
  </button>
</template>

<script>
export default {
  name: 'FilterComponent',
  props: {
    filterName: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isActive: this.modelValue,
    };
  },
  watch: {
    modelValue(newValue) {
      this.isActive = newValue;
    },
  },
  methods: {
    toggleActive() {
      this.isActive = !this.isActive;
      this.$emit('update:modelValue', this.isActive);
      this.$emit('change', this.isActive);
    },
  },
};
</script>

<style scoped>
.container-filter {
  &:hover {
    background-color: red;
  }

  &.active {
    color: white;
  }

  p {
    font-size: 0.8rem;
  }
}
</style>