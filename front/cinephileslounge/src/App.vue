<template>
  <main>
    <NavBar />
    <RouterView />
  </main>
</template>
<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
</script>

<style scoped>
main {
  background-color: #000;
  color: #eee;
}
</style>
