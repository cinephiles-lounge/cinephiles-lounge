import { createRouter, createWebHistory } from "vue-router";
import { useAccountStore } from "@/stores/account";
import HomeView from "@/views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import RegistrationView from "@/views/RegistrationView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import FeedView from "@/views/FeedView.vue";
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
      path: "/movies/:movie_id",
      name: "MovieDetailView",
      component: MovieDetailView,
    },
    {
      path: "/articles",
      name: "FeedView",
      component: FeedView,
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
