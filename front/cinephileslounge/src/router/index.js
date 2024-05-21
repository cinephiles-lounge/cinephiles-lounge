import { createRouter, createWebHistory } from "vue-router";
import { useAccountStore } from "@/stores/account";
import HomeView from "@/views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import RegistrationView from "@/views/RegistrationView.vue";
import UserUpdateView from "@/views/UserUpdateView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import FeedView from "@/views/FeedView.vue";
import FeedDetailView from "@/views/FeedDetailView.vue";
import FeedCreateView from "@/views/FeedCreateView.vue";
import MyPageView from "@/views/MyPageView.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/registration",
      name: "RegistrationView",
      component: RegistrationView,
    },
    {
      path: "/user/update",
      name: "UserUpdateView",
      component: UserUpdateView,
    },
    {
      path: "/movies/:movie_id",
      name: "MovieDetailView",
      component: MovieDetailView,
    },
    {
      path: "/articles",
      name: "FeedView",
      component: FeedView,
    },
    {
      path: "/articles/:article_pk",
      name: "FeedDetailView",
      component: FeedDetailView,
    },
    {
      path: "/articles/create",
      name: "FeedCreateView",
      component: FeedCreateView,
    },
    {
      path: "/articles/edit/:article_pk",
      name: "FeedEditView",
      component: FeedCreateView,
    },
    {
      path: "/mypage",
      name: "MyPageView",
      component: MyPageView,
    },
  ],
});
router.beforeEach((to, from) => {
  const accountStore = useAccountStore();
  if (
    (to.name === "LogInView" || to.name == "RegistrationView") &&
    accountStore.isLogin
  ) {
    window.alert("이미 로그인이 되어있습니다.");
    return { name: "HomeView" };
  }
});

export default router;
