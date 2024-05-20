<template>
  <nav :class="{ sticky: isSticky }">
    <div class="nav-content">
      <div class="nav-left">
        <div class="logo">
          <RouterLink :to="{ name: 'HomeView' }">CinePhile Lounge</RouterLink>
        </div>
        <ul class="nav-links">
          <li><RouterLink :to="{ name: 'HomeView' }">홈</RouterLink></li>
          <li><RouterLink :to="{ name: 'FeedView' }">피드</RouterLink></li>
          <li><a href="#">라운지</a></li>
          <li><a href="#">검색</a></li>
        </ul>
      </div>
      <div class="nav-right">
        <form action="#">
          <i @click="isSearch = !isSearch" class="bx bx-search"></i>
          <input
            v-if="isSearch"
            type="text"
            placeholder=" 검색어를 입력해주세요"
          />
        </form>
        <ul class="nav-links">
          <li v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
          </li>
          <li v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'RegistrationView' }">회원가입</RouterLink>
          </li>
          <li v-if="accountStore.isLogin" @click="logOut">로그아웃</li>
          <li v-if="accountStore.isLogin"><a href="#">마이페이지</a></li>
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
import { useRouter } from "vue-router";
import axios from "axios";

const accountStore = useAccountStore();
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
      router.push({ name: "HomeView" });
    })
    .catch((err) => {
      console.log("로그아웃 실패");
      console.log(err);
    });
};
</script>

<style scoped>
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
  background-color: #0b1010;
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
}

.nav-content .nav-links li a {
  color: #fff;
  text-decoration: none;
}
.nav-content .nav-links li a:hover {
  color: #b3b3b3;
  transition: all 0.4s ease;
}
.nav-content .nav-right form {
  padding: 10px 4px;
}

.nav-content .nav-right form i {
  color: #fff;
  cursor: pointer;
}

.nav-content .nav-right form input {
  margin-left: 10px;
  border: none;
  font-size: 15px;
  background-color: #fff;
  padding: 6px;
  color: black;
  border-radius: 8px;
  outline: none;
}
</style>
