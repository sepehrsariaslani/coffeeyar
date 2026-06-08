import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

export const useReviewsStore = defineStore("reviews", () => {
  const reviewsMap = ref({});

  async function fetchReviews(productId) {
    try {
      const list = await api.reviews.list(productId);
      reviewsMap.value[productId] = list;
      return list;
    } catch (e) {
      console.error(e.message);
      return [];
    }
  }

  function getReviews(productId) {
    return reviewsMap.value[productId] || [];
  }

  function averageRating(productId) {
    const list = getReviews(productId);
    if (!list.length) return 0;
    return Math.round((list.reduce((s, r) => s + r.rating, 0) / list.length) * 10) / 10;
  }

  async function addReview(productId, { name, rating, text, user_name }) {
    try {
      const rev = await api.reviews.create({
        product_id: productId,
        user_name: name || user_name || "کاربر",
        rating,
        text,
      });
      if (!reviewsMap.value[productId]) reviewsMap.value[productId] = [];
      reviewsMap.value[productId].unshift(rev);
      return { ok: true, review: rev };
    } catch (e) {
      return { ok: false, error: e.message };
    }
  }

  return { reviewsMap, getReviews, averageRating, addReview, fetchReviews };
});
