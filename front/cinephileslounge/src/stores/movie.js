import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useAccountStore } from "./account";
import axios from "axios";
export const useMovieStore = defineStore(
  "movie",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const accountStore = useAccountStore();
    // 좋아요 기반 콘텐츠 추천
    const likeMovies = ref();
    const getLikeMovies = () => {
      axios({
        method: "get",
        url: `${API_URL}/movies/recommend/like/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          likeMovies.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };
    // 구독한 사람이 좋아요 누른 영화 조회
    const subsMovies = ref();
    const getSubsMovies = () => {
      axios({
        method: "get",
        url: `${API_URL}/movies/subs/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          subsMovies.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 인기 상영작 1~5위 조회
    const popularMovie = ref();
    const getPopularMovie = () => {
      axios({
        method: "get",
        url: `${API_URL}/movies/popular/`,
      })
        .then((res) => {
          popularMovie.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 영화 디테일 조회
    const movie = ref();
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
    return {
      API_URL,
      movie,
      getMovieDetail,
      getPopularMovie,
      popularMovie,
      getLikeMovies,
      likeMovies,
      getSubsMovies,
      subsMovies,
    };
  },
  { persist: true }
);
