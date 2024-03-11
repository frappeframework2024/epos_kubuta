<template>

    <div>
        <template v-if="sale?.selected_sale_product">
            <div style="height:calc(-321px + 100vh);overflow-y:auto">
                <div class="border p-3 rounded-md searc-pro-res">
                    <div v-if="sale?.selected_sale_product?.product_photo"
                    class="product-image rounded-md overflow-hidden" style="width: 300px;">
                        <img class="h-100 w-100" style="object-fit: cover;"
                            :src="sale?.selected_sale_product?.product_photo" />
                    </div>
                    <br />
                    <div class="text-center">
                        <strong>{{ sale?.selected_sale_product?.product_code }} / {{
            sale?.selected_sale_product?.product_name
        }}
                            <template
                                v-if="sale?.selected_sale_product?.product_name != sale?.selected_sale_product?.product_name_kh">{{
            sale?.selected_sale_product?.product_name_kh }}
                            </template>
                        </strong>
                        <br />
                        <strong>{{ sale?.selected_sale_product?.note }}</strong>
                    </div>
                </div>

                <div class="border p-2 rounded-md mt-3">
                    <ComLabelValue label="Quantity" :value="sale?.selected_sale_product?.quantity" />
                    <ComLabelValue label="Selling Price">
                        <CurrencyFormat :value="sale?.selected_sale_product?.price" />
                    </ComLabelValue>
                    <ComLabelValue label="Regular Price">
                        <CurrencyFormat :value="sale?.selected_sale_product?.regular_price" />
                    </ComLabelValue>
                    <ComLabelValue label="Sub Total">
                        <CurrencyFormat :value="sale?.selected_sale_product?.sub_total" />
                    </ComLabelValue>
                    <ComLabelValue v-if="sale.selected_sale_product.discount_amount > 0">

                        <template v-slot:label>
                            {{ $t("Discount") }}
                            <span
                                v-if="sale.selected_sale_product.discount > 0 && sale.selected_sale_product.discount_type == 'Percent'">{{
            sale.selected_sale_product.discount }}%</span>
                        </template>
                        <CurrencyFormat :value="sale.selected_sale_product.discount_amount" />
                    </ComLabelValue>
                    <ComLabelValue label="Total Amount">
                        <CurrencyFormat :value="sale?.selected_sale_product?.total_revenue" />
                    </ComLabelValue>
                    <template v-if="sale.selected_product?.product?.is_inventory_product==1">
                    <h2 style="font-size: 20px">Inventory</h2>
                    <ComLabelValue v-for="(inv, index) in sale.selected_product.invenotry" :key="index"
                        >
                        <template #label>
                                {{ inv.stock_location }} <br/>
                                {{ $t("Re-order level") }} : {{ inv.reorder_level }}
                        </template>
                        {{ inv.quantity }} {{ inv.unit }} 
                    </ComLabelValue>

                </template>
                </div>
            </div>
        </template>

        <template v-else>
            <div style="height:calc(-355px + 100vh)">
                <div class="flex h-100 w-100 justify-center items-center">
                    <div class="text-center n-data-str">
                        <v-icon icon="mdi-database-remove" color="red" size="large"></v-icon><br />
                        No Product Selected
                    </div>
                </div>
            </div>
        </template>
    </div>




</template>

<script setup>
import { inject, ref, watch, onMounted, i18n } from '@/plugin';
import ComLabelValue from "@/views/sale/components/retail_ui/ComLabelValue.vue"

const { t: $t } = i18n.global;
const sale = inject("$sale") 
</script>

<style scoped>
.n-data-str {
    font-size: 30px;
}
.searc-pro-res {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    align-items: center;
}
</style>