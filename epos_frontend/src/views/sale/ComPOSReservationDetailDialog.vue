<template>
  <ComModal :mobileFullscreen="true" @onClose="onClose()" width="1200px" :hideOkButton="true">
    <template #title>
      {{ $t('Reservation') }}
      <span v-if="reservationDetail">
        {{ reservationDetail.name }}
        <v-chip class="ma-2" label variant="flat" :color="reservationDetail.reservation_status_background_color">
          {{ reservationDetail.reservation_status }}
        </v-chip>
      </span>
    </template>
    <template #content>
      <ComPlaceholder :loading="isLoading" :is-not-empty="reservationDetail" :text="$t('Empty Data')"
        icon="mdi-note-outline">
        <v-row class="!m-0">
          <v-col class="!p-0 border-b" cols="12" md="12">
            <v-card elevation="0" rounded="0">
              <template v-slot:prepend>

              </template>
              <table class="w-full" border="1">
                <tbody>
                  <tr>
                    <th class="text-left">{{ $t('Date') }}</th>
                    <td class="font-weight-black">{{ arrivalDate }}</td>
                    <th class="text-left">{{ $t('Guest') }}</th>
                    <td>{{ `${reservationDetail.guest}-${reservationDetail.guest_name}` }}</td>

                  </tr>
                  <tr>
                    <th class="text-left" v-if="reservationDetail.table_number">{{ $t('Table') }}</th>
                    <td v-if="reservationDetail.table_number">{{ reservationDetail.table_number }}</td>
                    <template v-if="reservationDetail.phone_number">
                      <th class="text-left">{{ $t('Phone') }}</th>
                      <td>{{ reservationDetail.phone_number }}</td>
                    </template>
                  </tr>
                  <tr>
                    <th class="text-left">{{ $t('Total Amount') }}</th>
                    <td>
                      <CurrencyFormat :value="reservationDetail.total_amount" />
                    </td>


                  </tr>
                  <tr v-if="reservationDetail.total_deposit > 0">
                    <th class="text-left">{{ $t('Total Deposit') }}</th>
                    <td>
                      <CurrencyFormat :value="reservationDetail.total_deposit" />
                    </td>

                  </tr>
                </tbody>
              </table>
              <div class="v-table__wrapper mt-6">
               
                <table class="w-full" border="1">

                  <thead>
                    <tr>
                      <th class="text-left py-2">{{ $t('Item') }}</th>
                      <th class="text-center py-2">{{ $t('QTY') }}</th>
                      <th class="text-right py-2">{{ $t('Price') }}</th>
                      <th class="text-right py-2">{{ $t('Amount') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr   v-for="product in reservationDetail.reservation_product">
                      <td class="text-left py-2">
                        {{ `${product.product_code}-${product.product_name}` }}
                      </td>
                      <td class="text-center py-2">
                        <CurrencyFormat :value="product.quantity" />

                      </td>
                      <td class="text-right py-2">
                        <CurrencyFormat :value="product.price" />

                      </td>
                      <td class="text-right py-2">
                        <CurrencyFormat :value="product.total_amount" />
                      </td>
                    </tr>

                  </tbody>
                </table>
              </div>
            </v-card>
            <!-- <CurrencyFormat :value="p.input_amount" :currency="{precision:p.currency_precision, pos_currency_format:p.pos_currency_format}" /> -->
          </v-col>
        </v-row>
      </ComPlaceholder>
    </template>
  </ComModal>
</template>
<script setup>
import { useRouter, defineProps, defineEmits, ref, inject, createToaster, i18n, onMounted, computed } from "@/plugin"
import ComModal from "../../components/ComModal.vue";
import ComPlaceholder from "../../components/layout/components/ComPlaceholder.vue";
import { useDisplay } from 'vuetify';
const moment = inject("$moment")

const { t: $t } = i18n.global;
const { mobile } = useDisplay();

const isLoading = ref(true);

const frappe = inject("$frappe");
const emit = defineEmits(["resolve"])
const gv = inject('$gv');
const toaster = createToaster({ position: "top" });

const db = frappe.db();
const call = frappe.call();

const props = defineProps({
  params: {
    type: Object,
    required: true,
  }
})
let reservationDetail = ref(null)
let reservationPaymentList = ref(null)
const reservationName = ref(props.params.name)

onMounted(() => {
  _onInit()
});

function _onInit() {
  isLoading.value = true;
  call.get("epos_restaurant_2023.api.api.get_resevation_detail", { name: reservationName.value }).then((res) => {
    reservationDetail.value = res.message.reservation
    reservationPaymentList.value = res.message.payment
    isLoading.value = false;
  }).catch((err) => {
    isLoading.value = false;
  });
}

const arrivalDate = computed(() => {
  if (reservationDetail) {
    return moment(`${reservationDetail.value.arrival_date} ${reservationDetail.value.arrival_time}`, "YYYY-MM-DD HH:mm:ss").format("YYYY-MM-DD HH:mm:ss");
  } else {
    return ""
  }

});

function onClose() {
  emit('resolve', false);
}
</script>