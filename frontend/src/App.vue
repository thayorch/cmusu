<template>
  <div
    class="font-kanit min-h-screen flex flex-col"
    style="background: #f0efff; color: #1a1040"
  >
    <main class="flex-grow">
      <router-view />
    </main>

    <FooterCta />
  </div>
</template>

<script setup>
import FooterCta from "./components/FooterCta.vue";
</script>
