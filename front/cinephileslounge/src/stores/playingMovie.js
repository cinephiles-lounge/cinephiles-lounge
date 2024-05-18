import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
export const usePlayingMovieStore = defineStore(
  "playingMovie",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const playingMovies = ref(null);
    const getPlayingMovies = () => {
      axios({
        method: "get",
        url: `${API_URL}/movies/playing`,
      })
        .then((res) => {
          playingMovies.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return { API_URL, getPlayingMovies, playingMovies };
  },
  { persist: true }
);
