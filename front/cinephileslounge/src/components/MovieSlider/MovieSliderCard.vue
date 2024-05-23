<template>
  <li class="card-container">
    <img
      @click="navigateToDetail(movie.movie_id)"
      class="card-movie-img"
      :src="`https://image.tmdb.org/t/p/w1280/${movie.poster_path}`"
      alt=""
    />
  </li>
</template>
<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
defineProps({
  movie: Object,
});

// 더보기 버튼 click -> 디테일 뷰로 이동
const navigateToDetail = (movieId) => {
  router.push({
    name: "MovieDetailView",
    params: { movie_id: movieId },
  });
};
</script>
<style scoped>
.card-container .card-movie-img {
  width: 190px;
  min-height: 285px;
  margin: 0px 6px;
  border-radius: 5px;
  transition: 0.3s;
  cursor: pointer;
  object-fit: cover;
}
.card-container .card-movie-img:hover {
  transform: scale(1.1);
  z-index: 1;
  filter: brightness(0.7);
}
</style>
