<template>
  <div class="animate-fade-in">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4">
      <div>
        <h3 class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2">
          <CalendarDaysIcon class="w-7 h-7 md:w-8 md:h-8 text-[#ffd166]" />
          จัดการตารางกิจกรรม
        </h3>
        <p class="text-gray-500 text-sm">ดู เพิ่ม แก้ไข หรือลบกิจกรรมในระบบ</p>
      </div>
      <button
        @click="openModal('add')"
        class="w-full md:w-auto px-6 py-3 bg-gray-900 hover:bg-black text-white font-bold rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
      >
        <PlusIcon class="w-5 h-5" />
        เพิ่มกิจกรรมใหม่
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">
      <div class="inline-flex flex-col items-center gap-3">
        <div class="w-8 h-8 border-4 border-[#ffd166]/30 border-t-[#ffd166] rounded-full animate-spin" />
        <span class="text-sm font-medium">กำลังโหลดข้อมูล...</span>
      </div>
    </div>

    <div v-else-if="activities.length === 0" class="text-center py-20 text-gray-400">
      <CalendarDaysIcon class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p class="font-medium">ยังไม่มีกิจกรรมในระบบ</p>
    </div>

    <div v-else class="flex flex-col gap-3">
      <div
        v-for="item in activities"
        :key="item.id"
        class="glass rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center gap-3 hover:shadow-md transition-all"
      >
        <div class="flex-1 min-w-0">
          <div class="flex flex-wrap items-center gap-2 mb-1">
            <span
              class="px-2 py-0.5 rounded-full text-xs font-bold text-white"
              :style="`background-color: ${item.item_color}`"
            >
              {{ item.phase }}
            </span>
            <span class="text-xs text-gray-400">{{ item.month_group }} · {{ item.time_seq }}</span>
            <span v-if="item.badge" class="px-2 py-0.5 rounded-full text-xs font-bold bg-gray-100 text-gray-600">
              {{ item.badge }}
            </span>
          </div>
          <p class="font-bold text-gray-900 text-sm leading-snug line-clamp-1">{{ item.title }}</p>
          <p class="text-xs text-gray-400 mt-0.5 line-clamp-1">{{ item.location_desc }}</p>
        </div>
        <div class="flex gap-2 shrink-0">
          <button
            @click="openModal('edit', item)"
            class="flex items-center gap-1.5 px-3 py-2 text-xs font-bold rounded-xl bg-yellow-50 text-yellow-600 hover:bg-yellow-500 hover:text-white transition-colors border border-yellow-100 hover:border-yellow-500"
          >
            <PencilIcon class="w-3.5 h-3.5" />
            แก้ไข
          </button>
          <button
            @click="deleteActivity(item.id)"
            class="flex items-center gap-1.5 px-3 py-2 text-xs font-bold rounded-xl bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-colors border border-red-100 hover:border-red-500"
          >
            <TrashIcon class="w-3.5 h-3.5" />
            ลบ
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
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
          v-if="isModalOpen"
          class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
          @mousedown.self="closeModal"
        >
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 scale-95 translate-y-2"
            enter-to-class="opacity-100 scale-100 translate-y-0"
            appear
          >
            <div
              v-if="isModalOpen"
              class="bg-white w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-3xl p-6 md:p-8 relative shadow-2xl"
            >
              <button
                @click="closeModal"
                class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 bg-gray-100 hover:bg-gray-200 p-2 rounded-full transition-colors"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>

              <h3 class="text-xl font-black mb-0.5">
                {{ isEditing ? "แก้ไขกิจกรรม" : "เพิ่มกิจกรรมใหม่" }}
              </h3>
              <p class="text-gray-400 text-sm mb-6">กรอกรายละเอียดกิจกรรม</p>

              <form @submit.prevent="submitActivity" class="space-y-4">
                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">
                    ชื่อกิจกรรม <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.title"
                    type="text"
                    required
                    placeholder="เช่น ประชุมนักศึกษา"
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all"
                  />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">
                      กลุ่มเดือน <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="form.month_group"
                      type="text"
                      required
                      placeholder="เช่น มิถุนายน 2568"
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">
                      ลำดับเวลา <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="form.time_seq"
                      type="text"
                      required
                      placeholder="เช่น 2568-06-15"
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all"
                    />
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">
                      ช่วงเวลา (Phase) <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="form.phase"
                      type="text"
                      required
                      placeholder="เช่น ต้นภาค"
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">Badge</label>
                    <input
                      v-model="form.badge"
                      type="text"
                      placeholder="เช่น สำคัญ"
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">สถานที่/รายละเอียด</label>
                  <textarea
                    v-model="form.location_desc"
                    rows="2"
                    placeholder="เช่น ห้องประชุมใหญ่ ชั้น 3 อาคาร..."
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 focus:border-[#ffd166] transition-all resize-none"
                  />
                </div>

                <IconPicker v-model="form.icon_name" :preview-color="form.item_color" />

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">สีรายการ</label>
                    <div class="flex items-center gap-2">
                      <input v-model="form.item_color" type="color" class="w-10 h-10 rounded-lg border border-gray-200 cursor-pointer" />
                      <input
                        v-model="form.item_color"
                        type="text"
                        class="flex-1 px-3 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 transition-all font-mono text-sm"
                      />
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">สีกลุ่ม</label>
                    <div class="flex items-center gap-2">
                      <input v-model="form.group_color" type="color" class="w-10 h-10 rounded-lg border border-gray-200 cursor-pointer" />
                      <input
                        v-model="form.group_color"
                        type="text"
                        class="flex-1 px-3 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#ffd166]/60 transition-all font-mono text-sm"
                      />
                    </div>
                  </div>
                </div>

                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-200">
                  <input
                    v-model="form.is_highlight"
                    type="checkbox"
                    id="highlight"
                    class="w-4 h-4 accent-[#ffd166] rounded cursor-pointer"
                  />
                  <label for="highlight" class="text-sm font-bold text-gray-700 cursor-pointer">
                    Highlight กิจกรรมนี้
                  </label>
                </div>

                <div class="flex gap-3 pt-2">
                  <button
                    type="button"
                    @click="closeModal"
                    class="flex-1 py-3 bg-gray-100 hover:bg-gray-200 font-bold rounded-xl transition-colors text-gray-700"
                  >
                    ยกเลิก
                  </button>
                  <button
                    type="submit"
                    :disabled="isSubmitting"
                    class="flex-1 py-3 text-white font-bold rounded-xl bg-gray-900 hover:bg-black transition-colors disabled:opacity-50"
                  >
                    {{ isSubmitting ? "กำลังบันทึก..." : isEditing ? "บันทึกการแก้ไข" : "เพิ่มกิจกรรม" }}
                  </button>
                </div>
              </form>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { CalendarDaysIcon, PlusIcon, PencilIcon, TrashIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useAlert } from "../../composables/useAlert";
import { useCsrf } from "../../composables/useCsrf";
import IconPicker from "./IconPicker.vue";

const { showAlert, showConfirm } = useAlert();
const { getCsrfToken } = useCsrf();

const activities = ref([]);
const isLoading = ref(false);
const isSubmitting = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

const form = reactive({
  month_group: "",
  time_seq: "",
  phase: "",
  title: "",
  location_desc: "",
  badge: "",
  item_color: "#A259FF",
  group_color: "#A259FF",
  icon_name: "CalendarDaysIcon",
  is_highlight: false,
});

const fetchActivities = async () => {
  isLoading.value = true;
  try {
    const res = await fetch("/api/admin/activity", { credentials: "include" });
    const json = await res.json();
    if (json.status === "success") activities.value = json.data;
  } catch (e) {
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchActivities);

const openModal = (mode, item = null) => {
  if (mode === "edit" && item) {
    isEditing.value = true;
    editingId.value = item.id;
    Object.assign(form, {
      month_group: item.month_group,
      time_seq: item.time_seq,
      phase: item.phase,
      title: item.title,
      location_desc: item.location_desc,
      badge: item.badge || "",
      item_color: item.item_color || "#A259FF",
      group_color: item.group_color || "#A259FF",
      icon_name: item.icon_name || "CalendarDaysIcon",
      is_highlight: item.is_highlight || false,
    });
  } else {
    isEditing.value = false;
    editingId.value = null;
    resetForm();
  }
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const resetForm = () => {
  form.month_group = "";
  form.time_seq = "";
  form.phase = "";
  form.title = "";
  form.location_desc = "";
  form.badge = "";
  form.item_color = "#A259FF";
  form.group_color = "#A259FF";
  form.icon_name = "CalendarDaysIcon";
  form.is_highlight = false;
};

const submitActivity = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const payload = { ...form, badge: form.badge || null };
    const url = isEditing.value ? `/api/admin/activity/${editingId.value}` : "/api/admin/activity";
    const res = await fetch(url, {
      method: isEditing.value ? "PUT" : "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
      credentials: "include",
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (res.ok) {
      await showAlert(data.message || "บันทึกเรียบร้อย", "success");
      closeModal();
      fetchActivities();
    } else {
      await showAlert(data.detail || "เกิดข้อผิดพลาด", "error");
    }
  } catch (e) {
    console.error(e);
    await showAlert("เกิดข้อผิดพลาดในการเชื่อมต่อ", "error");
  } finally {
    isSubmitting.value = false;
  }
};

const deleteActivity = async (id) => {
  if (!(await showConfirm("ลบกิจกรรมนี้?"))) return;
  try {
    const token = await getCsrfToken();
    const res = await fetch(`/api/admin/activity/${id}`, {
      method: "DELETE",
      headers: { "X-CSRF-Token": token },
      credentials: "include",
    });
    const data = await res.json();
    if (res.ok) {
      await showAlert(data.message || "ลบเรียบร้อย", "success");
      fetchActivities();
    } else {
      await showAlert(data.detail || "เกิดข้อผิดพลาด", "error");
    }
  } catch (e) {
    console.error(e);
  }
};
</script>
