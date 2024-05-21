<template>
  <!-- 라운지 없으면 만들라고 권장하는 문구 있어야 함 -->
  <div class="lounge-page">
    <div class="lounge-container">
      <h1>내가 관리하는 라운지</h1>
      <div class="card-container">
        <LoungeCard
          v-for="lounge in accountStore.managingLounges"
          :key="lounge.id"
          :lounge="lounge"
          @click="navigateToLoungeDetailView(lounge.id)"
        />
      </div>
    </div>
    <div class="lounge-container">
      <h1>내가 가입한 라운지</h1>
      <div class="card-container">
        <LoungeCard
          v-for="lounge in accountStore.joinedLounges"
          :key="lounge.id"
          :lounge="lounge"
          @click="navigateToLoungeDetailView(lounge.id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import LoungeCard from "@/components/Lounge/LoungeCard.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const accountStore = useAccountStore();
const navigateToLoungeDetailView = (loungePk) => {
  router.push({ name: "LoungeDetailView", params: { loungePk: loungePk } });
};
</script>

<style scoped>
.lounge-page {
  padding-top: 80px;
  width: 100vw;
  min-height: 100vh;
  background-color: black;
  color: #fff;
}

.card-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 40px;
}
</style>
