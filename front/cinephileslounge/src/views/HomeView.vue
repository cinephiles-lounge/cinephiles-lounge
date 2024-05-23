<template>
  <section>
    <div class="container">
      <div ref="carousel" class="carousel">
        <div class="list">
          <div class="item" v-for="movie in displayedMovies" :key="movie.id">
            <img
              :src="`https://image.tmdb.org/t/p/w1280/${movie.backdrop_path}`"
            />
            <div class="content">
              <div class="title">{{ movie.title }}</div>
              <div class="vote_average">
                평점 : {{ movie.vote_average.toFixed(1) }}
              </div>
              <div class="release_date">개봉일 : {{ movie.release_date }}</div>
              <div class="overview">
                {{ movie.overview }}
              </div>
              <div class="buttons">
                <button @click="navigateToDetail(movie.movie_id)">
                  더보기
                </button>
                <button>좋아요</button>
              </div>
            </div>
          </div>
        </div>
        <div class="posters">
          <div class="item" v-for="movie in posters" :key="movie.id">
            <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" />
          </div>
        </div>
        <div class="arrows">
          <button @click="showSlider('prev')"><</button>
          <button @click="showSlider('next')">></button>
        </div>
      </div>
    </div>
    <NewMovieSlider
      v-if="movieStore.newMovies && movieStore.newMovies.length > 0"
      :movies="movieStore.newMovies"
      :title="'새로 개봉한 영화'"
    />
    <MovieSlider
      v-if="movieStore.likeMovies && movieStore.likeMovies.length > 0"
      :movies="movieStore.likeMovies"
      :title="`${accountStore.userNickname}님이 좋아할 만한 영화`"
    />
    <MovieSlider
      v-if="movieStore.subsMovies && movieStore.subsMovies.length > 0"
      :movies="movieStore.subsMovies"
      :title="`${accountStore.userNickname}님이 구독한 유저가 좋아하는 영화`"
    />
    <MovieSlider
      v-if="movieStore.comedyMovies && movieStore.comedyMovies.length > 0"
      :movies="movieStore.comedyMovies"
      :title="'코미디 영화 추천'"
    />
    <MovieSlider
      v-if="movieStore.romanceMovies && movieStore.romanceMovies.length > 0"
      :movies="movieStore.romanceMovies"
      :title="'로맨스 영화 추천'"
    />
    <MovieSlider
      v-if="movieStore.horrorMovies && movieStore.horrorMovies.length > 0"
      :movies="movieStore.horrorMovies"
      :title="'공포 영화 추천'"
    />
    <PlayingMovies
      v-for="(playingMovie, ranking) in playingStore.playingMovies"
      :playingMovie="playingMovie"
      :ranking="ranking"
      :key="playingMovie.id"
    />
    <UpcommingMovies />

    <template v-if="accountStore.isLogin">
      <button
        @click="getWeatherRecommendation"
        class="weather-btn"
        title="오늘 날씨에 어울리는 영화를 추천해드려요"
      >
        <i class="bx bxs-sun"></i>
      </button>
      <div class="modal-wrap" v-show="isModalOpen" @click="toggleModal">
        <div class="modal-container" @click.stop="">
          <p class="weather-loc">현재 위치의 날씨에</p>
          <p>어울리는 영화들을 고르는 중이에요</p>
          <div class="loading-container">
            <div class="loading"></div>
            <div id="loading-text">불러오는 중</div>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import UpcommingMovies from "@/components/UpcomingMovies.vue";
import PlayingMovies from "@/components/PlayingMovies.vue";
import MovieSlider from "@/components/MovieSlider/MovieSlider.vue";
import NewMovieSlider from "@/components/MovieSlider/NewMovieSlider/NewMovieSlider.vue";
import { usePlayingMovieStore } from "@/stores/playingMovie";
import { useMovieStore } from "@/stores/movie";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/account";
import axios from "axios";
const router = useRouter();
const accountStore = useAccountStore();
const movieStore = useMovieStore();
const playingStore = usePlayingMovieStore();

movieStore.getLikeMovies(); // 좋아요 기반 영화 조회
movieStore.getSubsMovies(); // 구독 기반 영화 조회
movieStore.getNewMovies(); // 최신 영화 조회
movieStore.getPopularMovie(); // 인기 상역작 1~5위 조회
playingStore.getPlayingMovies(); // 현재 상영작 1,2,3 위 조회
movieStore.getComedyMovies(); // 코미디 영화 조회
movieStore.getRomanceMovies(); // 로맨스 영화 조회
movieStore.getHorrorMovies(); // 공포 영화 조회
const movies = ref(movieStore.popularMovie);

const currentIndex = ref(0); // 캐러셀 움직이기 위한 인덱스
const timeRunning = ref(3000); // 애니메이션 실행되는 시간
const timeAutoNext = ref(5000); // 다음 슬라이드로 이동하는 시간 간격
const carousel = ref(null); // 캐러셀 클래스 참조
let runTimeOut = null; // 애니메이션 실행 후 클래스 제거하기 위한 타이머
let runNextAuto = null; // 자동으로 다음 슬라이드로 이동하기 위한 타이머

const displayedMovies = computed(() => {
  const start = currentIndex.value;
  const end = movies.value.length;
  return [...movies.value.slice(start, end), ...movies.value.slice(0, start)]; //
});

const posters = computed(() => {
  // 인덱스 1, 2, 3, 4, 0 순서대로 반환
  const start = currentIndex.value + 1;
  const end = movies.value.length;
  return [...movies.value.slice(start, end), ...movies.value.slice(0, start)];
});

const showSlider = (type) => {
  // 다음 버튼 클릭시
  if (type === "next") {
    currentIndex.value = (currentIndex.value + 1) % movies.value.length; // 인덱스 +1
    carousel.value.classList.add("next"); //캐러셀에 next클래스 추가
  } else {
    // 이전 버튼 클릭시
    currentIndex.value =
      (currentIndex.value - 1 + movies.length) % movies.value.length; // 인덱스 -1
    carousel.value.classList.add("prev"); //캐러셀에 prev클래스 추가
  }

  clearTimeout(runTimeOut); // 이미 runTimeOut이 설정되어있으면 취소시키기
  runTimeOut = setTimeout(() => {
    carousel.value.classList.remove("next");
    carousel.value.classList.remove("prev");
  }, timeRunning.value); //timeRunning(3000ms)후에 캐러셀에 추가된 클래스들 제거

  clearTimeout(runNextAuto); // 이미 runNextAuto 설정되어있으면 취소시키기
  runNextAuto = setTimeout(() => {
    showSlider("next");
  }, timeAutoNext.value); // timeAutoNext(7000ms)후에 showSlider("next")함수 실행(자동으로 슬라이드 시키기 위해)
};

onMounted(() => {
  // 컴포넌트가 마운트 될 때, timeAutoNext(7000ms)초 후에 슬라이드 이동 타이머 설정
  runNextAuto = setTimeout(() => {
    showSlider("next");
  }, timeAutoNext.value);
});

onUnmounted(() => {
  // 컴포넌트가 언마운틀 될 때, 타이머 정리하기
  clearTimeout(runTimeOut);
  clearTimeout(runNextAuto);
});

// 더보기 버튼 click -> 디테일 뷰로 이동
const navigateToDetail = (movieId) => {
  router.push({
    name: "MovieDetailView",
    params: { movie_id: movieId },
  });
};

// 모달 여닫는 기능
const isModalOpen = ref(false);
const toggleModal = function () {
  isModalOpen.value = !isModalOpen.value;
};

// 날씨
function fail(err) {
  // 위치 정보를 가져오는데 실패했을 때 호출되는 콜백 함수
  alert("현위치를 찾을 수 없습니다.");
}

const getWeatherRecommendation = function () {
  toggleModal();
  navigator.geolocation.getCurrentPosition((position) => {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    movieStore.recommendMovieByWeather(lat, lon);
  }, fail);
};
</script>

<style scoped>
/* 캐러셀 */
.carousel {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
}
.carousel .list .item {
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0 0 0 0;
}
.carousel .list .item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.carousel .list .item .content {
  position: absolute;
  top: 20%;
  width: 1140px;
  max-width: 80%;
  left: 45%;
  transform: translateX(-50%);
  padding-right: 30%;
  box-sizing: border-box;
  color: #fff;
  text-shadow: 0 5px 10px #0004;
}

.carousel .list .item .title {
  font-size: 55px;
  font-weight: bold;
  line-height: 104px;
}
.carousel .list .item .content .overview {
  line-height: 23px;
}
.carousel .list .item .content .release_date {
  margin: 15px 0px;
}

.carousel .list .item .buttons {
  display: grid;
  grid-template-columns: repeat(2, 130px);
  grid-template-rows: 40px;
  gap: 5px;
  margin-top: 20px;
}

.carousel .list .item .buttons button {
  border: none;
  background-color: #eee;
  letter-spacing: 3px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s;
}
.carousel .list .item .buttons button:hover {
  transform: scale(1.1);
}
.carousel .list .item .buttons button:nth-child(2) {
  background-color: transparent;
  border: 1px solid #fff;
  color: #eee;
}
/* 포스터 */
.posters {
  position: absolute;
  bottom: 50px;
  left: 50%;
  width: max-content;
  z-index: 100;
  display: flex;
  gap: 20px;
}
.posters .item {
  width: 150px;
  height: 220px;
  flex-shrink: 0;
  position: relative;
}
.posters .item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 20px;
}

/* 방향버튼 */
.arrows {
  position: absolute;
  top: 80%;
  right: 52%;
  z-index: 100;
  width: 300px;
  max-width: 30%;
  display: flex;
  gap: 10px;
  align-items: center;
}
.arrows button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #eee4;
  border: none;
  color: #fff;
  font-family: monospace;
  font-weight: bold;
  transition: 0.5s;
}
.arrows button:hover {
  background-color: #fff;
  color: #000;
}

/* 애니메이션 */
.carousel .list .item:nth-child(1) {
  z-index: 1;
}

.carousel .list .item:nth-child(1) .content .title,
.carousel .list .item:nth-child(1) .content .vote_average,
.carousel .list .item:nth-child(1) .content .release_date,
.carousel .list .item:nth-child(1) .content .overview,
.carousel .list .item:nth-child(1) .content .buttons {
  transform: translateY(50px);
  filter: blur(20px);
  opacity: 0;
  animation: showContent 0.5s 1s linear 1 forwards;
}
@keyframes showContent {
  /* 슬라이드로 들어올 때 캐러셀에 제목, 설명, 버튼같은거 어떻게 보일지 */
  to {
    transform: translateY(0px);
    filter: blur(0px);
    opacity: 1;
  }
}
.carousel .list .item:nth-child(1) .content .title {
  animation-delay: 1s !important;
}
.carousel .list .item:nth-child(1) .content .vote_average {
  animation-delay: 1.1s !important;
}
.carousel .list .item:nth-child(1) .content .release_date {
  animation-delay: 1.2s !important;
}

.carousel .list .item:nth-child(1) .content .overview {
  animation-delay: 1.4s !important;
}
.carousel .list .item:nth-child(1) .content .buttons {
  animation-delay: 1.6s !important;
}

.carousel.next .list .item:nth-child(1) img {
  width: 150px;
  height: 220px;
  position: absolute;
  bottom: 50px;
  left: 50%;
  border-radius: 30px;
  animation: showImage 0.5s linear 1 forwards;
}
@keyframes showImage {
  /* 다음 슬라이드로 넘어갈 때 이미지 커지게 */
  to {
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
  }
}

.carousel.next .posters .item:nth-last-child(1) {
  overflow: hidden;
  animation: showPosters 1.5s linear 1 forwards;
}
.carousel.prev .list .item img {
  z-index: 100;
}
@keyframes showPosters {
  /* 다음 슬라이드로 넘어갈 때 마지막 포스터가 나타나는 효과*/
  from {
    width: 0;
    opacity: 0;
  }
}
.carousel.next .posters {
  animation: effectNext 0.5s linear 1 forwards;
}

@keyframes effectNext {
  /* 슬라이드가 넘어갈때 포스터 오른쪽에서 왼쪽으로 이동 */
  from {
    transform: translateX(150px);
  }
}

/* 이전버튼 눌러서 prev클래스가 추가될때 */
.carousel.prev .list .item:nth-child(2) {
  z-index: 2;
}

.carousel.prev .list .item:nth-child(2) img {
  animation: outFrame 0.5s linear 1 forwards;
  position: absolute;
  bottom: 0;
  left: 0;
}
@keyframes outFrame {
  /* 이전 슬라이드로 넘어갈때 현재 슬라이드 이미지 작아지면서 아래쪽포스터로 들어오는것처럼 보이게 */
  to {
    width: 150px;
    height: 220px;
    bottom: 50px;
    left: 50%;
    border-radius: 20px;
  }
}

.carousel.prev .posters .item:nth-child(1) {
  overflow: hidden;
  opacity: 0;
  animation: showPosters 0.8s linear 1 forwards;
}
.carousel.next .arrows button,
.carousel.prev .arrows button {
  pointer-events: none;
}
.carousel.prev .list .item:nth-child(2) .content .title,
.carousel.prev .list .item:nth-child(2) .content .vote_average,
.carousel.prev .list .item:nth-child(2) .content .release_date,
.carousel.prev .list .item:nth-child(2) .content .overview,
.carousel.prev .list .item:nth-child(2) .content .buttons {
  animation: contentOut 1.5s linear 1 forwards !important;
}

@keyframes contentOut {
  /* 이전 슬라이드로 넘어갈때 현재 슬라이드 콘텐츠(제목, 줄거리)들이 블러처리되면서 위로 사라지게 */
  to {
    transform: translateY(-150px);
    filter: blur(20px);
    opacity: 0;
  }
}

/* 날씨 추천 */
.weather-btn {
  z-index: 200;
  display: block;
  font-size: 30px;
  position: fixed;
  top: 90px;
  right: 70px;
  width: 60px;
  height: 60px;
  /* background: linear-gradient(to bottom, #fd82a1 0%, #f82e62 100%); */
  background-color: #eee;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  line-height: 20px;
  text-align: center;
  text-decoration: none;
  color: #646464;
  border: none;
}

.weather-btn::before {
  display: block;
  position: fixed;
  top: 90px;
  right: 70px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: black;
  opacity: 0;
  content: "";
  animation: pulse 1s infinite;
}

.weather-btn:hover::before {
  animation: none;
  opacity: 0.4;
  transform: scale(1.3);
}
.weather-btn.is-clicked {
  background: linear-gradient(to bottom, gray 0%, dimgray 100%);
}
.weather-btn.is-clicked:before {
  animation: blastOut 1s;
}

@keyframes pulse {
  from {
    transform: scale(1);
    opacity: 0.4;
  }
  to {
    transform: scale(1.3);
    opacity: 0;
  }
}

@keyframes blastOut {
  from {
    transform: scale(0.9);
    opacity: 0.4;
  }
  to {
    transform: scale(10);
    opacity: 0;
  }
}

/* 모달 */
.modal-wrap {
  z-index: 200;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* modal or popup */
.modal-container {
  z-index: 200;
  color: white;
  position: relative;
  height: 250px;
  width: 400px;
  background: #1d1d1d;
  border-radius: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 3px;
}

.modal-btn {
  display: flex;
  justify-content: center;
}

.modal-btn > button {
  margin: 5px;
}

/* 로딩 */
#link {
  color: #e45635;
  display: block;
  font: 12px "Helvetica Neue", Helvetica, Arial, sans-serif;
  text-align: center;
  text-decoration: none;
}
#link:hover {
  color: #cccccc;
}

#link,
#link:hover {
  -webkit-transition: color 0.5s ease-out;
  -moz-transition: color 0.5s ease-out;
  -ms-transition: color 0.5s ease-out;
  -o-transition: color 0.5s ease-out;
  transition: color 0.5s ease-out;
}

/** BEGIN CSS **/
body {
  background: #333333;
}
@keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-moz-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-webkit-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-o-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-moz-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-webkit-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@-o-keyframes rotate-loading {
  0% {
    transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
  }
}

@keyframes loading-text-opacity {
  0% {
    opacity: 0;
  }
  20% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-moz-keyframes loading-text-opacity {
  0% {
    opacity: 0;
  }
  20% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-webkit-keyframes loading-text-opacity {
  0% {
    opacity: 0;
  }
  20% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-o-keyframes loading-text-opacity {
  0% {
    opacity: 0;
  }
  20% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
.loading-container,
.loading {
  height: 100px;
  position: relative;
  width: 100px;
  border-radius: 100%;
}

.loading-container {
  margin: 40px auto;
}

.loading {
  border: 2px solid transparent;
  border-color: transparent #fff transparent #fff;
  -moz-animation: rotate-loading 1.5s linear 0s infinite normal;
  -moz-transform-origin: 50% 50%;
  -o-animation: rotate-loading 1.5s linear 0s infinite normal;
  -o-transform-origin: 50% 50%;
  -webkit-animation: rotate-loading 1.5s linear 0s infinite normal;
  -webkit-transform-origin: 50% 50%;
  animation: rotate-loading 1.5s linear 0s infinite normal;
  transform-origin: 50% 50%;
}

.loading-container:hover .loading {
  border-color: transparent #e45635 transparent #e45635;
}
.loading-container:hover .loading,
.loading-container .loading {
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
}

#loading-text {
  -moz-animation: loading-text-opacity 2s linear 0s infinite normal;
  -o-animation: loading-text-opacity 2s linear 0s infinite normal;
  -webkit-animation: loading-text-opacity 2s linear 0s infinite normal;
  animation: loading-text-opacity 2s linear 0s infinite normal;
  color: #ffffff;
  font-family: "Helvetica Neue, " Helvetica ", " "arial";
  font-size: 10px;
  font-weight: bold;
  margin-top: 45px;
  opacity: 0;
  position: absolute;
  text-align: center;
  text-transform: uppercase;
  top: 0;
  width: 100px;
}
</style>
