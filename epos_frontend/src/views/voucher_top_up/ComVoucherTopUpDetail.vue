<template>
    <ComModal @onClose="onClose" :mobileFullscreen="true" hideOkButton>
        <template #title>
            {{ voucherTopUp.customer }} - {{ voucherTopUp.customer_name }}
           
        </template>
        <template #content>
            <div  v-if="voucherTopUp">
                <div>
                <v-table>
                    <tr>
                        <th class="text-left">ID</th>
                        <td>{{ voucherTopUp.name }}</td>
                        <th class="text-left">{{ $t("Actual Amount") }}</th>
                        <td>
                            <CurrencyFormat :value="voucherTopUp.actual_amount" />
                        </td>
                    </tr>
                    <tr>
                        <th class="text-left">{{ $t("Posting Date") }}</th>
                        <td>{{ moment(voucherTopUp.posting_date).format("DD-MM-YYYY") }}</td>
                        <th class="text-left">{{ $t("Credit Amount") }}</th>
                        <td>
                            <CurrencyFormat :value="voucherTopUp.credit_amount" />
                        </td>
                    </tr>
                    <tr>
                        <th class="text-left">{{ $t("Customer") }}</th>
                        <td>{{ voucherTopUp.customer }} - {{ voucherTopUp.customer_name }}</td>
                        <th class="text-left">{{ $t("Balance") }}</th>
                        <td>
                            <CurrencyFormat :value="voucherTopUp.balance" />
                        </td>
                    </tr>
                    <tr>
                        <th class="text-left">{{ $t("Phone") }}</th>
                        <td>{{ voucherTopUp.phone }}</td>
                        <th class="text-left">{{ $t("Status") }}</th>
                        <td>
                            <v-chip v-if="voucherTopUp.docstatus == 1" color="success" density="comfortable" size="small">
                                {{ $t("Submitted") }}
                            </v-chip>
                            <v-chip v-if="voucherTopUp.docstatus == 0" color="warning" density="comfortable" size="small">
                                {{ $t("Draft") }}
                            </v-chip>
                        </td>
                    </tr>
                </v-table>
            </div>
            <div v-if="voucherTopUp?.payments?.length > 0">
                <p class="font-weight-bold pt-6 pb-2">
                    {{ $t('Payments') }}
                </p>
                <div>
                    <v-table>
                        <thead>
                            <tr>
                                <th class="text-center">{{ $t("Posting Date") }}</th>
                                <th>{{ $t("Reference Number") }}</th>
                                <th>{{ $t("Payment Type") }}</th>
                                <th class="text-right">{{ $t("Payment Amount") }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="payment in voucherTopUp.payments">
                                <td class="text-center">{{ moment(payment.posting_date).format("DD-MM-YYYY") }}</td>
                                <td>{{ payment.reference_no }}</td>
                                <td>{{ payment.payment_type }}</td>
                                <td class="text-right"><CurrencyFormat :value="payment.payment_amount" /></td>
                            </tr>
                        </tbody>
                    </v-table>
                </div>
            </div>
            </div>
           
        </template>
    </ComModal>
</template>

<script setup>
import { ref, inject, onMounted, i18n } from '@/plugin'
import { createToaster } from "@meforma/vue-toaster";
import ComModal from '../../components/ComModal.vue';
const moment = inject('$moment')

const { t: $t } = i18n.global;
const frappe = inject('$frappe')
const db = frappe.db();
const call = frappe.call();

const props = defineProps({
    params: {
        type: Object,
        required: true,
    },
})

const emit = defineEmits(["resolve"])

const voucherTopUp = ref({})
let loading = ref(false)

onMounted(async () => {
    db.getDoc('Voucher', props.params.name).then((result) => {
        voucherTopUp.value = result
    loading.value = false;
});
   
    
})


function onClose() {
    emit('resolve', false);
}

</script>

