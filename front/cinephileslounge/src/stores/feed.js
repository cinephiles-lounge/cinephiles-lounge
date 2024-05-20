import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
export const useFeedStore = defineStore(
  "feed",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const articles = ref();
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

    return { API_URL, getArticles, articles };
  },
  { persist: true }
);
