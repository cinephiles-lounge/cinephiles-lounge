<template>
  <h1>리뷰 페이지</h1>
  <p>한줄리뷰 작성</p>
  <p>{{ content }}</p>
  <form>
    <input type="text" v-model="content" />
    <input type="submit" />
  </form>
  <MovieDetailListItem
    v-for="shortReview in shortReviews"
    :key="shortReview.id"
    :shortReview="shortReview"
  />
</template>
<script setup>
import { ref } from "vue";
import MovieDetailListItem from "@/components/MovieDetailListItem.vue";
defineProps({
  shortReviews: Array,
});
const content = ref("");
</script>
<style scoped></style>
