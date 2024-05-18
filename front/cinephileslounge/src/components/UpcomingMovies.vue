<template>
  <div class="upcoming-container">
    <div class="movie" v-for="movie in movies" :key="movie.id">
      <div class="movie-img">
        <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" />
      </div>
      <div class="movie-content">
        <div>
          <h2>{{ movie.title }}</h2>
          <p>{{ changeOverview(movie.overview, 60) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/movie.js";
import axios from "axios";

const movieStore = useMovieStore();
const movies = ref(null);
axios({
  methods: "get",
  url: `${movieStore.API_URL}/movies/upcoming/`,
})
  .then((res) => {
    console.log(res.data);
    console.log("개봉예정작 조회 성공");
    movies.value = res.data;
  })
  .catch((err) => {
    console.log(err);
  });

// overview길이가 maxLength 이상이면 maxLength이후로는 ...으로 대체
const changeOverview = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + "...";
  } else {
    return text;
  }
};
</script>
<style scoped>
.upcoming-container {
  display: flex;
  background-color: black;
}
.upcoming-container .movie {
  width: 200px;
  height: 290px;
  position: relative;
  margin: 10px;
  overflow: hidden;
  transition: 0.5s;
}
.upcoming-container .movie:hover {
  z-index: 1;
  transform: scale(1.25);
  box-shadow: 0 25px 40px rgba(0, 0, 0, 0.5);
}
.upcoming-container .movie .movie-img {
  position: absolute;
}

.upcoming-container .movie .movie-img img {
  width: 200px;
  height: 290px;
  border-radius: 8px;
  object-fit: cover;
}

.upcoming-container .movie .movie-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  margin: 10px;
}
.upcoming-container .movie .movie-content h2 {
  color: #fff;
  transition: 0.5s;
  margin-bottom: 5px;
  font-size: 20px;
  transform: translateY(290px);
}
.upcoming-container .movie:hover .movie-content h2 {
  transform: translateY(150px);
  transition-delay: 0.3s;
  width: 80%;
}
.upcoming-container .movie .movie-content p {
  color: #fff;
  transform: translateY(290px);
  transition: 0.5s;
  font-size: 14px;
  margin-top: 14px;
  width: 90%;
}
.upcoming-container .movie:hover .movie-content p {
  transform: translateY(150px);
  transition-delay: 0.3s;
}
</style>
