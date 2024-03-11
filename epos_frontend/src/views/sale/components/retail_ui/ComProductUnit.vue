<template>
    <span class="link_line_action overflow-hidden" @click="getProductUnit">{{ sale_product.unit }}

        <v-menu activator="parent">

            <v-card class="mx-auto my-8" max-width="344" elevation="16">
                <v-card-item>
                    <v-card-title>
                        {{ $t("Change Unit") }}
                    </v-card-title>

                </v-card-item>

                <v-card-text>
                    <div v-if="loading">
                        Loading...
                    </div>
                    <v-list v-else>
                        <v-list-item @click="onChangeUnit(p)" v-for="(p, index) in prices" :key="index">
                            <v-list-item-title>{{ p.unit }} -
                                <CurrencyFormat :value="p.price" />
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-card-text>
            </v-card>

        </v-menu>

    </span>
</template>

<script setup>
import { ref, inject, i18n } from "@/plugin"
const props = defineProps({
    sale_product: Object
})
import { createToaster } from '@meforma/vue-toaster';
const toaster = createToaster({ position: "top-right" });
const frappe = inject("$frappe")
const db = frappe.db()
const prices = ref([])
const loading = ref(false)
const sale = inject("$sale")

const { t: $t } = i18n.global;

function getProductUnit() {
    prices.value = []

    loading.value = true
    db.getDoc("Product", props.sale_product.product_code).then((doc) => {
        loading.value = false
        prices.value = doc.product_price.filter(x=>x.price_rule==sale.sale.price_rule)

        if (prices.value.length == 0) {
            prices.value.push({
                unit: doc.unit,
                price: doc.price
            })
        }
    }).catch(err => {
        loading.value = false
    })

}

function onChangeUnit(p) {

    let sp = props.sale_product

    sp.portion = "Normal";
    sp.price = p.price || 0;
    sp.unit = p.unit || "Unit"

    sale.updateSaleProduct(sp);
    sale.updateSaleSummary();
    toaster.success($t("msg.Update successfully"))
}

</script>