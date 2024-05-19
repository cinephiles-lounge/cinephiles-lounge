<template>
  <div class="upcoming-container">
    <h1>개봉 예정작</h1>
    <vueper-slides
      :loop="true"
      :touchable="false"
      class="no-shadow slides"
      :visible-slides="7"
      slide-multiple
      :gap="2"
      :infinite="true"
      :bullets="false"
      :arrows-outside="false"
      :slide-ratio="1 / 5"
      transition-speed="700"
      :breakpoints="{ 800: { visibleSlides: 2, slideMultiple: 2 } }"
    >
      <vueper-slide
        class="slide"
        v-for="movie in movies"
        :key="movie.id"
        :image="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        style="width: 200px; height: 280px"
        @click="
          router.push({
            name: 'MovieDetailView',
            params: { movie_id: movie.movie_id },
          })
        "
      />
    </vueper-slides>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/movie.js";
import { useRouter } from "vue-router";
import { VueperSlides, VueperSlide } from "vueperslides";
import "vueperslides/dist/vueperslides.css";
import axios from "axios";
const movieStore = useMovieStore();
const movies = ref(null);
const router = useRouter();
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
  padding: 38px 50px;
  background-color: #948176;
}
.upcoming-container h1 {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  line-height: 26px;
  margin-bottom: 10px;
  margin-left: 10px;
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

  filter: brightness(60%);
}
</style>
