<template>
  <div class="create-container">
    <div class="userInput">
      <form @submit.prevent="isEditMode ? updateArticle() : createArticle()">
        <label for="title"> </label>
        <input type="text" id="title" v-model.trim="title" />
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
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useLoungeStore } from "@/stores/lounges";

const loungeStore = useLoungeStore();
const route = useRoute();
const router = useRouter();

const isEditMode = ref(false); // 수정인지 생성인지 구분하기 위해
const title = ref(null);
const content = ref(null);

// 마운트될때 url에 loungeArticlePk가 있으면 수정모드 없으면 생성모드
onMounted(() => {
  const loungeArticlePk = route.params.loungeArticlePk;
  if (loungeArticlePk) {
    isEditMode.value = true;
    loungeStore.getLoungeArticle(loungeArticlePk);
    title.value = loungeStore.loungeArticleDetail.title;
    content.value = loungeStore.loungeArticleDetail.content;
  }
});

// 게시글 생성
const createArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
  };
  loungeStore.createLoungeArticle(payload);
};

// 게시글 수정
const updateArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
  };
  loungeStore.updateLoungeArticle(payload);
};

// 게시글 수정 취소시 라운지 디테일 페이지로 이동
const cancelUpdate = () => {
  router.push({
    name: "LoungeDetailView",
    params: { loungePk: route.params.loungePk },
  });
};
</script>
<style scoped>
.create-container {
  padding: 100px;
  display: flex;
  justify-content: center;
  min-height: 100vh;
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
