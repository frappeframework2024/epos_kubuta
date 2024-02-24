<template>
    <ComModal @onClose="onClose" :mobileFullscreen="true" @onOk="onSave" width="960px">
        <template #title>
            {{ $t("Payments") }}: {{ params.title }} (<CurrencyFormat v-if="voucherTopup.actual_amount>0" :value="Number(voucherTopup.actual_amount)" />)
        </template>
        <template #content>
            <div class="d-flex justify-space-between m-1 align-center">
                <p class="font-weight-bold py2">
                    {{ $t('Payments') }}
                </p>
                <v-btn v-if="voucherTopup.docstatus==0" size="small" @click="addPayment" prepend-icon="mdi-plus" color="success" class="">
                    {{ $t("Add Payment") }}
                </v-btn>
            </div>
            <template v-if="voucherTopup">
                
                    <div>
                        <v-table>
                            <thead>
                                <tr>
                                    <th class="text-center">{{ $t("Posting Date") }}</th>
                                    <th>{{ $t("Reference Number") }}</th>
                                    <th>{{ $t("Payment Type") }}</th>
                                    <th class="text-right">{{ $t("Payment Amount") }}</th>
                                    <th class="text-right">{{ $t("Action") }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template  v-if="payments.length > 0">
                                    <tr v-for="payment in payments">
                                    <td class="text-center">{{ moment(payment.posting_date).format("DD-MM-YYYY") }}</td>
                                    <td>
                                        <ComInput :readonly="voucherTopup.docstatus==1" v-model="payment.reference_no" :label="$t('Reference No')" />
                                    </td>
                                    <td >
                                        <ComAutoComplete :label="$t('Payment Type')" v-model="payment.payment_type"
                                            :placeholder="$t('Payment Type')" doctype="Payment Type" variant="solo" />
                                    </td>
                                    <td class="text-right">
                                        <ComInput :readonly="voucherTopup.docstatus==1" type="number" v-model="payment.input_amount" :label="$t('Payment Amount')" />
                                        
                                    </td>
                                    <td >
                                        <v-btn v-if="voucherTopup.docstatus==0" icon="mdi-delete" size="small" color="error" variant="text" type="button" @click="deletePayment(payment)"/>
                                    </td>
                                </tr>
                                </template>
                                <template v-else>
                                    <tr>
                                        <td colspan="5" class="text-center">
                                            <p class="font-weight-bold pt-6 pb-2 text-disabled">
                                            {{ $t('Empty') }}
                                        </p>
                                        </td>
                                    </tr>
                                </template>
                                
                            </tbody>
                        </v-table>
                    </div>
                
            </template>


        </template>
    </ComModal>
</template>

<script setup>
import { ref, inject, i18n } from '@/plugin'
import { createToaster } from "@meforma/vue-toaster";
import ComInput from '../../components/form/ComInput.vue';
const moment = inject('$moment')
const toaster = createToaster({position:'top'});
const { t: $t } = i18n.global;
const gv = inject('$gv')
const frappe = inject('$frappe')
const props = defineProps({
    params: {
        type: Object,
        required: true,
    },
})
const emit = defineEmits(["resolve"])
let payments = ref([])
let voucherTopup = ref(props.params.topup)


if (voucherTopup?.value?.payments?.length > 0){
    payments.value=voucherTopup.value.payments
}

if (!payments.value){
    payments.value=[]
}





function addPayment() {
    payments.value.push({
        'doctype': 'POS Voucher Payment',
        'posting_date': voucherTopup.value.posting_date,
        'parent':voucherTopup.value.name,
        'parenttype':'Voucher',
        'parentfield':'payments'
    })
}

function deletePayment(payment){
    payments.value = payments.value.filter(obj => obj !== payment);
}

function onSave() {
    
    let totalPaid = payments.value.reduce((n, d) => n + (d.payment_amount || 0), 0)
    emit('resolve', payments.value);
}

function onClose() {
    emit('resolve', payments.value);
}

</script>

