<template>
  <div
    class="min-h-screen flex flex-col"
    style="background: #f0efff; color: #1a1040"
  >
    <main class="flex-grow">
      <router-view />
    </main>
    <FooterCta />
    <Alert />
  </div>
</template>

<script setup>
import FooterCta from "./components/FooterCta.vue";
import Alert from "./components/Alert.vue";
</script>
