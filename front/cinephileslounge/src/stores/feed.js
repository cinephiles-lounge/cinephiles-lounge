import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "@/stores/account.js";
import { useRouter } from "vue-router";

export const useFeedStore = defineStore(
  "feed",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const accountStore = useAccountStore();
    const router = useRouter();
    const articles = ref(); // 게시글 리스트
    const article = ref(); // 게시글 아이템
    const subscribedArticles = ref(null); // 구독한사람의 글
    const popularArticles = ref(null); // 인기 게시글

    // 구독한 사람의 글 조회(지금 되는지 모르겠음 구독부터 만들어야함)
    const getSubs = () => {
      axios({
        method: "get",
        url: `${API_URL}/articles/subs/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          console.log(res.data);
          subscribedArticles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 인기 게시글 조회
    const getPopular = () => {
      axios({
        method: "get",
        url: `${API_URL}/articles/popular/`,
      })
        .then((res) => {
          popularArticles.value = res.data.slice(0, 10);
          // 인기글이 너무 많으면 안되니까 상위 10개만 저장
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 전체 게시글 조회
    const getArticles = () => {
      axios({
        method: "get",
        url: `${API_URL}/articles/`,
      })
        .then((res) => {
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 게시글 상세 조회
    const getArticle = (articleId) => {
      axios({
        method: "get",
        url: `${API_URL}/articles/${articleId}/`,
      })
        .then((res) => {
          article.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 게시글 삭제
    const deleteArticle = (articleId) => {
      axios({
        method: "delete",
        url: `${API_URL}/articles/${articleId}/update/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          router.push({ name: "FeedView" });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 게시글 생성(수정해야됨 무비아이디)
    const createArticle = (payload) => {
      axios({
        method: "post",
        url: `${API_URL}/articles/create/${payload.movieId}/`,
        data: {
          title: payload.title,
          content: payload.content,
          rank: payload.rank,
        },
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          router.push({ name: "FeedView" });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 게시글 수정
    const updateArticle = (payload) => {
      axios({
        method: "put",
        url: `${API_URL}/articles/${payload.article_pk}/update/`,
        data: {
          title: payload.title,
          content: payload.content,
          rank: payload.rank,
        },
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      }).then((res) => {
        router
          .push({
            name: "FeedDetailView",
            params: { article_pk: payload.article_pk },
          })
          .catch((err) => {
            console.log(err);
          });
      });
    };
    return {
      API_URL,
      getArticles,
      articles,
      getArticle,
      article,
      deleteArticle,
      createArticle,
      updateArticle,
      getSubs,
      subscribedArticles,
      getPopular,
      popularArticles,
    };
  },
  { persist: true }
);
