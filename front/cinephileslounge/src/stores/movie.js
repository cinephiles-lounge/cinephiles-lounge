import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
export const useMovieStore = defineStore(
  "movie",
  () => {
    const API_URL = "http://127.0.0.1:8000";

    // 영화 디테일 조회
    const movie = ref(null);
    const getMovieDetail = (movieId) => {
      axios({
        method: "get",
        url: `${API_URL}/movies/${movieId}/`,
      })
        .then((res) => {
          movie.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };
    return { API_URL, movie, getMovieDetail };
  },
  { persist: true }
);
