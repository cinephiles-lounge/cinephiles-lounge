<template>
  <h1>리뷰 페이지</h1>
  <p>한줄리뷰 작성</p>
  <form v-if="accountStore.isLogin" @submit.prevent="createShortReview">
    <star-rating
      @update:rating="setRating"
      :increment="0.5"
      :max-rating="5"
      :rounded-corners="true"
      :inline="true"
      :show-rating="false"
      :active-color="['#520000', '#520000']"
      :active-border-color="['#F6546A', '#948989']"
      :border-width="3"
      :star-size="24"
      :active-on-click="true"
      :clearable="true"
    >
    </star-rating>
    <input type="text" v-model.trim="inputContent" />
    <input type="submit" />
  </form>
  <MovieDetailListItem
    v-for="shortReview in sortedShortReviews"
    :key="shortReview.id"
    :shortReview="shortReview"
    @delete="delete_review"
  />
</template>
<script setup>
import { ref, computed, watch } from "vue";
import { useAccountStore } from "@/stores/account";
import MovieDetailListItem from "@/components/MovieDetailListItem.vue";
import axios from "axios";
import StarRating from "vue-star-rating";
const userRating = ref(1);
// 사용자가 입력한 별점 userRating에 저장
const setRating = (rating) => {
  userRating.value = rating;
};
// shortReviews created_at 최신순으로 정렬
const sortedShortReviews = computed(() => {
  return [...reviews.value].sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );
});
const props = defineProps({
  shortReviews: Array,
  movieId: Number,
});
const reviews = ref(props.shortReviews);
const accountStore = useAccountStore();
const inputContent = ref("");

// 부모 컴포넌트한테 받은 shortReviews prop을 watch로 변할때마다 업데이트
watch(
  () => props.shortReviews,
  (newReviews) => {
    reviews.value = [...newReviews];
  }
);
// 한줄리뷰 생성
const createShortReview = () => {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/movies/short_review/create/${props.movieId}/`,
    data: {
      content: inputContent.value,
      rank: userRating.value,
    },
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      reviews.value = [...reviews.value, res.data];
      inputContent.value = "";
      // front 에서도 바로 추가된것처럼 보이게
    })
    .catch((err) => {
      console.log(err);
    });
};

const delete_review = (reviewId) => {
  reviews.value = reviews.value.filter((review) => review.id !== reviewId);
  // front에서도 바로 삭제된것처럼 보이게
};
</script>
<style scoped></style>
