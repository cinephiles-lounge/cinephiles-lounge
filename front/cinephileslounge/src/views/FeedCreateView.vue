<template>
  <div class="create-container">
    <div class="userInput">
      <form @submit.prevent="isEditMode ? updateArticle() : createArticle()">
        <label for="title"> </label>
        <input type="text" id="title" v-model.trim="title" />
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
        </star-rating
        ><br />
        <label for="content"></label>
        <textarea
          id="content"
          v-model.trim="content"
          cols="60"
          rows="10"
        ></textarea
        ><br />
        <div class="btn-wrapper">
          <input
            class="create-btn"
            type="submit"
            :value="isEditMode ? '수정' : '생성'"
          />
          <button @click="cancelUpdate" class="cancel-btn">취소</button>
        </div>
      </form>
    </div>

    <div class="movie-container">
      <div class="movie-title">
        <h1>
          {{ feedStore.articleMovieTitle }}
        </h1>
      </div>
      <img
        :src="`https://image.tmdb.org/t/p/w1280/${feedStore.articleMovieImg}`"
        alt=""
      />
      <div class="movie-overview">
        {{ feedStore.articleMovieOverview }}
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useFeedStore } from "@/stores/feed";
import StarRating from "vue-star-rating";
const feedStore = useFeedStore();
const route = useRoute();
const router = useRouter();

const isEditMode = ref(false); // 수정인지 생성인지 구분하기 위해

const title = ref(null);
const content = ref(null);
const userRating = ref(1);

// 마운트될때 url에 article_pk가 있으면 수정모드 없으면 생성모드
onMounted(() => {
  const article_pk = route.params.article_pk;
  if (article_pk) {
    isEditMode.value = true;
    feedStore.getArticle(article_pk);
    title.value = feedStore.article.title;
    content.value = feedStore.article.content;
    userRating.value = feedStore.article.rank;
  }
});

// 사용자가 입력한 별점 userRating에 저장
const setRating = (rating) => {
  userRating.value = rating;
};

// 게시글 생성
const createArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
    rank: userRating.value,
  };
  feedStore.createArticle(payload);
};

// 게시글 수정
const updateArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
    rank: userRating.value,
    article_pk: route.params.article_pk,
  };
  feedStore.updateArticle(payload);
};

// 게시글 수정 취소시 게시글 디테일 페이지로 이동
const cancelUpdate = () => {
  if (isEditMode.value) {
    router.push({
      name: "FeedDetailView",
      params: { article_pk: route.params.article_pk },
    });
  } else {
    router.push({ name: "FeedView" });
  }
};
</script>
<style scoped>
.create-container {
  padding: 100px;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}
.movie-container {
  display: flex;
  flex-direction: column;
  color: #eee;
  margin-left: 60px;
  margin-top: 20px;
}
.movie-container img {
  width: 800px;
  border-radius: 10px;
}
.movie-container .movie-overview {
  max-width: 800px;
  margin-top: 30px;
  color: #7c7b84;
  font-size: 15px;
  letter-spacing: 1px;
  line-height: 20px;
}
.movie-container h1 {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 15px;
}
.userInput {
  margin: 20px;
}
.userInput form {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.userInput input {
  width: 750px;
  height: 30px;
  margin-bottom: 10px;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
  background-color: #222326;
  border: none;
  color: #eee;
  padding: 5px;
}
.userInput textarea {
  height: 515px;
  border-radius: 5px;
  outline: none;
  font-size: 16px;
  background-color: #222326;
  border: none;
  color: #eee;
  padding: 10px;
}
.userInput .btn-wrapper {
  display: flex;
}
.userInput .btn-wrapper .create-btn {
  height: 50px;
  width: 90px;
  font-size: 15px;
  border-radius: 5px;
  background-color: #f82e62;
  color: #eee;
  border: none;
  transition: 0.3s;
  cursor: pointer;
}
.userInput .btn-wrapper .cancel-btn {
  height: 50px;
  width: 90px;
  font-size: 15px;
  border-radius: 5px;
  background-color: #262626;
  color: #eee;
  border: none;
  margin-left: 5px;
  transition: 0.3s;
  cursor: pointer;
}
.userInput .btn-wrapper .create-btn:hover {
  transform: scale(1.1);
}
.userInput .btn-wrapper .cancel-btn:hover {
  transform: scale(1.1);
}
</style>
