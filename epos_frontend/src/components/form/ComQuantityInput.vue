<template>
    <div v-if="!saleProduct.is_timer_product">
    
     
        <v-chip class="ml-1 mb-1" size="small" color="error" v-if="saleProduct.deleted_quantity > 0 && gv.device_setting.show_deleted_sale_product_in_sale_screen==1" variant="outlined">{{ `${$t('QTY Deleted')}: ${saleProduct.deleted_quantity}` }} </v-chip>
        

        <v-btn
            v-if="(saleProduct.sale_product_status == 'New' && saleProduct.append_quantity==1 && saleProduct.is_require_employee==0) || sale.setting.pos_setting.allow_change_quantity_after_submit == 1"
            color="error" size="x-small" variant="tonal" icon="mdi-arrow-down"
            @click="onUpdateQuantity(-1)"
            :disabled="saleProduct.quantity == 1 "></v-btn>        
            
        <v-btn class="mx-1" size="small" variant="tonal" @click="onChangeQuantity">{{
            saleProduct.quantity }}</v-btn>

        <v-btn
            v-if="(saleProduct.sale_product_status == 'New' && saleProduct.append_quantity==1 && saleProduct.is_require_employee==0 )|| sale.setting.pos_setting.allow_change_quantity_after_submit == 1"
            color="success" size="x-small" variant="tonal" icon="mdi-arrow-up"
            @click="onUpdateQuantity(1)"></v-btn>
    </div>
    <div v-else>
         
       

        <div v-if="saleProduct.time_in && !saleProduct.time_out_price">
            <span>{{stopwatch.hours.toString().padStart(2, '0') }}h</span>:<span>{{stopwatch.minutes.toString().padStart(2, '0')}}mn</span>:<span>{{stopwatch.seconds}}s</span>
        </div>
        <v-btn v-else class="mx-1" size="small"  variant="tonal">{{
            saleProduct.duration }}</v-btn>
      
    </div>
</template>
<script setup>
import { inject,i18n,computed,watch  } from '@/plugin'
import {createToaster} from '@meforma/vue-toaster';
import { useStopwatch } from 'vue-timer-hook';




const numberFormat = inject('$numberFormat');
const { t: $t } = i18n.global;  
const toaster = createToaster({ position: "top" })
const props = defineProps({
    saleProduct: Object
})
const sale = inject("$sale");
const gv = inject("$gv");
const autoStart = !props.saleProduct.time_out
const stopwatch = useStopwatch(autoStart);

if (props.saleProduct.is_timer_product){ 
    let time_in = new Date(props.saleProduct.time_in)
    if (!time_in){
        time_in = new Date()
    }
    const duration = getTimeDiff( time_in,  new Date())
    stopwatch.hours = duration.hours
    stopwatch.minutes = duration.minutes

}

watch(() => props.saleProduct.time_in, (newValue, oldValue) => {
    let time_in = new Date(props.saleProduct.time_in)
    if (!time_in){
        time_in = new Date()
    }
    const duration = getTimeDiff( time_in,  new Date())
    stopwatch.hours = duration.hours
    stopwatch.minutes = duration.minutes
});

watch(() => props.saleProduct.time_out, (newValue, oldValue) => {
    if (props.saleProduct.time_out){
        const duration = getTimeDiff( new Date(props.saleProduct.time_in),  new Date(props.saleProduct.time_out))
        stopwatch.hours = duration.hours
        stopwatch.minutes = duration.minutes

        setTimeout(function(){
            stopwatch.pause()
        },1000)
              
    }else{
        const duration = getTimeDiff(new Date(props.saleProduct.time_in),  new Date())
        stopwatch.hours = duration.hours
        stopwatch.minutes = duration.minutes
        stopwatch.start()
    }
});



//Add Key stroke
sale.vue.$onKeyStroke('PageUp', (e) => {
    e.preventDefault()
    if (props.saleProduct.selected && props.saleProduct.is_require_employee==0) {
        sale.updateQuantity(props.saleProduct, props.saleProduct.quantity + 1)
    }
})
sale.vue.$onKeyStroke('PageDown', (e) => {
    e.preventDefault()
    if (props.saleProduct.selected && props.saleProduct.quantity > 1 && props.saleProduct.is_require_employee==0) {
        sale.updateQuantity(props.saleProduct, props.saleProduct.quantity - 1)
    }
})

if (props.saleProduct.selected) {
    sale.vue.$onKeyStroke('F3', (e) => {
        e.preventDefault()
        if (props.saleProduct.selected && sale.dialogActiveState == false) {
            sale.dialogActiveState = true;
            sale.onChangeQuantity(props.saleProduct, gv)
        }
    })
}

const allow_change_price = computed(()=>{
    if(gv.device_setting.is_order_station == 1 && gv.device_setting.show_button_change_price_on_order_station==1)
    {
        return true;
    }
    else if(gv.device_setting.is_order_station==0 ){
        return true;
    }

    return false;
});

sale.vue.$onKeyStroke('F4', (e) => {
    e.preventDefault();
    if(!allow_change_price){
        return;
    }    
   
    if (props.saleProduct.selected && sale.dialogActiveState == false) {
        sale.dialogActiveState = true;
        sale.onChangePrice(props.saleProduct,gv, numberFormat);
    }
})

sale.vue.$onKeyStroke('F5', (e) => {
    e.preventDefault();

    if(gv.device_setting.is_order_station==1){
        return;
    }
    
    onDiscountClick("Percent")
})


sale.vue.$onKeyStroke('F6', (e) => {
    e.preventDefault();
    if(gv.device_setting.is_order_station==1){
        return;
    }

    onDiscountClick("Amount")
})

sale.vue.$onKeyStroke('F7', (e) => {
    e.preventDefault();  
    if(gv.device_setting.is_order_station==1){
        return;
    }
    
    if(props.saleProduct.selected && sale.dialogActiveState == false){
        
        if(!props.saleProduct.is_free){
            onSaleProductFree(props.saleProduct);
            
        }else{
            sale.onSaleProductCancelFree(props.saleProduct)
            toaster.warning($t('msg.This item is not allow to discount'));
        }
    }
    
})


function onUpdateQuantity(param){
   if((sale.sale.is_return??0) == 1)
   {
    if(props.saleProduct.quantity>=-1 && param == -1){
        return
    }
    sale.updateQuantity(props.saleProduct, props.saleProduct.quantity - param)
   }
   else
   {
    if(props.saleProduct.quantity<=1 && param == -1){
        return
    }
    sale.updateQuantity(props.saleProduct, props.saleProduct.quantity + param)
   }
    
}

function onDiscountClick(discount_type){
    if (props.saleProduct.selected && sale.dialogActiveState == false) {
        sale.dialogActiveState=true;
        if (props.saleProduct.allow_discount) {
            if (!sale.isBillRequested()) {
                gv.authorize("discount_item_required_password", "discount_item", "discount_item_required_note", "Discount Item Note", "", true).then((v) => {
                    if (v) {
                        sale.onDiscount(
                            gv,
                            `${props.saleProduct.product_name} Discount`,
                            props.saleProduct.amount,
                            props.saleProduct.discount,
                            discount_type,
                            v.discount_codes,
                            props.saleProduct.discount_note,
                            props.saleProduct,
                            v.category_note_name
                        );
                    }
                });

            }
        }
        else {
            toaster.warning($t('msg.This item is not allow to discount'));
        }
    }
}

function onSaleProductFree() {
    if (!sale.isBillRequested()) {
        gv.authorize("free_item_required_password", "free_item", "free_item_required_note", "Free Item Note", props.saleProduct.product_code).then((v) => {
            if (v) {
                props.saleProduct.free_note = v.note
                sale.dialogActiveState = true;
                sale.onSaleProductFree(props.saleProduct);
            }
        });

    }
}


function onChangeQuantity(){ 
    const sp = props.saleProduct;
    if(sp.append_quantity==1){
        if(sale.setting.pos_setting.allow_change_quantity_after_submit == 1 || sp.sale_product_status == 'Submitted' || sp.is_require_employee==1){
            return;
        }
        sale.onChangeQuantity(sp, gv);
    }
}

function getTimeDiff(startDate,endDate){
    const diffInMs = Math.abs(endDate - startDate);
    const diffInHrs = Math.floor((diffInMs / (1000 * 60 * 60)) % 24);
    const diffInMins = Math.floor((diffInMs / (1000 * 60)) % 60);
    const diffInSecs = Math.floor((diffInMs / 1000) % 60);
    return {
        hours: diffInHrs,
        minutes:diffInMins,
        seconds:diffInSecs
    }


}
</script>
<style lang="">
    
</style>