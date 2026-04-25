<template>
  <svg
    viewBox="0 0 24 24"
    :width="size"
    :height="size"
    aria-hidden="true"
    v-bind="svgProps"
  >
    <path v-if="name === 'facebook'" fill="currentColor"
      d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />

    <g v-else-if="name === 'instagram'" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
      <path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z" />
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
    </g>

    <path v-else-if="name === 'line'" fill="currentColor"
      d="M12 2C6.477 2 2 5.925 2 10.742c0 2.67 1.332 5.053 3.42 6.625.15.112.24.29.24.48 0 .234-.158.844-.186.96-.038.157-.125.603.526.329C8.41 17.7 11.714 15.4 13.335 14H13.336C13.554 14 21.863 13.563 21.996 10.76 22 10.754 22 10.748 22 10.742 22 5.925 17.523 2 12 2zM7.5 12.5h-2a.5.5 0 010-1H7V9a.5.5 0 011 0v3a.5.5 0 01-.5.5zm2.5 0a.5.5 0 01-.5-.5V9a.5.5 0 011 0v3a.5.5 0 01-.5.5zm4 0h-2a.5.5 0 01-.5-.5V9a.5.5 0 011 0v2.5h1.5a.5.5 0 010 1zm3-2.5a.5.5 0 010 1h-1V12a.5.5 0 01-1 0V9a.5.5 0 01.5-.5H17a.5.5 0 010 1h-1.5v.5H17z" />

    <path v-else-if="name === 'youtube'" fill="currentColor"
      d="M22.54 6.42a2.78 2.78 0 00-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 00-1.95 1.96A29 29 0 001 12a29 29 0 00.46 5.58 2.78 2.78 0 001.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 001.95-1.96A29 29 0 0023 12a29 29 0 00-.46-5.58zM9.75 15.02V8.98L15.5 12l-5.75 3.02z" />

    <path v-else-if="name === 'twitter'" fill="currentColor"
      d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />

    <path v-else-if="name === 'tiktok'" fill="currentColor"
      d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.87a8.19 8.19 0 004.79 1.52V7a4.85 4.85 0 01-1.02-.31z" />

    <g v-else-if="name === 'email'" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
      <polyline points="22,6 12,13 2,6" />
    </g>

    <g v-else-if="name === 'map'" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
      <circle cx="12" cy="10" r="3" />
    </g>
  </svg>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 16 },
});

const svgProps = computed(() => {
  const filled = ["facebook", "line", "youtube", "twitter", "tiktok"];
  return filled.includes(props.name) ? {} : {};
});
</script>
