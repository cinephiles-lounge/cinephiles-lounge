<template>
  <div class="upcoming-container">
    <h1>개봉 예정작</h1>
    <vueper-slides
      :loop="true"
      :touchable="false"
      class="no-shadow slides"
      :visible-slides="10"
      slide-multiple
      :gap="1"
      :infinite="true"
      :bullets="false"
      :arrows-outside="false"
      :slide-ratio="1 / 8"
      :breakpoints="{ 800: { visibleSlides: 2, slideMultiple: 2 } }"
    >
      <vueper-slide
        class="slide"
        v-for="movie in movies"
        :key="movie.id"
        :image="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        style="width: 160px; height: 220px"
        @click="console.log(movie.id)"
      />
    </vueper-slides>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/movie.js";
import { VueperSlides, VueperSlide } from "vueperslides";
import "vueperslides/dist/vueperslides.css";
import axios from "axios";

const movieStore = useMovieStore();
const movies = ref(null);
axios({
  methods: "get",
  url: `${movieStore.API_URL}/movies/upcoming/`,
})
  .then((res) => {
    movies.value = res.data;
  })
  .catch((err) => {
    console.log(err);
  });
</script>
<style scoped>
.upcoming-container {
  padding: 38px 80px;
  background-color: #948176;
}
.upcoming-container h1 {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  line-height: 26px;
  margin-bottom: 10px;
  margin-left: 20px;
}
.vueperslide--visible {
  border-radius: 5px;
  object-fit: cover;
}
.slide {
  transition: 0.5s;
}

.slide:hover {
  z-index: 1;
  transform: scale(1.25);
  box-shadow: 0 25px 40px rgba(0, 0, 0, 1.5);
  filter: brightness(60%);
}
</style>
