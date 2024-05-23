<template>
  <li class="card-container">
    <img
      @click="navigateToDetail(movie.movie_id)"
      class="card-movie-img"
      :src="`https://image.tmdb.org/t/p/w1280/${movie.poster_path}`"
      alt=""
    />
    <div class="movie-label">새로운 콘텐츠</div>
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
.card-container {
  position: relative;
}
.card-container .card-movie-img:hover {
  transform: scale(1.1);
  z-index: 1;
  filter: brightness(0.7);
}
.movie-label {
  position: absolute;
  bottom: 3px;
  background-color: #eee;
  color: #000;
  z-index: 99;
  left: 50%; /* 부모의 왼쪽에서 50% 위치 */
  transform: translateX(-50%); /* 자신의 너비의 50%만큼 왼쪽으로 이동 */
  padding: 5px;
  width: 110px;
  text-align: center;
  border-radius: 3px;
  font-weight: 600;
}
</style>
