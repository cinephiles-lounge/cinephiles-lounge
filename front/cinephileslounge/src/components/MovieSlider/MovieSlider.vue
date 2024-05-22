<template>
  <div class="movie-slider">
    <h1>{{ title }}</h1>
    <button @click="prevSlide" class="prev-btn">
      <i class="bx bxs-chevron-left"></i>
    </button>
    <div class="slider-wrapper">
      <div class="slider-track" :style="sliderStyle">
        <ul class="card-movie-container">
          <MovieSliderCard
            v-for="movie in movies"
            :key="movie.id"
            :movie="movie"
          />
        </ul>
      </div>
    </div>
    <button @click="nextSlide" class="next-btn">
      <i class="bx bxs-chevron-right"></i>
    </button>
  </div>
</template>

<script setup>
import MovieSliderCard from "@/components/MovieSlider/MovieSliderCard.vue";
import { ref, computed } from "vue";
const props = defineProps({
  movies: Array,
  title: String,
});
const currentSlide = ref(0); // 구독글 슬라이더
const slidesToShow = 5;
const cardWidth = 202; // 카드의 너비 + 양쪽마진 합

const sliderStyle = computed(() => {
  return {
    transform: `translate3d(-${currentSlide.value * cardWidth}px, 0, 0)`,
    transition: "transform 0.5s ease",
  };
});

const nextSlide = () => {
  if (currentSlide.value < props.movies.length - slidesToShow) {
    currentSlide.value++;
  }
};

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  }
};
</script>

<style scoped>
.movie-slider {
  position: relative;
  overflow: hidden;
  padding: 32px 60px;
}

.movie-slider h1 {
  font-size: 20px;
  font-weight: 700;
  line-height: 26px;
  margin-bottom: 5px;
}

.slider-wrapper {
  overflow: hidden;
}

.slider-track {
  display: flex;
  transition: transform 0.5s ease;
}

.card-movie-container {
  display: flex;
}

.prev-btn,
.next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  border: none;
  color: #bababa;
  cursor: pointer;
  outline: none;
  background: none;
  font-size: 25px;
}

.prev-btn {
  left: 25px;
}

.next-btn {
  right: 25px;
}
</style>
