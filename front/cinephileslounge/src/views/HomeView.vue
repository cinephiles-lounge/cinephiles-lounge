<template>
  <section>
    <div class="container">
      <div class="carousel">
        <div class="list">
          <div
            class="item"
            v-for="(path, index) in backdrop_paths"
            :key="index"
          >
            <img
              :src="`https://image.tmdb.org/t/p/w500/x1Ex090BNIXcmaBYB2US0j3hBUF.jpg`"
            />
            <div class="content">
              <div class="author">유니버설 픽쳐스</div>
              <div class="title">쿵푸팬더4</div>
              <div class="topic">애니메이션</div>
              <div class="des">
                오랜만이지! 드림웍스 레전드 시리즈 마침내 컴백! 마침내 내면의
                평화… 냉면의 평화…가 찾아왔다고 믿는 용의 전사 ‘포’ 이젠 평화의
                계곡의 영적 지도자가 되고, 자신을 대신할 후계자를 찾아야만 한다.
                “이제 용의 전사는 그만둬야 해요?” 용의 전사로의 모습이
                익숙해지고 새로운 성장을 하기보다 지금 이대로가 좋은 ‘포’ 하지만
                모든 쿵푸 마스터들의 능력을 그대로 복제하는 강력한 빌런
                ‘카멜레온’이 나타나고 그녀를 막기 위해 정체를 알 수 없는 쿵푸
                고수 ‘젠’과 함께 모험을 떠나게 되는데… 포는 가장 강력한 빌런과
                자기 자신마저 뛰어넘고 진정한 변화를 할 수 있을까?
              </div>
              <div class="buttons">
                <button>더보기</button>
                <button>구독</button>
              </div>
            </div>
          </div>
        </div>
        <div class="thumbnail">
          <div class="item" v-for="(path, index) in poster_paths" :key="index">
            <img :src="`https://image.tmdb.org/t/p/w500${path}`" />
            <div class="content">
              <!-- <div class="title">타이틀</div>
              <div class="description">overview</div> -->
            </div>
          </div>
        </div>
        <div class="arrows">
          <button ref="prev"><</button>
          <button ref="next">></button>
        </div>
        <div class="time"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

const backdrop_paths = [
  "/kYgQzzjNis5jJalYtIHgrom0gOx.jpg",
  "/qrGtVFxaD8c7et0jUtaYhyTzzPg.jpg",
  "/fypydCipcWDKDTTCoPucBsdGYXW.jpg",
  "/x1Ex090BNIXcmaBYB2US0j3hBUF.jpg",
];

const poster_paths = [
  "/4z1VMmlxHrziG45901esjB4dpIa.jpg",
  "/plNOSbqkSuGEK2i15A5btAXtB7t.jpg",
  "/buvBq2zLP7CcJth8tjrI4znvfEO.jpg",
  "/8uUU2pxm6IYZw8UgnKJyx7Dqwu9.jpg",
];
</script>
<style scoped>
/* carousel */
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
  left: 50%;
  transform: translateX(-50%);
  padding-right: 30%;
  box-sizing: border-box;
  color: #fff;
  text-shadow: 0 5px 10px #0004;
}
.carousel .list .item .author {
  font-weight: bold;
  letter-spacing: 10px;
}
.carousel .list .item .title,
.carousel .list .item .topic {
  font-size: 5em;
  font-weight: bold;
  line-height: 1.3em;
}
.carousel .list .item .topic {
  color: #f1683a;
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
  font-family: Poppins;
  font-weight: 500;
}
.carousel .list .item .buttons button:nth-child(2) {
  background-color: transparent;
  border: 1px solid #fff;
  color: #eee;
}
/* 아래 카드 썸네일 */
.thumbnail {
  position: absolute;
  bottom: 50px;
  left: 50%;
  width: max-content;
  z-index: 100;
  display: flex;
  gap: 20px;
}
.thumbnail .item {
  width: 150px;
  height: 220px;
  flex-shrink: 0;
  position: relative;
}
.thumbnail .item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 20px;
}
.thumbnail .item .content {
  color: #fff;
  position: absolute;
  bottom: 10px;
  left: 10px;
  right: 10px;
}
.thumbnail .item .content .title {
  font-weight: 500;
}
.thumbnail .item .content .description {
  font-weight: 300;
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

.carousel .list .item:nth-child(1) {
  z-index: 1;
}

.carousel .list .item:nth-child(1) .content .author,
.carousel .list .item:nth-child(1) .content .title,
.carousel .list .item:nth-child(1) .content .topic,
.carousel .list .item:nth-child(1) .content .des,
.carousel .list .item:nth-child(1) .content .buttons {
  transform: translateY(50px);
  filter: blur(20px);
  opacity: 0;
  animation: showContent 0.5s 1s linear 1 forwards;
}
@keyframes showContent {
  to {
    transform: translateY(0px);
    filter: blur(0px);
    opacity: 1;
  }
}
.carousel .list .item:nth-child(1) .content .title {
  animation-delay: 1.2s !important;
}
.carousel .list .item:nth-child(1) .content .topic {
  animation-delay: 1.4s !important;
}
.carousel .list .item:nth-child(1) .content .des {
  animation-delay: 1.6s !important;
}
.carousel .list .item:nth-child(1) .content .buttons {
  animation-delay: 1.8s !important;
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
  to {
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
  }
}

.carousel.next .thumbnail .item:nth-last-child(1) {
  overflow: hidden;
  animation: showThumbnail 0.5s linear 1 forwards;
}
.carousel.prev .list .item img {
  z-index: 100;
}
@keyframes showThumbnail {
  from {
    width: 0;
    opacity: 0;
  }
}
.carousel.next .thumbnail {
  animation: effectNext 0.5s linear 1 forwards;
}

@keyframes effectNext {
  from {
    transform: translateX(150px);
  }
}

.carousel .time {
  position: absolute;
  z-index: 1000;
  width: 0%;
  height: 3px;
  background-color: #f1683a;
  left: 0;
  top: 0;
}

.carousel.next .time,
.carousel.prev .time {
  animation: runningTime 3s linear 1 forwards;
}
@keyframes runningTime {
  from {
    width: 100%;
  }
  to {
    width: 0;
  }
}

/* prev click */

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
  to {
    width: 150px;
    height: 220px;
    bottom: 50px;
    left: 50%;
    border-radius: 20px;
  }
}

.carousel.prev .thumbnail .item:nth-child(1) {
  overflow: hidden;
  opacity: 0;
  animation: showThumbnail 0.5s linear 1 forwards;
}
.carousel.next .arrows button,
.carousel.prev .arrows button {
  pointer-events: none;
}
.carousel.prev .list .item:nth-child(2) .content .author,
.carousel.prev .list .item:nth-child(2) .content .title,
.carousel.prev .list .item:nth-child(2) .content .topic,
.carousel.prev .list .item:nth-child(2) .content .des,
.carousel.prev .list .item:nth-child(2) .content .buttons {
  animation: contentOut 1.5s linear 1 forwards !important;
}

@keyframes contentOut {
  to {
    transform: translateY(-150px);
    filter: blur(20px);
    opacity: 0;
  }
}
@media screen and (max-width: 678px) {
  .carousel .list .item .content {
    padding-right: 0;
  }
  .carousel .list .item .content .title {
    font-size: 30px;
  }
}
</style>
