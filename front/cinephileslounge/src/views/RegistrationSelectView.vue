<template>
  <div class="movie-container">
    <div class="btn-wrapper">
      <h1>관심있는 영화를 선택해주세요</h1>
      <div>
        <button @click="navigateToHome" class="select-btn">선택완료</button>
        <button @click="navigateToHome" class="cancel-btn">건너뛰기</button>
      </div>
    </div>
    <div class="movie-wrapper">
      <ul>
        <AllMovies
          v-for="movie in movieStore.allMovies"
          :key="movie.id"
          :movie="movie"
        />
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
}
.movie-container .btn-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  margin-right: 100px;
}
.movie-container .btn-wrapper h1 {
  margin-left: 100px;
}
.movie-container .btn-wrapper .cancel-btn {
  margin-left: 7px;
  background-color: #4c4b4b;
}
.movie-container .btn-wrapper button {
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
.movie-container .btn-wrapper button:hover {
  transform: scale(1.1);
}
.movie-container .btn-wrapper h1 {
  font-size: 40px;
}
.movie-container .movie-wrapper ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}
</style>
