<template>
  <nav :class="{ sticky: isSticky }">
    <div class="nav-content">
      <div class="nav-left">
        <div class="logo">
          <a href="#">CinePhile Lounge</a>
        </div>
        <ul class="nav-links">
          <li><RouterLink :to="{ name: 'home' }">홈</RouterLink></li>
          <li><a href="#">피드</a></li>
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
          <li><RouterLink :to="{ name: 'login' }">로그인</RouterLink></li>
          <li><RouterLink :to="{ name: 'registration' }">회원가입</RouterLink></li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
// 로그인하면 회원가입버튼 안보이고 마이페이지랑 알람 뜨도록
import { ref, onMounted, onBeforeUnmount } from "vue";
import { RouterLink, RouterView } from "vue-router";

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
</script>

<style scoped>
nav {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 70px;
  transition: all 0.4s ease;
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
