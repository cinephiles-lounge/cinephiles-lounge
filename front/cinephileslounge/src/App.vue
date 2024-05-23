<template>
  <main>
    <NavBar />
    <RouterView />
    <i @click="scrollToTop" class="bx bx-arrow-to-top"></i>
  </main>
</template>
<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};
</script>

<style scoped>
main {
  background-color: #000;
  color: #eee;
  width: 100vw;
}
.bx-arrow-to-top {
  position: fixed;
  bottom: 25px;
  right: 35px;
  font-size: 25px;
  padding: 8px;
  color: #8a8a8c;
  background-color: #eee;
  border-radius: 50%;
  transition: 0.3s;
  cursor: pointer;
  z-index: 999;
}
.bx-arrow-to-top:hover {
  transform: scale(1.1);
  filter: brightness(0.7);
}
</style>
