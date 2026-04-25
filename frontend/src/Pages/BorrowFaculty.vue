<template>
  <div class="min-h-screen bg-[#F0EFFF]">
    <Navbar />

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
      <div class="mb-10 text-center md:text-left">
        <h2 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">
          รายการพัสดุและครุภัณฑ์ของแต่ละคณะที่สามารถให้ยืมได้
        </h2>
        <p class="text-gray-500">
          กดเลือกคณะเพื่อดูข้อมูลสิ่งของและช่องทางการติดต่อ
        </p>
      </div>

      <div
        v-if="isLoading"
        class="fixed inset-0 z-50 flex items-center justify-center bg-white/60 backdrop-blur-sm"
      >
        <div
          class="bg-white px-6 py-4 rounded-2xl shadow-xl flex items-center gap-3"
        >
          <div
            class="w-6 h-6 border-4 border-[#a259ff] border-t-transparent rounded-full animate-spin"
          ></div>
          <span class="font-bold text-gray-700">กำลังโหลดข้อมูล...</span>
        </div>
      </div>

      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
      >
        <button
          v-for="faculty in faculties"
          :key="faculty.id"
          @click="fetchFacultyData(faculty.id)"
          class="group text-left p-5 bg-white/70 backdrop-blur-md rounded-3xl shadow-sm transition-all duration-300 focus:outline-none relative overflow-hidden"
          :style="{ '--faculty-color': faculty.color }"
        >
          <div
            class="absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-300"
            :style="{ backgroundColor: faculty.color }"
          ></div>

          <div class="flex items-start gap-4 relative z-10">
            <div
              class="shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center font-black text-lg shadow-inner group-hover:scale-110 transition-transform duration-300 border border-gray-100"
              :style="{
                backgroundColor: faculty.color,
                color: faculty.textColor,
              }"
            >
              {{ faculty.id }}
            </div>

            <div class="flex flex-col">
              <span
                class="font-bold text-gray-800 leading-tight transition-colors duration-300 group-hover:text-[var(--faculty-color)]"
              >
                {{ faculty.nameTh }}
              </span>
              <span
                class="text-[11px] text-gray-500 mt-1 font-mono leading-tight"
              >
                {{ faculty.nameEn }}
              </span>
            </div>
          </div>

          <div
            class="absolute bottom-0 left-0 h-1 w-0 group-hover:w-full transition-all duration-500 ease-out"
            :style="{ backgroundColor: faculty.color }"
          ></div>
        </button>
      </div>
    </main>

    <Teleport to="body">
      <div
        v-if="isModalOpen"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-gray-900/40 backdrop-blur-sm animate-fade-in"
        @click.self="closeModal"
      >
        <div
          class="bg-white w-full max-w-3xl max-h-[85vh] flex flex-col rounded-3xl shadow-2xl overflow-hidden relative"
        >
          <div
            class="p-6 md:p-8 border-b border-gray-100 flex justify-between items-start gap-4 bg-gray-50/50"
          >
            <div>
              <div
                class="inline-block px-3 py-1 font-bold text-xs rounded-full mb-2 border"
                :style="{
                  backgroundColor: selectedFaculty?.color + '22',
                  color:
                    selectedFaculty?.color === '#FFFFFF' ||
                    selectedFaculty?.color === '#FFEE4C'
                      ? '#374151'
                      : selectedFaculty?.color,
                  borderColor: selectedFaculty?.color + '44',
                }"
              >
                รหัสคณะ: {{ selectedFaculty?.id }}
              </div>
              <h3 class="text-2xl font-black text-gray-800">
                {{ selectedFaculty?.nameTh }}
              </h3>
              <p class="text-gray-500 text-sm mt-1 font-mono">
                {{ selectedFaculty?.nameEn }}
              </p>
            </div>
            <button
              @click="closeModal"
              class="shrink-0 p-2 bg-gray-100 hover:bg-gray-200 text-gray-500 rounded-full transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <div
            class="p-6 md:p-8 overflow-y-auto custom-scrollbar flex-1 bg-[#F0EFFF]/30"
          >
            <div v-if="selectedFaculty?.contact" class="mb-8">
              <p
                class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3 pl-1"
              >
                ช่องทางการติดต่อ
              </p>
              <a
                :href="selectedFaculty.contact.href"
                target="_blank"
                class="group flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-white rounded-2xl border border-gray-200 hover:border-[#a259ff]/50 hover:shadow-lg transition-all duration-300"
              >
                <div class="flex items-center gap-4">
                  <div
                    class="w-12 h-12 shrink-0 rounded-full bg-gradient-to-br from-blue-50 to-indigo-50 text-blue-500 flex items-center justify-center group-hover:scale-110 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                      />
                    </svg>
                  </div>
                  <div>
                    <h4
                      class="font-bold text-gray-800 text-base group-hover:text-[#a259ff] transition-colors"
                    >
                      {{ selectedFaculty.contact.name }}
                    </h4>
                    <p class="text-sm text-gray-500 mt-0.5">
                      {{ selectedFaculty.contact.description }}
                    </p>
                  </div>
                </div>
                <div
                  class="bg-[#a259ff]/10 text-[#a259ff] px-4 py-2 rounded-xl text-sm font-bold group-hover:bg-[#a259ff] group-hover:text-white transition-colors text-center sm:text-left whitespace-nowrap"
                >
                  ติดต่อไปยังคณะ ↗
                </div>
              </a>
            </div>

            <p
              class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3 pl-1"
            >
              รายการอุปกรณ์
            </p>

            <div
              v-if="facultyEquipments.length === 0"
              class="text-center py-8 bg-white border border-gray-100 rounded-2xl"
            >
              <div
                class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-3"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-8 w-8 text-gray-300"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                  />
                </svg>
              </div>
              <p class="text-gray-500 font-bold text-sm">
                ยังไม่มีข้อมูลอุปกรณ์ให้ยืมสำหรับคณะนี้
              </p>
            </div>

            <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div
                v-for="item in facultyEquipments"
                :key="item.id"
                class="group bg-white p-4 rounded-2xl border border-gray-100 flex items-center gap-4 hover:shadow-md hover:border-[#a259ff]/30 transition-all"
              >
                <div
                  class="w-16 h-16 shrink-0 bg-gray-50 rounded-xl overflow-hidden border border-gray-100 flex items-center justify-center group-hover:scale-105 transition-transform"
                >
                  <img
                    v-if="item.image_url"
                    :src="item.image_url"
                    class="w-full h-full object-cover"
                    alt="equipment"
                  />
                  <span v-else class="text-[10px] text-gray-400">ไม่มีรูป</span>
                </div>
                <div class="flex flex-col flex-1">
                  <h4
                    class="font-bold text-gray-800 line-clamp-1 group-hover:text-[#a259ff] transition-colors"
                  >
                    {{ item.name }}
                  </h4>
                  <div class="flex items-center gap-2 mt-1">
                    <span class="text-xs text-gray-500">คงเหลือ:</span>
                    <span
                      class="text-sm font-black"
                      :class="
                        item.available_quantity > 0
                          ? 'text-green-500'
                          : 'text-red-500'
                      "
                    >
                      {{ item.available_quantity || 0 }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "../components/Navbar.vue";

const isLoading = ref(false);

const isModalOpen = ref(false);
const selectedFaculty = ref(null);
const facultyEquipments = ref([]);

const faculties = [
  {
    id: "01",
    nameTh: "คณะมนุษยศาสตร์",
    nameEn: "Faculty of Humanities",
    color: "#FFFFFF",
    textColor: "#374151",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะมนุษยศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smohumancmu.official/",
    },
  },
  {
    id: "02",
    nameTh: "คณะศึกษาศาสตร์",
    nameEn: "Faculty of Education",
    color: "#43C7F4",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะศึกษาศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoedu.cmu/",
    },
  },
  {
    id: "03",
    nameTh: "คณะวิจิตรศิลป์",
    nameEn: "Faculty of Fine Arts",
    color: "#E41E26",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะวิจิตรศิลป์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smofinearts.cmu/",
    },
  },
  {
    id: "04",
    nameTh: "คณะสังคมศาสตร์",
    nameEn: "Faculty of Social Sciences",
    color: "#4BA2DB",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะสังคมศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smosoccmu/",
    },
  },
  {
    id: "05",
    nameTh: "คณะวิทยาศาสตร์",
    nameEn: "Faculty of Science",
    color: "#FACB21",
    textColor: "#374151",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะวิทยาศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoscicmu.official/",
    },
  },
  {
    id: "06",
    nameTh: "คณะวิศวกรรมศาสตร์",
    nameEn: "Faculty of Engineering",
    color: "#5B171E",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smo.ent.cmu/",
    },
  },
  {
    id: "07",
    nameTh: "คณะแพทยศาสตร์",
    nameEn: "Faculty of Medicine",
    color: "#007832",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/cmso.medcmu/",
    },
  },
  {
    id: "08",
    nameTh: "คณะเกษตรศาสตร์",
    nameEn: "Faculty of Agriculture",
    color: "#FAA61A",
    textColor: "#374151",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะเกษตรศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/aggie.smo_cmu/",
    },
  },
  {
    id: "09",
    nameTh: "คณะทันตแพทยศาสตร์",
    nameEn: "Faculty of Dentistry",
    color: "#6D2C90",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะทันตแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smodent.cmu/",
    },
  },
  {
    id: "10",
    nameTh: "คณะเภสัชศาสตร์",
    nameEn: "Faculty of Pharmacy",
    color: "#5C990E",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะเภสัชศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smo_rxcmu/",
    },
  },
  {
    id: "11",
    nameTh: "คณะเทคนิคการแพทย์",
    nameEn: "Faculty of Associated Medical Sciences",
    color: "#28487F",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะเทคนิคการแพทย์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smomedtech69_official/",
    },
  },
  {
    id: "12",
    nameTh: "คณะพยาบาลศาสตร์",
    nameEn: "Faculty of Nursing",
    color: "#F16422",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะพยาบาลศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smonurse_official/",
    },
  },
  {
    id: "13",
    nameTh: "คณะอุตสาหกรรมเกษตร",
    nameEn: "Faculty of Agro-Industry",
    color: "#CC9933",
    textColor: "#FFFFFF",
    contact: {
      name: "ติดต่อสโมสรนักศึกษา",
      description: "เพจสโมสรนักศึกษาคณะอุตสาหกรรมเกษตร",
      href: "#",
    },
  },
  {
    id: "14",
    nameTh: "คณะสัตวแพทยศาสตร์",
    nameEn: "Faculty of Veterinary Medicine",
    color: "#5EAFD2",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะสัตวแพทยศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoagro_official/",
    },
  },
  {
    id: "15",
    nameTh: "คณะบริหารธุรกิจ",
    nameEn: "Faculty of Business Administration",
    color: "#008EAA",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะบริหารธุรกิจ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smobala.official/",
    },
  },
  {
    id: "16",
    nameTh: "คณะเศรษฐศาสตร์",
    nameEn: "Faculty of Economics",
    color: "#ED4081",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะเศรษฐศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoeconcmu/",
    },
  },
  {
    id: "17",
    nameTh: "คณะสถาปัตยกรรมศาสตร์",
    nameEn: "Faculty of Architecture",
    color: "#FEE4C2",
    textColor: "#374151",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะสถาปัตยกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoarchcmu/",
    },
  },
  {
    id: "18",
    nameTh: "คณะการสื่อสารมวลชน",
    nameEn: "Faculty of Mass Communication",
    color: "#838383",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะการสื่อสารมวลชน มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smomc.official/",
    },
  },
  {
    id: "19",
    nameTh: "คณะรัฐศาสตร์และรัฐประศาสนศาสตร์",
    nameEn: "Faculty of Political Science and Public Admin.",
    color: "#173C6E",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะรัฐศาสตร์ฯ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smo.polsci_cmu/",
    },
  },
  {
    id: "20",
    nameTh: "คณะนิติศาสตร์",
    nameEn: "Faculty of Law",
    color: "#B2A4D4",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษาคณะนิติศาสตร์ มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smolawcmu.official/",
    },
  },
  {
    id: "21",
    nameTh: "วิทยาลัยศิลปะ สื่อ และเทคโนโลยี",
    nameEn: "College of Arts, Media and Technology",
    color: "#AC6B4D",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษา CAMT มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smocamt.official/",
    },
  },
  {
    id: "22",
    nameTh: "วิทยาลัยนานาชาตินวัตกรรมดิจิทัล",
    nameEn: "International College of Digital Innovation",
    color: "#012169",
    textColor: "#FFFFFF",
    contact: {
      name: "Instagram",
      description: "สโมสรนักศึกษา ICIT มหาวิทยาลัยเชียงใหม่",
      href: "https://www.instagram.com/smoicit.official/",
    },
  },
];

const fetchFacultyData = async (id) => {
  isLoading.value = true;
  selectedFaculty.value = faculties.find((f) => f.id === id);

  try {
    const response = await fetch(`/api/borrow/faculty/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    const json = await response.json();
    facultyEquipments.value = json.data || [];
    isModalOpen.value = true;
  } catch (error) {
    console.error("Error fetching faculty data:", error);
    alert("เกิดข้อผิดพลาดในการดึงข้อมูล กรุณาลองใหม่อีกครั้ง");
  } finally {
    isLoading.value = false;
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  setTimeout(() => {
    selectedFaculty.value = null;
    facultyEquipments.value = [];
  }, 300);
};
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
