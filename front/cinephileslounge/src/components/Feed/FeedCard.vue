<template>
  <li class="subs-container">
    <div class="movie-img">
      <img
        :src="`https://image.tmdb.org/t/p/w1280/${article.movie.backdrop_path}`"
        alt=""
      />
      <p class="song-myung-regular">{{ article.movie.title }}</p>
    </div>
    <div class="movie-content">
      <div class="movie-content-title">{{ article.title }}</div>
      <div class="movie-content-des">
        <div class="profile-img">
          <i class="bx bxl-github"></i>
          <span>
            {{ article.user.nickname }}
          </span>
          <span>|</span>
          <span> 좋아요 {{ article.like_count }} 개 </span>
        </div>
        <p>{{ formatTimeDifference(article.created_at) }}</p>
      </div>
    </div>
  </li>
</template>

<script setup>
defineProps({
  article: Object,
});

// 시간 포멧팅 함수
const formatTimeDifference = (dateString) => {
  const now = new Date(); //현재시간
  const date = new Date(dateString); //게시글 작성시간
  const diff = (now - date) / 1000; // 초 단위 차이

  if (diff < 60) {
    return `${Math.floor(diff)}초 전`;
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}분 전`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}시간 전`;
  } else {
    return `${Math.floor(diff / 86400)}일 전`;
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Song+Myung&display=swap");
.song-myung-regular {
  font-family: "Song Myung", serif;
  font-weight: 400;
  font-style: normal;
}
.subs-container {
  width: 330px;
  height: 280px;
  background-color: #191a1c;
  border-radius: 10px;
  margin-left: 7px;
  margin-right: 7px;
  transition: 0.5s;
}
.subs-container:hover {
  z-index: 1;
  transform: scale(1.15);
  filter: brightness(70%);
}

.subs-container .movie-img {
  position: relative;
  width: 100%;
  height: 180px;
  border-bottom: 2px solid #48484b;
}
.subs-container .movie-img img {
  width: 100%;
  height: 180px;
}

.subs-container .movie-img p {
  position: absolute;
  bottom: 25px;
  left: 50%; /* 부모의 왼쪽에서 50% 위치 */
  transform: translateX(-50%); /* 자신의 너비의 50%만큼 왼쪽으로 이동 */
  font-size: 40px;
}
.subs-container .movie-content {
  display: flex;
  flex-direction: column;
  font-size: 18px;
  padding: 12px;
}
.subs-container .movie-content .movie-content-title {
  margin-top: 10px;
}
.subs-container .movie-content .movie-content-des {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #84868d;
  font-size: 13px;
  margin-top: 15px;
}
.subs-container .movie-content .movie-content-des i {
  font-size: 30px;
}
.subs-container .movie-content .movie-content-des span {
  margin-left: 5px;
  margin-right: 5px;
}
.subs-container .movie-content .movie-content-des .profile-img {
  display: flex;
  align-items: center;
}
</style>
