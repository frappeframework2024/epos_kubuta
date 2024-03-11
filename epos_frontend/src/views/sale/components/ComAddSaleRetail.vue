<template>
    <div class="px-2">
        <div class="v-col-12">
            <ComSaleInformation />
        </div>
        <div class="v-row pt-1">
            <div class="v-col-9">
                <div class="flex flex-column justify-between product-detail-st" style="height:calc(-144px + 100vh)">
                    <div class="first-div">
                        <ComSaleProductList />
                    </div>
                    <div class="second-div">
                        <div class="v-row">
                            <div class="v-col-6">
                                <ComSaleNote />

                            </div>
                            <div class="v-col-6">
                                <ComSaleSummary v-if="sale.sale?.sale_products?.length > 0" />
                            </div>
                        </div>
                        <hr class="my-4">
                        <div>
                            <ComSaleActionButton />
                        </div>
                    </div>
                </div>
            </div>
            <div class="v-col-3" style="border-left: 1px solid #ccc">
                <ComExchangeRate />
                <div class="m-3"></div>
                <ComSelectCustomer padding="p-3" />
                <div class="m-3"></div>
                <ComSelectedProduct v-if="sale.sale?.sale_products?.filter(r=>r.selected).length>0"/>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, inject } from "@/plugin"
import ComSaleInformation from "@/views/sale/components/retail_ui/ComSaleInformation.vue"
import ComExchangeRate from "@/views/sale/components/retail_ui/ComExchangeRate.vue"
import ComSaleActionButton from "@/views/sale/components/retail_ui/ComSaleActionButton.vue"
import ComSaleNote from "@/views/sale/components/retail_ui/ComSaleNote.vue"
import ComSaleProductList from "@/views/sale/components/retail_ui/ComSaleProductList.vue"
import ComSaleSummary from "@/views/sale/components/retail_ui/ComSaleSummary.vue"
import ComSelectedProduct from "@/views/sale/components/retail_ui/ComSelectedProduct.vue"
import ComSelectCustomer from "@/views/sale/components/ComSelectCustomer.vue"

const sale = inject("$sale")
sale.show_unit_in_select_portion = true

</script>

<style scoped>
.product-detail-st .first-div {
    flex: 1;
}

/* .product-detail-st .second-div {
    height: 272px;
} */
</style>