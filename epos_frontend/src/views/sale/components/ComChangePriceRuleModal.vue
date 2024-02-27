<template>
    <ComModal @onClose="onClose()" :hide-ok-button="true" width="350px">
        <template #title>
            <div>{{ $t('Change Price Rule') }}</div>
        </template>
        <template #content>
            <ComPlaceholder :is-not-empty="price_rules.length > 0">
                <v-list class="!p-0">
                    <v-list-item v-for="(item, index) in price_rules" :key="index" class="!p-0">
                        <v-btn class="w-full" color="primary"
                            @click="onSelect(item.price_rule)">
                           {{ item.price_rule }}
                        </v-btn>
                    </v-list-item>
                </v-list>
            </ComPlaceholder>
        </template>
    </ComModal>
</template>
<script setup>
import { defineEmits, inject, confirm,i18n } from '@/plugin'
import ComPlaceholder from '../../../components/layout/components/ComPlaceholder.vue';
import { FrappeApp } from 'frappe-js-sdk';
const gv = inject("$gv");
const frappe = new FrappeApp();
const call = frappe.call();
const { t: $t } = i18n.global;  

const emit = defineEmits(['resolve'])
const props = defineProps({
    params: Object
})

const sale = inject('$sale')
const product = inject('$product')
const price_rules = JSON.parse(localStorage.getItem('setting')).price_rules;

function onClose() {
    emit('resolve', false)
}

async function onSelect(result) {
    if (sale.sale.sale_products.length > 0) {
        const yesNo = await confirm({ title: $t('msg.are you sure to change price rule'), text: $t('msg.All items will be remove from bill') })
        if (yesNo == true) {
            let product_list = []
            for(let p of sale.sale.sale_products){
                product_list.push({"product_code":p.product_code})
            }
            await  call.get("epos_restaurant_2023.api.product.get_product_price_by_price_rule",{products:JSON.stringify(product_list),business_branch:gv.setting.business_branch,price_rule:result})
            .then(async (res)=>{
                for (let sp of sale.sale.sale_products) {
                    JSON.parse(res.message) .forEach((e) => { if (e.product_code == sp.product_code){sp.price = e.price}});
                    sale.updateSaleProduct(sp)
                }
                await onConfrim(result)
             })
            
        }
    } else {
        await onConfrim(result)
    }
}
async function onConfrim(result) {
    sale.sale.price_rule = result;
    sale.setting.price_rule = result;
    product.parentMenu = '';
    product.searchProductKeyword = '';
    product.searchProductKeywordStore = '';
    product.selectedProduct = {};
    sale.updateSaleSummary()
    
    
    await emit('resolve', true)
}
</script>