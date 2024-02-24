<template>

   
   <div v-if="saleProduct.time_in && !saleProduct.time_out_price">
    <span style="color:green; font-size: 12px;" class="mr-2">EST. Price</span>
    <CurrencyFormat :value="est_price" />
   </div> 
 
    
</template>

<script setup>
import { ref,defineProps,inject,watch,onMounted } from "@/plugin"
const est_price = ref(0)
const frappe = inject("$frappe")
const call = frappe.call()
const sale = inject("$sale")

const props = defineProps({
    saleProduct: Object,
})


watch(() => props.saleProduct.time_in, (newValue, oldValue) => {
    
    getEstimatePrice()
});
function getEstimatePrice(){
    const data = props.saleProduct
    data.price_rule = sale.sale.price_rule
    
    
    call.post("epos_restaurant_2023.api.timer_product.get_timer_product_estimate_price", { sale_product: data }).then((result) => {
        est_price.value = result.message
    })
}
onMounted(() => {
    getEstimatePrice()
})

</script>