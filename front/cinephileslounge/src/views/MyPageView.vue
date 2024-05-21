<template>
  <div class="my-page">
    <div class="profile-container">
      <div class="reviewItem-img">
        <i class="bx bxl-github"></i>
      </div>
      <p class="profile-name-p">
        <span id="nickname">{{ accountStore.userNickname }}</span>
        <RouterLink :to="{ name: 'UserUpdateView' }"
          ><i class="bx bxs-edit-alt"></i
        ></RouterLink>
      </p>
    </div>

    <div class="slide-container">
      <h3>내가 좋아요 누른 영화</h3>
      <ul v-if="accountStore.likedMovies" class="slide">
        <li v-for="movie in accountStore.likedMovies" :key="movie.movie_id">
          <img
            class="liked-movie-img"
            @click="
              router.push({
                name: 'MovieDetailView',
                params: { movie_id: movie.movie_id },
              })
            "
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          />
        </li>
      </ul>
      <p v-else>아직 좋아요를 누른 영화가 없습니다.</p>
    </div>

    <div class="slide-container">
      <h3>내가 작성한 글</h3>
      <ul v-if="accountStore.postedArticles" class="slide">
        <FeedCard
          v-for="article in accountStore.postedArticles"
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
      <p v-else>아직 작성한 게시글이 없습니다.</p>
    </div>

    <div class="slide-container">
      <h3>
        내가 가입한 라운지
        <button
          id="join-lounge-button"
          @click="switchMode('join'), toggleModal($event)"
        >
          <i class="bx bx-network-chart"></i>
        </button>
        <button
          id="create-lounge-button"
          @click="switchMode('create'), toggleModal($event)"
        >
          <i class="bx bx-add-to-queue"></i>
        </button>
      </h3>
      <ul v-if="accountStore.joinedLounges" class="slide">
        <!-- 내가 관리자인 라운지를 먼저 렌더링 -->
        <li v-for="lounge in accountStore.joinedLounges" :key="lounge.id">
          {{ lounge.name }}
        </li>
      </ul>
      <p v-else>아직 가입한 라운지가 없습니다.</p>
    </div>

    <div class="modal-wrap" v-show="isModalOpen" @click="toggleModal">
      <div class="modal-container" @click.stop="">
        <template v-if="currentMode === 'join'">
          <form @submit.prevent="joinLounge">
            <div class="modal-input">
              <label for="code">가입 코드를 입력하세요.</label>
              <input type="text" id="code" v-model="codeInput" />
            </div>

            <p v-show="errorMessage">{{ errorMessage }}</p>

            <div class="modal-btn">
              <button type="submit">가입</button>
              <button @click.prevent="toggleModal">닫기</button>
            </div>
          </form>
        </template>

        <template v-if="currentMode === 'create'">
          <form @submit.prevent="createLounge">
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
              <button type="submit">생성</button>
              <button @click.prevent="toggleModal">닫기</button>
            </div>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref } from "vue";
import { useAccountStore } from "@/stores/account";
import { useLoungeStore } from "@/stores/lounges";
import { useRouter } from "vue-router";
import FeedCard from "@/components/Feed/FeedCard.vue";
import axios from "axios";

const router = useRouter();
const accountStore = useAccountStore();

accountStore.getUserInfo();

// 모달 모드: 'join' || 'create'
const currentMode = ref("");
const switchMode = function (status) {
  currentMode.value = status;
};

// 모달 여닫는 기능
const isModalOpen = ref(false);
const toggleModal = function () {
  isModalOpen.value = !isModalOpen.value;
  codeInput.value = "";
  loungeName.value = "";
  loungeDescription.value = "";
  errorMessage.value = "";
};

// 라운지 가입 - 코드 작성란 v-model
const codeInput = ref("");

// 라운지 생성 - 이름, 소개 작성란 v-model
const loungeName = ref("");
const loungeDescription = ref("");

// 가입, 생성 시 요청 에러가 나면 메시지를 띄운다
const errorMessage = ref("");

// axios 요청은 에러 메시지 처리 위해 loungeStore가 아닌 해당 뷰에서 진행
const joinLounge = function () {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/lounges/join/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
    data: {
      code: codeInput.value,
    },
  })
    .then((res) => {
      accountStore.getUserInfo();
      toggleModal();
    })
    .catch((err) => {
      errorMessage.value = JSON.parse(err.request.response).message;
    });
};

const createLounge = function () {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/lounges/create/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
    data: {
      name: loungeName.value,
      description: loungeDescription.value,
    },
  })
    .then((res) => {
      accountStore.getUserInfo();
      toggleModal();
    })
    .catch((err) => {
      errorMessage.value = JSON.parse(err.request.response).message;
    });
};
</script>

<style scoped>
/* 최상위 div */
.my-page {
  padding-top: 80px;
  width: 100vw;
  min-height: 100vh;
  background-color: black;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 프로필 정보 */

.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reviewItem-img {
  font-size: 200px;
}

.profile-name-p {
  font-size: 30px;
}

#nickname {
  margin-right: 10px;
}

/* 각 슬라이드 섹션 */
h3 {
  font-size: 20px;
  font-weight: 700;
  margin: 20px;
}

.slide-container {
  margin: 50px 0;
  width: 100%;
}

/* 내가 좋아요 한 영화 목록 */

.liked-movie-img {
  height: 300px;
}

/* 각 슬라이드 */

.slide {
  display: flex;
}

/* 라운지 */

#join-lounge-button,
#create-lounge-button {
  color: #fff;
  background-color: transparent;
  border: none;
  margin-left: 10px;
  font-size: 20px;
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
