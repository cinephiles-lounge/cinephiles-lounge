<template>
  <li class="container">
    <img src="@/assets/lounge.png" alt="" />
    <p>{{ lounge.name }}</p>
  </li>
</template>

<script setup>
defineProps({
  lounge: Object,
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Song+Myung&display=swap");
img {
  width: 300px;
}

.container {
  list-style-type: none;
  width: 330px;
  height: 280px;
  background-color: #fff;
  color: black;
  border-radius: 10px;
  transition: 0.5s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.container:hover {
  z-index: 1;
  transform: scale(1.15);
  filter: brightness(70%);
}
</style>
