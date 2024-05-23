<template>
  <div class="movie-container">
    <h1 class="weather-message">{{ movieStore.weatherRecommendMovies.weather_message }} <br>
      오늘같은 날엔 이런 영화 어떠세요?
    </h1>
    <div class="movie-wrapper">
      <ul>
        <li v-for="movie in movieStore.weatherRecommendMovies.recommended_movies">
          <img
            class="liked-movie-img"
            @click="
              router.push({
                name: 'MovieDetailView',
                params: { movie_id: movie.movie_id },
              })
            "
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          />
        </li>
      </ul>
    </div>
  </div>
</template>
<script setup>
import { useMovieStore } from "@/stores/movie";
import AllMovies from "@/components/AllMovies.vue";
import { useRouter } from "vue-router";
const movieStore = useMovieStore();
const router = useRouter();
const navigateToHome = () => {
  router.push({ name: "HomeView" });
};

console.log(movieStore.weatherRecommendMovies)

</script>
<style scoped>
.movie-container {
  background-color: #000;
  max-width: 1440px;
  min-height: 100vh;
  padding-top: 90px;
  padding-left: 150px;
  padding-right: 150px;
  position: flex;
  justify-content: center;
  flex-direction: column;
  margin-left: 100px;
}

.movie-container button {
  height: 50px;
  width: 90px;
  font-size: 15px;
  border-radius: 5px;
  background-color: #f82e62;
  color: #eee;
  border: none;
  cursor: pointer;
  transition: 0.3s;
}
.movie-container button:hover {
  transform: scale(1.1);
}
.movie-container h1 {
  font-size: 40px;
}

.movie-container .movie-wrapper ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

/* 현재 페이지 커스텀 */
.weather-message {
  text-align: center;
  margin-bottom: 50px;
}

.liked-movie-img {
  width: 210px;
  height: 300px;
  transition: 0.3s;
  cursor: pointer;
  margin: 0 20px;
  object-fit: cover;
}

.liked-movie-img:hover {
  transform: scale(1.1);
}
</style>
