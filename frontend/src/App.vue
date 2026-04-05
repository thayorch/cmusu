<template>
  <div
    class="font-kanit min-h-screen"
    style="background: #f0efff; color: #1a1040"
  >
    <router-view />
    <FooterCta />
  </div>
</template>
<script setup>
import FooterCta from "./components/FooterCta.vue";
</script>
