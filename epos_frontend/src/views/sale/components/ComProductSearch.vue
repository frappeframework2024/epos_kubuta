<template>
 
    <div :class="small ? 'px-2' : 'px-6'">
        <div class="search-box my-0 mx-auto" :class="small ? 'w-full' : 'max-w-[350px]'">
            <ComInput
                :autofocus="!getIsMobile()"
                keyboard
                variant="outlined"
                :placeholder="$t('Search...')"
                prepend-inner-icon="mdi-magnify"
                v-model="product.searchProductKeywordStore"
                v-debounce="onSearch"
                @onInput="onSearch"
                @keydown="onKeyDown"
                :ref="txtSearch"
                />

<!-- 
            <ComAutoComplete v-model="selected_product" doctype="Product" :autoFetch="false"
                @onSelected="onSelectProduct" /> -->

        </div>
    </div>

</template>

<script setup>
import { inject, ref, defineProps, createResource, addModifierDialog, onUnmounted, onMounted } from '@/plugin';
import ComInput from '../../../components/form/ComInput.vue';
import { createToaster } from '@meforma/vue-toaster';
import ComAutoComplete from '@/components/form/ComAutoComplete.vue';
import { useDisplay } from 'vuetify';
import { computed } from 'vue';
const product = inject("$product")
const sale = inject("$sale")
const frappe = inject("$frappe")
const { mobile } = useDisplay();
const db = frappe.db();
let control = ref(null)
const toaster = createToaster({ position: 'top-right', maxToasts: 2, duration: 1000 });
const props = defineProps({
    small: {
        type: Boolean,
        default: false
    }
});

const selected_product = ref()

const doSearch = ref(true)

function getIsMobile() {
    return  localStorage.getItem("flutterWrapper")==1 || mobile;
}

function onSearch(key) {
    if (sale.setting.use_retail_ui == 0) {


        if (key) {
            doSearch.value = true
        }
        if (product.setting.pos_menus.length > 0) {
            product.searchProductKeyword = key;

        } else {
            //search product from db

            if (doSearch.value) {
                product.getProductFromDbByKeyword(db, key)
            }
        }
    }
}
function onSelectProduct(p) {
    if(p){ 
    onSearchProductByBarcode(p)
    selected_product.value = ""
    }
}
function onKeyDown(event) {
    if (event.key == "Enter") {

        if (!sale.isBillRequested()) {
            onSearchProductByBarcode(product.searchProductKeywordStore)
        }
    }
}

function onSearchProductByBarcode(barcode){
    const searchProductResource = createResource({
                url: "epos_restaurant_2023.api.product.get_product_by_barcode",
                params: {
                    barcode: barcode
                }
            });

            searchProductResource.fetch().then(async (doc) => {

                const p = JSON.parse(JSON.stringify(doc));

                const portions = JSON.parse(p.prices)?.filter(r => (r.branch == sale.sale.business_branch || r.branch == '') && r.price_rule == sale.sale.price_rule);
                const check_modifiers = product.onCheckModifier(JSON.parse(p.modifiers));
                if (portions?.length == 1) {
                    p.price = portions[0].price
                    p.unit = portions[0].unit
                }

                if (check_modifiers || portions?.length > 1) {
                    product.setSelectedProduct(doc);

                    let productPrices = await addModifierDialog();

                    if (productPrices) {
                        if (productPrices.portion != undefined) {
                            p.price = productPrices.portion.price;
                            p.portion = productPrices.portion.portion;
                            p.unit = productPrices.portion.unit
                        }
                        p.modifiers = productPrices.modifiers.modifiers;
                        p.modifiers_data = productPrices.modifiers.modifiers_data;
                        p.modifiers_price = productPrices.modifiers.price

                    } else {
                        return;
                    }
                } else {
                    p.modifiers = "";
                    p.modifiers_data = "[]";
                    p.portion = "";
                }

                sale.addSaleProduct(p);

                toaster.success("Added product " + barcode + " successfully")
                product.searchProductKeywordStore = "";
                doSearch.value = false

            });

            product.searchProductKeywordStore = ""
       
}


const actionClickHandler = async function (e) {

    if (e.isTrusted) {
        if (e.data.action == "set_focus_in_search_product") {
            const el = document.querySelector(".search-box input");
            if (el) {

                el.focus();
            }
        }
    }
}

onMounted(() => {
    window.addEventListener('message', actionClickHandler, false);
})

onUnmounted(() => {
    window.removeEventListener('message', actionClickHandler, false);
})


</script>