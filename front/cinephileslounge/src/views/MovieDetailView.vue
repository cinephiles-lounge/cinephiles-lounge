<template>
  <div class="detail-container">
    <iframe
      class="movie-video"
      width="1200"
      height="530"
      :src="`https://www.youtube.com/embed/${movieStore.movie.trailer_key}?autoplay=1&controls=0&loop=1&playlist=${movieStore.movie.trailer_key}&mute=1`"
      allow="autoplay"
      allowfullscreen
    ></iframe>
    <h1>{{ movieStore.movie }}</h1>
    <h1>{{ movieStore.movie.title }}</h1>
    <p>{{ genres }}</p>
    <p>{{ movieStore.movie.release_date }}</p>
    <p>{{ movieStore.movie.overview }}</p>
    <p v-if="movieStore.movie.vote_average">
      {{ movieStore.movie.vote_average }}
    </p>
    <img
      :src="`https://image.tmdb.org/t/p/w1280/${movieStore.movie.poster_path}`"
      width="150px"
      height="200px"
    />
    <MovieDetailList :shortReviews="movieStore.movie.shortreview_set" />
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useMovieStore } from "@/stores/movie";
import MovieDetailList from "@/components/MovieDetailList.vue";
const movieStore = useMovieStore();
const route = useRoute();
const movieId = ref(route.params.movie_id);
const genres = movieStore.movie.genres.map((item) => item.name).join("  "); // 장르 이름만 뽑아서 공백으로 구분
movieStore.getMovieDetail(movieId.value);
</script>
<style scoped>
.detail-container {
  padding-top: 50px;
}
</style>
