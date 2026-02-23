<template>
  <q-page class="page-root q-px-md q-pt-xl q-pb-xl">
    <div class="content-layer">
      <!-- Header -->
      <div class="row justify-between items-center q-mb-xl animate-in">
        <div>
          <div class="section-label q-mb-sm">{{ $t('prof_support') }}</div>
          <h1 class="font-display" style="font-size: 2.8rem; color: var(--text-primary); margin: 0">
            Therapy <span class="text-gradient">{{ $t('book') }}</span>
          </h1>
        </div>
        <button class="icon-btn" @click="$router.back()">
          <q-icon name="arrow_back" size="20px" />
        </button>
      </div>

      <!-- Search & Filter -->
      <div class="row q-gutter-sm q-mb-lg animate-in delay-1">
        <div
          class="col aura-input q-px-md row items-center"
          style="height: 52px; border-radius: 100px"
        >
          <q-icon name="search" size="20px" color="primary" class="q-mr-sm" />
          <input
            v-model="searchQuery"
            :placeholder="$t('search_therapist')"
            style="
              background: transparent;
              border: none;
              outline: none;
              color: var(--text-primary);
              font-family: 'Plus Jakarta Sans', sans-serif;
              width: 100%;
              font-size: 0.95rem;
            "
          />
        </div>
        <button
          class="icon-btn"
          style="width: 52px; height: 52px; border-radius: 50%"
          @click="filterDialog = true"
        >
          <q-icon name="tune" size="20px" />
        </button>
      </div>

      <!-- Categories -->
      <div class="row q-gutter-sm q-mb-xl no-wrap overflow-hidden" style="overflow-x: auto">
        <button
          v-for="cat in categories"
          :key="cat"
          class="chip animate-in delay-2"
          :class="{ active: currentCategory === cat }"
          @click="currentCategory = cat"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Therapist List -->
      <div class="section-label q-mb-md animate-in delay-3">{{ $t('available_specialists') }}</div>

      <div class="row q-gutter-md q-mb-xl">
        <div
          v-for="(t, i) in filteredTherapists"
          :key="t.name"
          class="glass-card col-12 row items-center q-gutter-md q-pa-md list-item"
          :style="{ animationDelay: `${i * 0.1 + 0.4}s` }"
        >
          <img :src="t.avatar" class="t-avatar" :alt="t.name" />
          <div class="col">
            <div class="font-heading" style="font-size: 1.1rem; color: var(--text-primary)">
              {{ t.name }}
              <span style="font-size: 0.8rem; color: var(--indigo-light); font-weight: 600">{{
                t.credentials
              }}</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin: 4px 0">
              {{ t.specialty }}
            </div>
            <div class="row q-gutter-xs items-center">
              <span class="badge-indigo" style="font-size: 0.6rem; padding: 2px 6px"
                >⭐ {{ t.rating }}</span
              >
              <span class="text-caption" style="text-transform: none"
                >{{ t.reviews }} {{ $t('reviews') }}</span
              >
            </div>
          </div>
          <div class="column justify-between items-end q-gutter-sm">
            <div class="font-heading" style="color: var(--mint); font-size: 1rem">
              ${{ t.rate }}/hr
            </div>
            <button
              class="btn-primary"
              style="padding: 10px 20px; font-size: 0.8rem"
              @click="book(t)"
            >
              {{ $t('book') }}
            </button>
          </div>
        </div>
        <div v-if="!filteredTherapists.length" class="text-center col-12 q-py-xl">
          <q-icon name="search_off" size="40px" color="grey-7" class="q-mb-sm" />
          <div class="text-secondary font-heading">{{ $t('no_therapists') }}</div>
        </div>
      </div>
    </div>

    <!-- Booking Dialog -->
    <q-dialog v-model="bookingDialog">
      <q-card class="q-pa-xl" style="width: 100%; max-width: 440px">
        <div class="row items-center q-mb-lg q-gutter-md">
          <img
            :src="selectedTherapist?.avatar"
            class="t-avatar"
            style="width: 56px; height: 56px"
          />
          <div>
            <div class="font-heading" style="font-size: 1.2rem">
              {{ $t('book_with') }} {{ selectedTherapist?.name }}
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary)">
              {{ selectedTherapist?.specialty }}
            </div>
          </div>
        </div>

        <div class="q-mb-md">
          <div class="text-caption q-mb-xs">{{ $t('select_date') }}</div>
          <q-input outlined v-model="bookingDate" type="date" dense />
        </div>
        <div class="q-mb-xl">
          <div class="text-caption q-mb-xs">{{ $t('select_time') }}</div>
          <q-select
            outlined
            v-model="bookingTime"
            :options="['09:00 AM', '11:00 AM', '02:00 PM', '04:30 PM']"
            dense
          />
        </div>

        <div class="row q-gutter-sm">
          <button class="btn-ghost col" @click="bookingDialog = false">{{ $t('cancel') }}</button>
          <button class="btn-mint col" @click="confirmBooking">
            {{ $t('confirm_booking_btn') }}
          </button>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useQuasar } from 'quasar'

const { t } = useI18n()
const $q = useQuasar()
const searchQuery = ref('')
const currentCategory = ref('All')
const bookingDialog = ref(false)
const filterDialog = ref(false)
const selectedTherapist = ref(null)
const bookingDate = ref('')
const bookingTime = ref('')

const categories = ['All', 'Anxiety', 'Depression', 'Trauma', 'Couples', 'Youth']

const therapists = ref([
  {
    name: 'Dr. Sarah Jenkins',
    credentials: 'PhD, PsyD',
    specialty: 'Cognitive Behavioral Therapy (CBT) · Anxiety',
    rating: '4.9',
    reviews: 128,
    rate: 120,
    avatar: 'https://i.pravatar.cc/150?u=a042581f4e29026024d',
  },
  {
    name: 'Mark Davis',
    credentials: 'LCSW',
    specialty: 'Trauma Counseling · EMDR',
    rating: '4.8',
    reviews: 95,
    rate: 90,
    avatar: 'https://i.pravatar.cc/150?u=a042581f4e29026704d',
  },
  {
    name: 'Dr. Liyana Sen',
    credentials: 'MD, Psychiatry',
    specialty: 'Depression · Medication Management',
    rating: '5.0',
    reviews: 210,
    rate: 180,
    avatar: 'https://i.pravatar.cc/150?u=a04258114e29026702d',
  },
  {
    name: 'James Wilson',
    credentials: 'MFT',
    specialty: 'Couples & Family Therapy',
    rating: '4.7',
    reviews: 64,
    rate: 110,
    avatar: 'https://i.pravatar.cc/150?u=a048581f4e29026701d',
  },
])

const filteredTherapists = computed(() => {
  return therapists.value.filter((t) => {
    const matchSearch =
      t.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      t.specialty.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCat = currentCategory.value === 'All' || t.specialty.includes(currentCategory.value)
    return matchSearch && matchCat
  })
})

function book(t) {
  selectedTherapist.value = t
  bookingDialog.value = true
}

function confirmBooking() {
  if (!bookingDate.value || !bookingTime.value) {
    $q.notify({ message: t('select_datetime'), color: 'negative', position: 'top' })
    return
  }
  $q.notify({
    message: t('session_booked', {
      name: selectedTherapist.value.name,
      date: bookingDate.value,
      time: bookingTime.value,
    }),
    color: 'positive',
    position: 'top',
    icon: 'check_circle',
  })
  bookingDialog.value = false
  bookingDate.value = ''
  bookingTime.value = ''
}
</script>

<style scoped>
.t-avatar {
  width: 72px;
  height: 72px;
  border-radius: var(--r-md);
  object-fit: cover;
  border: 2px solid var(--indigo);
  padding: 2px;
  background: var(--bg-elevated);
}

.list-item {
  animation: fade-in-up 0.5s var(--ease-out) both;
  cursor: default;
}
.list-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--indigo);
}
</style>
