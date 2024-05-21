import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "@/stores/account.js";
import { useRouter } from "vue-router";

export const useLoungeStore = defineStore(
  "lounges",
  () => {
    return {};
  },
  { persist: true }
);
