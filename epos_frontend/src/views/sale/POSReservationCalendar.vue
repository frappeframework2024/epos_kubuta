<template>
     <PageLayout full :title="$t('POS Reservation Calendar')" icon="mdi-calendar-clock-outline" class="p-3">
      <FullCalendar :options="options"/>
    </PageLayout>
</template>
  <script setup>
  
  import '@fullcalendar/core/vdom' 
  import FullCalendar from '@fullcalendar/vue3'
  import dayGridPlugin from '@fullcalendar/daygrid'
  import interactionPlugin from '@fullcalendar/interaction'
  import PageLayout from '../../components/layout/PageLayout.vue';
  import { useRouter, defineProps, defineEmits, ref, inject, createToaster,posReservationCalendarDialog,i18n,onMounted } from "@/plugin"
  import { useDisplay } from 'vuetify';  
  import moment from '@/utils/moment.js';
  


  const { t: $t } = i18n.global;  
  const { mobile } = useDisplay();

  const isLoading = ref(true);
  const reservationData = ref([]); 

  const frappe = inject("$frappe");
  const emit = defineEmits(["resolve"])
  const events = ref([])

  const db = frappe.db();
  const call = frappe.call();
  
  const options = ref({
      timeZone: 'UTC',
      plugins:[dayGridPlugin,interactionPlugin ],
        initialView: 'dayGridMonth',

        eventSources: [
          {
            url: '/api/method/epos_restaurant_2023.api.api.get_resevation_calendar',
            method: 'GET',
            extraParams: {
              business_branch: 'ESTC HOTEL',
            },
            
          },
         
        ],
        eventSourceSuccess: function (content, response) {
              return content.message;

            },
            eventClick:async function(info) {
              const data = info.event._def.extendedProps;
              posReservationCalendarDialog({
                name: data.name
              });
            }
    })
  
   



  </script>