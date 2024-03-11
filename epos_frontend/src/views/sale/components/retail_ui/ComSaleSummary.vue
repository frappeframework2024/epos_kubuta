<template lang="">
  <div class="border p-2 rounded-md">
    <ComLabelValue label="Total QTY" :value="sale.sale.total_quantity"/>
    <!-- sub total -->
    <ComLabelValue v-if="sale.sale.sub_total!=sale.sale.grand_total" label="Sub Total">

      <CurrencyFormat :value="sale.sale.sub_total" />
    </ComLabelValue>
    <ComLabelValue v-if="sale.sale.product_discount" label="Product Discount" :value="sale.sale.product_discount"/>
    <ComLabelValue v-if="sale.sale.sale_discount>0" label="Discountable Amount" :value="sale.sale.sale_discountable_amount"/>
    

    <ComLabelValue v-if="sale.sale.sale_discount>0">
      <template v-slot:label>
            {{$t("Sale Discount")}} 
            <span v-if="sale.sale.discount>0 && sale.sale.discount_type=='Percent'">{{sale.sale.discount}}%</span>
      </template>
      <CurrencyFormat :value="sale.sale.sale_discount" />
    </ComLabelValue>
    <ComLabelValue v-if="sale.sale.sale_discount>0 && sale.sale.product_discount" label="Total Discount">
      <CurrencyFormat :value="sale.sale.total_discount" />
    </ComLabelValue>
    
    <!-- Tax 1 -->
    <ComLabelValue v-if="sale.sale.tax_1_amount > 0">
      <template v-slot:label>
        <template v-if="sale.sale.percentage_of_price_to_calculate_tax_1==100">{{ getTaxData()?.tax_1_name }}{{sale.sale.tax_1_rate>0?"("+sale.sale.tax_1_rate+"%)":""}}</template>
        <template v-else>{{ getTaxData()?.tax_1_name }} ({{sale.sale.tax_1_rate+"%"}} {{$t('of')}} {{sale.sale.percentage_of_price_to_calculate_tax_1+"% "+$t('Revenue')}})</template>
      </template>
      <CurrencyFormat :value="sale.sale.tax_1_amount" />
    </ComLabelValue>
    <!-- Tax 2 -->
    <ComLabelValue v-if="sale.sale.tax_2_amount > 0">
      <template v-slot:label>
        <template v-if="sale.sale.percentage_of_price_to_calculate_tax_2==100">{{ getTaxData()?.tax_2_name }}{{sale.sale.tax_2_rate>0?"("+sale.sale.tax_2_rate+"%)":""}}</template>
        <template v-else>{{ getTaxData()?.tax_2_name }} ({{sale.sale.tax_2_rate+"%"}} {{$t('of')}} {{sale.sale.percentage_of_price_to_calculate_tax_2+"% "+$t('Revenue')}})</template>
      </template>
      <CurrencyFormat :value="sale.sale.tax_2_amount" />
    </ComLabelValue>
    <!-- Tax 3 -->
    <ComLabelValue v-if="sale.sale.tax_3_amount > 0">
      <template v-slot:label>
        <template v-if="sale.sale.percentage_of_price_to_calculate_tax_3==100">{{ getTaxData()?.tax_3_name }}{{sale.sale.tax_3_rate>0?"("+sale.sale.tax_3_rate+"%)":""}}</template>
        <template v-else>{{ getTaxData()?.tax_3_name }} ({{sale.sale.tax_3_rate+"%"}} {{$t('of')}} {{sale.sale.percentage_of_price_to_calculate_tax_3+"% "+$t('Revenue')}})</template>
      </template>
      <CurrencyFormat :value="sale.sale.tax_3_amount" />
    </ComLabelValue>
    <!-- Total Tax -->
    <ComLabelValue v-if="sale.sale.total_tax > 0" label="Total Tax">
      <CurrencyFormat :value="sale.sale.total_tax" />
    </ComLabelValue>
    <!-- Deposit -->
    <ComLabelValue v-if="sale.sale.deposit > 0" label="Deposit">
      <CurrencyFormat :value="sale.sale.deposit" />
    </ComLabelValue>

    <!-- Commission -->
    <ComLabelValue v-if="(sale.sale.commission_amount || 0) >0" label="Commission">
      <CurrencyFormat :value="sale.sale.commission_amount" />
    </ComLabelValue>
    <ComLabelValue>
      <template v-slot:label> <div class="text-h5" style="color:green"> {{$t("Grand Total")}} ({{sale.setting.pos_setting.main_currency_name}}) </div></template>      
      <div class="text-h5" style="color:green"><CurrencyFormat :value="(sale.sale.grand_total-sale.sale.deposit)" /></div>
    </ComLabelValue>
    <ComLabelValue>
      <template v-slot:label> <div class="text-h5" style="color:green">{{$t("Grand Total")}} ({{sale.setting.pos_setting.second_currency_name}}) </div></template>      
      <div class="text-h5" style="color:green"><CurrencyFormat :value="((sale.sale.grand_total * (sale.sale.exchange_rate || 1)) - (sale.sale.deposit * (sale.sale.exchange_rate || 1)))"
                :currency="sale.setting.pos_setting.second_currency_name" /></div>
                
    </ComLabelValue>


    

  </div>

</template>


<script setup>
import { ref, inject, onMounted } from '@/plugin'
import ComLabelValue from "@/views/sale/components/retail_ui/ComLabelValue.vue"
const sale = inject('$sale')
const gv = inject("$gv")
const setting = gv.setting;
const data = ref([]);

onMounted(() => {
  data.value = JSON.parse(JSON.stringify(sale.setting.tax_rules));
})

function getTaxData() {
  if (sale.sale.tax_rule || "" != "") {
    const tax = data.value.filter((r) => r.tax_rule == sale.sale.tax_rule);
    if (tax.length > 0) {
      return JSON.parse(tax[0].tax_rule_data);
    }
  }
  return null
}

</script>