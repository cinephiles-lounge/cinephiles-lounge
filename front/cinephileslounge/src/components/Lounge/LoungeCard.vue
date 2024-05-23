<template>
  <li class="container">
    <i class="bx bx-ghost"></i>
    <p>{{ lounge.name }}</p>
  </li>
</template>

<script setup>
defineProps({
  lounge: Object,
});
</script>

<style scoped>
img {
  width: 300px;
}

.container {
  list-style-type: none;
  width: 230px;
  height: 180px;
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
i {
  font-size: 60px;
}
</style>
