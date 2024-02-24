<template>
    <PageLayout :title="$t('Voucher Top-Up')" icon="mdi-wallet-plus" full>
        <template #action>
            <v-btn  prepend-icon="mdi-wallet-plus" type="button" @click="onAddVoucherTopUp">
              {{ $t("Add Top-Up") }}
            </v-btn>
        </template>
        <ComTable :headers="headers" doctype="Voucher" @callback="onCallback" />
  </PageLayout>
</template>
<script setup>
import { ref, AddVoucherTopUpDialog,VoucherTopUpDetailDialog,i18n,inject } from '@/plugin'
import PageLayout from '@/components/layout/PageLayout.vue';
import ComVoucherCard from './ComVoucherCard.vue'
import ComTable from '@/components/table/ComTable.vue';
import {useDisplay} from 'vuetify';

const { t: $t } = i18n.global; 
const gv = inject("$gv")
const {mobile} = useDisplay()
async function onAddVoucherTopUp() {
    
    gv.authorize("add_voucher_top_up_required_password","add_voucher_top_up").then(async (v)=>{
        if(v){
            console.log(v)
            const result = await AddVoucherTopUpDialog ({title: $t("Add New"), value:  '',authUser:v});   
            if (result == true){
                onCallback()
            }
        }
    })
    
}


async function onCallback(data) { 
        const result = await VoucherTopUpDetailDialog({
            name: data.data.name
        });
        
    
}

const headers = ref([
    { title: $t('Voucher'), align: 'start', key: 'name', callback: true },
    { title: $t('Customer'), align: 'start', key: 'customer' },
    { title: $t('Customer Name'), align: 'start', key: 'customer_name' },
    { title: $t('Phone'), align: 'start', key: 'phone'},
    { title: $t('Amount'),fieldtype : 'Currency', align: 'end', key: 'actual_amount'},
    { title: $t('Credit Amount'),fieldtype : 'Currency' ,align: 'end', key: 'credit_amount'},
    { title: $t('Balance'), fieldtype : 'Currency',align: 'end', key: 'balance'}
])

 

</script>