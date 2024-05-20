<template>
  <div class="popular-container">
    <h1>{{ popularArticle.id }}</h1>
    <h1>제목 : {{ popularArticle.title }}</h1>
    <p>작성자 : {{ popularArticle.user.nickname }}</p>
    <p>좋아요 : {{ popularArticle.like_count }}</p>
    <p>작성시간 : {{ formatTimeDifference(popularArticle.created_at) }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  popularArticle: Object,
});

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

<style scoped></style>
