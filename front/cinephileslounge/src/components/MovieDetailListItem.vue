<template>
  <h1>내용 : {{ review.content }}</h1>
  <p>작성자 : {{ review.user.nickname }}</p>
  <p>별점 : {{ review.rank }}</p>
  <button
    @click="delete_shortReview"
    v-if="!isUpdate && accountStore.userNickname === review.user.nickname"
  >
    <!--유저 닉네임 말고 유저 아이디로 수정-->
    삭제
  </button>
  <button
    @click="isUpdate = !isUpdate"
    v-if="!isUpdate && accountStore.userNickname === review.user.nickname"
  >
    수정
  </button>
  <star-rating
    v-if="isUpdate"
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
  <input v-if="isUpdate" v-model.trim="content" type="text" />
  <input
    @click.prevent="update_shortReview"
    v-if="isUpdate"
    type="submit"
    value="수정"
  />
  <input
    v-if="isUpdate"
    type="submit"
    value="취소"
    @click.prevent="isUpdate = !isUpdate"
  />
</template>
<script setup>
import axios from "axios";
import { useAccountStore } from "@/stores/account";
import { ref } from "vue";
import StarRating from "vue-star-rating";
const accountStore = useAccountStore();
const props = defineProps({
  shortReview: Object,
});
const emit = defineEmits(["delete"]);
const review = ref(props.shortReview);
const isUpdate = ref(false);
const userRating = ref();
const content = ref("");

// 사용자가 입력한 별점 userRating에 저장
const setRating = (rating) => {
  userRating.value = rating;
};
// 한줄 리뷰 삭제
const delete_shortReview = () => {
  axios({
    method: "delete",
    url: `${accountStore.API_URL}/movies/short_review/${review.value.id}`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      emit("delete", review.value.id); //emit으로 부모 컴포넌트에게 reviewId 보내고 거기서 front에 보이도록 삭제
    })
    .catch((err) => {
      console.log(err);
    });
};
// 한줄 리뷰 수정
const update_shortReview = () => {
  axios({
    method: "put",
    url: `${accountStore.API_URL}/movies/short_review/${review.value.id}/`,
    data: {
      content: content.value,
      rank: userRating.value,
    },
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      review.value.content = res.data.content; // front에서도 수정 된것처럼 랜더링
      review.value.rank = res.data.rank;
      isUpdate.value = false; // html요소들 다시 안보이게 isUpdate false
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>
<style scoped></style>
