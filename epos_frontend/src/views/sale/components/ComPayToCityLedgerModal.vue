<template>
    <ComModal :fullscreen="false" width="1400px" :persistent="true" @onClose="onClose" :titleOKButton="$t('Ok')"
        @onOk="onConfirm" :fill="false" contentClass="h-full">
        <template #title>
            {{ $t('Payment') }} {{ selected_city_ledger?.name == '' ? '' : (selected_city_ledger?.city_ledger_name ?? '') }}
        </template>
        <template #content>
            <v-row no-gutters>
                <v-col cols="12" sm="12" md="6">
                    <ComInput
                    ref="searchTextField"
                    keyboard
                    class="m-1"
                    v-model="search"
                    :placeholder="$t('City Ledger Name')"
                    v-debounce="onSearchCityLedgerName"
                    @onInput="onSearchCityLedgerName"/>
                   
                </v-col>
                <v-col cols="12" sm="12" md="6">
                    <ComInput
                    ref="searchTextField"
                    keyboard
                    class="m-1"
                    v-model="search"
                    :placeholder="$t('Phone Number')"
                    v-debounce="onSearchCityLedgerPhoneNumber"
                    @onInput="onSearchCityLedgerPhoneNumber"/>
                </v-col>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" sm="12" md="3">
                    <v-row no-gutters>
                        <v-col cols="12" class="pa-1">
                            <template v-for="(t, index) in city_ledger_types">
                                <div @click="(() => cityLedgerTypeClick(t))"
                                    class="flex items-center justify-center cursor-pointer border border-stone-500 rounded-sm text-center hover:bg-slate-300 p-3"
                                    :class="(selected_city_ledger_type.name == t.name ? 'bg-pink-lighten-4' : '')"
                                    style="margin: 1px;">

                                    {{ t.label }}


                                </div>
                            </template>

                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="12" sm="12" md="9">
                    <div>
                        <template v-if="city_ledgers.length > 0">
                            <v-row no-gutters>
                                <v-col cols="12" class="pa-1" sm="12" md="4" v-for="(r, index) in city_ledgers" :key="index"
                                    @click="(() => onCityLedgerPressed(r))">
                                    <div :class="selected_city_ledger?.name == r.name ? 'bg-indigo-lighten-2' : 'bg-deep-purple-lighten-5'"
                                        class="btn-post-to-room cursor-pointer border border-stone-500 pa-1 rounded-sm">
                                        <div>
                                            <span><strong>{{ $t('City Ledger') }}:</strong> #{{ r.city_ledger_name }}</span>
                                        </div>
                                        <div>
                                            <span><strong>{{ $t("City Ledger Type") }}:</strong> {{ r.city_ledger_type
                                            }}</span>
                                        </div>
                                        <div>
                                            <span><strong>{{ $t("Phone Number") }}:</strong> {{ r.phone_number }}</span>
                                        </div>

                                    </div>
                                </v-col>
                            </v-row>
                        </template>
                        <template v-else>
                            <div class="flex items-center justify-center">{{ $t("Empty Data") }}</div>
                        </template>
                    </div>
                </v-col>
            </v-row>
        </template>
    </ComModal>
</template>
<script setup>

import { ref, onMounted, i18n, inject, computed  } from '@/plugin';
import {watch} from 'vue'
import { createToaster } from '@meforma/vue-toaster';

const gv = inject("$gv")
const frappe = inject("$frappe")
const { t: $t } = i18n.global;

const emit = defineEmits(['resolve'])
const toaster = createToaster({ position: "top" })
const props = defineProps({
    params: Object
})

const call = frappe.call();
const db = frappe.db();


const city_ledger_data = ref([]);
const city_ledgers = ref({});
const city_ledger_types = ref([]);
const selected_city_ledger = ref();
const selected_city_ledger_type = ref({});



function onSearchCityLedgerName(keywork){
    onGetCityLedger(['city_ledger_name', 'like', "%"+ keywork +"%"])
}

function onSearchCityLedgerPhoneNumber(keywork){
    onGetCityLedger(['phone_number', 'like', "%"+ keywork +"%"])
}



function debouncer(fn, delay) {
    var timeoutID = null;
    return function () {
        clearTimeout(timeoutID);
        var args = arguments;
        var that = this;
        timeoutID = setTimeout(function () {
            fn.apply(that, args);
        }, delay);
    };
}

onMounted(() => {

    city_ledger_types.value.push({
        "name": "all",
        "label": $t("All"),
        "sort_order": -9999,
        "selected": true
    })
    selected_city_ledger_type.value = city_ledger_types.value.filter((r) => r.name == "all")[0]
    onGetCityLedger();
    onGetCityLedgerType()

})



function onGetCityLedgerType() {
    db.getDocList('City Ledger Type').then((result) => {
        result.forEach((r, i) => {
            city_ledger_types.value.push({
                "name": r.name,
                "label": r.name,
                "sort_order": i
            })
        })
    });

}

function onGetCityLedger(_filters = []) {
    let custom_filter = [['property', '=', gv.setting?.business_branch], ['status', '=', 'Open']]
    if (_filters.length > 0) {
        custom_filter.push(_filters)
    }
    db.getDocList('City Ledger', {
        fields: ['name', 'phone_number', 'city_ledger_name', 'city_ledger_type', 'property', 'business_source'],
        filters: custom_filter
    }).then((result) => {
        city_ledgers.value = result;
        city_ledgers.value.city_ledger_type = []
        if (city_ledgers.value) {
            city_ledgers.value.city_ledger_type.forEach((t) => {
                city_ledger_types.value.push({
                    "name": t.name,
                    "sort_order": t.sort_order,
                    "selected": false
                })
            })


        }
    });
}

function cityLedgerTypeClick(city_ledger_type_click) {
    selected_city_ledger_type.value = city_ledger_type_click
    if( city_ledger_type_click.name == 'all'){
        onGetCityLedger()
    }else{
        onGetCityLedger(['city_ledger_type', '=', city_ledger_type_click.name])
    }
    
}

function onConfirm() {
    if (selected_city_ledger.value) {
        emit("resolve", {
            folio_transaction_number: selected_city_ledger.value.name,
            city_ledger_name: selected_city_ledger.value.city_ledger_name
        });
    } else {
        toaster.warning($t("Please select a city ledger"));
    }




}
function onCityLedgerPressed(r) {

    selected_city_ledger.value = r;


}
function onClose() {
    emit("resolve", false);
}






</script>
<style>
.btn-post-to-room {
    width: 100%;
    text-align: start;
    display: block !important;
}

.btn-post-to-room .v-btn__content {
    white-space: normal !important;
    display: block !important;
    line-height: 1.5;
}
</style>