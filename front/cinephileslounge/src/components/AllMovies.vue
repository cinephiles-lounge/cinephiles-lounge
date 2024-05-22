<template>
  <li class="movie-img">
    <img
      @click="isSelected = !isSelected"
      :class="{ selected: isSelected }"
      :src="`https://image.tmdb.org/t/p/w1280/${movie.poster_path}`"
      alt=""
    />
  </li>
</template>

<script setup>
import { ref } from "vue";
defineProps({
  movie: Object,
});
const isSelected = ref(false);
</script>

<style scoped>
.movie-img img {
  width: 190px;
  height: 280px;
  border-radius: 5px;
  transition: 0.3s;
  cursor: pointer;
  filter: brightness(0.5);
}
.movie-img:hover {
  transform: scale(1.2);
  z-index: 1;
}
.movie-img img.selected {
  filter: none;
  border: 1px solid #eee;
}
</style>
