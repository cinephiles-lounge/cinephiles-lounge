import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
export const useMovieStore = defineStore(
  "movie",
  () => {
    const API_URL = "http://127.0.0.1:8000";

    // 전체 영화 조회
    const movieList = ref();
    const getMovieList = () => {
      axios({
        method: "get",
        url: `${API_URL}/movies/list/`,
      })
        .then((res) => {
          movieList.value = res.data;
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
      getMovieList,
      movieList,
    };
  },
  { persist: true }
);
