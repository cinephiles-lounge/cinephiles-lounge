<template>
  <div>
    <p>{{ loungeStore }}</p>
  </div>
</template>

<script setup>
import { useLoungeStore } from "@/stores/lounges";
import { useRoute } from "vue-router";
const loungeStore = useLoungeStore();
const route = useRoute();
const loungePk = route.params.loungePk;
</script>

<style lang="scss" scoped></style>
