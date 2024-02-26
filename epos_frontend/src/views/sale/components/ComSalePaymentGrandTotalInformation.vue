<template>
    <div class="bg-red-200 mb-2 rounded-sm" :class="mobile ? 'p-2' : 'p-4 text-lg'" @click="emit('onClick')">
        <div class="text-center">{{ $t('Total Amount') }}</div>
        <div class="flex justify-around">
            <div>
                <CurrencyFormat :value="(sale.sale.grand_total - sale.sale.deposit )" />
            </div>
           
            <div>
                <CurrencyFormat :value="((sale.sale.grand_total -sale.sale.deposit) * (sale.sale.exchange_rate||1) )"
                    :currency="gv.setting?.pos_setting?.second_currency_name" />
            </div>
            <div  v-if="gv.setting.pos_setting.third_currency_name">
                <CurrencyFormat :value="((sale.sale.grand_total -sale.sale.deposit) * (third_currency_exchange_rate))"
                    :currency="gv.setting?.pos_setting?.third_currency_name" />
            </div>
        </div>
    </div>
</template>
<script setup>
import { inject,ref, defineEmits } from 'vue'
import { useDisplay} from 'vuetify'
const {mobile} = useDisplay()
const sale = inject('$sale')
const gv = inject('$gv')
const emit = defineEmits()
const frappe = inject("$frappe");
const call = frappe.call();
let third_currency_exchange_rate = ref(1)

if(gv.setting.pos_setting.third_currency_name ){
    call.get('epos_restaurant_2023.api.api.get_third_exchange_rate').then((res)=>{
        third_currency_exchange_rate.value=res.message
    })
}


</script>