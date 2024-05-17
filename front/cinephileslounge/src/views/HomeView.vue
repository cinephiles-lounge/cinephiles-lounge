<template>
  <section>
    <div class="container">
      <div ref="carousel" class="carousel">
        <div class="list">
          <div class="item" v-for="movie in movies" :key="movie.id">
            <img
              :src="`https://image.tmdb.org/t/p/w1280/${movie.backdrop_path}`"
            />
            <div class="content">
              <div class="title">{{ movie.title }}</div>
              <div class="vote_average">평점 : {{ movie.vote_average }}</div>
              <div class="release_date">개봉일 : {{ movie.release_date }}</div>
              <div class="overview">
                {{ movie.overview }}
              </div>
              <div class="buttons">
                <button>더보기</button>
                <button>찜</button>
              </div>
            </div>
          </div>
        </div>
        <div class="posters">
          <div
            class="item"
            v-for="(movie, index) in movies"
            :key="movie.id"
            @click="thumbnailClick(index)"
          >
            <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" />
          </div>
        </div>
        <div class="arrows">
          <button @click="showSlider('prev')"><</button>
          <button @click="showSlider('next')">></button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
const movies = [
  {
    id: 0,
    title: "혹성탈출:새로운 시대",
    overview:
      "진화한 유인원과 퇴화된 인간들이 살아가는 땅. 유인원 리더 프록시무스는 완전한 군림을 위해 인간들을 사냥하며 자신의 제국을 건설한다. 한편, 또 다른 유인원 노아는 우연히 숨겨진 과거의 이야기와 시저의 가르침을 듣게 되고 인간과 유인원이 함께 할 새로운 세상을 꿈꾼다. 어느 날 그의 앞에 나타난 의문의 한 인간 소녀. 노아는 그녀와 함께 자유를 향한 여정을 시작하게 되는데…",
    release_date: "2024-05-08",
    vote_average: 7.171,
    poster_path: "/plNOSbqkSuGEK2i15A5btAXtB7t.jpg",
    backdrop_path: "/fypydCipcWDKDTTCoPucBsdGYXW.jpg",
  },
  {
    id: 1,
    title: "쿵푸팬더 4",
    overview:
      "마침내 내면의 평화… 냉면의 평화…가 찾아왔다고 믿는 용의 전사 ‘포’ 이젠 평화의 계곡의 영적 지도자가 되고, 자신을 대신할 후계자를 찾아야만 한다. “이제 용의 전사는 그만둬야 해요?” 용의 전사로의 모습이 익숙해지고 새로운 성장을 하기보다 지금 이대로가 좋은 ‘포’ 하지만 모든 쿵푸 마스터들의 능력을 그대로 복제하는 강력한 빌런 ‘카멜레온’이 나타나고 그녀를 막기 위해 정체를 알 수 없는 쿵푸 고수 ‘젠’과 함께 모험을 떠나게 되는데… 포는 가장 강력한 빌런과 자기 자신마저 뛰어넘고 진정한 변화를 할 수 있을까?",
    release_date: "2024-03-02",
    vote_average: 7.126,
    poster_path: "/1ZNOOMmILNUzVYbzG1j7GYb5bEV.jpg",
    backdrop_path: "/kYgQzzjNis5jJalYtIHgrom0gOx.jpg",
  },
  {
    id: 2,
    title: "인사이드 아웃2",
    overview:
      "13살이 된 라일리의 행복을 위해 매일 바쁘게 머릿속 감정 컨트롤 본부를 운영하는 ‘기쁨’, ‘슬픔’, ‘버럭’, ‘까칠’, ‘소심’. 그러던 어느 날, 낯선 감정인 ‘불안’, ‘당황’, ‘따분’, ‘부럽’이가 본부에 등장하고, 언제나 최악의 상황을 대비하며 제멋대로인 ‘불안’이와 기존 감정들은 계속 충돌한다. 결국 새로운 감정들에 의해 본부에서 쫓겨나게 된 기존 감정들은 다시 본부로 돌아가기 위해 위험천만한 모험을 시작하는데…",
    release_date: "2024-06-06",
    vote_average: 7.332,
    poster_path: "/pmemGuhr450DK8GiTT44mgwWCP7.jpg",
    backdrop_path: "/pI5jxew0I9kub4IXrtsOB8F40dw.jpg",
  },
  {
    id: 3,
    title: "이프: 상상의 친구",
    overview:
      "상상의 친구 ‘이프’를 볼 수 있는 능력을 지닌 한 소녀가 아이들에게 잊혀졌던 ‘이프’를 다시 되찾아주기 위해 마법 같은 모험을 시작하는 이야기를 그린 영화",
    release_date: "2024-05-08",
    vote_average: 7.711,
    poster_path: "/9GAOhSzXjXJR4AxYCa2AMzMGPVg.jpg",
    backdrop_path: "/jTWllMddJzCb7hBVNZICtgKhYM9.jpg",
  },
];

const carousel = ref(null); // carousel클래스 참조
const timeRunning = ref(3000); // 애니메이션 실행되는 시간
const timeAutoNext = ref(7000); // 다음 슬라이드로 이동하는 시간 간격

let runTimeOut = null; // 애니메이션 실행 후 클래스 제거하기 위한 타이머
let runNextAuto = null; // 자동으로 다음 슬라이드로 이동하기 위한 타이머

const showSlider = (type) => {
  const carouselList = carousel.value.querySelector(".list");
  const carouselListItem = carouselList.querySelectorAll(".item");
  const posterList = carousel.value.querySelector(".posters");
  const posterListItem = posterList.querySelectorAll(".item");

  if (type === "next") {
    // 다음 버튼 클릭 시
    carouselList.appendChild(carouselListItem[0]); // 캐러셀에 0번이 제일 뒤로 추가
    posterList.appendChild(posterListItem[0]); // 포스터 0번이 제일 뒤로 추가
    carousel.value.classList.add("next"); // 캐러셀에 next class 추가
  } else {
    // 이전 버튼 클릭 시
    carouselList.prepend(carouselListItem[carouselListItem.length - 1]); // 캐러셀 마지막요소를 맨 앞으로 추가
    posterList.prepend(posterListItem[posterListItem.length - 1]); // 포스터 마지막요소를 맨 앞으로 추가
    carousel.value.classList.add("prev"); // 캐러셀에 prev class 추가
  }

  clearTimeout(runTimeOut); // 이미 runTimeOut이 설정되어있으면 취소시키기
  runTimeOut = setTimeout(() => {
    carousel.value.classList.remove("next");
    carousel.value.classList.remove("prev");
  }, timeRunning.value); // timeRunning.value(3000ms)후에 캐러셀에 추가된 클래스들 제거

  clearTimeout(runNextAuto); // 이미 runNextAuto가 설정되어있으면 취소시키기
  runNextAuto = setTimeout(() => {
    showSlider("next");
  }, timeAutoNext.value); //timeAutoNext(7000ms)후에 showSlider("next")함수 실행. 자동으로 슬라이드 이동시키기 위해
};

onMounted(() => {
  // 컴포넌트가 마운트될 때, 슬라이드 이동 타이머 설정
  runNextAuto = setTimeout(() => {
    showSlider("next");
  }, timeAutoNext.value);
});

onUnmounted(() => {
  //컴포넌트 언마운트될 때, 타이머 정리하기
  clearTimeout(runTimeOut);
  clearTimeout(runNextAuto);
});
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
  font-size: 60px;
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
</style>
