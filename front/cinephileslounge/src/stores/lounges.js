import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "@/stores/account.js";
import { useRouter } from "vue-router";

export const useLoungeStore = defineStore(
  "lounges",
  () => {
    const accountStore = useAccountStore();
    const router = useRouter();

    const loungeData = ref([]); // 라운지 전체 정보
    const loungeMovies = ref([]); // 라운지 회원들이 좋아하는 영화
    const loungeReviews = ref([]); // 라운지 회원들이 작성한 영화 리뷰 게시글
    const loungeArticles = ref([]); // 라운지 전체 게시글 (영화 리뷰 X)
    const loungeArticleDetail = ref({}); // 라운지 디테일 페이지 게시글

    // 라운지 전체 정보 조회
    const getLounge = function (loungePk) {
      axios({
        method: "get",
        url: `${accountStore.API_URL}/lounges/${loungePk}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeData.value = res.data;
        })
        .then((res) => {
          getMovies(loungePk);
          getReviews(loungePk);
          getArticles(loungePk);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 회원들이 좋아요 한 영화 조회
    const getMovies = function (loungePk) {
      axios({
        method: "get",
        url: `${accountStore.API_URL}/lounges/${loungePk}/movies/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeMovies.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 회원들이 작성한 영화 리뷰 조회
    const getReviews = function (loungePk) {
      axios({
        method: "get",
        url: `${accountStore.API_URL}/lounges/${loungePk}/reviews/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeReviews.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 내의 게시글 조회
    const getArticles = function (loungePk) {
      axios({
        method: "get",
        url: `${accountStore.API_URL}/lounges/${loungePk}/articles/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeArticles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 게시글 상세 조회
    const getLoungeArticle = function (loungeArticlePk) {
      axios({
        method: "get",
        url: `${accountStore.API_URL}/lounges/articles/${loungeArticlePk}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeArticleDetail.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 게시글 생성
    const createLoungeArticle = function (payload) {
      const { title, content } = payload;
      axios({
        method: "post",
        url: `${accountStore.API_URL}/lounges/${loungeData.value.id}/articles/create/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: {
          title,
          content,
        },
      })
        .then((res) => {
          console.log(res.data.id);
          router.push({
            name: "LoungeArticleDetailView",
            params: { loungeArticlePk: res.data.id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 게시글 수정
    const updateLoungeArticle = function (payload) {
      const { title, content } = payload;
      axios({
        method: "put",
        url: `${accountStore.API_URL}/lounges/articles/${loungeArticleDetail.value.id}/update/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: {
          title,
          content,
        },
      })
        .then((res) => {
          router.push({
            name: "LoungeArticleDetailView",
            params: { loungeArticlePk: res.data.id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 게시글 삭제
    const deleteLoungeArticle = function (loungeArticlePk) {
      axios({
        method: "delete",
        url: `${accountStore.API_URL}/lounges/articles/${loungeArticlePk}/update/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          router.push({
            name: "LoungeDetailView",
            params: { loungePk: loungeData.value.id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 게시글 댓글 생성
    const createLoungeComment = function (payload) {
      const { loungeArticlePk, content } = payload;
      axios({
        method: "post",
        url: `${accountStore.API_URL}/lounges/articles/${loungeArticlePk}/comment/create/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: {
          content,
        },
      })
        .then((res) => {
          getLoungeArticle(loungeArticlePk);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 정보 삭제
    const deleteLounge = function () {
      axios({
        method: "delete",
        url: `${accountStore.API_URL}/lounges/${loungeData.value.id}/update/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeData.value = [];
          loungeMovies.value = [];
          loungeReviews.value = [];
          loungeArticles.value = [];
          accountStore.getUserInfo();
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 라운지 탈퇴
    const leaveLounge = function () {
      axios({
        method: "post",
        url: `${accountStore.API_URL}/lounges/${loungeData.value.id}/leave/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          loungeData.value = [];
          loungeMovies.value = [];
          loungeReviews.value = [];
          loungeArticles.value = [];
          accountStore.getUserInfo();
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return {
      loungeData,
      loungeMovies,
      loungeReviews,
      loungeArticles,
      loungeArticleDetail,
      getLounge,
      getMovies,
      getReviews,
      getArticles,
      getLoungeArticle,
      createLoungeArticle,
      updateLoungeArticle,
      deleteLoungeArticle,
      createLoungeComment,
      deleteLounge,
      leaveLounge,
    };
  },
  { persist: true }
);
