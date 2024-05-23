<template>
  <div class="lounge-detail-page">
    <MovieSlider
      v-if="loungeStore.loungeMovies && loungeStore.loungeMovies.length > 0"
      :movies="loungeStore.loungeMovies"
      :title="`${loungeStore.loungeData.name}의 회원들이 좋아하는 영화`"
    />

    <section class="current-review-container">
      <header>
        <h1>
          {{ loungeStore.loungeData.name }}의 회원들이 가장 최근에 작성한 영화
        </h1>
      </header>
      <ul class="article-card-wrapper">
        <LoungeArticleCard
          v-for="article in loungeStore.loungeReviews"
          :key="article.id"
          :article="article"
          @click="
            router.push({
              name: 'FeedDetailView',
              params: { article_pk: article.id },
            })
          "
        />
      </ul>
    </section>

    <main classs="member-articles-container">
      <div class="review">
        <h1>
          {{ loungeStore.loungeData.name }}의 회원들이 가장 최근에 작성한 영화
          리뷰
        </h1>
        <ul v-if="loungeStore.loungeReviews" class="slide">
          <FeedCard
            v-for="article in loungeStore.loungeReviews"
            :key="article.id"
            :article="article"
            @click="
              router.push({
                name: 'FeedDetailView',
                params: { article_pk: article.id },
              })
            "
          />
        </ul>
        <p v-else>아직 작성한 영화 리뷰가 없습니다.</p>
      </div>

      <div class="lounge-article">
        <div class="lounge-article-header">
          <h1>라운지 전체 게시글</h1>
          <button
            @click="
              router.push({
                name: 'LoungeArticleCreateView',
              })
            "
          >
            생성
          </button>
        </div>
        <ul v-if="loungeStore.loungeArticles">
          <li
            v-for="article in loungeStore.loungeArticles"
            :key="article.id"
            :article="article"
            @click="
              router.push({
                name: 'LoungeArticleDetailView',
                params: {
                  loungeArticlePk: article.id,
                },
              })
            "
          >
            {{ article.title }}
          </li>
        </ul>
        <p v-else>아직 작성한 게시글이 없습니다.</p>
      </div>
    </main>

    <aside class="member-info-container">
      <div class="admin">
        <h1>관리자</h1>
        <div class="profile-container">
          <i class="bx bxl-github"></i>
          <p class="profile-name-p">
            {{ loungeStore.loungeData.admin.nickname }}
          </p>
        </div>
      </div>

      <div class="info">
        <div class="member">
          <h1>멤버</h1>
          <div
            class="profile-container"
            v-for="member in loungeStore.loungeData.non_admin_members"
            :key="member.id"
          >
            <i class="bx bxl-github"></i>
            <p class="profile-name-p">
              {{ member.nickname }}
            </p>
          </div>
        </div>

        <div class="setting">
          <template
            v-if="loungeStore.loungeData.admin.id === accountStore.userPk"
          >
            <button @click="toggleModal">수정</button>
            <button @click="deleteLounge">삭제</button>
          </template>
          <template v-else>
            <button @click="leaveLounge">탈퇴</button>
          </template>
        </div>
      </div>
    </aside>

    <div class="modal-wrap" v-show="isModalOpen" @click="toggleModal">
      <div class="modal-container" @click.stop="">
        <form @submit.prevent="updateLounge">
          <div class="modal-input">
            <label for="name">라운지 이름</label>
            <input
              type="text"
              name="name"
              id="name"
              v-model="loungeName"
              required
            />
          </div>
          <div class="modal-input">
            <label for="description">라운지 소개</label>
            <textarea
              name="description"
              id="description"
              v-model="loungeDescription"
              required
            ></textarea>
          </div>

          <p v-show="errorMessage">{{ errorMessage }}</p>

          <div class="modal-btn">
            <button type="submit">수정</button>
            <button @click.prevent="toggleModal">닫기</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useLoungeStore } from "@/stores/lounges";
import { useRoute, useRouter } from "vue-router";
import FeedCard from "@/components/Feed/FeedCard.vue";
import { useAccountStore } from "@/stores/account";
import axios from "axios";
import MovieSlider from "@/components/MovieSlider/MovieSlider.vue";
import LoungeArticleCard from "@/components/Lounge/LoungeArticleCard.vue";
const route = useRoute();
const router = useRouter();

const loungeStore = useLoungeStore();
const accountStore = useAccountStore();

loungeStore.getLounge(route.params.loungePk);

// 모달 변수
const isModalOpen = ref(false);
const loungeName = ref(loungeStore.loungeData.name);
const loungeDescription = ref(loungeStore.loungeData.description);

// 모달 여닫는 기능
const toggleModal = function () {
  isModalOpen.value = !isModalOpen.value;
  loungeName.value = loungeStore.loungeData.name;
  loungeDescription.value = loungeStore.loungeData.description;
};

// 라운지 수정
const updateLounge = function () {
  if (window.confirm("수정하시겠습니까?")) {
    axios({
      method: "put",
      url: `${accountStore.API_URL}/lounges/${loungeStore.loungeData.id}/update/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
      data: {
        name: loungeName.value,
        description: loungeDescription.value,
      },
    })
      .then((res) => {
        console.log(res);
        loungeStore.loungeData = res.data;
        console.log(loungeStore.loungeData);
        return res;
      })
      .then((res) => {
        toggleModal();
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

// 라운지 삭제
const deleteLounge = function () {
  if (window.confirm("라운지를 삭제하시겠습니까?")) {
    loungeStore.deleteLounge();
    router.push({ name: "LoungeView" });
  }
};

// 라운지 탈퇴
const leaveLounge = function () {
  if (window.confirm("라운지를 탈퇴하시겠습니까?")) {
    loungeStore.leaveLounge();
    router.push({ name: "LoungeView" });
  }
};
</script>

<style scoped>
/* 전체 페이지 */
.lounge-detail-page {
  padding-top: 80px;
  width: 100vw;
  min-height: 100vh;
  background-color: black;
  color: #fff;
}

/* 회원들이 가장 최근에 작성한 리뷰 */
.current-review-container {
  margin: 30px 65px;
}

/* 라운지 전체 게시글 */

.lounge-article {
  background-color: white;
  opacity: 0.9;
  color: black;
  border-radius: 10px;
  padding: 20px;
}

.lounge-article-header {
  display: flex;
  justify-content: space-between;
}

.member-info-container {
  background-color: white;
  opacity: 0.9;
  color: black;
  border-radius: 10px;
  padding: 20px;
  margin: 10px;
}

/* 모달 */

/* dimmed */
.modal-wrap {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* modal or popup */
.modal-container {
  color: black;
  position: relative;
  height: 200px;
  width: 300px;
  background: #fff;
  border-radius: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 3px;
}

.modal-btn {
  display: flex;
  justify-content: center;
}

.modal-btn > button {
  margin: 5px;
}
</style>
