import { ref, computed } from "vue";
import { defineStore } from "pinia";
import {useRouter} from 'vue-router'
import axios from "axios";
export const useAccountStore = defineStore(
  "account",
  () => {
    const router = useRouter()
    const token = ref(null)
    const API_URL = 'http://127.0.0.1:8000'
    const isLogin = computed(()=>{
      if (token.value === null){
        return false
      } else{
        return true
      }
    })

    // 회원가입
    const signUp = (payload)=>{
      const {username, password1, password2} = payload

      axios({
        method:'post',
        url:`${API_URL}/auth/registration/`,
        data:{
        username:payload.username,
        password1:payload.password1,
        password2 : payload.password2,
        }
      })
      .then((res)=>{
        console.log('회원가입 성공')
        const password = password1
        logIn({username, password})
      })
      .catch((err)=>{console.log('회원가입 실패')})
    }

    // 로그인
    const logIn = (payload)=>{
      const username = payload.username
      const password = payload.password
      
      axios({
        method:'post',
        url:`${API_URL}/auth/login/`,
        data:{
          username, password
        }
      }).then((res)=>{
        console.log('로그인 성공')
        token.value = res.data.key
        router.push({name:'HomeView'})
      })
      .catch((err)=>{
        console.log('로그인 실패')
        console.log(err)
      })
    }

    return {signUp, logIn, token, isLogin};
  },
  { persist: true }
);
