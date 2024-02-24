<template>
    <div class="grid gap-1" :class="mobile ? 'grid-cols-3 text-sm' : 'grid-cols-2'">
        <div class="border rounded-sm px-2 py-4 text-center cursor-pointer bg-orange-100 hover:bg-orange-300 flex justify-center items-center"
            v-for="(pt, index) in gv.setting?.payment_types" :key="index"
            @click="onPaymentTypeClick(pt)">
            <div>
                {{ pt.payment_method }} 
            </div>
        </div>
    </div>
</template>
<script setup>
import { inject , payToRoomDialog,createToaster,payToCityLedgerDialog,payDeskfolioDialog,i18n ,computed,keyboardDialog} from '@/plugin';
import { useDisplay } from 'vuetify'
const {mobile} = useDisplay()
const gv = inject("$gv")
const sale = inject("$sale")
const { t: $t } = i18n.global;  
const toaster = createToaster({ position: "top" });

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

const balance = computed(()=>{
    if(sale.sale?.balance>0){ 
        return Number(sale.sale.balance.toFixed(gv.setting.pos_setting.main_currency_precision));
    }else {
        return 0;
    }
})

 


</script>