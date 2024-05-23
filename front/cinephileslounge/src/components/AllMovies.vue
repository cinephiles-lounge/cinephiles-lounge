<template>
  <li class="movie-img">
    <img
      @click="likeMovie"
      :class="{ selected: isSelected }"
      :src="`https://image.tmdb.org/t/p/w1280/${movie.poster_path}`"
      alt=""
    />
  </li>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/account";
import { useRouter } from "vue-router";
import axios from "axios";
const props = defineProps({
  movie: Object,
});
const accountStore = useAccountStore();
const router = useRouter();
const isSelected = ref(false); // 영화 선택 여부

const likeMovie = () => {
  isSelected.value = !isSelected.value; // 영화 선택 상태 toggle
  // 영화 좋아요 toggle
  axios({
    method: "post",
    url: `${accountStore.API_URL}/movies/${props.movie.movie_id}/like/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      console.log("좋아요성공");
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
.movie-img img {
  width: 190px;
  height: 280px;
  border-radius: 5px;
  transition: 0.3s;
  cursor: pointer;
  filter: brightness(0.5);
}
.movie-img:hover {
  transform: scale(1.2);
  z-index: 1;
}
.movie-img img.selected {
  filter: none;
  border: 1px solid #eee;
}
</style>
