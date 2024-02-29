<template>
    <ComModal :persistent="true" @onClose="onClose()" @onOk="onOK()" title-ok-button="OK" :fullscreen="mobile">
        <template #title>
            <div>{{$t('Product Stock')}}</div>
        </template>
        <template #content>
            <v-table fixed-header class="ma-2">
              <thead>
                <tr>
                  <th class="text-center">
                    {{ $t('Product Code') }}
                  </th>
                  <th class="text-center">
                    {{ $t('Stock Location') }}
                  </th>
                  <th class="text-center">
                    {{ $t('Quantity') }}
                  </th>
                  <th class="text-center">
                    {{ $t('Unit') }}
                  </th>
                </tr>
              </thead>
              <tbody >
                <tr v-for=" d in stock_product">
                  <td class="text-center">{{ d.product_code }}</td>
                  <td class="text-center">{{ d.stock_location }}</td>
                  <td class="text-center">{{ d.quantity }}</td>
                  <td class="text-center">{{ d.unit }}</td>
                </tr>
              </tbody>
            </v-table>
        </template>
    </ComModal>
</template>
<script setup>
import { ref, defineEmits,i18n,inject } from '@/plugin'
import { onMounted } from 'vue';
import { useDisplay } from 'vuetify';
const { t: $t } = i18n.global; 
const frappe = inject("$frappe");
const call = frappe.call();
const props = defineProps({
    params:Object
})
let stock_product=ref([])
onMounted(async ()=>{
   await call.get("epos_restaurant_2023.api.product.get_product_stock",{product_code:props.params.data.sale_product.product_code})
  .then((res)=>{
    stock_product.value = res.message;
    
  })
})

const emit = defineEmits(['resolve'])
const { mobile } = useDisplay()
function onClose() {
    emit('resolve',false)
}
</script>