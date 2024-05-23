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
          리뷰
          <div class="icon-box">
            <i @click="copyToClipboard" class="bx bx-copy"></i>
            <i @click="settingState = !settingState" class="bx bx-cog"></i>
          </div>
        </h1>
      </header>
      <ul class="article-card-wrapper">
        <LoungeArticleCard
          v-for="article in loungeStore.loungeReviews"
          :key="article.id"
          :article="article"
        />
      </ul>
    </section>

    <main class="member-articles-container">
      <h1>라운지 전체 게시글</h1>
      <div class="lounge-article">
        <div class="lounge-article-header">
          <button
            class="article-create-btn"
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
            class="lounge-article-item"
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
            <div class="article-content">
              {{ article.title }}
              <div class="author">
                <i class="bx bxl-github"></i>
                {{ article.user.nickname }}<span> | </span>
                {{ formatTimeDifference(article.created_at) }}
              </div>
            </div>
          </li>
        </ul>
        <p v-else>아직 작성한 게시글이 없습니다.</p>
      </div>
    </main>

    <aside v-if="settingState" class="member-info-container">
      <div @click="settingState = !settingState" class="x-btn">X</div>
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
            <button class="create-btn" type="submit">수정</button>
            <button class="cancel-btn" @click.prevent="toggleModal">
              닫기
            </button>
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

// 클립보드 기능
const copyToClipboard = () => {
  navigator.clipboard
    .writeText(loungeStore.loungeData.uuid)
    .then(() => {
      alert("주소가 클립보드에 복사되었습니다.");
    })
    .catch((err) => {
      console.error("클립보드 복사 실패:", err);
    });
};

// 회원관리 모달 변수
const settingState = ref(false);

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

// 시간 포멧팅 함수
const formatTimeDifference = (dateString) => {
  const now = new Date(); //현재시간
  const date = new Date(dateString); //게시글 작성시간
  const diff = (now - date) / 1000; // 초 단위 차이

  if (diff < 60) {
    return `${Math.floor(diff)}초 전`;
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}분 전`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}시간 전`;
  } else {
    return `${Math.floor(diff / 86400)}일 전`;
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
  padding-bottom: 100px;
}

/* 회원들이 가장 최근에 작성한 리뷰 */
.current-review-container {
  margin: 30px 65px;
}
.current-review-container .article-card-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}
.member-articles-container h1,
.current-review-container header h1 {
  font-size: 20px;
  line-height: 26px;
  font-weight: 700;
  margin-bottom: 5px;
  position: relative;
}
/* 라운지 전체 게시글 */
.member-articles-container {
  margin: 30px 65px;
  max-width: 1440px;
}
.member-articles-container .lounge-article-item {
  border-bottom: 1px solid #e5e5e5;
  height: 30px;
}
.article-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 11px;
  margin-left: 5px;
}
.lounge-article {
  background-color: rgb(212, 210, 210);
  color: black;
  border-radius: 10px;
  padding: 20px;
}

.lounge-article-header {
  display: flex;
  justify-content: space-between;
}
.lounge-article-header .article-create-btn {
  background-color: #f82e62;
  color: #eee;
  outline: none;
  border: none;
  padding: 5px;
  border-radius: 5px;
  width: 40px;
  cursor: pointer;
  transition: 0.3s;
  margin-left: 5px;
}
/* copy, setting 버튼 */
.icon-box {
  position: absolute;
  justify-content: flex-end;
  font-size: 25px;
  top: 0px;
  right: 140px;
}
.icon-box i {
  cursor: pointer;
  transition: 0.3s;
}
.icon-box i:hover {
  transform: scale(1.1);
}

.bx-cog {
  margin-left: 10px;
}
/* 회원관리 */
.member-info-container {
  width: 200px;
  top: 200px;
  right: 50px;
  position: fixed;
  background-color: white;
  color: black;
  border-radius: 10px;
  padding: 20px;
  margin: 10px;
}
.member-info-container .x-btn {
  position: absolute;
  top: 15px;
  right: 18px;
  transition: 0.3s;
  cursor: pointer;
}
.menber-info-container .x-btn:hover {
  transform: scale(1.1);
}
.member-info-container .profile-container {
  display: flex;
  margin-top: 3px;
}
.admin {
  margin-bottom: 10px;
}
.setting {
  margin-top: 10px;
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
  color: #eee;
  position: relative;
  height: 300px;
  width: 300px;
  background: #262626;
  border-radius: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.modal-container textarea {
  height: 150px;
  width: 250px;
  padding-left: 5px;
}
.modal-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 3px;
}
textarea:focus,
input:focus {
  outline: none;
  box-shadow: none;
}
#name {
  margin: 5px 0px;
  width: 250px;
  padding-left: 5px;
}
#description {
  margin: 5px 0px;
}
.modal-btn {
  display: flex;
  justify-content: center;
}

.modal-btn > button {
  margin: 5px;
}
.modal-btn .create-btn {
  background-color: #f82e62;
  color: #eee;
  outline: none;
  border: none;
  padding: 5px;
  border-radius: 5px;
  width: 50px;
  cursor: pointer;
  transition: 0.3s;
  margin-left: 5px;
}
.modal-btn .cancel-btn {
  background-color: #a49fa1;
  color: #eee;
  outline: none;
  border: none;
  padding: 5px;
  border-radius: 5px;
  width: 50px;
  cursor: pointer;
  transition: 0.3s;
  margin-left: 5px;
}
.modal-btn .create-btn:hover,
.modal-btn .cancel-btn:hover {
  transform: scale(1.1);
}
</style>
