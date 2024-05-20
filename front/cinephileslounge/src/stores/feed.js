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
    const articles = ref();
    const article = ref();
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
    };
  },
  { persist: true }
);
