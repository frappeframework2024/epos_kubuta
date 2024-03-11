<template>
    <ComModal @onClose="onClose(false)" :loading="loading" :fullscreen="true" :hide-ok-button="true"
        :hide-close-button="true">
        <template #title>
            {{ params.title }}
        </template>

        <template #content>
            <div class="search-box my-0 mx-auto w-full">
                <ComInput autofocus keyboard variant="outlined" :placeholder="$t('Search...')"
                    prepend-inner-icon="mdi-magnify" v-model="keyword" v-debounce="onSearch" /> <br />
                
                <v-row>
                    <v-col cols="3">
                        <div class="invs-det">
                            <v-select density="comfortable"  @update:modelValue="onSortField" v-model="sortOrder.field" label="Sort Order"
                                item-title="label" item-value="fieldname"
                                :items="meta?.fields?.filter(r => r.in_list_view == 1 || r.in_filter == 1 || r.fieldname == 'product_code' || r.bold == 1 || r.fieldname == 'modified')"></v-select>
                        </div>
                    </v-col>
                    <v-col cols="1">
                        <v-btn class="h-100 w-100" @click="onSortOrderBy('asc')">ASC</v-btn>
                    </v-col>
                    <v-col cols="1">
                        <v-btn class="h-100 w-100" @click="onSortOrderBy('desc')">DESC</v-btn>
                    </v-col>
                </v-row>
                <v-row v-if="data?.length > 0">
                   
                        <v-col cols="7">
                            <div style="height:calc(100vh - 225px);" class="overflow-auto">
                                <div class="flex flex-column h-100">
                                    <div>
                                        <v-table style="border-top: 1px solid #ccc" fixed-header>
                                            <thead>
                                                <tr>
                                                    <th class="text-left">{{ $t("Photo") }}</th>
                                                    <th class="text-left">{{ $t("Product Code") }}</th>
                                                    <th class="text-left">{{ $t("Product Name") }}</th>
                                                    <th class="text-left">{{ $t("Category") }}</th>
                                                    <th class="text-right">{{ $t("Price") }}</th>
                                                    <th class="text-center">{{ $t("Unit") }}</th>
                                                    <th></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(p, index) in data" :key="index">
                                                    <td class="text-left">
                                                        <div class="p-2">
                                                            <v-img :width="90" :height="90" aspect-ratio="16/9" cover
                                                                :src="p.photo"></v-img>
                                                        </div>
                                                    </td>
                                                    <td>{{ p.name }}

                                                        <template v-if="p.product_code_2"> <br /> {{ p.product_code_2}}</template>
                                                        <template v-if="p.product_code_3"> <br /> {{ p.product_code_3 }}</template>
                                                    </td>
                                                    <td style="max-width: 30rem;" class="overflow-hidden">
                                                        <div class="elp-pro-name">
                                                            <v-tooltip v-if="p.product_name_en != p.product_name_kh"
                                                                :text="`${p.product_name_en}${p.product_name_kh}`">
                                                                <template v-slot:activator="{ props }">
                                                                    <div class="elp-pro-name" v-bind="props">{{p.product_name_en }} <template
                                                                            v-if="p.product_name_en != p.product_name_kh">{{p.product_name_kh }}</template>
                                                                    </div>
                                                                </template>
                                                            </v-tooltip>
                                                            <v-tooltip v-else :text="`${p.product_name_en}`">

                                                                <template v-slot:activator="{ props }">
                                                                    <div class="elp-pro-name" v-bind="props">{{p.product_name_en }} <template
                                                                            v-if="p.product_name_en != p.product_name_kh">{{p.product_name_kh }}</template>
                                                                    </div>
                                                                </template>
                                                            </v-tooltip>
                                                        </div>
                                                    </td>

                                                    <td>{{ p.product_category }}</td>
                                                
                                                    <td class="text-right">
                                                        <div v-for="item in productPriceList(p.prices)">
                                                        {{ item.price_rule }} : <CurrencyFormat :value="item.price" /> | <CurrencyFormat :currency="gv.setting.pos_setting.second_currency_name" :value="item.price * second_currency_exchange_rate" />
                                                        </div>
                                                    </td>
                                                    <td class="text-center">
                                                        {{ p.unit }}
                                                    </td>
                                                    <td>
                                                        <v-btn @click="onSelectProductClick(p)">Select Product</v-btn>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </v-table>
                                        
                                    </div>
                                    <div>
                                        <!-- <template v-if="data.length > 0">
                                            <div class="text-center">
                                                <v-pagination
                                                v-model="page"
                                                :length="4"
                                                rounded="circle"
                                                ></v-pagination> 
                                            </div> 
                                        </template> -->
                                    </div>
                                </div>
                            </div>
                        </v-col>
                        <v-col cols="5">
                            <div style="height:calc(100vh - 225px);" class="overflow-auto">
                                <div class="flex flex-column h-100">
                                    <div>
                                        <v-table style="border-top: 1px solid #ccc;">
                                            <thead>
                                                <tr>
                                                    <th class="text-left">{{ $t("Photo") }}</th>
                                                    <th class="text-left">{{ $t("Product Code") }}</th>
                                                    <th class="text-left">{{ $t("Product Name") }}</th>
                                                    <th class="text-left">{{ $t("Category") }}</th>
                                                    <th class="text-right">{{ $t("Price") }}</th>
                                                    <th class="text-center">{{ $t("Unit") }}</th>
                                                    <th></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(p, index) in selectedProductList" :key="index">
                                                    <td class="text-left">
                                                        <div class="p-2">
                                                            <v-img :width="90" :height="90" aspect-ratio="16/9" cover
                                                                :src="p.photo"></v-img>
                                                        </div>
                                                    </td>
                                                    <td>{{ p.name }}

                                                        <template v-if="p.product_code_2"> <br /> {{ p.product_code_2}}</template>
                                                        <template v-if="p.product_code_3"> <br /> {{ p.product_code_3 }}</template>
                                                    </td>
                                                    <td style="max-width: 30rem;" class="overflow-hidden">
                                                        <div class="elp-pro-name">
                                                            <v-tooltip v-if="p.product_name_en != p.product_name_kh"
                                                                :text="`${p.product_name_en}${p.product_name_kh}`">
                                                                <template v-slot:activator="{ props }">
                                                                    <div class="elp-pro-name" v-bind="props">{{p.product_name_en }} <template
                                                                            v-if="p.product_name_en != p.product_name_kh">{{p.product_name_kh }}</template>
                                                                    </div>
                                                                </template>
                                                            </v-tooltip>
                                                            <v-tooltip v-else :text="`${p.product_name_en}`">

                                                                <template v-slot:activator="{ props }">
                                                                    <div class="elp-pro-name" v-bind="props">{{p.product_name_en }} <template
                                                                            v-if="p.product_name_en != p.product_name_kh">{{p.product_name_kh }}</template>
                                                                    </div>
                                                                </template>
                                                            </v-tooltip>
                                                        </div>
                                                    </td>

                                                    <td>{{ p.product_category }}</td>
                                                
                                                    <td class="text-right">
                                                        <div v-for="item in productPriceList(p.prices)">
                                                        {{ item.price_rule }} : <CurrencyFormat :value="item.price" /> | <CurrencyFormat :currency="gv.setting.pos_setting.second_currency_name" :value="item.price * second_currency_exchange_rate" />
                                                        </div>
                                                    </td>
                                                    <td class="text-center">
                                                        {{ p.unit }}
                                                    </td>
                                                    <td>
                                                        <v-btn @click="onSelectProduct(p)">Select Product</v-btn>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </v-table>
                                        
                                    </div>
                                    <div>
                                        <!-- <template v-if="data.length > 0">
                                            <div class="text-center">
                                                <v-pagination
                                                v-model="page"
                                                :length="4"
                                                rounded="circle"
                                                ></v-pagination> 
                                            </div> 
                                        </template> -->
                                    </div>
                                </div>
                            </div>
                            <div>
                                
                            </div>
                        </v-col>
                    
                    <!-- <v-col v-if="selectedProduct">
                        <div class="h-100 p-2 pt-0"  >
                            <ComSearchSelectedProduct/>
                        </div>
                    </v-col> -->
                </v-row>


            </div>
        </template>
    </ComModal>
</template>

<script setup>

import { inject, ref, computed, onMounted, reactive, i18n, addModifierDialog } from '@/plugin'
import { createToaster } from '@meforma/vue-toaster';
import ComSearchSelectedProduct from './ComSearchSelectedProduct.vue';
const sale = inject("$sale")
const product = inject("$product")

const gv = inject("$gv")
const frappe = inject('$frappe');
const db = frappe.db()
const call = frappe.call();
const data = ref([])
const { t: $t } = i18n.global;
const keyword = ref("")
const toaster = createToaster({ position: "top-right" })
const loading = ref(false)
const selectedProduct = ref()
const meta = ref({})

const sortOrder = ref({ field: "product_name_en", order: "asc" })
const selectedProductList = ref([])
let second_currency_exchange_rate=ref(1)

    if(gv.setting.pos_setting.second_currency_name ){
        call.get('epos_restaurant_2023.api.api.get_exchange_rate').then((res)=>{
            second_currency_exchange_rate.value=res.message
        })
    }

const props = defineProps({
    params: {
        type: Object,
        require: true
    }
})

const emit = defineEmits(["resolve"])


function onSortOrderBy(type) {
    sortOrder.value.order = type
    onSearch()
}

function onSortField(field) {
    sortOrder.value.field = field
    onSearch()
}

function onSelectProductClick(p){
    call.get("epos_restaurant_2023.api.product.get_product_by_barcode", { barcode: d.name }).then(async (result) => {
        const p = result.message
        const portions = JSON.parse(p.prices)?.filter(r => (r.branch == sale.sale.business_branch || r.branch == '') && r.price_rule == sale.sale.price_rule);
        if (portions?.length == 1) {
            p.price = portions[0].price
            p.unit = portions[0].unit
        }

        if (portions?.length > 1) {
            product.setSelectedProduct(p);

            let productPrices = await addModifierDialog();

            if (productPrices) {
                if (productPrices.portion != undefined) {
                    p.price = productPrices.portion.price;
                    p.portion = productPrices.portion.portion;
                    p.unit = productPrices.portion.unit
                }

            } else {
                return;
            }
        } else {
            p.modifiers = "";
            p.modifiers_data = "[]";
            p.portion = "";
        }
        selectedProductList.value.unshift(p)
        // sale.addSaleProduct(p);
        toaster.success($t("Add product to order successfully"))
    })
   
}

function onSearch() {
    loading.value = true
    db.getDocList('Product', {
        fields: ['name', "product_code_2", "product_code_3", 'product_name_en', 'product_name_kh', 'price', "photo", "product_category", 'prices', 'unit'],
        orFilters: [
            ["name", 'like', '%' + keyword.value + "%"],
            ["product_code_2", 'like', '%' + keyword.value + "%"],
            ["product_code_3", 'like', '%' + keyword.value + "%"],
            ["product_name_en", 'like', '%' + keyword.value + "%"],
            ["product_name_kh", 'like', '%' + keyword.value + "%"],
            ["Product Price", "barcode", "like", "%" + keyword.value + "%"]
        ],
        filters: [
            ["Product Price", "price_rule", "=", sale.sale.price_rule]
        ],
        orderBy: sortOrder.value,
        limit: 50
    })
        .then((docs) => {
            data.value = docs
            loading.value = false

        })
        .catch((error) => {
            loading.value = false
        });

}

function productPriceList(prices){
    return JSON.parse(prices)
}

function onClose(isClose) {
    emit('resolve', isClose);
}

async function onSelectProduct(d) {
    call.get("epos_restaurant_2023.api.product.get_product_by_barcode", { barcode: d.name }).then(async (result) => {
        const p = result.message
        const portions = JSON.parse(p.prices)?.filter(r => (r.branch == sale.sale.business_branch || r.branch == '') && r.price_rule == sale.sale.price_rule);
        if (portions?.length == 1) {
            p.price = portions[0].price
            p.unit = portions[0].unit
        }

        if (portions?.length > 1) {
            product.setSelectedProduct(p);

            let productPrices = await addModifierDialog();

            if (productPrices) {
                if (productPrices.portion != undefined) {
                    p.price = productPrices.portion.price;
                    p.portion = productPrices.portion.portion;
                    p.unit = productPrices.portion.unit
                }

            } else {
                return;
            }
        } else {
            p.modifiers = "";
            p.modifiers_data = "[]";
            p.portion = "";
        }

        sale.addSaleProduct(p);
        toaster.success($t("Add product to order successfully"))
    })



}


onMounted(() => {

    call.get("epos_restaurant_2023.api.api.get_meta", { "doctype": "Product" }).then((data) => {
        meta.value = data.message
    })

})

</script>

<style>
.elp-pro-name {
    width: 30rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

.invs-det .v-input__details {
    display: none !important;
}
</style>