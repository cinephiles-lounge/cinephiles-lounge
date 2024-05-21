<template>
  <div class="detail-container">
    <h1>{{ articleId }}번게시글 상세조회</h1>
    <p>제목 : {{ feedStore.article.title }}</p>
    <p>내용 : {{ feedStore.article.content }}</p>
    <p>작성자 : {{ feedStore.article.user.nickname }}</p>
    <p>작성시간 : {{ formatTimeDifference(feedStore.article.created_at) }}</p>
    <p>좋아요 수 : {{ feedStore.article.like_count }}</p>
    <p>영화 : {{ feedStore.article.movie.title }}</p>
    <p>평점 : {{ feedStore.article.rank }}</p>
    <p>내가 구독하는 사람들 {{ accountStore.subscriptions }}</p>
    <p>내 구독자들 {{ accountStore.subscribers }}</p>
    <button
      @click="subscribe"
      v-if="feedStore.article.user.id !== accountStore.userPk"
    >
      {{ isSubs ? "구독취소" : "구독" }}
    </button>
    <div
      v-if="feedStore.article.user.id !== accountStore.userPk"
      class="content-btn"
    >
      <i @click="toggleLike" v-if="!isLiked" class="bx bx-heart"></i>
      <i @click="toggleLike" v-if="isLiked" class="bx bxs-heart"></i>
    </div>

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

    <div class="comment-container">
      <h1>게시글 댓글</h1>
      <div v-if="accountStore.isLogin">
        <input type="text" v-model.trim="content" />
        <input @click="createComment" type="submit" value="작성" />
      </div>
      <div v-for="comment in feedStore.article.comment_set" :key="comment.id">
        <p>
          {{ comment.user.nickname }}: {{ comment.content }}
          {{ formatTimeDifference(comment.created_at) }}
        </p>
        <button
          v-if="comment.user.id === accountStore.userPk"
          @click="deleteComment(comment.id)"
        >
          삭제
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { useAccountStore } from "@/stores/account";
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import axios from "axios";
const feedStore = useFeedStore();
const accountStore = useAccountStore();
const route = useRoute();
const router = useRouter();
const articleId = route.params.article_pk;
const content = ref(null);

// 구독 확인
const isSubs = computed(() => {
  if (!accountStore.subscriptions) return false; // 내가 구독하는 사람이 아무도 없으면 false
  return accountStore.subscriptions.some(
    // 현재 게시글 작성자를 구독하고 있으면 true
    (user) => user.id === feedStore.article.user.id
  );
});

// 구독 & 구독취소(toggle)
const subscribe = () => {
  feedStore.subscribe(feedStore.article.user.id, isSubs.value);
};

// 게시글 좋아요 확인
const isLiked = computed(() => {
  if (!feedStore.article.liked_users) return false; // 좋아요 누른 유저가 아무도 없으면 false
  return feedStore.article.liked_users.some(
    // 현재 유저가 좋아요 눌렀으면 true
    (user) => user === accountStore.userPk
  );
});

// 게시글 좋아요 & 취소(toggle)
const toggleLike = () => {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/articles/${articleId}/like/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      feedStore.getArticle(articleId);
    })
    .catch((err) => {
      console.log(err);
    });
};

// 게시글 상세 조회
feedStore.getArticle(articleId);

// 게시글 삭제
const deleteArticle = () => {
  feedStore.deleteArticle(articleId);
};

// 댓글 생성
const createComment = () => {
  const payload = {
    articleId: articleId,
    content: content.value,
  };
  feedStore.createComment(payload);
};

// 댓글 삭제
const deleteComment = (commentId) => {
  axios({
    method: "delete",
    url: `${accountStore.API_URL}/articles/comment/${commentId}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      console.log("삭제성공");
      feedStore.getArticle(articleId);
    })
    .catch((err) => {
      console.log(err);
    });
};
// 수정폼으로 이동
const updateArticle = () => {
  router.push({ name: "FeedEditView", params: { article_pk: articleId } });
};

// 시간 포멧팅 함수
const formatTimeDifference = (dateString) => {
  const now = new Date(); //현재시간
  const date = new Date(dateString); //게시글 작성시간
  const diff = (now - date) / 1000; // 초 단위 차이

  if (diff < 60) {
    return `${Math.floor(diff)}초 전`;
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}분 전`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}시간 전`;
  } else {
    return `${Math.floor(diff / 86400)}일 전`;
  }
};
</script>

<style scoped>
.detail-container {
  padding-top: 50px;
}
</style>
