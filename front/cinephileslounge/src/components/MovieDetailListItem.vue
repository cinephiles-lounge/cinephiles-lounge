<template>
  <div class="reviewItem-container">
    <div class="reviewItem-img">
      <i class="bx bxl-github"></i>
    </div>
    <div class="reviewItem">
      <div class="review-writer">
        <p>{{ review.user.nickname }}</p>
        <div v-if="!isUpdate">{{ review.rank }}</div>
      </div>
      <div class="review-overview" v-if="!isUpdate">
        <p>{{ review.content }}</p>
      </div>
      <i
        @click="isUpdate = !isUpdate"
        v-if="!isUpdate && accountStore.userPk === review.user.id"
        class="bx bxs-edit-alt"
      ></i>
      <i
        @click="delete_shortReview"
        v-if="!isUpdate && accountStore.userPk === review.user.id"
        class="bx bxs-message-square-x"
      ></i>
      <div class="review-update">
        <star-rating
          v-if="isUpdate"
          @update:rating="setRating"
          :increment="0.5"
          :max-rating="5"
          :rounded-corners="true"
          :inline="true"
          :show-rating="false"
          :active-color="['#f82e62']"
          :active-border-color="['#f82e62']"
          :border-width="1"
          :star-size="24"
          :active-on-click="true"
          :clearable="true"
        >
        </star-rating>
        <input
          class="review-update-text"
          v-if="isUpdate"
          v-model.trim="content"
          type="text"
        />
        <input
          class="review-update-updateBtn"
          @click.prevent="update_shortReview"
          v-if="isUpdate"
          type="submit"
          value="수정"
        />

        <input
          class="review-update-cancelBtn"
          v-if="isUpdate"
          type="submit"
          value="취소"
          @click.prevent="isUpdate = !isUpdate"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { useAccountStore } from "@/stores/account";
import { ref } from "vue";
import StarRating from "vue-star-rating";
const accountStore = useAccountStore();
const props = defineProps({
  shortReview: Object,
});
const emit = defineEmits(["delete"]);
const review = ref(props.shortReview);
const isUpdate = ref(false);
const userRating = ref(1);
const content = ref("");

// 사용자가 입력한 별점 userRating에 저장
const setRating = (rating) => {
  userRating.value = rating;
};
// 한줄 리뷰 삭제
const delete_shortReview = () => {
  axios({
    method: "delete",
    url: `${accountStore.API_URL}/movies/short_review/${review.value.id}`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      emit("delete", review.value.id); //emit으로 부모 컴포넌트에게 reviewId 보내고 거기서 front에 보이도록 삭제
    })
    .catch((err) => {
      console.log(err);
    });
};
// 한줄 리뷰 수정
const update_shortReview = () => {
  axios({
    method: "put",
    url: `${accountStore.API_URL}/movies/short_review/${review.value.id}/`,
    data: {
      content: content.value,
      rank: userRating.value,
    },
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      review.value.content = res.data.content; // front에서도 수정 된것처럼 랜더링
      review.value.rank = res.data.rank;
      isUpdate.value = false; // html요소들 다시 안보이게 isUpdate false
      content.value = "";
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>
<style scoped>
.reviewItem-container {
  margin-top: 10px;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.reviewItem-container .reviewItem {
  width: 777px;
  height: 88px;
  margin-left: 10px;
}
.reviewItem-container .reviewItem .review-writer {
  display: flex;
  align-items: center;
  width: 100%;
}
.reviewItem-container .reviewItem .review-writer p {
  font-size: 15px;
  line-height: 1.33em;
  font-size: 15px;
  font-weight: 400;
  margin-right: 4px;
  height: 20px;
}
.reviewItem-container .reviewItem .review-writer div {
  font-size: 16px;
  line-height: 21px;
}

.reviewItem-container .reviewItem .review-overview {
  margin: 4px 0px;
  width: 100%;
}
.reviewItem-container .reviewItem .review-overview p {
  font-size: 15px;
  line-height: 1.33em;
  width: 100%;
  color: #7c7b84;
}
.reviewItem-container .reviewItem-img i {
  font-size: 40px;
}
.bxs-edit-alt {
  margin-right: 6px;
  color: #7c7b84;
  cursor: pointer;
}
.bxs-edit-alt:hover {
  color: #eee;
}
.bxs-message-square-x {
  color: #7c7b84;
  cursor: pointer;
}
.bxs-message-square-x:hover {
  color: #eee;
}
.review-update {
  display: flex;
}
.review-update .review-update-text {
  margin: 0px 10px;
  width: 500px;
  border-radius: 5px;
  outline: none;
  color: #eee;
  background-color: #222326;
  border: none;
}
.review-update .review-update-updateBtn {
  margin-right: 5px;
  border-radius: 5px;
  background-color: #f82e62;
  color: #eee;
  border: none;
  height: 40px;
  padding: 10px;
  cursor: pointer;
}
.review-update .review-update-cancelBtn {
  border-radius: 5px;
  border: none;
  height: 40px;
  padding: 10px;
  cursor: pointer;
}
</style>
