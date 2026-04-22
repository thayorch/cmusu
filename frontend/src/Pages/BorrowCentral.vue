<template>
  <Navbar />
  <section class="relative z-10 max-w-7xl mx-auto px-6 pt-10 pb-24 lg:pb-20 animate-fade-in">

    <!-- Page Header -->
    <div class="text-center mb-10">
      <div class="glass inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5">
        <ArchiveBoxIcon class="w-4 h-4 text-[#a259ff]" />
        <span class="font-mono text-xs font-bold tracking-widest uppercase" style="color:#a259ff">
          CMUSU Borrow
        </span>
      </div>
      <h2 class="font-black text-dark text-4xl md:text-5xl mb-3">ครุภัณฑ์ส่วนกลาง</h2>
      <p class="text-lg text-[#8b7bae]">ระบบแคตตาล็อกและตะกร้ายืมครุภัณฑ์</p>
    </div>

    <!-- Auth checking -->
    <div v-if="isCheckingAuth" class="text-center py-20 text-[#8b7bae]">
      กำลังตรวจสอบสิทธิ์...
    </div>

    <!-- Not logged in -->
    <div
      v-else-if="!user"
      class="glass max-w-md mx-auto p-10 text-center rounded-3xl mt-10 shadow-xl"
    >
      <div class="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
        <LockClosedIcon class="w-10 h-10 text-blue-500" />
      </div>
      <h3 class="text-2xl font-bold mb-3">กรุณาเข้าสู่ระบบ</h3>
      <p class="text-sm text-gray-500">สงวนสิทธิ์การยืมเฉพาะนักศึกษามหาวิทยาลัยเชียงใหม่</p>
      <p class="text-sm text-gray-500 mb-8">(Login with CMU Account)</p>
      <a
        href="/api/auth/login"
        class="w-full py-4 bg-white hover:bg-gray-50 text-gray-800 font-bold rounded-2xl shadow-sm border flex items-center justify-center gap-3"
      >
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
          alt="Microsoft"
          class="w-5 h-5"
        />
        เข้าสู่ระบบด้วย Microsoft
      </a>
    </div>

    <!-- Main layout: Catalog + Desktop Cart -->
    <div v-else class="flex flex-col lg:flex-row gap-6 items-start">

      <!-- ─── LEFT: Catalog ─── -->
      <div class="flex-1 min-w-0">

        <!-- User bar -->
        <div class="flex justify-between items-center mb-6 glass p-3.5 px-5 rounded-2xl shadow-sm">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 bg-gradient-to-br from-[#a259ff] to-[#5bc8ff] text-white rounded-full flex items-center justify-center font-bold">
              {{ user.email[0].toUpperCase() }}
            </div>
            <div>
              <p class="text-sm font-bold text-gray-800 leading-tight">{{ user.email }}</p>
              <button @click="logout" class="text-xs text-red-400 hover:text-red-600 font-medium">
                ออกจากระบบ
              </button>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="text-center py-20 text-gray-400">
          <div class="inline-flex flex-col items-center gap-3">
            <div class="w-7 h-7 border-4 border-[#a259ff]/20 border-t-[#a259ff] rounded-full animate-spin" />
            <span class="text-sm">กำลังโหลดแคตตาล็อก...</span>
          </div>
        </div>

        <!-- Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          <div
            v-for="item in equipments"
            :key="item.id"
            class="glass rounded-3xl overflow-hidden flex flex-col group hover:-translate-y-0.5 transition-all duration-200 shadow-sm hover:shadow-md"
          >
            <div class="h-44 overflow-hidden bg-gray-100 relative">
              <img
                :src="item.image_url"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div
                class="absolute top-3 right-3 px-2.5 py-1 rounded-full text-xs font-black shadow-sm"
                :class="item.available_quantity > 0 ? 'bg-green-500/90 text-white' : 'bg-red-500/90 text-white'"
              >
                {{ item.available_quantity > 0 ? `เหลือ ${item.available_quantity}` : 'หมด' }}
              </div>
            </div>
            <div class="p-5 flex-1 flex flex-col">
              <h3 class="font-black text-gray-900 text-base mb-1.5 line-clamp-1">{{ item.name }}</h3>
              <p class="text-xs text-gray-400 mb-5 flex-1 line-clamp-2 leading-relaxed">
                {{ item.description || 'ไม่มีรายละเอียด' }}
              </p>
              <button
                @click="addToCart(item)"
                :disabled="item.available_quantity <= 0"
                class="w-full py-2.5 rounded-xl font-bold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                :class="item.available_quantity > 0
                  ? 'bg-gradient-to-r from-[#a259ff] to-[#5bc8ff] text-white hover:opacity-90 shadow-md'
                  : 'bg-gray-100 text-gray-400'"
              >
                {{ item.available_quantity > 0 ? '+ เพิ่มลงตะกร้า' : 'ของหมดชั่วคราว' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── RIGHT: Desktop Cart Panel (always visible on lg+) ─── -->
      <div class="hidden lg:block w-[380px] shrink-0 sticky top-6">
        <div class="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden flex flex-col" style="max-height: calc(100vh - 6rem);">
          <!-- Header -->
          <div class="px-5 py-4 border-b border-gray-100 shrink-0">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 bg-[#a259ff]/10 rounded-xl flex items-center justify-center shrink-0">
                <ShoppingCartIcon class="w-5 h-5 text-[#a259ff]" />
              </div>
              <div>
                <h3 class="font-black text-gray-900 text-base leading-tight">ตะกร้ายืมครุภัณฑ์</h3>
                <p class="text-xs text-gray-400 mt-0.5">
                  <template v-if="cart.length > 0">{{ cart.length }} รายการ · {{ totalCartQty }} ชิ้น</template>
                  <template v-else>ยังไม่มีรายการ</template>
                </p>
              </div>
            </div>
          </div>
          <!-- Body -->
          <div class="overflow-y-auto flex-1 px-5 py-4 space-y-3">
            <div v-if="cart.length === 0" class="flex flex-col items-center justify-center py-10 text-gray-300">
              <ShoppingCartIcon class="w-12 h-12 mb-3" />
              <p class="text-sm font-bold text-gray-400">ตะกร้าว่างเปล่า</p>
              <p class="text-xs text-gray-300 mt-1">เลือกอุปกรณ์จากแคตตาล็อกทางซ้าย</p>
            </div>
            <TransitionGroup
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="opacity-0 -translate-x-2"
              enter-to-class="opacity-100 translate-x-0"
              leave-active-class="transition duration-150 ease-in absolute w-full"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0 scale-95"
            >
              <div
                v-for="(cartItem, index) in cart"
                :key="cartItem.equipment.id"
                class="flex items-center gap-3 bg-gray-50 hover:bg-white p-3 rounded-2xl border border-gray-100 hover:border-[#a259ff]/20 hover:shadow-sm transition-all"
              >
                <img :src="cartItem.equipment.image_url" class="w-12 h-12 object-cover rounded-xl shrink-0" />
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-xs text-gray-900 line-clamp-1">{{ cartItem.equipment.name }}</p>
                  <p class="text-[10px] text-gray-400 mt-0.5">คงเหลือ {{ cartItem.equipment.available_quantity }} ชิ้น</p>
                </div>
                <div class="flex items-center bg-white border border-gray-200 rounded-xl overflow-hidden shrink-0">
                  <button @click="updateCartQty(index, -1)" class="w-7 h-7 flex items-center justify-center text-gray-500 hover:bg-gray-100 font-bold transition-colors">−</button>
                  <input v-model.number="cartItem.quantity" @change="validateCartQty(index)" type="number" class="w-9 text-center text-sm font-black outline-none bg-transparent" />
                  <button @click="updateCartQty(index, 1)" class="w-7 h-7 flex items-center justify-center text-gray-500 hover:bg-gray-100 font-bold transition-colors">+</button>
                </div>
                <button @click="removeFromCart(index)" class="p-1.5 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors shrink-0">
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </TransitionGroup>
            <div class="pt-3 border-t border-gray-100">
              <p class="text-[10px] font-black uppercase tracking-wider text-gray-400 mb-3">ข้อมูลผู้ยืม</p>
              <form id="borrow-form-desktop" @submit.prevent="submitBorrowCheckout" class="space-y-2.5">
                <div class="grid grid-cols-2 gap-2.5">
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">ชื่อ-นามสกุล <span class="text-red-500">*</span></label>
                    <input v-model="formData.full_name" type="text" required placeholder="ชื่อ นามสกุล" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">รหัสนักศึกษา <span class="text-red-500">*</span></label>
                    <input v-model="formData.student_id" type="text" required placeholder="6xxxxxxxx" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                </div>
                <div>
                  <label class="block text-[11px] font-bold mb-1 text-gray-500">ช่องทางติดต่อ <span class="text-red-500">*</span></label>
                  <input v-model="formData.contact_info" type="text" required placeholder="เบอร์โทร หรือ Line ID" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                </div>
                <div>
                  <label class="block text-[11px] font-bold mb-1 text-gray-500">สังกัดคณะ/วิทยาลัย/หน่วยงาน <span class="text-red-500">*</span></label>
                  <input v-model="formData.faculty" type="text" required placeholder="เช่น คณะวิศวกรรมศาสตร์" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                </div>
                <div>
                  <label class="block text-[11px] font-bold mb-1 text-gray-500">สถานที่ที่นำไปใช้ <span class="text-red-500">*</span></label>
                  <input v-model="formData.purpose_location" type="text" required placeholder="เช่น ห้องประชุม อาคาร A" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                </div>
                <div class="grid grid-cols-2 gap-2.5">
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">วันที่ยืม <span class="text-red-500">*</span></label>
                    <input v-model="formData.borrow_date" type="date" required class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">วันที่คืน <span class="text-red-500">*</span></label>
                    <input v-model="formData.return_date" type="date" required class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                </div>
              </form>
            </div>
          </div>
          <!-- Footer -->
          <div class="px-5 py-4 border-t border-gray-100 shrink-0">
            <button
              form="borrow-form-desktop"
              type="submit"
              :disabled="isSubmitting || cart.length === 0"
              class="w-full py-3 bg-gray-900 hover:bg-black text-white font-black rounded-xl transition-colors shadow-md disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
            >
              <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              {{ isSubmitting ? 'กำลังดำเนินการ...' : 'ยืนยันการยืม' }}
            </button>
          </div>
        </div>
      </div>

    </div><!-- end main layout -->
  </section>

  <!-- ─── MOBILE: Floating Cart Button ─── -->
  <Teleport to="body">
    <button
      v-if="user && !isCheckingAuth"
      @click="isCartOpen = true"
      class="fixed bottom-6 right-6 z-40 lg:hidden w-14 h-14 bg-gray-900 hover:bg-black text-white rounded-full shadow-xl flex items-center justify-center transition-transform active:scale-95"
    >
      <ShoppingCartIcon class="w-6 h-6" />
      <span
        v-if="cart.length > 0"
        class="absolute -top-1 -right-1 w-5 h-5 bg-[#a259ff] text-white text-[10px] font-black rounded-full flex items-center justify-center leading-none"
      >{{ cart.length }}</span>
    </button>
  </Teleport>

  <!-- ─── MOBILE: Cart Bottom Sheet ─── -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-250 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isCartOpen" class="fixed inset-0 z-50 flex items-end lg:hidden">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="isCartOpen = false" />

        <!-- Sheet -->
        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="translate-y-full"
          enter-to-class="translate-y-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="translate-y-0"
          leave-to-class="translate-y-full"
        >
          <div v-if="isCartOpen" class="relative w-full bg-white rounded-t-3xl shadow-2xl flex flex-col" style="max-height: 88dvh">
            <!-- Drag handle + close -->
            <div class="flex justify-center items-center pt-3 pb-2 shrink-0 relative">
              <div class="w-10 h-1 bg-gray-200 rounded-full" />
              <button
                @click="isCartOpen = false"
                class="absolute right-4 p-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <!-- Header -->
            <div class="px-5 py-3 border-b border-gray-100 shrink-0">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 bg-[#a259ff]/10 rounded-xl flex items-center justify-center shrink-0">
                  <ShoppingCartIcon class="w-5 h-5 text-[#a259ff]" />
                </div>
                <div>
                  <h3 class="font-black text-gray-900 text-base leading-tight">ตะกร้ายืมครุภัณฑ์</h3>
                  <p class="text-xs text-gray-400 mt-0.5">
                    <template v-if="cart.length > 0">{{ cart.length }} รายการ · {{ totalCartQty }} ชิ้น</template>
                    <template v-else>ยังไม่มีรายการ</template>
                  </p>
                </div>
              </div>
            </div>

            <!-- Body -->
            <div class="overflow-y-auto flex-1 px-5 py-4 space-y-3">
              <div v-if="cart.length === 0" class="flex flex-col items-center justify-center py-10 text-gray-300">
                <ShoppingCartIcon class="w-12 h-12 mb-3" />
                <p class="text-sm font-bold text-gray-400">ตะกร้าว่างเปล่า</p>
                <p class="text-xs text-gray-300 mt-1">ปิดแล้วเพิ่มอุปกรณ์จากแคตตาล็อก</p>
              </div>
              <div
                v-for="(cartItem, index) in cart"
                :key="cartItem.equipment.id"
                class="flex items-center gap-3 bg-gray-50 p-3 rounded-2xl border border-gray-100"
              >
                <img :src="cartItem.equipment.image_url" class="w-12 h-12 object-cover rounded-xl shrink-0" />
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-xs text-gray-900 line-clamp-1">{{ cartItem.equipment.name }}</p>
                  <p class="text-[10px] text-gray-400 mt-0.5">คงเหลือ {{ cartItem.equipment.available_quantity }} ชิ้น</p>
                </div>
                <div class="flex items-center bg-white border border-gray-200 rounded-xl overflow-hidden shrink-0">
                  <button @click="updateCartQty(index, -1)" class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-100 font-bold transition-colors">−</button>
                  <input v-model.number="cartItem.quantity" @change="validateCartQty(index)" type="number" class="w-10 text-center text-sm font-black outline-none bg-transparent" />
                  <button @click="updateCartQty(index, 1)" class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-100 font-bold transition-colors">+</button>
                </div>
                <button @click="removeFromCart(index)" class="p-1.5 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors shrink-0">
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>

              <div class="pt-3 border-t border-gray-100">
                <p class="text-[10px] font-black uppercase tracking-wider text-gray-400 mb-3">ข้อมูลผู้ยืม</p>
                <form id="borrow-form-mobile" @submit.prevent="submitBorrowCheckout" class="space-y-2.5">
                  <div class="grid grid-cols-2 gap-2.5">
                    <div>
                      <label class="block text-[11px] font-bold mb-1 text-gray-500">ชื่อ-นามสกุล <span class="text-red-500">*</span></label>
                      <input v-model="formData.full_name" type="text" required placeholder="ชื่อ นามสกุล" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                    </div>
                    <div>
                      <label class="block text-[11px] font-bold mb-1 text-gray-500">รหัสนักศึกษา <span class="text-red-500">*</span></label>
                      <input v-model="formData.student_id" type="text" required placeholder="6xxxxxxxx" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                    </div>
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">ช่องทางติดต่อ <span class="text-red-500">*</span></label>
                    <input v-model="formData.contact_info" type="text" required placeholder="เบอร์โทร หรือ Line ID" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">สังกัดคณะ/วิทยาลัย/หน่วยงาน <span class="text-red-500">*</span></label>
                    <input v-model="formData.faculty" type="text" required placeholder="เช่น คณะวิศวกรรมศาสตร์" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold mb-1 text-gray-500">สถานที่ที่นำไปใช้ <span class="text-red-500">*</span></label>
                    <input v-model="formData.purpose_location" type="text" required placeholder="เช่น ห้องประชุม อาคาร A" class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                  </div>
                  <div class="grid grid-cols-2 gap-2.5">
                    <div>
                      <label class="block text-[11px] font-bold mb-1 text-gray-500">วันที่ยืม <span class="text-red-500">*</span></label>
                      <input v-model="formData.borrow_date" type="date" required class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                    </div>
                    <div>
                      <label class="block text-[11px] font-bold mb-1 text-gray-500">วันที่คืน <span class="text-red-500">*</span></label>
                      <input v-model="formData.return_date" type="date" required class="w-full px-3 py-2 rounded-xl bg-gray-50 border border-gray-200 focus:bg-white focus:ring-2 focus:ring-[#a259ff]/30 focus:border-[#a259ff] outline-none text-xs transition-all" />
                    </div>
                  </div>
                </form>
              </div>
            </div>

            <!-- Footer -->
            <div class="px-5 py-4 border-t border-gray-100 shrink-0">
              <button
                form="borrow-form-mobile"
                type="submit"
                :disabled="isSubmitting || cart.length === 0"
                class="w-full py-3.5 bg-gray-900 hover:bg-black text-white font-black rounded-xl transition-colors shadow-md disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
              >
                <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                {{ isSubmitting ? 'กำลังดำเนินการ...' : 'ยืนยันการยืม' }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from "vue";
import Navbar from "../components/Navbar.vue";
import {
  LockClosedIcon,
  ArchiveBoxIcon,
  ShoppingCartIcon,
  TrashIcon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../composables/useAlert";

const { showAlert } = useAlert();

const user = ref(null);
const equipments = ref([]);
const isCheckingAuth = ref(true);
const isLoading = ref(false);
const isCartOpen = ref(false);

const cart = ref([]);
const isSubmitting = ref(false);
const totalCartQty = computed(() =>
  cart.value.reduce((sum, item) => sum + item.quantity, 0),
);

const formData = reactive({
  full_name: "",
  student_id: "",
  contact_info: "",
  faculty: "",
  purpose_location: "",
  borrow_date: "",
  return_date: "",
});

onMounted(async () => {
  try {
    const res = await fetch("/api/auth/me", { credentials: "include" });
    const json = await res.json();
    user.value = json.user;
    if (user.value) fetchEquipments();
  } catch (error) {
    console.error("Not logged in");
  } finally {
    isCheckingAuth.value = false;
  }
});

const logout = async () => {
  await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
  window.location.reload();
};

const fetchEquipments = async () => {
  isLoading.value = true;
  try {
    const res = await fetch("/api/equipments/central");
    const json = await res.json();
    if (json.status === "success") equipments.value = json.data;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const addToCart = (equipment) => {
  const existing = cart.value.find((item) => item.equipment.id === equipment.id);
  if (existing) {
    if (existing.quantity < equipment.available_quantity) existing.quantity++;
    else showAlert("ไม่สามารถเพิ่มได้เกินจำนวนที่มีในคลัง", "warning");
  } else {
    cart.value.push({ equipment, quantity: 1 });
  }
};

const updateCartQty = (index, amount) => {
  const item = cart.value[index];
  const newQty = item.quantity + amount;
  if (newQty > 0 && newQty <= item.equipment.available_quantity) item.quantity = newQty;
};

const validateCartQty = (index) => {
  const item = cart.value[index];
  if (item.quantity > item.equipment.available_quantity) {
    item.quantity = item.equipment.available_quantity;
    showAlert(`ปรับจำนวนสูงสุดได้ที่ ${item.equipment.available_quantity} ชิ้น`, "warning");
  } else if (item.quantity < 1 || isNaN(item.quantity)) {
    item.quantity = 1;
  }
};

const removeFromCart = (index) => {
  cart.value.splice(index, 1);
};

const submitBorrowCheckout = async () => {
  isSubmitting.value = true;
  try {
    const csrfRes = await fetch("/api/csrf-token", { method: "GET", credentials: "include" });
    const { csrf_token } = await csrfRes.json();

    const res = await fetch("/api/borrow/request", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": csrf_token },
      credentials: "include",
      body: JSON.stringify({
        ...formData,
        items: cart.value.map((item) => ({
          equipment_id: item.equipment.id,
          quantity: item.quantity,
        })),
      }),
    });

    if (res.ok) {
      await showAlert("ส่งคำร้องสำเร็จ! ระบบตัดยอดอุปกรณ์เรียบร้อยแล้ว", "success");
      cart.value = [];
      Object.keys(formData).forEach((key) => (formData[key] = ""));
      isCartOpen.value = false;
      fetchEquipments();
    } else {
      const errorData = await res.json();
      await showAlert(`ผิดพลาด: ${errorData.detail}`, "error");
    }
  } catch (error) {
    await showAlert("เกิดข้อผิดพลาดในการเชื่อมต่อ", "error");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>
