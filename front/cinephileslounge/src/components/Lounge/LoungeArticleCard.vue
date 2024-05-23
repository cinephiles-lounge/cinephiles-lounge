<template>
  <li class="card-wrapper">
    <div class="card-header">
      <div class="profile">
        <i class="bx bxl-github"></i>
        <h1>{{ article.user.nickname }}</h1>
      </div>
      <div class="rank">
        <i class="bx bxs-star"></i>
        <span class="rank">{{ article.rank }}</span>
      </div>
    </div>
    <div class="card-main">
      <p>
        {{ truncateOverview(article.content, 125) }}
      </p>
    </div>
    <div class="card-section">
      <i class="bx bxs-like"></i>
      {{ article.like_count }}
      <i class="bx bxs-message-rounded"></i>
      {{ article.comment_set.length }}
    </div>
    <div class="card-footer">
      <div>{{ formatTimeDifference(article.created_at) }}</div>
      <div
        class="btn"
        @click="
          router.push({
            name: 'FeedDetailView',
            params: { article_pk: article.id },
          })
        "
      >
        더보기
      </div>
    </div>
  </li>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
defineProps({
  article: Object,
});
// 글 내용 길면 자르기
const truncateOverview = (overview, maxLength) => {
  return overview.length > maxLength
    ? overview.substring(0, maxLength) + "..."
    : overview;
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
.card-wrapper {
  width: 324px;
  background-color: rgb(212, 210, 210);
  border-radius: 5px;
  color: #000;
  padding: 0px 12px;
}
.card-wrapper .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e5e5;
  font-size: 17px;
  height: 55px;
  width: 100%;
}
.card-wrapper .card-header .profile {
  display: flex;
}
.card-wrapper .card-header .rank {
  font-size: 14px;
  display: flex;
  align-items: center;
}
.card-wrapper .card-main {
  margin-top: 12px;
  margin-bottom: 15px;
  height: 120px;
  max-height: 120px;
  overflow: hidden;
}
.card-wrapper .card-main p {
  font-size: 15px;
  line-height: 1.6em;
}
.card-wrapper .card-section {
  border-top: 1px solid #e5e5e5;
  border-bottom: 1px solid #e5e5e5;
  height: 30px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.card-wrapper .card-footer {
  padding: 0px 0.9px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-wrapper .card-footer .btn {
  cursor: pointer;
  transition: 0.3s;
}
.card-wrapper .card-footer .btn:hover {
  transform: scale(1.03);
}
</style>
