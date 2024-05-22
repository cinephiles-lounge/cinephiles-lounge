<template>
  <main>
    <div class="playing-container">
      <div class="playing-wrapper">
        <iframe
          class="movie-video"
          width="1200"
          height="530"
          :src="`https://www.youtube.com/embed/${playingMovie.trailer_key}?autoplay=1&controls=0&loop=1&playlist=${playingMovie.trailer_key}&mute=1`"
          allow="autoplay"
          allowfullscreen
        ></iframe>
        <div class="content-box">
          <div class="content-wrapper">
            <img
              @click="navigateToDetail(playingMovie.movie_id)"
              :src="`https://image.tmdb.org/t/p/w1280/${playingMovie.poster_path}`"
              alt=""
            />
            <div class="content-text">
              <h2 class="black-han-sans-regular">
                <span class="black-han-sans-regular">{{ ranking + 1 }}.</span
                >{{ playingMovie.title }}
              </h2>
              <div class="des">
                <p class="genre">{{ getGenres(playingMovie.genres) }}</p>
                <p class="release_date">{{ playingMovie.release_date }}</p>
              </div>
              <div class="overview-box">
                <p class=".hahmlet-tmp">"{{ playingMovie.overview }}"</p>
              </div>
              <p class="vote_average">
                <i class="bx bxs-star"></i>
                <span>{{ playingMovie.vote_average.toFixed(1) }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

defineProps({
  playingMovie: Object,
  ranking: Number,
});
// 장르 언패킹
const router = useRouter();

const getGenres = (genres) => {
  let genreNames = genres.map((genre) => {
    return genre.name;
  });
  return genreNames.join(" ");
};
// 이미지 click -> 디테일 뷰로 이동
const navigateToDetail = (movieId) => {
  router.push({
    name: "MovieDetailView",
    params: { movie_id: movieId },
  });
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=DM+Serif+Display:ital@0;1&family=Honk&display=swap");
.black-han-sans-regular {
  font-family: "Black Han Sans", sans-serif;
  font-weight: 600;
  font-style: normal;
}

main {
  position: relative;
  width: 100vw;
  height: 100vh;
  background-color: #948176;
  padding-bottom: 50px;
}
.playing-container {
  position: absolute;
  top: 48px;
  left: 80px;
  right: 80px;
  bottom: auto;
  color: #fff;
}

.playing-container .playing-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.playing-container .playing-wrapper iframe {
  width: 70%;
  filter: brightness(1) contrast(1) saturate(1);
  border-radius: 20px;
  box-shadow: 0px 20px 48px rgba(0, 0, 0, 0.6);
}
.playing-container .playing-wrapper .content-box {
  margin-left: 200px;
  margin-right: 200px;
  position: relative;
  width: 1200px;
  max-width: 100%;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
}
.playing-container .playing-wrapper .content-wrapper {
  position: relative;
  margin-left: 30px;
  margin-right: 330px;
  width: 1200px;
  max-width: 100%;
  display: flex;
}
.playing-container .playing-wrapper .content-wrapper img {
  position: absolute;
  top: -120px;
  left: 980px;
  width: 220px;
  max-width: 220px;
  height: 330px;
  filter: brightness(1) contrast(1) saturate(1);
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.6);
  border-radius: 8px;
  transition: 0.3s;
  cursor: pointer;
}
.playing-container .playing-wrapper .content-wrapper img:hover {
  transform: scale(1.1);
}
.playing-container .playing-wrapper .content-wrapper .content-text {
  margin-left: 30px;
  margin-right: 330px;
  position: relative;
  width: 840px;
  height: 210px;
}
.playing-container .playing-wrapper .content-wrapper .content-text h2 {
  font-weight: 400;
  font-size: 48px;
  line-height: 1em;
  position: absolute;
  display: inline;
  margin-left: -3px;
  margin-right: 0px;
  margin-top: -20px;
}
.playing-container .playing-wrapper .content-wrapper .content-text h2 span {
  font-weight: 400;
  font-size: 40px;
  line-height: 1em;
  padding-top: 4px;
  padding-bottom: 6px;
  position: absolute;
  top: 0px;
  left: -45px;
  bottom: 180px;
  right: 820px;
  width: 50px;
  height: 40px;
}
.playing-container .playing-wrapper .content-wrapper .content-text .des {
  font-size: 15px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  margin-top: 50px;
}
.playing-container .playing-wrapper .content-wrapper .content-text .des .genre {
  width: 200px;
  height: 16px;
}
.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .des
  .release_date {
  width: 330px;
  height: 28px;
}
.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .overview-box {
  font-weight: 400;
  font-size: 13px;
  line-height: 1.38em;
  margin-top: 5px;
}
.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .overview-box
  p {
  font-size: 17px;
  line-height: 1.52em;
  width: 100%;
  height: 104px;
}

.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .vote_average {
  font-size: 20px;
  font-weight: 400;
  line-height: 1.3em;
  position: absolute;
  top: 85px;
  left: -50px;
  bottom: 0px;
  right: 820px;
  width: 50px;
  height: 59px;
  display: flex;
  flex-direction: column;
}
.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .vote_average
  i {
  font-size: 35px;
  margin-left: -3px;
  margin-right: 11px;
  margin-top: 0px;
  margin-bottom: 5px;
  color: #c2b6af;
}
.playing-container
  .playing-wrapper
  .content-wrapper
  .content-text
  .vote_average
  span {
  font-size: 20px;
  width: 100%;
  height: 26px;
}
</style>
