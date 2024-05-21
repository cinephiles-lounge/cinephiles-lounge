import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "@/stores/account.js";
import { useRouter } from "vue-router";

export const useLoungeStore = defineStore(
  "lounges",
  () => {
    const accountStore = useAccountStore();

    const joinLounge = function (codeInput) {
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
          console.log("라운지 가입 완료");
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const createLounge = function (payload) {
      const { loungeName, loungeDescription } = payload;

      axios({
        method: "post",
        url: `${accountStore.API_URL}/lounges/create/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: {
          name: loungeName,
          description: loungeDescription,
        },
      })
        .then((res) => {
          console.log("라운지 생성 완료");
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return {
      joinLounge,
      createLounge,
    };
  },
  { persist: true }
);
