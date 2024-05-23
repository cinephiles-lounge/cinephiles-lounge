<template>
  <nav :class="{ sticky: isSticky }">
    <div class="nav-content">
      <div class="nav-left">
        <div class="logo">
          <RouterLink
            :to="{ name: 'HomeView' }"
            class="dm-serif-display-regular-italic"
            >CinePhile's Lounge</RouterLink
          >
        </div>
        <ul class="nav-links">
          <li><RouterLink :to="{ name: 'HomeView' }">홈</RouterLink></li>
          <li><RouterLink :to="{ name: 'FeedView' }">피드</RouterLink></li>
          <li><RouterLink :to="{ name: 'LoungeView' }">라운지</RouterLink></li>
          <li>
            <RouterLink :to="{ name: 'SearchMovieView' }">검색</RouterLink>
          </li>
        </ul>
      </div>
      <div class="nav-right">
        <ul class="nav-links">
          <li v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
          </li>
          <li v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'RegistrationView' }">회원가입</RouterLink>
          </li>
          <li v-if="accountStore.isLogin" @click="logOut">로그아웃</li>
          <li v-if="accountStore.isLogin">
            <RouterLink
              :to="{
                name: 'UserProfileView',
                params: { userId: accountStore.userPk },
              }"
              >내 프로필</RouterLink
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
// 로그인하면 회원가입버튼 안보이고 마이페이지랑 알람 뜨도록
import { ref, onMounted, onBeforeUnmount } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/account";
import { useLoungeStore } from "@/stores/lounges";
import { useMovieStore } from "@/stores/movie";
import { useRouter } from "vue-router";
import axios from "axios";

const accountStore = useAccountStore();
const loungeStore = useLoungeStore();
const movieStore = useMovieStore();
const router = useRouter();

const isSticky = ref(false);
const isSearch = ref(false);

const handleScroll = () => {
  if (window.scrollY > 20) {
    isSticky.value = true;
  } else {
    isSticky.value = false;
  }
};
onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
});

const logOut = () => {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/auth/logout/`,
  })
    .then((res) => {
      console.log("로그아웃 성공");
      accountStore.token = null; // 토큰 초기화
      accountStore.userId = ""; //유저 이름 초기화
      accountStore.userNickname = ""; //닉네임 초기화
      accountStore.userPk = ""; //유저 pk 초기화
      accountStore.subscriptions = []; // 내가 구독하는 사람들 초기화
      accountStore.subscribers = []; // 나를 구독한 사람들 초기화
      accountStore.likedMovies = [];
      accountStore.likedArticles = [];
      accountStore.postedArticles = [];
      accountStore.joinedLounges = [];
      accountStore.managingLounges = [];
      accountStore.nonManagingLounges = [];
      loungeStore.loungeData = [];
      loungeStore.loungeMovies = [];
      loungeStore.loungeReviews = [];
      loungeStore.loungeArticles = [];
      loungeStore.loungeArticleDetail = [];
      movieStore.movie = [];
      router.push({ name: "HomeView" });
    })
    .catch((err) => {
      console.log("로그아웃 실패");
      console.log(err);
    });
};
</script>

<style scoped>
@font-face {
  font-family: "TiemposHeadline-Semibold";
  src: url("@/assets/fonts/TiemposHeadline-Semibold.otf") format("opentype");
}

.dm-serif-display-regular-italic {
  font-family: "DM Serif Display", serif;
  font-weight: 400;
  font-style: italic;
}
nav {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 70px;
  transition: all 0.4s ease;
  z-index: 99999;
}
nav.sticky {
  background-color: #141517;
}
nav .nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  margin: 0 50px;
}
nav .nav-content .nav-left {
  display: flex;
  align-items: center;
}
nav .nav-content .nav-right {
  display: flex;
}

.nav-content .nav-left ul {
  margin-left: 50px;
}

.nav-content .nav-left .logo a {
  font-size: 25px;
  font-weight: 500;
  color: #e50815;
  text-decoration: none;
}

.nav-content .nav-links {
  display: flex;
  align-items: center;
}

.nav-content .nav-links li {
  margin: 0 16px;
  font-size: 15px;
  padding: 10px 4px;
  color: #fff;
  cursor: pointer;
  transition: 0.3s ease;
}
.nav-content .nav-links li:hover {
  transform: scale(1.1);
}

.nav-content .nav-links li a {
  color: #fff;
  text-decoration: none;
}
.nav-content .nav-links li a:hover {
  color: #b3b3b3;
  transition: all 0.4s ease;
  transform: scale(1.1);
}
</style>
