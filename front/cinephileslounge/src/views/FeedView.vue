<template>
  <div class="feed">
    <div class="card">
      <h1>구독한 사람의 글</h1>
      <button
        v-if="
          feedStore.subscribedArticles &&
          feedStore.subscribedArticles.length >= 1
        "
        class="prev-button"
        @click="prevSlide('subscribed')"
      >
        <
      </button>
      <div
        v-if="
          feedStore.subscribedArticles &&
          feedStore.subscribedArticles.length >= 1
        "
        class="slider-wrapper"
      >
        <div class="slider-container">
          <div class="slider-track" :style="subscribedSliderStyle">
            <ul class="card-movie-container">
              <FeedCard
                @click="navigateToArticleDetail(subscribedArticle.id)"
                v-for="subscribedArticle in feedStore.subscribedArticles"
                :key="subscribedArticle.id"
                :article="subscribedArticle"
              />
            </ul>
          </div>
        </div>
      </div>
      <button
        v-if="feedStore.subscribedArticles.length >= 1"
        class="next-button"
        @click="nextSlide('subscribed')"
      >
        >
      </button>
      <div v-if="feedStore.subscribedArticles.length == 0">
        <h1>아직 구독한 사람이 없습니다.</h1>
      </div>
    </div>
    <hr />
    <div class="card">
      <h1>인기글</h1>
      <button class="prev-button" @click="prevSlide('popular')"><</button>
      <div class="slider-wrapper">
        <div class="slider-container">
          <div class="slider-track" :style="popularSliderStyle">
            <ul class="card-movie-container">
              <FeedCard
                @click="navigateToArticleDetail(popularArticle.id)"
                v-for="popularArticle in feedStore.popularArticles"
                :key="popularArticle.id"
                :article="popularArticle"
              />
            </ul>
          </div>
        </div>
      </div>
      <button class="next-button" @click="nextSlide('popular')">></button>
    </div>
    <hr />
    <div class="card">
      <div class="article-title">
        <h1>게시글 전체조회</h1>
      </div>
      <ul class="article-movie-container">
        <FeedCard
          @click="navigateToArticleDetail(article.id)"
          v-for="article in feedStore.articles"
          :key="article.id"
          :article="article"
        />
      </ul>
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
const navigateToArticleDetail = (id) => {
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

// 시간 포멧팅 함수
const formatTimeDifference = (dateString) => {
  const now = new Date(); //현재시간
  const date = new Date(dateString); //게시글 작성시간
  const diff = (now - date) / 1000; // 초 단위 차이

  if (diff < 60) {
    return `${Math.floor(diff)}초 전`;
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}분 전`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}시간 전`;
  } else {
    return `${Math.floor(diff / 86400)}일 전`;
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Song+Myung&display=swap");
.song-myung-regular {
  font-family: "Song Myung", serif;
  font-weight: 400;
  font-style: normal;
}
.feed {
  padding-top: 100px;
  color: #fff;
  background-color: black;
  padding-left: 150px;
  padding-right: 150px;
  padding-bottom: 100px;
}
.feed .card {
  margin-bottom: 32px;
  position: relative;
}
.feed .card h1 {
  font-size: 20px;
  font-weight: 700;
  line-height: 26px;
  margin-bottom: 5px;
}
.slider-wrapper {
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
.article-movie-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  margin-top: 15px;
}
.article-movie-container > li {
  margin-bottom: 32px;
}
.article-title {
  display: flex;
  justify-content: space-between;
}

.next-button,
.prev-button {
  position: absolute;
  z-index: 9;
  top: 45%;
  font-size: 15px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  color: #48484b;
  transition: 0.5s;
}
.next-button:hover,
.prev-button:hover {
  transform: scale(1.2);
}
.next-button {
  right: -15px;
}
.prev-button {
  left: -10px;
}
</style>
