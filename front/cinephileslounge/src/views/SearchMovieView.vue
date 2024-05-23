<template>
  <div class="search-container">
    <div class="userInput">
      <div class="userInput-wrapper">
        <i class="bx bx-search"></i>
        <i @click="deleteInput" class="bx bx-x"></i>
        <input
          :value="inputText"
          @input="onInput"
          class="userInput-text"
          type="text"
        />
      </div>
      <input @click="rollBack" class="cancel-btn" type="submit" value="취소" />
    </div>
    <div class="movie-card-list">
      <ul class="card-wrapper">
        <li
          v-for="movie in searchMovies"
          :key="movie.id"
          @click="navigateToDetail(movie.movie_id)"
        >
          <div class="card-img">
            <img
              :src="`https://image.tmdb.org/t/p/w1280/${movie.backdrop_path}`"
            />
            <span class="card-title black-han-sans-regular">{{
              movie.title
            }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useAccountStore } from "@/stores/account";
import { useRouter } from "vue-router";
const searchMovies = ref();
const accountStore = useAccountStore();
const inputText = ref("");
const router = useRouter();

// 입력값 초기화
const deleteInput = () => {
  inputText.value = "";
};

// 영화이미지 click -> movieDetailView로 이동
const navigateToDetail = (movieId) => {
  router.push({ name: "MovieDetailView", params: { movie_id: movieId } });
};

const onInput = (e) => {
  inputText.value = e.currentTarget.value;
  // 입력이 들어올때마다 조회 요청 보내기
  axios({
    method: "get",
    url: `${accountStore.API_URL}/movies/search/`,
    params: {
      q: inputText.value,
    },
  })
    .then((res) => {
      searchMovies.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

const rollBack = () => {
  router.go(-1);
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Black+Han+Sans&display=swap");
.black-han-sans-regular {
  font-family: "Black Han Sans", sans-serif;
  font-weight: 400;
  font-style: normal;
}
.search-container {
  padding-top: 100px;
  padding-left: 150px;
  padding-right: 150px;
  padding-bottom: 100px;
  min-height: 100vh;
}
.search-container .userInput {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
}
.search-container .userInput input {
  outline: none;
  border: none;
  color: #eee;
}
.search-container .userInput .userInput-text {
  width: 800px;
  height: 50px;
  font-size: 20px;
  padding-left: 50px;
  margin-right: 20px;
  border-radius: 8px;
  background-color: #222326;
}
.search-container .userInput .cancel-btn {
  width: 100px;
  height: 52px;
  border-radius: 8px;
  background-color: #222326;
  font-size: 20px;
  transition: 0.3s;
  cursor: pointer;
}
.search-container .userInput .cancel-btn:hover {
  transform: scale(1.05);
}
.search-container .userInput .userInput-wrapper {
  position: relative;
}
.bx-search {
  font-size: 20px;
  position: absolute;
  top: 17px;
  left: 17px;
}
.bx-x {
  position: absolute;
  font-size: 20px;
  right: 35px;
  top: 12px;
  background-color: #84868d;
  border-radius: 50%;
  padding: 4px;
}
.userInput-wrapper i {
  transition: 0.3s;
  cursor: pointer;
}
.userInput-wrapper i:hover {
  transform: scale(1.1);
}
.search-container .movie-card-list .card-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.search-container .movie-card-list .card-img img {
  width: 300px;
  height: 168.75px;
  border-radius: 5px;
}
.search-container .movie-card-list .card-img {
  position: relative;
  transform: 0.3s;
  cursor: pointer;
}
.search-container .movie-card-list .card-img:hover {
  transform: scale(1.1);
  filter: brightness(0.6);
}

.search-container .movie-card-list .card-title {
  position: absolute;
  font-size: 20px;
  left: 10px;
  bottom: 10px;
}
</style>
