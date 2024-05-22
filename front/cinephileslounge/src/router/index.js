import { createRouter, createWebHistory } from "vue-router";
import { useAccountStore } from "@/stores/account";
import HomeView from "@/views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import RegistrationView from "@/views/RegistrationView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import FeedView from "@/views/FeedView.vue";
import FeedDetailView from "@/views/FeedDetailView.vue";
import FeedCreateView from "@/views/FeedCreateView.vue";
import MyPageView from "@/views/MyPageView.vue";
import LoungeView from "@/views/LoungeView.vue";
import LoungeDetailView from "@/views/LoungeDetailView.vue";
import LoungeArticleCreateView from "@/views/LoungeArticleCreateView.vue";
import LoungeArticleDetailView from "@/views/LoungeArticleDetailView.vue";

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
    {
      path: "/lounge",
      name: "LoungeView",
      component: LoungeView,
      beforeEnter: (to, from) => {
        const accountStore = useAccountStore();
        if (!accountStore.isLogin) {
          alert("로그인이 필요한 서비스입니다.");
          return { name: "LogInView" };
        }
      },
    },
    {
      path: "/lounge/:loungePk",
      name: "LoungeDetailView",
      component: LoungeDetailView,
      // beforeEnter: (to, from) => {
      //   // 자신의 그룹만 들어갈 수 있도록
      //   // const accountStore = useAccountStore();
      //   // if (!accountStore.isLogin) {
      //   //   alert("로그인이 필요한 서비스입니다.");
      //   //   return { name: "LogInView" };
      //   }
      // },
    },
    {
      path: "/lounge/:loungePk/article/create",
      name: "LoungeArticleCreateView",
      component: LoungeArticleCreateView,
    },
    {
      path: "/lounge/:loungePk/article/:loungeArticlePk",
      name: "LoungeArticleDetailView",
      component: LoungeArticleDetailView,
    },
    {
      path: "/lounge/:loungePk/article/update/:loungeArticlePk",
      name: "LoungeArticleUpdateView",
      component: LoungeArticleCreateView,
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
