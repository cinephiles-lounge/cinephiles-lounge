<template>
  <div class="detail-container">
    <!-- <iframe
      class="movie-video"
      width="1200"
      height="530"
      :src="`https://www.youtube.com/embed/${movieStore.movie.trailer_key}?autoplay=1&controls=0&loop=1&playlist=${movieStore.movie.trailer_key}&mute=1`"
      allow="autoplay"
      allowfullscreen
    ></iframe> -->
    <h1>{{ movieStore.movie.title }}</h1>
    <i v-if="!isLiked" @click="movie_like" class="bx bx-heart"></i>
    <i v-if="isLiked" @click="movie_like" class="bx bxs-heart"></i>
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
    <MovieDetailList
      :shortReviews="movieStore.movie.shortreview_set"
      :movieId="movieStore.movie.movie_id"
    />
  </div>
</template>
<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useMovieStore } from "@/stores/movie";
import { useAccountStore } from "@/stores/account";
import MovieDetailList from "@/components/MovieDetailList.vue";
import axios from "axios";
const movieStore = useMovieStore();
const accountStore = useAccountStore();
const route = useRoute();
const movieId = ref(route.params.movie_id);
const genres = movieStore.movie.genres.map((item) => item.name).join("  "); // 장르 이름만 뽑아서 공백으로 구분
movieStore.getMovieDetail(movieId.value);

// 좋아요 눌렀는지 확인
const isLiked = computed(() => {
  if (!movieStore.movie.liked_users) return false;
  return movieStore.movie.liked_users.some(
    (user) => user.id === accountStore.userPk
  );
});

// 영화 좋아요
const movie_like = () => {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/movies/${movieStore.movie.movie_id}/like/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      console.log("좋아요 성공");
      if (movieStore.movie.liked_users) {
        const userIndex = movieStore.movie.liked_users.findIndex(
          (user) => user.id === accountStore.userPk
        );
        if (userIndex > -1) {
          movieStore.movie.liked_users.splice(userIndex, 1);
        } else {
          movieStore.movie.liked_users.push({
            id: accountStore.userPk,
            username: accountStore.username,
          });
        }
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>
<style scoped>
.detail-container {
  padding-top: 50px;
}
</style>
