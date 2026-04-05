<template>
  <div
    class="overflow-hidden relative z-10 py-3"
    style="
      background: rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(12px);
      border-top: 1.5px solid rgba(255, 255, 255, 0.9);
      border-bottom: 1.5px solid rgba(255, 255, 255, 0.9);
    "
  >
    <div
      class="inline-flex whitespace-nowrap"
      style="animation: ticker 28s linear infinite"
    >
      <span
        v-for="(tool, i) in [...tools, ...tools]"
        :key="i"
        class="inline-flex items-center gap-2 px-7 font-mono text-xs font-bold tracking-wider"
        :style="{ color: tool.color }"
      >
        <component :is="tool.icon" class="w-4 h-4" />
        <span>{{ tool.name }}</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import {
  TicketIcon,
  HeartIcon,
  LightBulbIcon,
  LanguageIcon,
  ComputerDesktopIcon,
  BriefcaseIcon,
  BuildingLibraryIcon,
  PuzzlePieceIcon,
  GlobeAsiaAustraliaIcon,
  BoltIcon,
  ShieldCheckIcon,
} from "@heroicons/vue/24/solid";

const tools = [
  { name: "CMU Festival", icon: TicketIcon, color: "#FF6EC7" },
  { name: "CMU Continue", icon: HeartIcon, color: "#A259FF" },
  { name: "CMU Potential", icon: LightBulbIcon, color: "#FFD166" },
  { name: "CMU Language", icon: LanguageIcon, color: "#06D6A0" },
  { name: "CMU Digital Literacy", icon: ComputerDesktopIcon, color: "#5BC8FF" },
  { name: "CMU Job Fair", icon: BriefcaseIcon, color: "#FF9A5C" },
  { name: "CMU Politics", icon: BuildingLibraryIcon, color: "#FF6EC7" },
  { name: "CMU Variety", icon: PuzzlePieceIcon, color: "#A259FF" },
  { name: "CMU Green Shift", icon: GlobeAsiaAustraliaIcon, color: "#06D6A0" },
  { name: "CMU Healthy", icon: BoltIcon, color: "#FFD166" },
  { name: "CMU Security", icon: ShieldCheckIcon, color: "#5BC8FF" },
];
</script>

<style scoped>
@keyframes ticker {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>
