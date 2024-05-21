<template>
  <div class="feed">
    <div class="card">
      <h1>구독한 사람의 글</h1>
      <div
        v-if="feedStore.subscribedArticles.length >= 1"
        class="slider-wrapper"
      >
        <button class="prev-button" @click="prevSlide('subscribed')">
          Prev
        </button>
        <div class="slider-container">
          <div class="slider-track" :style="subscribedSliderStyle">
            <ul class="card-movie-container">
              <FeedCard
                @click="navigateToFeedDetailView(subscribedArticle.id)"
                v-for="subscribedArticle in feedStore.subscribedArticles"
                :key="subscribedArticle.id"
                :article="subscribedArticle"
              />
            </ul>
          </div>
        </div>
        <button class="next-button" @click="nextSlide('subscribed')">
          Next
        </button>
      </div>
      <div v-if="feedStore.subscribedArticles.length == 0">
        <h1>아직 구독한 사람이 없습니다.</h1>
      </div>
    </div>
    <hr />
    <div class="card">
      <h1>인기글</h1>
      <div class="slider-wrapper">
        <button class="prev-button" @click="prevSlide('popular')">Prev</button>
        <div class="slider-container">
          <div class="slider-track" :style="popularSliderStyle">
            <ul class="card-movie-container">
              <FeedCard
                @click="navigateToPopularArticleDetail(popularArticle.id)"
                v-for="popularArticle in feedStore.popularArticles"
                :key="popularArticle.id"
                :article="popularArticle"
              />
            </ul>
          </div>
        </div>
        <button class="next-button" @click="nextSlide('popular')">Next</button>
      </div>
    </div>
    <hr />
    <div class="board-container">
      <h1>게시글 전체조회</h1>
      <div v-for="article in feedStore.articles" :key="article.id">
        <RouterLink
          :to="{ name: 'FeedDetailView', params: { article_pk: article.id } }"
        >
          {{ article.title }}
        </RouterLink>
      </div>
      <button>
        <RouterLink :to="{ name: 'FeedCreateView' }">글 생성</RouterLink>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useFeedStore } from "@/stores/feed.js";
import { ref, onMounted, computed } from "vue";
import { RouterLink } from "vue-router";
import { useRouter } from "vue-router";
import FeedCard from "@/components/Feed/FeedCard.vue";

const feedStore = useFeedStore();
const router = useRouter();

feedStore.getArticles(); // 전체 게시글 조회
feedStore.getSubs(); // 구독한 사람의 게시글 조회
feedStore.getPopular(); // 인기 게시글 조회

// 게시글 클릭 -> 디테일 페이지로 이동
const navigateToPopularArticleDetail = (id) => {
  router.push({ name: "FeedDetailView", params: { article_pk: id } });
};

const navigateToFeedDetailView = (id) => {
  router.push({ name: "FeedDetailView", params: { article_pk: id } });
};

const currentSlideSubscribed = ref(0); // 구독글 슬라이더
const currentSlidePopular = ref(0); // 인기글 슬라이더
const slidesToShow = 5; // 한번에 보여질 카드 수
const cardWidth = 344; // 카드의 너비 + 마진%2

const subscribedSliderStyle = computed(() => {
  return {
    transform: `translate3d(-${
      currentSlideSubscribed.value * cardWidth
    }px, 0, 0)`,
    transition: "transform 0.5s ease",
  };
});

const popularSliderStyle = computed(() => {
  return {
    transform: `translate3d(-${currentSlidePopular.value * cardWidth}px, 0, 0)`,
    transition: "transform 0.5s ease",
  };
});

const nextSlide = (type) => {
  if (type === "subscribed") {
    if (
      currentSlideSubscribed.value <
      feedStore.subscribedArticles.length - slidesToShow
    ) {
      currentSlideSubscribed.value++;
    }
  } else if (type === "popular") {
    if (
      currentSlidePopular.value <
      feedStore.popularArticles.length - slidesToShow
    ) {
      currentSlidePopular.value++;
    }
  }
};

const prevSlide = (type) => {
  if (type === "subscribed") {
    if (currentSlideSubscribed.value > 0) {
      currentSlideSubscribed.value--;
    }
  } else if (type === "popular") {
    if (currentSlidePopular.value > 0) {
      currentSlidePopular.value--;
    }
  }
};
</script>

<style scoped>
.feed {
  padding-top: 100px;
  color: #fff;
  background-color: black;
  padding-left: 150px;
  padding-right: 150px;
}
.feed .card {
  margin-bottom: 32px;
}
.feed .card h1 {
  font-size: 20px;
  font-weight: 700;
  line-height: 26px;
  margin-bottom: 5px;
}
.slider-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
}
.slider-container {
  display: flex;
  overflow: hidden;
}
.slider-track {
  display: flex;
  transition: transform 0.5s ease;
}

.card-movie-container {
  display: flex;
}
hr {
  height: 1px;
  background-color: #48484b;
  border: none;
  margin: 32px 0px;
}
</style>
