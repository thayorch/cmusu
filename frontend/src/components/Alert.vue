<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="state.visible"
        class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
        @mousedown.self="onBackdropClick"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" />

        <!-- Modal -->
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 scale-100 translate-y-0"
          leave-to-class="opacity-0 scale-95 translate-y-2"
          appear
        >
          <div
            v-if="state.visible"
            class="relative bg-white rounded-3xl shadow-2xl w-full max-w-sm p-6 flex flex-col items-center gap-4 text-center"
          >
            <!-- Icon -->
            <div
              class="w-14 h-14 rounded-2xl flex items-center justify-center"
              :class="iconBg"
            >
              <component :is="icon" class="w-7 h-7" :class="iconColor" />
            </div>

            <!-- Message -->
            <p class="text-gray-800 font-semibold text-base leading-relaxed">
              {{ state.message }}
            </p>

            <!-- Buttons -->
            <div class="flex gap-3 w-full mt-1">
              <button
                v-if="state.type === 'confirm'"
                @click="close(false)"
                class="flex-1 py-2.5 px-4 rounded-xl text-sm font-bold border border-gray-200 text-gray-600 hover:bg-gray-50 transition-colors"
              >
                ยกเลิก
              </button>
              <button
                @click="close(true)"
                class="flex-1 py-2.5 px-4 rounded-xl text-sm font-bold text-white transition-colors"
                :class="confirmBtnClass"
              >
                {{ state.type === "confirm" ? "ยืนยัน" : "ตกลง" }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from "vue";
import {
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  QuestionMarkCircleIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../composables/useAlert";

const { state, close } = useAlert();

const onBackdropClick = () => {
  if (state.type !== "confirm") close(true);
};

const icon = computed(() => {
  const icons = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    warning: ExclamationTriangleIcon,
    confirm: QuestionMarkCircleIcon,
    info: InformationCircleIcon,
  };
  return icons[state.type] ?? InformationCircleIcon;
});

const iconBg = computed(() => {
  const map = {
    success: "bg-green-100",
    error: "bg-red-100",
    warning: "bg-yellow-100",
    confirm: "bg-purple-100",
    info: "bg-blue-100",
  };
  return map[state.type] ?? "bg-blue-100";
});

const iconColor = computed(() => {
  const map = {
    success: "text-green-600",
    error: "text-red-500",
    warning: "text-yellow-500",
    confirm: "text-purple-600",
    info: "text-blue-500",
  };
  return map[state.type] ?? "text-blue-500";
});

const confirmBtnClass = computed(() => {
  const map = {
    success: "bg-green-500 hover:bg-green-600",
    error: "bg-red-500 hover:bg-red-600",
    warning: "bg-yellow-500 hover:bg-yellow-600",
    confirm: "bg-[#a259ff] hover:bg-[#8b3dff]",
    info: "bg-blue-500 hover:bg-blue-600",
  };
  return map[state.type] ?? "bg-blue-500 hover:bg-blue-600";
});
</script>
