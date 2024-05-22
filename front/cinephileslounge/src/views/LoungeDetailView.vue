<template>
  <div class="lounge-detail-page">
    <header class="member-movies-container">
      <h1>{{ loungeStore.loungeData.name }}의 회원들이 좋아하는 영화</h1>
      <ul v-if="loungeStore.loungeMovies" class="slide">
        <li v-for="movie in loungeStore.loungeMovies" :key="movie.movie_id">
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
      <p v-else>아직 좋아요를 누른 영화가 없습니다.</p>
    </header>

    <main classs="member-articles-container">
      <div class="review">
        <h1>
          {{ loungeStore.loungeData.name }}의 회원들이 가장 최근에 작성한 영화
          리뷰
        </h1>
        <ul v-if="loungeStore.loungeReviews" class="slide">
          <FeedCard
            v-for="article in loungeStore.loungeReviews"
            :key="article.id"
            :article="article"
            @click="
              router.push({
                name: 'FeedDetailView',
                params: { article_pk: article.id },
              })
            "
          />
        </ul>
        <p v-else>아직 작성한 영화 리뷰가 없습니다.</p>
      </div>

      <div class="lounge-article">
        <h1>라운지 전체 게시글</h1>
        <ul v-if="loungeStore.loungeArticles">
          <li
            v-for="article in loungeStore.loungeArticles"
            :key="article.id"
            :article="article"
            @click="
              router.push({
                name: 'FeedDetailView',
                params: { article_pk: article.id },
              })
            "
          >
            {{ article.title }}
          </li>
        </ul>
        <p v-else>아직 작성한 게시글이 없습니다.</p>
      </div>
    </main>

    <aside class="member-info-container">
      <div class="admin">
        <h1>관리자</h1>
        <div class="profile-container">
          <i class="bx bxl-github"></i>
          <p class="profile-name-p">
            {{ loungeStore.loungeData.admin.nickname }}
          </p>
        </div>
      </div>

      <div class="info">
        <div class="member">
          <h1>멤버</h1>
          <div class="profile-container" v-for="member in loungeStore.loungeData.non_admin_members" :key="member.id">
            <i class="bx bxl-github"></i>
            <p class="profile-name-p">
              {{ member.nickname }}
            </p>
          </div>
        </div>
        
        <div class="setting">
          <template v-if="loungeStore.loungeData.admin.id === accountStore.userPk">
            <button>수정</button>
            <button>삭제</button>
          </template>
          <template v-else>
            <button>탈퇴</button>
          </template>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { useLoungeStore } from "@/stores/lounges";
import { useRoute, useRouter } from "vue-router";
import FeedCard from "@/components/Feed/FeedCard.vue";
import { useAccountStore } from "@/stores/account";

const loungeStore = useLoungeStore();
const accountStore = useAccountStore()
const route = useRoute();
const router = useRouter();

loungeStore.getLounge(route.params.loungePk);
</script>

<style scoped>
header {
  grid-area: header;
}

main {
  grid-area: main;
}

aside {
  grid-area: aside;
}
/* 전체 페이지 */
.lounge-detail-page {
  padding-top: 80px;
  width: 100vw;
  min-height: 100vh;
  background-color: black;
  color: #fff;
  display: grid;
  grid-template-areas: 
    "header header header header"
    "main main main aside"
    "main main main aside"
    "main main main aside";
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: 2fr 1fr 1fr 1fr;
}

/* 회원 좋아요 영화 */
.liked-movie-img {
  height: 300px;
  transition: 0.3s;
  cursor: pointer;
  margin: 0 20px;
}

.liked-movie-img:hover {
  transform: scale(1.1);
}

ul.slide {
  display: flex;
}

/* 라운지 전체 게시글 */

.lounge-article {
  background-color:white;
  opacity: 0.9;
  color: black;
  border-radius: 10px;
  padding: 20px;
}
</style>
