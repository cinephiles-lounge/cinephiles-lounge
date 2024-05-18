import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useMovieStore = defineStore(
  "movie",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    return { API_URL };
  },
  { persist: true }
);
