<template>
  <div class="detail-container">
    <h1>{{ articleId }}번게시글 상세조회</h1>
    <p>제목 : {{ feedStore.article.title }}</p>
    <p>내용 : {{ feedStore.article.content }}</p>
    <p>작성자 : {{ feedStore.article.user.nickname }}</p>
    <p>좋아요 수 : {{ feedStore.article.like_count }}</p>
    <p>영화 : {{ feedStore.article.movie.title }}</p>
    <p>평점 : {{ feedStore.article.rank }}</p>
    <button
      @click="subs"
      v-if="feedStore.article.user.id !== accountStore.userPk"
    >
      구독
    </button>
    <button v-if="feedStore.article.user.id !== accountStore.userPk">
      좋아요
    </button>
    <button
      v-if="feedStore.article.user.id === accountStore.userPk"
      @click="updateArticle"
    >
      수정
    </button>
    <button
      v-if="feedStore.article.user.id === accountStore.userPk"
      @click="deleteArticle"
    >
      삭제
    </button>
  </div>
</template>
<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { useAccountStore } from "@/stores/account";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
const feedStore = useFeedStore();
const accountStore = useAccountStore();
const route = useRoute();
const router = useRouter();
const articleId = route.params.article_pk;

onMounted(() => {
  feedStore.getArticle(articleId);
});

// 게시글 삭제
const deleteArticle = () => {
  feedStore.deleteArticle(articleId);
};

// 수정폼으로 이동
const updateArticle = () => {
  router.push({ name: "FeedEditView", params: { article_pk: articleId } });
};

// 구독 & 구독취소
const subs = () => {};
</script>

<style scoped>
.detail-container {
  padding-top: 50px;
}
</style>
