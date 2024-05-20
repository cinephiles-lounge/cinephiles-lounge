<template>
  <div class="create-container">
    <h1>
      {{ isEditMode ? "글 수정 페이지" : "글 생성 페이지" }}
    </h1>
    <form @submit.prevent="isEditMode ? updateArticle() : createArticle()">
      <label for="title">제목 : </label>
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
      <label for="content">내용</label>
      <textarea
        id="content"
        v-model.trim="content"
        cols="30"
        rows="10"
      ></textarea
      ><br />
      <input type="submit" :value="isEditMode ? '수정' : '생성'" />
    </form>
    <button v-if="isEditMode" @click="cancelUpdate">취소</button>
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

// 게시글 생성(movie_id 수정해야됨)
const createArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
    rank: userRating.value,
    movieId: 808, //이거 검색으로 할지? 아직 미정
  };
  feedStore.createArticle(payload);
};

// 게시글 수정(movie_id 수정해야됨)
const updateArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
    rank: userRating.value,
    article_pk: route.params.article_pk,
    movieId: 808,
  };
  feedStore.updateArticle(payload);
};

// 게시글 수정 취소시 게시글 디테일 페이지로 이동
const cancelUpdate = () => {
  router.push({
    name: "FeedDetailView",
    params: { article_pk: route.params.article_pk },
  });
};
</script>
<style scoped>
.create-container {
  margin-top: 50px;
}
</style>
