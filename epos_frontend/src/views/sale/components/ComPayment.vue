<template>
    <ComModal :fullscreen="true" :persistent="true" @onClose="onClose" :hide-close-button="true" :hide-ok-button="true"
        :fill="true" contentClass="h-full">
        <template #title>
            {{ $t('Payment') }}
        </template>
        <template #bar_custom>

            <ComSelectPaymentPrinter @onClick="onSelectedReceipt" :selected="selectedReceipt.name" v-if="mobile" />
        </template>
        <template #content>
            <div v-if="mobile" class="!p-1 overflow-auto">
                <ComSmallSalePayment />
            </div>
            <div v-else class="!px-0 !pt-1 !pb-0 overflow-hidden h-full">
                <v-row class="!m-0 h-full">
                    <v-col class="!p-1 h-full" md="4">
                        <ComPaymentInputNumber />
                    </v-col>
                    <v-col class="!p-1 h-full" md="4">
                        <div class="overflow-auto h-full">
                            
                            <ComSalePaymentMethodList />
                        </div>
                    </v-col>
                    <v-col class="!p-0 h-full" md="4">
                        <div class="bg-gray-100 p-1 h-full">
                            <div class="grid h-full" style="grid-template-rows: max-content;">
                                <ComSalePaymentGrandTotalInformation />
                                <div class="overflow-auto h-full">
                                    <ComSalePaymentList />
                                </div>
                                <ComPaymentSummaryInformation />
                            </div>
                        </div>
                    </v-col>
                </v-row>
            </div>
        </template>
        <template #action>
            <v-row class="!m-0">
                <v-col class="!p-0" cols="12" md="4">
                   
                </v-col> 
                <v-col class="!p-0" cols="12" md="4">
                    <div v-if="gv.setting.show_button_tip==1" class="border rounded-sm px-2 py-4 text-center cursor-pointer bg-orange-100 hover:bg-orange-300 flex justify-center items-center m-1" @click="onTipPressed">
                      
                            <span v-if="((sale.sale.tip_amount||0)<=0)">{{ $t('TIP') }}</span>
                            <span v-else>{{ $t('Remove TIP') }}</span>
                        
                    </div>
                </v-col>

                <v-col class="!p-0" cols="12" md="4">
                    <v-row class="!m-0">
                        <v-col class="!p-0" cols="6">
                            <div class="p-1" >
                                <v-btn size="small" class="w-full" color="primary" @click="onPayment" stacked
                                    prepend-icon="mdi-printer">
                                    <span>{{ $t('Payment with Print') }}</span>
                                </v-btn>
                            </div>
                        </v-col>
                        <v-col class="!p-0" cols="6">
                            <div class="p-1">
                                <v-btn size="small" class="w-full" color="primary" @click="onPaymentWithoutPrint" stacked
                                    prepend-icon="mdi-currency-usd">{{ $t('Payment') }}</v-btn>

                            </div>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </template>
    </ComModal>
</template>
<script setup>

import { inject, ref, onUnmounted,onMounted,i18n } from '@/plugin';
import ComPaymentInputNumber from "./ComPaymentInputNumber.vue"
import ComSmallSalePayment from "./mobile_screen/ComSmallSalePayment.vue"
import { useDisplay } from 'vuetify'
import ComSalePaymentMethodList from './ComSalePaymentMethodList.vue';
import ComSalePaymentGrandTotalInformation from './ComSalePaymentGrandTotalInformation.vue';
import ComSalePaymentList from './ComSalePaymentList.vue';
import ComSelectPaymentPrinter from './ComSelectPaymentPrinter.vue';
import ComPaymentSummaryInformation from './ComPaymentSummaryInformation.vue';
import { createToaster } from '@meforma/vue-toaster';
onMounted(()=> {
    sale.is_payment_first_load = true;
    backup.value = JSON.parse(JSON.stringify(sale.sale));
    document.addEventListener('keydown', OnKeyDown)
})

const { t: $t } = i18n.global;  

const { mobile } = useDisplay()

const sale = inject("$sale")
const gv = inject("$gv")

const emit = defineEmits(['resolve'])
const toaster = createToaster({ position: "top" })
const props = defineProps({
    params: Object
})
async function onPaymentTypeClick(pt) { 
    let room = null;
    let folio_transaction_number = null
    let folio_transaction_type=null
    let folio = null
    let city_ledger_name = null
    let desk_folio = null
    if(pt.payment_type_group=="Pay to Room" ){ 
        if(sale.paymentInputNumber<=0){
            toaster.warning($t("msg.Please enter payment amount"));
            return
        }

        const result = await payToRoomDialog({
            data : pt
        });

        //
        if(result == false){
            return
        }
        room = result.room;
        folio = result.folio;
        folio_transaction_number =result.folio;
        folio_transaction_type="Reservation Folio"
        sale.sale.customer = result.guest
        sale.sale.customer_name = result.guest_name
    }
    else if(pt.payment_type_group == "City Ledger"){
        const result = await payToCityLedgerDialog({
            data : pt
        });
        //if close
        if(result == false){
            return
        }
         
        folio_transaction_number =result.folio_transaction_number;
        folio_transaction_type="City Ledger"
        city_ledger_name = result.city_ledger_name
    }
    else if(pt.payment_type_group == "Desk Folio"){
        const result = await payDeskfolioDialog({
            data : pt
        });
        //if close
        if(result == false){
            return
        }
         
        folio_transaction_number =result.folio_transaction_number;
        folio_transaction_type="Desk Folio"
        desk_folio = result.desk_folio
    }


    //check if payment exist manual fee

    let fee_amount = 0;
    if(pt.is_manual_fee==1){
        const fee = await keyboardDialog({ title:$t("Enter Fee Amount"), type: 'number', value: 0 });
        if(!fee){
            return;
        }      
        fee_amount = fee;
    }

    if(mobile.value){
        sale.is_payment_first_load = false;
    }  

    if(pt.allow_change==0 &&  parseFloat(sale.paymentInputNumber) > parseFloat(balance.value * pt.exchange_rate)){
        sale.paymentInputNumber = balance.value *  pt.exchange_rate;
        
    }
    else  if(sale.is_payment_first_load){       
        sale.paymentInputNumber = sale.paymentInputNumber * pt.exchange_rate;       
    }

  
    const payment_obj={paymentType: pt, amount:sale.paymentInputNumber,fee_amount:fee_amount,room:room, folio : folio, folio_transaction_type:folio_transaction_type,folio_transaction_number:folio_transaction_number,city_ledger_name:city_ledger_name}  
    // sale.onAddPayment(pt, sale.paymentInputNumber,fee_amount,room,folio,folio_transaction_type,folio_transaction_number);   
    sale.onAddPayment(payment_obj);

}

let backup = ref({})
const selectedReceipt = ref({})
selectedReceipt.value = gv.setting.default_pos_receipt;
sale.paymentInputNumber = ((sale.sale?.grand_total||0) - (sale.sale?.deposit||0)).toFixed(sale.setting.pos_setting.main_currency_precision);

function onSelectedReceipt(r) {
    selectedReceipt.value = r;
}

function OnKeyDown(e){
    if (e.key == "Enter") 
    {
        if(sale.keycount==0){
            let default_payment = gv.setting?.payment_types.filter(r => r.is_default == 1)
            onPaymentTypeClick(default_payment[0])
        }
        else{
            document.removeEventListener('keydown', OnKeyDown)
            onPayment()
        }
        sale.keycount++
    }
}

function onClose() {    
    sale.sale.total_paid = backup.value.total_paid;
    sale.sale.balance = backup.value.balance;
    sale.sale.changed_amount = backup.value.changed_amount;
    sale.sale.second_changed_amount = backup.value.second_changed_amount;
    sale.sale.tip_amount = 0;
    sale.sale.tip_account_code = "";
    sale.sale.payment =  backup.value.payment;
    sale.sale.sale_status = backup.value.sale_status;
    sale.sale.docstatus = backup.value.docstatus;

    emit("resolve", false);
}

async function onPayment() { 
    if (sale.sale.payment.filter(r => r.required_customer == 1).length > 0) {
        if (sale.sale.customer == sale.setting.customer) {
            toaster.warning($t("msg.Please select customer for payment type")+" " + sale.sale.payment.filter(r => r.required_customer == 1)[0].payment_type);
            return;
        }
    }
    sale.pos_receipt = selectedReceipt.value;
    sale.message = $t("msg.Payment successfully");

    onPaymentAudit()  ;

    sale.onSubmitPayment(true).then((v) => {
        if (v) {            
            emit("resolve", true);
        }
        else{
            document.addEventListener('keydown', OnKeyDown)
        }
    })
}

function onTipPressed(){ 
    if((sale.sale.tip_amount||0)>0){
        sale.sale.tip_amount = 0;
        sale.sale.tip_account_code = "";
    }else{
        if(parseFloat(sale.paymentInputNumber)>0){
            sale.sale.tip_amount = parseFloat(sale.paymentInputNumber);
            sale.sale.tip_account_code = gv.setting.tip_account_code;
        }   
        else{
            toaster.warning($t('msg.Please input amount for TIP'));
        }  
    }
}

async function onPaymentWithoutPrint() {
    if (sale.sale.payment.filter(r => r.required_customer == 1).length > 0) {
        if (sale.sale.customer == sale.setting.customer) {

            toaster.warning($t('msg.Please select customer for payment type')+" " + sale.sale.payment.filter(r => r.required_customer == 1)[0].payment_type);
            return;
        }
    }
    sale.pos_receipt = undefined;
    sale.message = $t("msg.Payment successfully");

    onPaymentAudit();
   
    sale.onSubmitPayment(false).then((v) => {
        if (v) {
            emit("resolve", true);
        }
    })
}

function onPaymentAudit(){
    const u = JSON.parse(localStorage.getItem('make_order_auth')); 
    let msg = `${u.name} process payment `; 
    let _payment_type ="";
    sale.sale.payment.forEach(sp => {
        _payment_type += `${sp.payment_type }: ${sp.input_amount}\n`
    });
    
    msg += `Payment Types: ${_payment_type}`
    sale.auditTrailLogs.push({
        doctype:"Comment",
        subject:"Payment",
        comment_type:"Info",
        reference_doctype:"Sale",
        reference_name:"New",
        comment_by:u.name,
        content:msg,
        custom_item_description: "",
        custom_note:"",
        custom_amount: ((sale.sale.total_paid ||0) - (sale.sale.changed_amount||0))
    });  

}

onUnmounted(() => {
    sale.sale.payment = [];
    sale.is_payment_first_load = false;
    sale.keycount = 0;
    document.removeEventListener('keydown', OnKeyDown)
})

</script>