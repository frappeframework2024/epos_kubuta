<template>
  <div>
    <div>
      <div class="flex">
        <div class="flex-grow cursor-pointer bg-green-600 text-white pa-2  hover:bg-green-700" @click="onPayment()">
          <div style="margin-bottom: 0px!important;" class="flex justify-between mb-2 text-lg">
            <div  style="margin: 0px; padding: 0px; font-size: 22px">{{ $t("Payment") }}</div>
            <div  style="margin: 0px; padding: 0px; font-size: 28px; font-weight: bold;">
              <CurrencyFormat :value="(sale.sale.grand_total-sale.sale.deposit)" />
            </div>
          </div>
          <div class="flex justify-between">
            <div style="margin: 0px; padding: 0px; font-size: 18px">{{ $t('Total Qty') }} : <span>{{ sale.sale.total_quantity ||0}}</span></div>
            <div style="margin: 0px; padding: 0px; font-size: 22px; font-weight: bold;">
              <CurrencyFormat :value="((sale.sale.grand_total * (sale.sale.exchange_rate || 1)) - (sale.sale.deposit * (sale.sale.exchange_rate || 1)))"
                :currency="sale.setting.pos_setting.second_currency_name" />
            </div>
          </div>
        </div>
        <div style="width: 120px;">
          <div
            class="w-full h-full cursor-pointer flex justify-center items-center bg-blue-600 text-white p-3 hover:bg-blue-700 text-center"
            @click="onSubmit()">
            <div v-if="gv.setting.table_groups && gv.setting.table_groups.length > 0">
              <v-icon icon="mdi-arrow-right-thick"></v-icon>
              <div style="font-size: 18px">{{ $t('Submit Order') }}</div>
            </div>
            <div v-else>
              <v-icon icon="mdi-content-save"></v-icon>
              <div style="font-size: 14px">{{ $t('Save Order') }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { inject, useRouter, paymentDialog,searchSaleDialog, createToaster,i18n } from '@/plugin';
import ComExchangeRate from './ComExchangeRate.vue';
import { whenever,useMagicKeys  } from '@vueuse/core';
const { t: $t } = i18n.global;  

const sale = inject("$sale")
const gv = inject("$gv")
const product = inject("$product")
const tableLayout = inject("$tableLayout");
const router = useRouter();
const toaster = createToaster({ position: 'top' });
const device_setting = JSON.parse(localStorage.getItem("device_setting"))
const frappe = inject("$frappe")
const call = frappe.call();

sale.vue.$onKeyStroke('F12', (e) => {
    e.preventDefault();
    if(gv.device_setting.show_option_payment==0){
        return;
    }
    
    if(sale.dialogActiveState==false){
      onPayment();
    } 
})

const { ctrl_o } = useMagicKeys({
    passive: false,
    onEventFired(e) {
      if (e.ctrlKey && e.key === 'o' && e.type === 'keydown')
        e.preventDefault()
    },
})
const { ctrl_s } = useMagicKeys({
    passive: false,
    onEventFired(e) {
      if (e.ctrlKey && e.key === 's' && e.type === 'keydown')
        e.preventDefault()
    },
})

whenever(ctrl_o, () => onSearchSale())
whenever(ctrl_s, () => onSubmit())




const setting = JSON.parse(localStorage.getItem("setting"))
async function onSearchSale(){
    sale.dialogActiveState=true;
    let msg = $t('msg.please save or submit your current order first',[(setting.table_groups && setting.table_groups.length > 0 ? $t( 'Submit') : $t('Save'))]);
    const isOrdered = sale.isOrdered(msg)    
    if(isOrdered == false) {
        const result = await searchSaleDialog({ })
        sale.dialogActiveState=false;
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

async function onSubmit() {
  if (!sale.isBillRequested()) {
    const action = sale.action;
    const message = sale.message;
    const sale_status = sale.sale.sale_status; 
    sale.action = "submit_order";
    sale.message = $t("msg.Submit order successfully");
    sale.sale.sale_status = "Submitted"; 
   
    await sale.onSubmit().then((doc) => {
      product.onClearKeyword(); 
      if (doc) {
        if (onRedirectSaleType()) {
          if (tableLayout.table_groups.length > 0) {
            sale.sale = {};
            router.push({ name: 'TableLayout' })
          }
          else {
            
            sale.newSale()
            router.push({ name: "AddSale" });
            sale.tableSaleListResource.fetch();

            call.get('epos_restaurant_2023.api.api.get_current_shift_information',{
              business_branch: sale.setting?.business_branch,
              pos_profile: localStorage.getItem("pos_profile")
              }).then((data)=>{
                if (data.message.cashier_shift == null) {
                  toaster.warning($t("msg.Please start shift first"));
                  router.push({ name: "OpenShift" });
              } else if (data.message.working_day == null) {
                  toaster.warning($t('msg.Please start working day first'));
                  router.push({ name: "StartWorkingDay" });
              } else {
                  sale.sale.working_day = data.message.working_day.name;
                  sale.sale.cashier_shift = data.message.cashier_shift.name;
                  sale.sale.shift_name = data.message.cashier_shift.shift_name;
                  gv.confirm_close_working_day(data.message.working_day.posting_date);
              }
            })
          }
        }
      }else{ 
        sale.action =  action;
        sale.message = message;
        sale.sale.sale_status =  sale_status;
      }
    });
  }
}



async function onPayment() {
  sale.dialogActiveState=true
  if (device_setting.show_option_payment==0){
    return
  }

  if (sale.sale.sale_products.length == 0) {
    toaster.warning($t('msg.Please select a menu item to process payment'));
    return
  }

  const check_employee = sale.sale.sale_products.filter((sp)=>sp.is_require_employee && (JSON.parse(sp.employees||"[]")).length <=0)
  if(check_employee.length> 0){
      toaster.warning($t('msg.Please assign employee to items'));
      return;
  }
  
  const check_stop_timer = sale.sale.sale_products.filter((sp)=>sp.is_timer_product && !sp.time_out_price )

  if(check_stop_timer.length> 0){
      toaster.warning($t('msg.Please stop timer on timer product'));
      return;
  }
  
  const result = await paymentDialog({})
  sale.dialogActiveState=false
  if (result) { 
    
    product.onClearKeyword()
    sale.newSale();
    if (onRedirectSaleType()) {
      if (sale.setting.table_groups.length > 0) {
        router.push({ name: "TableLayout" });
      } else {
        sale.tableSaleListResource.fetch();
        router.push({ name: "AddSale" });
      }
    }
  }
}

function onRedirectSaleType() {
  const redirect_sale_type = localStorage.getItem("redirect_sale_type") || null
  if (redirect_sale_type) {
    router.push({ name: 'AddSaleNoTable', params: { sale_type: redirect_sale_type } })
    return false
  }
  return true
}
</script>
<style lang="">

</style>