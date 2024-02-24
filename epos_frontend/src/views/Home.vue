<template>  
    <div>    
        <div class="h-60 bg-no-repeat bg-cover"
            v-bind:style="{ 'background-image': 'url(' + gv.setting.home_background + ')','background-position':'center' }"> 
            <div class="wrap-overlay w-full h-full flex items-end justify-center">
                <div>
                    <div class="text-center text-white mb-3">
                        <img :src="gv.setting.logo" class="w-24 inline-block mb-2" />
                        <p class="text-xl">{{ gv.setting.business_branch }}</p>
                        <p>
                            <span class="font-bold">{{ $t('POS Profile') }}</span> : {{ gv.setting.pos_profile }} /
                            <span class="font-bold">{{ $t('Outlet') }}</span> : {{ gv.setting.outlet }} /
                            <span class="font-bold">{{ $t('Device Name') }}</span> :{{ device_name }}
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
        <v-container>
            <div class="pb-16">
                <div class="mx-auto mt-4 mb-0 md:w-[600px]">
                    <ComMessagePromotion />
                    <div class="grid xs:grid-cols-2 md:grid-cols-4 grid-cols-2" style="grid-gap: 20px;">
                        <WorkingDayButton  v-if="device_setting?.show_start_close_working_day==1 && device_setting?.is_order_station==0"/>
                        <OpenShiftButton  v-if="device_setting?.show_start_close_cashier_shift==1 && device_setting?.is_order_station==0"/>
                        
                        
                        <ComButton @click="onPOS()" :title="$t('POS')" icon="mdi-cart-outline" class="bg-green-600 text-white" icon-color="#fff" />
                        <ComButton @click="onViewPendingOrder()" :title="$t('Pending Order')" icon="mdi-arrange-send-backward"  icon-color="#e99417" />

                        <ComButton @click="onReservation()" :title="$t('Reservation')" v-if="(device_setting?.show_button_pos_reservation||0) == 1" icon="mdi mdi-calendar-text-outline" class="bg-teal-600 text-white" icon-color="#fff" />

                        <ComButton @click="onRoute('ClosedSaleList')" :title="$t('Closed Receipt')" v-if="device_setting?.is_order_station==0 && (gv.workingDay || gv.cashierShift)" icon="mdi-file-document"  icon-color="#e99417" />
                        
                        
                        <ComButton @click="onRoute('ReceiptList')" :title="$t('Receipt List')" v-if="device_setting?.is_order_station==0" icon="mdi-file-chart"  icon-color="#e99417" />

                        <ComButton @click="onRoute('Customer')" :title="$t('Customer')" v-if="device_setting?.is_order_station==0" icon-color="#e99417"  icon="mdi-account-multiple-outline" />

                        <ComButton :title="$t('Park Item')" v-if="gv.device_setting.show_park_button" icon-color="#e99417"  icon="mdi-parking" />
                        <ComButton @click="onVoucherTopUp()"  :title="$t('Top-Up Voucher')" v-if="gv.device_setting.show_top_up && !mobile" icon-color="#e99417"  icon="mdi-wallet-plus" />
                        <ComButton @click="onCashInCashOut" :title="$t('Cash Drawer')" v-if="device_setting?.is_order_station==0" icon-color="#e99417" icon="mdi-currency-usd" />
                        <ComButton v-if="isWindow() && device_setting?.is_order_station==0"  @click="onOpenCashDrawer" :title="$t('Open Cash Drawer')" icon="mdi-cash-multiple" icon-color="#e99417" />
                        
                        <ComButton @click="onRoute('Report')" :title="$t('Report')" v-if="device_setting?.is_order_station==0" icon="mdi-chart-bar" icon-color="#e99417" />
                
                        <ComButton v-if="isWindow() && device_setting?.show_button_customer_display==1"  @click="onOpenCustomerDisplay"  :title="$t('Customer Display')" icon="mdi-monitor" icon-color="#e99417" />

                        <ComButton v-if="isWindow()"  @click="onPrintWifiPassword" :title="$t('Wifi Password')" icon="mdi-wifi" icon-color="#e99417" /> 
                        
                        <ComButton @click="onLogout()" text-color="#fff" icon-color="#fff" :title="$t('Logout')" icon="mdi-logout" background-color="#b00020" />
                        
                    </div>
                </div>
            </div>
        </v-container>
    </div>
    
</template>
<script setup>
import { useRouter,SelectDateTime,computed, posReservationDialog, createToaster,pendingSaleListDialog,inject,onMounted,printWifiPasswordModal,i18n } from '@/plugin'
import ComButton from '../components/ComButton.vue';
import WorkingDayButton from './shift/components/WorkingDayButton.vue';
import OpenShiftButton from './shift/components/OpenShiftButton.vue';
import ComMessagePromotion from '../components/ComMessagePromotion.vue';
import moment from '@/utils/moment.js';
import { useDisplay } from 'vuetify'; 

const auth = inject('$auth')
const gv = inject('$gv');
const frappe = inject('$frappe');
const call = frappe.call();
const { mobile } = useDisplay();


const { t: $t } = i18n.global; 
const toaster = createToaster({ position: "top" }); 

const router = useRouter();
const device_setting = JSON.parse(localStorage.getItem("device_setting"));
let already_load_confirm_close_working_day = false;

function isWindow(){
    return localStorage.getItem('is_window') == 1;
}

const device_name = computed(() => {
    return localStorage.getItem('device_name')
})
 
//on init
onMounted(async () => { 
    localStorage.removeItem('make_order_auth');    
    call.get("epos_restaurant_2023.api.api.get_current_working_day",{business_branch: gv.setting?.business_branch})
    .then((_res)=>{
        if(!already_load_confirm_close_working_day){
                if(_res.message){
                already_load_confirm_close_working_day = true;
                gv.confirm_close_working_day(_res.message.posting_date); 
            }
        } 
    });
})


function onRoute(page) {   
    router.push({ name: page })
}

async function onCashInCashOut(){
    await gv.authorize("cash_in_check_out_required_password", "cash_in_check_out").then(async (v) => {
        if (v) {
            router.push({ name: "CashDrawer" });
        }
    });
}

function onPOS() {
    call.get("epos_restaurant_2023.api.api.get_current_shift_information",{
        business_branch: gv.setting?.business_branch,
        pos_profile: localStorage.getItem("pos_profile")
    }).then((_res)=>{
        const _data = _res.message;
        if(_data){
            if (_data.working_day == null) {
                toaster.warning($t("msg.Please start working day first"))
            } else if (_data.cashier_shift == null) {
                toaster.warning($t("msg.Please start shift first"))
            } else {
                if (gv.setting.table_groups.length > 0) {
                    router.push({ name: 'TableLayout' })
                }
                else {
                    gv.authorize("open_order_required_password","make_order").then((v)=>{
                        if(v){  
                            const make_order_auth = {"username":v.username,"name":v.user,discount_codes:v.discount_codes }; 
                            localStorage.setItem('make_order_auth',JSON.stringify(make_order_auth));
                            router.push({ name: 'AddSale' })                            
                        }
                    })                    
                }
            }
        } 
    });
}

function onReservation(){ 
    call.get("epos_restaurant_2023.api.api.get_current_shift_information",{
        business_branch: gv.setting?.business_branch,
        pos_profile: localStorage.getItem("pos_profile")
    }).then(async (_res)=>{
        const _data = _res.message;
        if (_data.working_day == null) {
            toaster.warning($t("msg.Please start working day first"))
        } else if (_data.cashier_shift == null) {
                toaster.warning($t("msg.Please start shift first"))
        } else {
            const today =  moment(new Date()).format('yyyy-MM-DD');
            const result = await posReservationDialog({
            data: {
                working_day:(_data.working_day?.name||""), 
                cashier_shift: (_data.cashier_shift?.name||""), 
                posting_date: (_data.cashier_shift?.posting_date||today)
            }});
        }    
    });
}

function onVoucherTopUp(){
    call.get("epos_restaurant_2023.api.api.get_current_shift_information",{
        business_branch: gv.setting?.business_branch,
        pos_profile: localStorage.getItem("pos_profile")
    }).then((_res)=>{
        const _data = _res.message;
        if(_data){
            if (_data.working_day == null) {
                toaster.warning($t("msg.Please start working day first"))
            } else if (_data.cashier_shift == null) {
                toaster.warning($t("msg.Please start shift first"))
            } else {
                    router.push({ name: 'VoucherTopUp' })
            }
        } 
    });
}

async function onViewPendingOrder() { 
    call.get("epos_restaurant_2023.api.api.get_current_shift_information",{
        business_branch: gv.setting?.business_branch,
        pos_profile: localStorage.getItem("pos_profile")
    }).then(async (_res)=>{
        const _data = _res.message;
        if (_data.working_day == null) {
            toaster.warning($t("msg.Please start working day first"))
        } else if (_data.cashier_shift == null) {
                toaster.warning($t("msg.Please start shift first"))
        } else {
            const result = await pendingSaleListDialog({
                    data: {
                    working_day:(_data.working_day?.name||""), 
                    cashier_shift: (_data.cashier_shift?.name||"")
                }
            });            
        }  
    });
}

function onOpenCustomerDisplay(){
    window.chrome.webview.postMessage(JSON.stringify({ action: "open_customer_display" }));
}

function onLogout() {
    auth.logout().then((r) => {
        router.push({ name: 'Login' })
    })
}
    


async function onPrintWifiPassword(){
    await printWifiPasswordModal({})
}



//open cashdrawer
function onOpenCashDrawer(){
    window.chrome.webview.postMessage(JSON.stringify({action:"open_cashdrawer"}));
} 

</script>
<style scoped>
.wrap-overlay {
    background: rgb(0, 0, 0);
    background: linear-gradient(7deg, rgba(0, 0, 0, 1) 0%, rgba(0, 212, 255, 0) 100%);
}
</style>