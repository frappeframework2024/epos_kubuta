<template>
    <v-list class="!p-0">
        <v-list-item v-for="sp, index in (readonly == true ? getSaleProducts(groupKey) : sale.getSaleProducts(groupKey))" 
            :key="index" @click="!readonly ? { click: sale.onSelectSaleProduct(sp) } : {}"
            class="!border-t !border-gray-300 !mb-0 !p-2"
            :class="{ 'selected': (sp.selected && !readonly), 'submitted relative': sp.sale_product_status == 'Submitted', 'item-list': !readonly }">
            <template v-slot:prepend>
                <v-avatar v-if="sp.product_photo">
                    <v-img :src="sp.product_photo"></v-img>
                </v-avatar>
                <avatar v-else :name="sp.product_name" class="mr-4" size="40"></avatar>
                
            </template>
            <template v-slot:default>
                <div class="text-sm">
                    <div class="flex">
                        <div class="grow">
                            <div style="white-space: pre-wrap;" v-if="!sale.load_menu_lang"> {{ getMenuName(sp) }}<v-chip class="ml-1" size="x-small"
                                    color="error" variant="outlined" v-if="sp.portion">{{ sp.portion }}</v-chip>
                                <v-chip v-if="sp.is_free" size="x-small" color="success" variant="outlined">{{ $t('Free')
                                }}</v-chip>
                                <v-chip v-if="sp.is_park" size="x-small" color="error" variant="outlined">
                                {{ $t('Park') }}</v-chip>
                                <ComChip :tooltip="sp.happy_hours_promotion_title"
                                    v-if="sp.happy_hour_promotion && sp.discount > 0" size="x-small" variant="outlined"
                                    color="orange" text-color="white" prepend-icon="mdi-tag-multiple">
                                    <span>{{ sp.discount }}%</span>
                                </ComChip>
                                <ComHappyHour :saleProduct="sp" v-if="sp.is_render" />
                            </div>
                            
                            <div v-if="!sp.is_timer_product">
                                {{ sp.quantity }} x 
                                <CurrencyFormat :value="sp.price" />
                                <span class="font-weight-black"> / </span>
                                <CurrencyFormat :value="(sp.price*sale.sale.exchange_rate)"
                                    :currency="sale.setting.pos_setting.second_currency_name" />
                                
                            </div>
                            <div v-else>
                                <template v-if="sp.time_in">
                                    {{$t("Time In")}}: {{ moment(sp.time_in).format('hh:mm A') }}
                                    <span v-if="sp.time_out">
                                        {{$t("Time Out")}}
                                         {{ moment(sp.time_out).format('hh:mm A') }}
                                    </span>
                                    
                                </template>
                               
                            </div>
                            <div class="text-xs pt-1">
                                <div v-if="sp.modifiers && !sp.is_timer_product">
                                    <span>{{ sp.modifiers }} (
                                        <CurrencyFormat :value="sp.modifiers_price * sp.quantity" />)
                                       
                                    </span>
                                </div>

                                <div v-if="sp.is_combo_menu">
                                    <div v-if="sp.use_combo_group && sp.combo_menu_data">
                                        <ComSaleProductComboMenuGroupItemDisplay :combo-menu-data="sp.combo_menu_data" />
                                    </div>
                                    <span v-else>{{ sp.combo_menu }}</span>
                                </div>
                                <div v-if="sp.discount > 0 && !sp.is_free">
                                    <span class="text-red-500">
                                        {{ $t('Discount') }} :
                                        <span v-if="sp.discount_type == 'Percent'">{{ sp.discount }}%</span>
                                        <CurrencyFormat v-else :value="parseFloat(sp.discount)" />
                                    </span>
                                </div>

                                <div v-if="(sp.is_require_employee || 0) == 1">
                                    <span v-for="emp, idx in getEmployees(sp.employees)" :key="idx" class="text-gray-500">
                                        <v-chip class="m-0.5" size="x-small" variant="outlined" color="primary"
                                            text-color="white">
                                            {{ emp.employee_display_name }}
                                        </v-chip>
                                    </span>

                                </div>
                                <v-chip color="blue" size="x-small" v-if="sp.seat_number"> {{ $t('Seat') + "# " + sp.seat_number
                                }}</v-chip>
                                <div class="text-gray-500" v-if="sp.note">
                                    {{ $t('Note') }}: <span>{{ sp.note }}</span>
                                </div>
                                <div class="text-gray-500" v-if="sp.is_park">
                                    {{ $t('Expiry') + ": " + moment(sp.expired_date).format('DD-MM-yyyy')  }}
                                </div>
                            </div>
                        </div>

                        <div class="flex-none text-right">
                            <div class="text-lg">
                                
                                <ComTimerProductEstimatePrice v-if="sp.is_timer_product && !sp.time_out_price" :saleProduct="sp" />
                                <div v-else>
                                    <CurrencyFormat  :value="(sp.amount - sp.total_tax)" />
                                    <span> / </span>
                                    <CurrencyFormat  :value="((sp.amount - sp.total_tax) * sale.sale.exchange_rate)" :currency="gv.setting.pos_setting.second_currency_name"/>
                                </div>
                                
                            </div>
                            <span v-if="sp.product_tax_rule && sp.total_tax > 0" class="text-xs">
                                {{ $t('Tax') }}:
                                <CurrencyFormat :value="sp.total_tax" />
                            </span>
                            
                            <ComQuantityInput v-if="!readonly" :sale-product="sp" />
                        </div>
                    </div>

                    <div v-if="sp.selected && !readonly" class="-mx-1 flex pt-1">
                        <template v-if="sp.is_timer_product" >
                            <!-- start time  -->
                            <v-chip color="green"  v-if="!sp.time_out && !sp.reference_sale_product" class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                                @click="onStartTime(sp)">{{ $t('Start Timer') }}</v-chip>
                            <!-- stop time -->
                            <v-chip color="orange"  v-if="sp.name && sp.time_in && !sp.time_out && !sp.reference_sale_product" class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                                @click="onStopTimer(sp)">{{ $t('Stop Timer') }}</v-chip>

                            <v-chip color="green" v-if="sp.time_out" class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                                @click="onContinueTimer(sp)">{{ $t('Continue Timer') }}</v-chip>
                        </template>
                        

                        <v-chip v-if="show_button_change_price && !sp.is_timer_product" color="teal"
                            class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                            @click="sale.onChangePrice(sp, gv, numberFormat)">{{ $t('Price') }}</v-chip>

                        <template v-if="(sp.is_require_employee || 0) == 0 && !sp.is_timer_product">
                            <v-chip
                                :disabled="sale.setting.pos_setting.allow_change_quantity_after_submit == 0"
                                color="teal" class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                                @click="sale.onChangeQuantity(sp)">{{ $t('Qty') }}</v-chip>

                            <!-- <v-chip color="teal" class="mx-1 grow text-center justify-center" variant="elevated"
                                size="small" @click="onReorder(sp)">{{ $t('Re-Order') }}</v-chip> -->
                        </template>
                        <template v-if="(sp.is_require_employee || 0) == 1">
                            <v-chip color="primary" class="mx-1 grow text-center justify-center" variant="elevated"
                                size="small" @click="sale.onAssignEmployee(sp)">{{ $t('Employee') }}</v-chip>
                        </template>

                        <v-chip v-if="!sp.reference_sale_product" color="red" class="mx-1 grow text-center justify-center" variant="elevated" size="small"
                            @click="sale.onRemoveItem(sp, gv, numberFormat)">{{ $t('Delete') }}</v-chip>

                        <ComSaleProductButtonMore :sale-product="sp" />
                    </div>


                </div>

            </template>
        </v-list-item>
    </v-list>
</template>
<script setup>
import { computed, inject, defineProps,confirmDialog, createToaster, i18n, ref, SelectDateTime,stopTimerModal } from '@/plugin'

import ComSaleProductButtonMore from './ComSaleProductButtonMore.vue';
import ComQuantityInput from '../../../components/form/ComQuantityInput.vue';
import Enumerable from 'linq';
import ComSaleProductComboMenuGroupItemDisplay from './combo_menu/ComSaleProductComboMenuGroupItemDisplay.vue';
import ComHappyHour from './happy_hour_promotion/ComHappyHour.vue';
import ComTimerProductEstimatePrice from '@/views/sale/components/ComTimerProductEstimatePrice.vue';

const { t: $t } = i18n.global;
const numberFormat = inject('$numberFormat');
const sale = inject('$sale');
const product = inject('$product');
const gv = inject('$gv');
const moment = inject('$moment');
const toaster = createToaster({ position: 'top' });
const frappe = inject("$frappe")
const call = frappe.call()

const props = defineProps({
    groupKey: Object,
    readonly: Boolean,
    saleCustomerDisplay: Object
});


function getMenuName(sp) {
    const mlang = localStorage.getItem('mLang');
    let code = gv.setting.show_item_code_in_sale_screen == 0 ? "" : sp.product_code_2 ? `${sp.product_code} / ${sp.product_code_2} - `:`${sp.product_code} - `;
    let shelf_name = sp.shelf_name ? `\n${sp.shelf_name}` : ""
    if (mlang != null) {
        if (mlang == "en") {
            return `${code}${sp.product_name}${shelf_name}`;
        } else {
            return `${code}${sp.product_name_kh}${shelf_name}`;
        }

    } else {
        localStorage.setItem('mLang', 'en');
        return `${code}${sp.product_name}`;
    }
}

const show_button_change_price = computed(() => {
    if (gv.device_setting.is_order_station == 1 && gv.device_setting.show_button_change_price_on_order_station == 1) {
        return true;
    }
    else if (gv.device_setting.is_order_station == 0) {
        return true;
    }

    return false;
});

function onReorder(sp) {
    if (!sale.isBillRequested()) {
        const u = JSON.parse(localStorage.getItem('make_order_auth'));
        let is_append = false;
        let prev_sale_product = JSON.parse(JSON.stringify(sp));

        if ((sp.sale_product_status == "New" && sp.append_quantity == 1) || sale.setting.pos_setting.allow_change_quantity_after_submit == 1) {
            sale.updateQuantity(sp, sp.quantity + 1);
            is_append = true;
        } else {
            let strFilter = `$.product_code=='${sp.product_code}' && $.append_quantity ==1 && $.price==${sp.price} && $.portion=='${sp.portion}'  && $.modifiers=='${sp.modifiers}'  && $.unit=='${sp.unit}'  && $.is_free==0`

            if (!gv.setting?.pos_setting?.allow_change_quantity_after_submit) {
                strFilter = strFilter + ` && $.sale_product_status == 'New'`
            }
            const sale_product = Enumerable.from(sale.sale.sale_products).where(strFilter).firstOrDefault();
            if (sale_product != undefined) {
                sale_product.quantity = parseFloat(sale_product.quantity) + 1;
                sale.updateSaleProduct(sp);
                is_append = true;

            } else {
                setTimeout(() => {
                    sale.cloneSaleProduct(sp, sp.quantity + 1);
                }, 100);
            }
        } 

        if (is_append) {

            let item_description = `${sp.product_code}-${sp.product_name}${(sp.portion || "") == "" ? "" : `(${sp.portion})`} ${sp.modifiers}`;
            let msg = `${u.name} was append a quantity to item: ${item_description} (from ${prev_sale_product.quantity} to ${sp.quantity})`;
            sale.auditTrailLogs.push({
                doctype: "Comment",
                subject: "Append Quantity",
                comment_type: "Info",
                reference_doctype: "Sale",
                reference_name: "New",
                comment_by: u.name,
                content: msg,
                custom_item_description: `${(sp.quantity||0) - prev_sale_product.quantity} x ${item_description}`,
                custom_note: "",
                custom_amount: (sp.amount / ((sp.quantity||0)==0?1:sp.quantity)) * ((sp.quantity||0) - prev_sale_product.quantity)
            });
        }
    }
}

function getSaleProducts(groupByKey) {
    if (props.saleCustomerDisplay && props.saleCustomerDisplay.sale_products) {
        if (groupByKey) {
            return Enumerable.from(props.saleCustomerDisplay.sale_products).where(`$.order_by=='${groupByKey.order_by}' && $.order_time=='${groupByKey.order_time}'`).orderByDescending("$.modified").toArray()
        } else {
            return Enumerable.from(props.saleCustomerDisplay.sale_products).orderByDescending("$.modified").toArray();
        }
    }
    return [];
}



function getEmployees(data) {
    if ((data || "") != "") {
        const result = JSON.parse(data);
        if (result) {
            if (result.length > 0) {
                result.forEach((e) => {
                    e.employee_display_name = e.employee_name + '(' + e.duration_title + ')';
                })
            }
        }
        return result;
    }
    return []
}

async function onStartTime(sp) { 
    if((sp.name||"")!="" && (sp.time_in||"")!=""){
        gv.authorize("", "change_item_time_in").then(async (res) => {
            if (res) {   
                _onStartTimer(sp);
            }
        });
    }else{
        _onStartTimer(sp);
    }
    
}

async function _onStartTimer(sp){
    let selectdatetime = await SelectDateTime({"time_in":sp.time_in});
            if (selectdatetime) {
                if (selectdatetime !='Set Later'){
                    sp.time_in = moment(selectdatetime).format('yyyy-MM-DD HH:mm:ss');
                }else{
                    sp.time_in= undefined;
                }
                
            }
}
async function onStopTimer(sp) {
    if((sp.name||"")!="" && (sp.time_out||"")!=""){
        gv.authorize("", "change_item_time_out").then(async (res) => {
            if (res) {   
                _onStopTimer(sp);
            }
        });
    }else{
        _onStopTimer(sp);
    }
}
async function _onStopTimer(sp){
    if (sale.sale.sale_products.filter(r=>!r.name).length>0){
        toaster.warning($t('msg.Please submit your order first'));
        return
    }

    let stopTimer= await stopTimerModal(sp)
    if(stopTimer){
        sp.time_in = stopTimer.time_in
        sp.time_out = stopTimer.time_out
    }
}
async function onContinueTimer(sp){
    if (!sale.isBillRequested()) {
    if (sale.sale.sale_products.filter(r=>!r.name).length>0){
        toaster.warning($t('msg.Please submit your order first'));
        return
    }

    if (await confirmDialog({ title: $t("Continue Timer"), text: $t("msg.Are you sure to continue timer") })) {
        sale.loading=true;
        call.post("epos_restaurant_2023.api.timer_product.continue_timer", { sale_product: sp  }).then(async (result) =>  {
            sp.time_out = undefined;
            sale.sale = result.message
            sale.loading=false;
        }).catch((err)=>{
            sale.loading=false;
        })
    }
    
}
}

</script>


<style scoped>
.selected,
.item-list:hover {
    background-color: #ffebcc !important;
}

.submitted::before {
    content: '';
    position: absolute;
    top: 1px;
    bottom: 1px;
    left: 0px;
    width: 2px;
    background: #75c34a;
    border-radius: 12px;
}
</style>
 