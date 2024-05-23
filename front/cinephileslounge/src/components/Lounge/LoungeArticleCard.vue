<template>
  <li class="card-wrapper">
    <div class="card-header">
      <div class="profile">
        <i class="bx bxl-github"></i>
        <h1>{{ article.user.nickname }}</h1>
      </div>
      <div>
        <i class="bx bxs-star"></i>
        <span class="rank">{{ article.rank }}</span>
      </div>
    </div>
    <div class="card-main">
      <p>
        {{ article.content }}
      </p>
    </div>
    <div class="card-section">
      <i class="bx bxs-like"></i>
      {{ article.like_count }}
      <i class="bx bxs-message-rounded"></i>
      {{ article.comment_set.length }}
    </div>
    <div class="card-footer">좋아요</div>
  </li>
</template>

<script setup>
defineProps({
  article: Object,
});
</script>

<style scoped>
.card-wrapper {
  width: 324px;
  background-color: #f2f2f2;
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
}
.card-wrapper .card-main {
  margin-top: 12px;
  margin-bottom: 15px;
  height: 120px;
}
.card-wrapper .card-main p {
  font-size: 15px;
  line-height: 1.6em;
}
.card-wrapper .card-section {
  border-top: 1px solid #e5e5e5;
  border-bottom: 1px solid #e5e5e5;
}
.card-wrapper .card-footer {
  padding: 0px 0.9px;
}
</style>
