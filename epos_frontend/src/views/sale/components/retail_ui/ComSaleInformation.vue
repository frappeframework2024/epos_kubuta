<template>
    <div class="py-2 flex flex-wrap">

        <div class="v-row ga-3">
            <ComSaleInformationbox bgColor="bg-blue-500" title="POS Profile" :value="sale.sale.pos_profile" size="large"
                icon="mdi-cash-register" />
            <ComSaleInformationbox bgColor="bg-blue-500" title="Outlet/WareHouse"
                :value="sale.sale.outlet + '/' + sale.sale.stock_location" size="large" icon="mdi-store" />
            <ComSaleInformationbox bgColor="bg-blue-500" title="Working Day" :value="sale.sale.working_day" size="large"
                icon="mdi-calendar" />
            <ComSaleInformationbox bgColor="bg-blue-500" title="Cashier Shift" :value="sale.sale.cashier_shift"
                size="large" icon="mdi-clock-time-nine-outline" />
                <v-menu>
      <template v-slot:activator="{ props }">
        <ComSaleInformationbox  v-bind="props" bgColor="bg-blue-500" title="Price Rule" :value="sale.sale.price_rule" size="large"
                icon="mdi-currency-usd" />
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in price_rules"
          :key="index"
          :value="index"
        >
          <v-list-item-title @click="changePriceRule(item)">{{ item.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
           
        </div>
    </div>
</template>

<script setup>
import ComSaleInformationbox from '@/views/sale/components/retail_ui/ComSaleInformationbox.vue';

import { ref, inject, keyboardDialog, changePriceRuleDialog, createToaster, i18n, computed } from '@/plugin';
import { onMounted } from 'vue';


const { t: $t } = i18n.global;


const toaster = createToaster({ position: 'top-right' })
const sale = inject("$sale")
const product = inject("$product")
const setting = JSON.parse(localStorage.getItem("setting"))

const frappe = inject("$frappe")
const gv = inject("$gv")
const db = frappe.db()
const call = frappe.call()
const price_rules = ref([])

async function onChangeMenuLanguage() {
    sale.onChangeMenuLanguage();
    await setTimeout(function () {
        sale.load_menu_lang = false;
    }, 1);
}

 function changePriceRule(price_rule){
    sale.sale.price_rule= price_rule.name
    if (sale.sale.sale_products.length > 0) {
            let product_list = []
            
            for(let p of sale.sale.sale_products){
                product_list.push({"product_code":p.product_code})
            }
            call.get("epos_restaurant_2023.api.product.get_product_price_by_price_rule",{products:JSON.stringify(product_list),business_branch:gv.setting.business_branch,price_rule:price_rule.name})
            .then( (res)=>{
                for (let sp of sale.sale.sale_products) {
                    JSON.parse(res.message) .forEach((e) => { if (e.product_code == sp.product_code){sp.price = e.price}});
                    sale.updateSaleProduct(sp)
                }
               
             })
            
    }
}
onMounted(()=>{
    db.getDocList("Price Rule").then(data=>{
        price_rules.value = data
    })
})
</script>