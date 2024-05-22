import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "@/stores/account.js";
import { useRouter } from "vue-router";

export const useLoungeStore = defineStore(
  "lounges",
  () => {
    const accountStore = useAccountStore();

    const loungeData = ref([]);
    const loungeMovies = ref([])
    const loungeReviews = ref([])
    const loungeArticles = ref([])

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
          getMovies(loungePk)
          getReviews(loungePk)
          getArticles(loungePk)
        })
        .catch((err) => {
          console.log(err);
        });
    };

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
    }

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
    }

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
    }

    return { 
      loungeData,
      loungeMovies,
      loungeReviews,
      loungeArticles,
      getLounge, 
      getMovies, 
      getReviews, 
      getArticles, 
    };
  },
  { persist: true }
);
