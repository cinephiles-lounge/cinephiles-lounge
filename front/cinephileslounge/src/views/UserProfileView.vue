<template>
  <div class="my-page">
    <div class="profile-container">
      <div class="reviewItem-img">
        <i class="bx bxl-github"></i>
      </div>
      <template v-if="isMyProfile">
        <span id="nickname">{{ accountStore.userNickname }}</span>
      </template>
      <template v-else>
        <span id="nickname">{{ currentUser.nickname }}</span>
        <button @click="subscribe">
          <i v-if="!isSubs" class="bx bx-bell"></i>
          <i v-if="isSubs" class="bx bxs-bell"></i>
          {{ isSubs ? "구독취소" : "구독" }}
        </button>
      </template>
    </div>

    <div class="slide-container">
      <h3 v-if="isMyProfile">내가 좋아요 누른 영화</h3>
      <h3 v-else>{{ currentUser.nickname }}님이 좋아요 누른 영화</h3>
      <ul v-if="currentUser.liked_movies" class="slide">
        <li v-for="movie in currentUser.liked_movies" :key="movie.movie_id">
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
      <h3 v-if="isMyProfile">내가 작성한 글</h3>
      <h3 v-else>{{ currentUser.nickname }}님이 작성한 글</h3>
      <ul v-if="currentUser.posted_articles.length" class="slide">
        <FeedCard
          v-for="article in currentUser.posted_articles"
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

    <div class="slide-container" v-if="isMyProfile">
      <h3>
        내 라운지
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
        <LoungeCard
          v-for="lounge in accountStore.joinedLounges"
          :key="lounge.id"
          :lounge="lounge"
          @click="navigateToLoungeDetailView(lounge.id)"
        />
      </ul>
      <p v-else>아직 가입한 라운지가 없습니다.</p>
    </div>

    <template v-if="isMyProfile">
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
    </template>
  </div>
</template>

<script setup>
import { RouterLink, useRoute, onBeforeRouteUpdate } from "vue-router";
import { computed, ref, watch } from "vue";
import { useAccountStore } from "@/stores/account";
import { useLoungeStore } from "@/stores/lounges";
import { useFeedStore } from "@/stores/feed";
import { useRouter } from "vue-router";
import FeedCard from "@/components/Feed/FeedCard.vue";
import LoungeCard from "@/components/Lounge/LoungeCard.vue";
import axios from "axios";
import MovieSlider from "@/components/MovieSlider/MovieSlider.vue";
const route = useRoute();
const router = useRouter();

const accountStore = useAccountStore();

const userId = route.params.userId;
const currentUser = ref({}); // 해당 페이지에서 렌더링할 유저

// 내 정보 초기화
accountStore.getUserInfo();

// 내 프로필로 들어왔는지 다른 유저의 프로필로 들어왔는지 여부를 반환
const isMyProfile = computed(() => {
  return route.params.userId == accountStore.userPk;
});

// currentUser를 불러오는 해주는 함수
const getCurrentUser = function (userId) {
  axios({
    method: "get",
    url: `${accountStore.API_URL}/accounts/${userId}/`,
  })
    .then((res) => {
      currentUser.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

// 해당 프로필에서 렌더링할 currentUser에 데이터 넣어주기
getCurrentUser(userId);

// 현재 유저 페이지에서 다른 유저 페이지로 가면서 컴포넌트 재사용 되더라도 라우트 업데이트 감지하여 currentUser 업데이트
onBeforeRouteUpdate((to, from) => {
  getCurrentUser(to.params.userId);
});

// 구독 확인
const isSubs = ref(false);

if (accountStore.subscriptions.length > 0) {
  for (const user of accountStore.subscriptions) {
    if (user.id == userId) {
      isSubs.value = true;
      break;
    }
  }
}

// 구독 & 구독취소(toggle)
const subscribe = () => {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/accounts/subscribe/${userId}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      isSubs.value = !isSubs.value;
      accountStore.getUserInfo();
    })
    .catch((err) => {
      console.log(err);
    });
};

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

// 라운지 카드 클릭하면 라운지 디테일 뷰로 route
const navigateToLoungeDetailView = (loungePk) => {
  router.push({ name: "LoungeDetailView", params: { loungePk: loungePk } });
};
</script>

<style scoped>
/* 최상위 div */
.my-page {
  padding: 100px 150px;
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

#nickname {
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
  overflow: hidden;
}
.slide-container h3 {
  margin-bottom: 30px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
/* 내가 좋아요 한 영화 목록 */

.liked-movie-img {
  height: 300px;
  transition: 0.3s;
  cursor: pointer;
  margin: 0 20px;
}

.liked-movie-img:hover {
  transform: scale(1.1);
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
  font-size: 20px;
  padding: 0;
  width: 22px;
  margin-left: 5px;
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

button {
  width: 200px;
  height: 37px;
  background-color: transparent;
  border: none;
  color: #eee;
  font-size: 18px;
  cursor: pointer;
  transition: 0.3s;
  color: #babac1;
}
</style>
