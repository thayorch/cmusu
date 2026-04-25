<template>
  <div>
    <label class="block text-sm font-bold mb-1.5 text-gray-700">ไอคอน</label>

    <div class="p-3 bg-gray-50 border border-gray-200 rounded-xl">
      <!-- Preview -->
      <div class="flex items-center gap-2 mb-3">
        <div
          class="w-8 h-8 rounded-lg flex items-center justify-center"
          :style="`background-color: ${previewColor}20; color: ${previewColor}`"
        >
          <component :is="selectedIconComponent" class="w-5 h-5" />
        </div>
        <span class="text-sm font-bold text-gray-700">{{ modelValue }}</span>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-7 gap-1.5">
        <button
          v-for="icon in ICONS"
          :key="icon.name"
          type="button"
          @click="$emit('update:modelValue', icon.name)"
          :title="icon.name"
          :class="[
            'p-2 rounded-lg flex items-center justify-center transition-all',
            modelValue === icon.name
              ? 'bg-white shadow-sm ring-2 ring-offset-1'
              : 'hover:bg-white/80 text-gray-500 hover:text-gray-800',
          ]"
          :style="modelValue === icon.name ? `ring-color: ${previewColor}; color: ${previewColor}` : ''"
        >
          <component :is="icon.component" class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  NewspaperIcon,
  CalendarDaysIcon,
  MegaphoneIcon,
  BellIcon,
  StarIcon,
  FireIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  TrophyIcon,
  AcademicCapIcon,
  BuildingLibraryIcon,
  UserGroupIcon,
  HeartIcon,
  SparklesIcon,
  GlobeAltIcon,
  DocumentTextIcon,
  ChatBubbleLeftIcon,
  ClockIcon,
  MapPinIcon,
  FlagIcon,
  MicrophoneIcon,
  MusicalNoteIcon,
  BookOpenIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  HandRaisedIcon,
  GiftIcon,
  PresentationChartBarIcon,
  CameraIcon,
  SpeakerWaveIcon,
  PencilSquareIcon,
  WrenchScrewdriverIcon,
  ComputerDesktopIcon,
} from "@heroicons/vue/24/solid";

const props = defineProps({
  modelValue: { type: String, default: "NewspaperIcon" },
  previewColor: { type: String, default: "#A259FF" },
});

defineEmits(["update:modelValue"]);

const ICONS = [
  { name: "NewspaperIcon", component: NewspaperIcon },
  { name: "CalendarDaysIcon", component: CalendarDaysIcon },
  { name: "MegaphoneIcon", component: MegaphoneIcon },
  { name: "BellIcon", component: BellIcon },
  { name: "StarIcon", component: StarIcon },
  { name: "FireIcon", component: FireIcon },
  { name: "CheckCircleIcon", component: CheckCircleIcon },
  { name: "InformationCircleIcon", component: InformationCircleIcon },
  { name: "ExclamationTriangleIcon", component: ExclamationTriangleIcon },
  { name: "TrophyIcon", component: TrophyIcon },
  { name: "AcademicCapIcon", component: AcademicCapIcon },
  { name: "BuildingLibraryIcon", component: BuildingLibraryIcon },
  { name: "UserGroupIcon", component: UserGroupIcon },
  { name: "HeartIcon", component: HeartIcon },
  { name: "SparklesIcon", component: SparklesIcon },
  { name: "GlobeAltIcon", component: GlobeAltIcon },
  { name: "DocumentTextIcon", component: DocumentTextIcon },
  { name: "ChatBubbleLeftIcon", component: ChatBubbleLeftIcon },
  { name: "ClockIcon", component: ClockIcon },
  { name: "MapPinIcon", component: MapPinIcon },
  { name: "FlagIcon", component: FlagIcon },
  { name: "MicrophoneIcon", component: MicrophoneIcon },
  { name: "MusicalNoteIcon", component: MusicalNoteIcon },
  { name: "BookOpenIcon", component: BookOpenIcon },
  { name: "LightBulbIcon", component: LightBulbIcon },
  { name: "RocketLaunchIcon", component: RocketLaunchIcon },
  { name: "HandRaisedIcon", component: HandRaisedIcon },
  { name: "GiftIcon", component: GiftIcon },
  { name: "PresentationChartBarIcon", component: PresentationChartBarIcon },
  { name: "CameraIcon", component: CameraIcon },
  { name: "SpeakerWaveIcon", component: SpeakerWaveIcon },
  { name: "PencilSquareIcon", component: PencilSquareIcon },
  { name: "WrenchScrewdriverIcon", component: WrenchScrewdriverIcon },
  { name: "ComputerDesktopIcon", component: ComputerDesktopIcon },
];

const selectedIconComponent = computed(
  () => ICONS.find((i) => i.name === props.modelValue)?.component ?? NewspaperIcon
);
</script>
