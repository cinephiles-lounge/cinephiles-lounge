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

    const getLounge = function (loungePk) {
      axios({
        method: "get",
        url: `${API_URL}/lounges/{loungePk}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          subscribedArticles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return { getLounge };
  },
  { persist: true }
);
