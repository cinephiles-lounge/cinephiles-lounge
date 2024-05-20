<template>
  <div class="create-review-container" v-if="accountStore.isLogin">
    <star-rating
      @update:rating="setRating"
      :increment="0.5"
      :max-rating="5"
      :rounded-corners="true"
      :inline="true"
      :show-rating="false"
      :active-color="['#f82e62']"
      :active-border-color="['#f82e62']"
      :border-width="1"
      :star-size="24"
      :active-on-click="true"
      :clearable="true"
    >
    </star-rating>
    <div class="review-userInput">
      <input
        class="review-userInput-text"
        type="text"
        v-model.trim="inputContent"
      />
      <input
        class="review-userInput-btn"
        @click.prevent="createShortReview"
        type="submit"
        value="작성"
      />
    </div>
  </div>
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
const userRating = ref(0);
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
      userRating.value = 0;
      // front 에서도 바로 추가된것처럼 보이게
    })
    .catch((err) => {
      console.log(err);
      if (userRating.value === 0) {
        window.alert("평점을 입력해주세요");
      }
    });
};

const delete_review = (reviewId) => {
  reviews.value = reviews.value.filter((review) => review.id !== reviewId);
  // front에서도 바로 삭제된것처럼 보이게
};
</script>
<style scoped>
.create-review-container {
  border-bottom: 1px solid #1b1c1d;
  max-width: 1680px;
  display: flex;
  flex-direction: column;
  padding-top: 5px;
  padding-bottom: 20px;
}
.create-review-container .review-userInput {
  margin-top: 10px;
  display: flex;
  align-items: center;
}

.create-review-container .review-userInput .review-userInput-text {
  height: 50px;
  width: 500px;
  border: none;
  border-radius: 5px;
  margin-right: 13px;
  background-color: #222326;
  outline: none;
  color: #eee;
  font-size: 15px;
}
.create-review-container .review-userInput .review-userInput-btn {
  height: 50px;
  width: 90px;
  font-size: 15px;
  border-radius: 5px;
  background-color: #f82e62;
  color: #eee;
  border: none;
}
</style>
