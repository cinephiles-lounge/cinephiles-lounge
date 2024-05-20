<template>
  <div class="feed">
    <p>{{ feedStore.articles }}</p>
  </div>
</template>
<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { ref, onMounted } from "vue";
const feedStore = useFeedStore();
onMounted(() => {
  feedStore.getArticles();
});
</script>
<style scoped>
.feed {
  padding-top: 50px;
  background-color: black;
}
</style>
