<template>
  <div class="detail-container">
    <div class="article-container">
      <div class="content">
        <div class="author">
          <i class="bx bxl-github"></i>
          <p
            class="article-user"
            @click="
              accountStore.navigateToUserProfile(feedStore.article.user.id)
            "
          >
            {{ feedStore.article.user.nickname }}
          </p>
          <p>
            {{ formatTimeDifference(feedStore.article.created_at) }}
          </p>
        </div>
        <h1>{{ feedStore.article.title }}</h1>

        <div class="movie-title">
          <p>영화 · {{ feedStore.article.movie.title }}</p>
        </div>
        <div class="movie-rank">
          <i class="bx bxs-star"></i>
          <p>{{ parseFloat(feedStore.article.rank).toFixed(1) }}</p>
        </div>
        <div class="movie-content">{{ feedStore.article.content }}</div>
        <div class="like-count">
          좋아요 {{ feedStore.article.like_count }}
          <div class="article-btn">
            <button
              class="article-update-btn"
              v-if="feedStore.article.user.id === accountStore.userPk"
              @click="updateArticle"
            >
              수정
            </button>
            <button
              class="article-delete-btn"
              v-if="feedStore.article.user.id === accountStore.userPk"
              @click="deleteArticle"
            >
              삭제
            </button>
          </div>
        </div>
        <hr />
        <div class="btn-wrapper">
          <div class="btn-box">
            <button @click="toggleLike">
              <i v-if="!isLiked" class="bx bx-like"></i>
              <i v-if="isLiked" class="bx bxs-like"></i>
              좋아요
            </button>
            <span>|</span>
            <button><i class="bx bx-message-rounded"></i>댓글</button>
            <span>|</span>

            <button @click="subscribe">
              <i v-if="!isSubs" class="bx bx-bell"></i>
              <i v-if="isSubs" class="bx bxs-bell"></i>
              {{ isSubs ? "글쓴이 구독취소" : "글쓴이 구독" }}
            </button>
          </div>
        </div>
        <hr />
      </div>
      <div
        class="img-box"
        :style="{
          '--backdrop-url': `url(https://image.tmdb.org/t/p/w1280/${feedStore.article.movie.backdrop_path})`,
        }"
      ></div>
    </div>

    <div class="comment-container">
      <h1>Comments</h1>
      <div v-if="accountStore.isLogin" class="comment-userInput">
        <input
          class="comment-userInput-text"
          type="text"
          v-model.trim="content"
        />
        <input
          class="comment-userInput-btn"
          @click="createComment"
          type="submit"
          value="작성"
        />
      </div>
      <div v-for="comment in sortedComments" :key="comment.id">
        <div class="comment-wrapper">
          <div class="profile-img">
            <i class="bx bxl-github"></i>
          </div>
          <div class="comment-content">
            <div class="comment-header">
              <span
                class="comment-nickname"
                @click="accountStore.navigateToUserProfile(comment.user.id)"
                >{{ comment.user.nickname }}</span
              >
              <span class="writed-at">{{
                formatTimeDifference(comment.created_at)
              }}</span>
            </div>
            <div class="comment-des">
              <p>{{ comment.content }}</p>
              <i
                v-if="comment.user.id === accountStore.userPk"
                @click="deleteComment(comment.id)"
                class="bx bxs-message-square-x"
              ></i>
            </div>
          </div>
        </div>
        <hr />
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

// 댓글 최신순으로 정렬
const sortedComments = computed(() => {
  return [...feedStore.article.comment_set].sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );
});

// 댓글 생성
const createComment = () => {
  const payload = {
    articleId: articleId,
    content: content.value,
  };
  feedStore.createComment(payload);
  content.value = "";
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
  padding: 70px;
  position: relative;
  min-height: 100vh;
}
.detail-container .article-container {
  display: flex;
  margin-top: 100px;
  margin-left: 110px;
  margin-right: 110px;
}
.detail-container .article-container .img-box {
  background: linear-gradient(
      to right top,
      rgba(0, 0, 0, 1) 0%,
      rgba(0, 0, 0, 1) 30%,
      rgba(0, 0, 0, 0.8) 35%,
      rgba(0, 0, 0, 0.7) 40%,
      rgba(0, 0, 0, 0.6) 50%,
      rgba(0, 0, 0, 0) 100%
    ),
    var(--backdrop-url);
  width: 1200px;
  height: 500px;
  position: absolute;
  top: 70px;
  right: 170px;
}
.detail-container .article-container .content {
  z-index: 1;
}
.detail-container .article-container .content h1 {
  font-size: 40px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.detail-container .article-container .content .author {
  display: flex;
  color: #babac1;
}
.detail-container .article-container .content .author i {
  margin-right: 10px;
}
.detail-container .article-container .content .author p {
  margin-right: 10px;
}
.detail-container .article-container .content .movie-title {
  color: #babac1;
}
.detail-container .article-container .content .movie-rank {
  display: flex;
  margin-top: 10px;
  margin-bottom: 20px;
  /* color: #babac1; */
}
.detail-container .article-container .content .movie-rank i {
  margin-right: 5px;
}
.detail-container .article-container .content .movie-content {
  font-size: 17px;
  line-height: 20px;
  margin-bottom: 10px;
  min-width: 1000px;
  min-height: 250px;
}
.detail-container .article-container .content .like-count {
  color: #babac1;
  margin-top: 32px;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.detail-container .article-container .content .like-count .article-btn button {
  background-color: #f82e62;
  margin-right: 10px;
  border-radius: 5px;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 15px;
  transition: 0.3s ease;
  color: #eee;
  width: 70px;
}
.detail-container
  .article-container
  .content
  .like-count
  .article-btn
  button:hover {
  transform: scale(1.1);
}
.detail-container
  .article-container
  .content
  .like-count
  .article-btn
  .article-delete-btn {
  margin-left: 10px;
  background-color: #262626;
}

.detail-container .article-container .content .btn-wrapper {
  width: 100%;
  height: 43px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.detail-container .article-container .content .btn-wrapper button {
  width: 515px;
  height: 37px;
  background-color: transparent;
  border: none;
  color: #eee;
  font-size: 18px;
  cursor: pointer;
  transition: 0.3s;
  color: #babac1;
}
.detail-container .article-container .content .btn-wrapper button:hover {
  transform: scale(1.1);
}
.detail-container .article-container .content .btn-wrapper button i {
  margin-right: 10px;
}
.detail-container .article-container .content .btn-wrapper span {
  color: #48484b;
}
hr {
  height: 1px;
  background-color: #48484b;
  border: none;
}
/* 여기부터 댓글 */
.detail-container .comment-container {
  margin-left: 110px;
  margin-right: 110px;
  margin-top: 32px;
}
.detail-container .comment-container h1 {
  font-size: 22px;
}
.detail-container .comment-container .comment-wrapper {
  display: flex;
  padding: 5px;
}
.detail-container .comment-container .comment-wrapper .profile-img {
  margin-right: 5px;
}
.detail-container .comment-container .comment-wrapper i {
  font-size: 40px;
}
.detail-container .comment-container .comment-wrapper .comment-content {
  display: flex;
  flex-direction: column;
}
.detail-container .comment-container .comment-wrapper .comment-des {
  display: flex;
  color: #7c7b84;
}
.detail-container .comment-container .comment-wrapper .comment-des i {
  font-size: 17px;
  transition: 0.3s;
  cursor: pointer;
}
.detail-container .comment-container .comment-wrapper .comment-des i:hover {
  transform: scale(1.1);
  color: #eee;
}
.detail-container .comment-container .comment-wrapper .comment-content p {
  margin-right: 6px;
}
.detail-container
  .comment-container
  .comment-wrapper
  .comment-content
  .comment-header {
  margin-bottom: 6px;
}
.detail-container
  .comment-container
  .comment-wrapper
  .comment-content
  .comment-header
  .comment-nickname {
  margin-right: 7px;
}
.detail-container
  .comment-container
  .comment-wrapper
  .comment-content
  .comment-header
  .writed-at {
  color: #7c7b84;
  font-size: 14px;
}
/* 댓글 생성폼 */
.comment-container .comment-userInput {
  margin-top: 10px;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.comment-container .comment-userInput .comment-userInput-text {
  height: 50px;
  width: 100%;
  border: none;
  border-radius: 5px;
  margin-right: 13px;
  background-color: #222326;
  outline: none;
  color: #eee;
  font-size: 15px;
}
.comment-container .comment-userInput .comment-userInput-btn {
  height: 50px;
  width: 90px;
  font-size: 15px;
  border-radius: 5px;
  background-color: #f82e62;
  color: #eee;
  border: none;
  cursor: pointer;
  transition: 0.3s;
}
.comment-container .comment-userInput .comment-userInput-btn:hover {
  transform: scale(1.1);
}
.detail-container .article-container .article-user {
  cursor: pointer;
  transition: 0.3s;
}
.detail-container .article-container .article-user:hover {
  transform: scale(1.1);
}
.comment-nickname {
  cursor: pointer;
  transition: 0.3s;
}
</style>
