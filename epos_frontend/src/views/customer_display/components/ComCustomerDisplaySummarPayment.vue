<template>

    <div class="cursor-pointer bg-green-600 text-white px-2 py-0  hover:bg-green-700">
        <div style="margin-bottom: 0px!important;" class="flex justify-between mb-2 text-lg">
            <div>{{$t('Grand Total')}}</div>
            <div style="margin: 0px; padding: 0px; font-size: 26px; font-weight: bold;">
                <CurrencyFormat :value="data.grand_total" />
            </div>
        </div>
        <div v-for="(p, index) in data.payment" :key="index" style="margin-bottom: 0px!important;" class="flex justify-between mb-2 text-lg">
            <div>{{p.payment_type}}</div>
            <div style="margin: 0px; padding: 0px; font-size: 26px; font-weight: bold;">
                <CurrencyFormat :value="p.input_amount" :currency="p.currency" />
            </div>
        </div>

        <!-- change amount -->
        <hr v-if="data.changed_amount > 0"/>
        <div class="flex justify-between mb-2 text-lg" v-if="data.changed_amount > 0">
            <div>{{ $t('Change Amount') }}({{ gv.setting.pos_setting.main_currency_name }}):</div>
            <div style="margin: 0px; padding: 0px; font-size: 26px; font-weight: bold;">
                <CurrencyFormat :value="data.changed_amount" />
            </div>
        </div>
        <div class="flex justify-between mb-2 text-lg" v-if="data.changed_amount > 0">
            <div>{{ $t('Change Amount') }}({{ gv.setting.pos_setting.second_currency_name }}):</div>
            <div style="margin: 0px; padding: 0px; font-size: 26px; font-weight: bold;">
                <CurrencyFormat :value="data.second_changed_amount"
                    :currency="gv.setting.pos_setting.second_currency_name" />
            </div>
        </div>
        <!-- end change amount -->

        <div class="flex justify-between">
            <div>{{$t('Total Qty')}} : <span>{{ data.total_quantity }}</span></div>
            <div>
                <ComExchangeRate />
                <CurrencyFormat :value="(data.grand_total || 0) * (data.exchange_rate || 1)"
                    :currency="gv.setting.pos_setting.second_currency_name" />
            </div>
        </div>
    </div>
</template>
<script setup>
import { inject } from '@/plugin';
import ComExchangeRate from '../../sale/components/ComExchangeRate.vue';
const props = defineProps({
    data: Object
})
const gv = inject("$gv")
</script>
<style lang="">
  
  </style>