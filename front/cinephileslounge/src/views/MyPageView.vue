<template>
  <div class="my-page">

    <div class="profile-container">
      <div class="reviewItem-img">
        <i class="bx bxl-github"></i>
      </div>
      <p class="profile-name-p">
        <span id="nickname">{{ accountStore.userNickname }}</span>
        <i class="bx bxs-edit-alt"></i>
      </p>
    </div>

    <div class="slide-container">
      <h3>내가 좋아요 누른 영화</h3>
      <ul v-if="accountStore.likedMovies" class="slide">
        <li v-for="movie in accountStore.likedMovies" :key="movie.movie_id">
          <img class="liked-movie-img"
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
      <p v-else>
        아직 좋아요를 누른 영화가 없습니다.
      </p>
    </div>

    <div class="slide-container">
      <h3>내가 작성한 글</h3>
      <ul v-if="accountStore.postedArticles" class="slide">
        <li v-for="article in accountStore.postedArticles" :key="article.id">
          <RouterLink
            :to="{ name: 'FeedDetailView', params: { article_pk: article.id } }"
            >{{ article.title }}
          </RouterLink>
        </li>
      </ul>
      <p v-else>
        아직 작성한 게시글이 없습니다.
      </p>
    </div>

    <div class="slide-container">
      <h3>내가 가입한 라운지 
        <button id="join-lounge-button" @click="openModal"><i class='bx bx-network-chart'></i></button>
        <button id="join-lounge-button" @click=""><i class='bx bx-add-to-queue'></i></button>
      </h3>
      <ul v-if="accountStore.joinedLounges" class="slide">
        <li v-for="lounge in accountStore.joinedLounges" :key="lounge.id">
          {{ lounge.name }}
        </li>
      </ul>
      <p v-else>
        아직 가입한 라운지가 없습니다.
      </p>
    </div>

    <div class="modal-wrap" v-show="isModalOpen" @click="openModal">
      <div class="modal-container" @click.stop="">
        <form @submit.prevent="joinLounge">
          <label for="code">가입 코드를 입력하세요.</label>
          <input type="text" id="code" v-model="codeInput">
          <div class="modal-btn">
            <button type="submit">확인</button>
            <button @click.prevent="openModal">닫기</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
// 영화 최상위 ul, 영화하나하나는 li
import { ref } from 'vue';
import { useAccountStore } from "@/stores/account";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const accountStore = useAccountStore();

accountStore.getUserInfo();

const isModalOpen = ref(false);

const openModal = function () {
  isModalOpen.value = !isModalOpen.value
};

const codeInput = ref('')

const joinLounge = function () {
  axios({
    method: "post",
    url: `${accountStore.API_URL}/lounges/join/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
    data: {
      code: codeInput.value
    }
  })
    .then((res) => {
      console.log(res.data)
    })
    .catch((err) => {
      console.log(err);
    });
}
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
  margin: 50px 0 ;
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

#join-lounge-button {
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
}

/* modal or popup */
.modal-container {
  color: black;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 200px;
  width: 300px;
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
}
</style>