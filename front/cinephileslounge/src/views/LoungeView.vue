<template>
  <div class="lounge-page">
    <div class="lounge-container" v-show="hasManagingLounge">
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
    <div class="lounge-container" v-show="hasNonManagingLounges">
      <h1>내가 가입한 라운지</h1>
      <div class="card-container">
        <LoungeCard
          v-for="lounge in accountStore.nonManagingLounges"
          :key="lounge.id"
          :lounge="lounge"
          @click="navigateToLoungeDetailView(lounge.id)"
        />
      </div>
    </div>
    <div v-show="!hasManagingLounge && !hasJoinedLounge">
      <p>나만의 라운지를 만들어보세요.</p>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import LoungeCard from "@/components/Lounge/LoungeCard.vue";
import { useRouter } from "vue-router";
import { computed, ref } from "vue";

const router = useRouter();
const accountStore = useAccountStore();

const hasNonManagingLounges = computed(() => {
  console.log(accountStore.nonManagingLounges)
  if (accountStore.nonManagingLounges) {
    return !!accountStore.nonManagingLounges.length
  }
  return false
})

const hasManagingLounge = computed(() => {
  console.log(accountStore.managingLounges)
  if (accountStore.managingLounges) {
    return !!accountStore.managingLounges.length
  }
  return false
})

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
