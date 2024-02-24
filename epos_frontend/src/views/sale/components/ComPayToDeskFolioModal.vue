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
                    :placeholder="$t('City Ledger Name')"
                    v-debounce="onSearchCityLedgerPhoneNumber"
                    @onInput="onSearchCityLedgerPhoneNumber"/>
                </v-col>
            </v-row>
            
            <v-row no-gutters>
               
                <v-col cols="12" sm="12" md="12">
                    <div>
                        <template v-if="desk_folio_list.length > 0">
                            <v-row no-gutters>
                                <v-col cols="12" class="pa-1" sm="12" md="4" v-for="(r, index) in desk_folio_list" :key="index"
                                    @click="(() => onDeskFolioPressed(r))">
                                    <div :class="selected_desk_folio?.name == r.name ? 'bg-indigo-lighten-2' : 'bg-deep-purple-lighten-5'"
                                        class="btn-post-to-room cursor-pointer border border-stone-500 pa-1 rounded-sm">
                                        <div>
                                            <span><strong>{{ $t('Desk Folio Number') }}:</strong> #{{ r.name  }}</span>
                                        </div>
                                        <div>
                                            <span><strong>{{ $t("Guest") }}:</strong> {{ r.guest_name }}</span>
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


const desk_folio_list = ref([]);
const selected_desk_folio = ref();



function onSearchCityLedgerName(keywork){
    onGetCityLedger(['city_ledger_name', 'like', "%"+ keywork +"%"])
}

function onSearchCityLedgerPhoneNumber(keywork){
    onGetCityLedger(['phone_number', 'like', "%"+ keywork +"%"])
}



onMounted(() => {
    onGetDeskFolio();
})

function onGetDeskFolio(_filters = []) {
    let custom_filter = [
        ['property', '=', gv.setting?.business_branch], 
        ['status', '=', 'Open']
    ]
    if (_filters.length > 0) {
        custom_filter.push(_filters)
    }
    db.getDocList('Desk Folio', {
        fields: ['name', 'guest', 'phone_number', 'guest_name', 'property', 'room_number'],
        filters: custom_filter
    }).then((result) => {
        desk_folio_list.value = result;
    });
}

function onConfirm() {
    if (selected_desk_folio.value) {
        emit("resolve", {
            folio_transaction_number: selected_desk_folio.value.name,
            desk_folio: selected_desk_folio.value.name
        });
    } else {
        toaster.warning($t("Please select a city ledger"));
    }




}
function onDeskFolioPressed(r) {
    selected_desk_folio.value = r;


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