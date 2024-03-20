<template >
    <v-btn v-if="(sale.tableSaleListResource?.data?.length||0)>0" class="text-none" stacked :size="mobile ? 'x-small' : 'small'" @click="onSearchSale">
        <v-badge :content="counter" color="success">
            <v-icon>mdi-cart</v-icon>
        </v-badge>
    </v-btn>
</template>
<script setup>
import { useDisplay } from 'vuetify'
import {searchSaleDialog, inject,useRouter,i18n} from '@/plugin';
import { onMounted, ref ,onUpdated} from 'vue';
const { t: $t } = i18n.global;
// import { createToaster } from '@meforma/vue-toaster'; 
const { mobile } = useDisplay()
const sale = inject('$sale')
const router = useRouter();
const counter = ref(0)
// const socket = inject('$socket');
// const toaster = createToaster({position:"top"});
onUpdated(()=>{
    counter.value = sale.tableSaleListResource?.data?.filter(a=>a.name != sale.sale.name).length
})

const setting = JSON.parse(localStorage.getItem("setting"))
async function onSearchSale(){
    let msg = $t('msg.please save or submit your current order first',[(setting.table_groups && setting.table_groups.length > 0 ? $t( 'Submit') : $t('Save'))]);
    const isOrdered = sale.isOrdered(msg)    
    if(isOrdered == false) {
        const result = await searchSaleDialog({ })
        counter.value = sale.tableSaleListResource?.data?.filter(a=>a.name != result.name).length
        if(result != false){ 
            router.push({
                name: "AddSale", params: {
                    name: result.name
                }
            });
            sale.LoadSaleData(result.name)
        }
    }
}
</script>