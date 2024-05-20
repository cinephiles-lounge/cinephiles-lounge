import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";
export const useAccountStore = defineStore(
  "account",
  () => {
    const router = useRouter();
    const token = ref(null);
    const API_URL = "http://127.0.0.1:8000";
    const userPk = ref(null); // 로그인 한 유저 pk
    const userId = ref(null); // 로그인 한 유저 아이디
    const userNickname = ref(null); // 로그인 한 유저 닉네임
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });

    // 회원가입
    const signUp = (payload) => {
      const { username, password1, password2 } = payload;

      axios({
        method: "post",
        url: `${API_URL}/auth/registration/`,
        data: {
          username: payload.username,
          password1: payload.password1,
          password2: payload.password2,
        },
      })
        .then((res) => {
          console.log("회원가입 성공");
          const password = password1;
          logIn({ username, password });
        })
        .catch((err) => {
          console.log("회원가입 실패");
          console.log(err);
        });
    };

    // 로그인
    const logIn = (payload) => {
      const username = payload.username;
      const password = payload.password;

      axios({
        method: "post",
        url: `${API_URL}/auth/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key;
          router.push({ name: "HomeView" });
          axios({
            method: "get",
            url: `${API_URL}/auth/user/`,
            headers: {
              Authorization: `Token ${res.data.key}`,
            },
          })
            .then((res) => {
              userPk.value = res.data.pk; // 로그인 한 유저 pk 저장
              userId.value = res.data.username; // 로그인 한 유저 아이디 저장
              userNickname.value = res.data.nickname; // 로그인 한 유저 닉네임 저장
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log("로그인 실패");
          console.log(err.response.status);
          if (err.response.status === 400) {
            window.alert("아이디 또는 비밀번호가 잘못되었습니다.");
            router.go(0);
          }
        });
    };

    return {
      signUp,
      logIn,
      API_URL,
      token,
      isLogin,
      userPk,
      userId,
      userNickname,
    };
  },
  { persist: true }
);
