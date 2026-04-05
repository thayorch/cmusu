<template>
  <RouterLink
    :to="to"
    class="bg-white/50 inline-flex items-center gap-2 px-5 py-2.5 rounded-lg font-bold text-sm transition-all duration-200 hover:-translate-y-0.5 hover:cursor-pointer"
    style="color: #a259ff; box-shadow: 0 4px 16px rgba(162, 89, 255, 0.21)"
  >
    <component :is="icon" class="w-4 h-4" />
    {{ text }}
  </RouterLink>
</template>
<script setup>
import { RouterLink } from "vue-router";
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: true,
  },
  icon: {
    type: Object,
    required: true,
  },
});
</script>
