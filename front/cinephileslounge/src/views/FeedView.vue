<template>
  <div class="feed">
    <div class="subs">
      <h1>구독한 사람의 글</h1>
      <p>{{ feedStore.subscribedArticles }}</p>
      <p v-if="feedStore.subscribedArticles.length >= 1">게시글 채워야함</p>
      <p v-if="feedStore.subscribedArticles.length == 0">
        아직 구독한 사람이 없습니다.
      </p>
    </div>
    <div class="popular">
      <h1>인기글</h1>
      <FeedPopular
        @click="navigateToPopularArticleDetail(popularArticle.id)"
        v-for="popularArticle in feedStore.popularArticles"
        :key="popularArticle.id"
        :popularArticle="popularArticle"
      />
    </div>
    <div class="board-container">
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
  </div>
</template>
<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { useRouter } from "vue-router";
import FeedPopular from "@/components/Feed/FeedPopular.vue";
const feedStore = useFeedStore();
const router = useRouter();

feedStore.getArticles(); // 전체 게시글 조회
feedStore.getSubs(); // 구독한 사람의 게시글 조회
feedStore.getPopular(); // 인기 게시글 조회

// 게시글 클릭 -> 디테일 페이지로 이동
const navigateToPopularArticleDetail = (id) => {
  router.push({ name: "FeedDetailView", params: { article_pk: id } });
};
</script>

<style scoped>
.feed {
  padding-top: 50px;
}
h1 {
  font-size: 50px;
  margin-top: 50px;
}
</style>
