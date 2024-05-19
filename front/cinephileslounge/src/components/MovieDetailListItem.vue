<template>
  <h1>내용 : {{ review.content }}</h1>
  <p>작성자 : {{ review.user.nickname }}</p>
  <p>{{ review.rank }}</p>
  <h1>{{ review.id }}</h1>
  <button @click="delete_shortReview">삭제</button>
</template>
<script setup>
import axios from "axios";
import { useAccountStore } from "@/stores/account";
import { ref } from "vue";
const accountStore = useAccountStore();
const props = defineProps({
  shortReview: Object,
});
const emit = defineEmits(["delete"]);
const review = ref(props.shortReview);

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
      emit("delete", review.value.id); //emit으로 부모 컴포넌트에게 reviewId 보내고 거기서 front단에 보이도록 삭제
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>
<style scoped></style>
