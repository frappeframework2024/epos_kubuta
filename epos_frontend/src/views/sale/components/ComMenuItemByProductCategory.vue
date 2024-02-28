<template >
    <div v-for="(m, index) in product.menuProducts" :key="index" class="h-40" >
        <ComMenuItem :data="m" :exchange-rate="second_currency_exchange_rate"/>
        
    </div>
</template>
<script setup>
    import {inject,ref } from "@/plugin"
    import ComMenuItem from './ComMenuItem.vue';
    const product = inject("$product")
    const frappe = inject("$frappe")
    const gv = inject("$gv");
    const call = frappe.call();
    let second_currency_exchange_rate=ref(1)

    if(gv.setting.pos_setting.second_currency_name ){
        call.get('epos_restaurant_2023.api.api.get_exchange_rate').then((res)=>{
            second_currency_exchange_rate.value=res.message
        })
    }
    
</script>