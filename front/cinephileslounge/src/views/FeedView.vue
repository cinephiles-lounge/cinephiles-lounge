<template>
  <div class="feed">
    <h1>게시글 전체조회</h1>
    <div v-for="article in feedStore.articles" :key="article.id">
      <RouterLink
        :to="{ name: 'FeedDetailView', params: { article_pk: article.id } }"
        >{{ article.title }}</RouterLink
      >
    </div>
    <button>
      <RouterLink :to="{ name: 'FeedCreateView' }">글 생성</RouterLink>
    </button>
  </div>
</template>
<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
const feedStore = useFeedStore();
onMounted(() => {
  feedStore.getArticles();
});
</script>

<style scoped>
.feed {
  padding-top: 50px;
}
</style>
