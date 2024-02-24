
<template>
    <ComModal  :fullscreen="mobile" @onClose="onClose" width="1200px" :hideOkButton="true" :hideCloseButton="true">
        <template #title>
            {{ $t('Table') }}#: {{ params.table.tbl_no }}
        </template>
        <template #content>
            <ComLoadingDialog v-if="isLoading" />
            <ComPlaceholder :is-not-empty="params.data.length > 0">
                <v-row class="!-m-1">
                    <v-col class="!p-0" cols="12" md="6" v-for="(s, index) in params.data" :key="index">
                        <ComSaleListItem :sale="s" @click="openOrder(s)" />
                    </v-col>
                </v-row>
            </ComPlaceholder>
        </template>
        <template #action>
            <ComSelectSaleOrderAction
                :isDesktop="isDesktop"
                :is-bill-requested="isDesktop && params.data.filter(r =>r.sale_status == 'Bill Requested' ).length > 0"
                @onClose="onClose"
                @onNewOrder="onNewOrder"
                @onQuickPay="onQuickPay"
                @onPrintAllBill="onPrintAllBill"
                @onCancelPrintBill="onCancelPrintBill"
                />
        </template>
    </ComModal>
    
</template>
<script setup>
import { inject, ref, useRouter, confirmDialog,  createDocumentResource ,createResource,smallViewSaleProductListModal,i18n,onMounted } from '@/plugin'
import { useDisplay } from 'vuetify'
import ComSaleListItem from './ComSaleListItem.vue';
import ComLoadingDialog from '@/components/ComLoadingDialog.vue';
import { createToaster } from "@meforma/vue-toaster";
import ComSelectSaleOrderAction from './ComSelectSaleOrderAction.vue';

const { t: $t } = i18n.global; 

const isLoading = ref(false);
const { mobile } = useDisplay()
const sale = inject("$sale")
const frappe = inject("$frappe")
const gv = inject("$gv")
const tableLayout = inject("$tableLayout")
const router = useRouter()
const toaster = createToaster({ position: "top" });
const isDesktop = localStorage.getItem('is_window');
const emit = defineEmits(["resolve"]);

const db = frappe.db();
const call = frappe.call();
const payment_promises = ref([])

const props = defineProps({
    params: {
        type: Object,
        require: true
    }
});




async function onPrintAllBill(r) {
    if (r.pos_receipt_file_name == null) {
        toaster.warning($t('msg.This receipt have not POS receipt file'));
        return;
    }
    if (props.params.data.filter(r => r.sale_status == "Submitted").length == 0) {
        toaster.warning($t('msg.All receipts were printed'));
        return;
    }

    if (await confirmDialog({ title:$t('Print all Receipts'), text:$t('msg.are you sure to print all receipts') })) {
        let promises = [];
        isLoading.value = true;
        props.params.data.filter(r => r.sale_status == "Submitted").forEach(async (d) => {
            promises.push(PrintReceipt(d, r));
        });
        
        Promise.all(promises).then(() => {
            toaster.success($t('msg.All receipts has been sent to printer successfully'));
            tableLayout.getSaleList();
            isLoading.value = false;
            emit('resolve', true);
        })
    }

}

async function onQuickPay(isPrint=true) {
     if (props.params.data.filter(r => r.sale_status == "Submitted" || r.sale_status == "Bill Requested" ).length == 0) {
        toaster.warning($t("msg.There are no bills to settle"));
        return;
    }

    if (await confirmDialog({ title: $t("Quick Pay"), text: $t('msg.are you sure to process quick pay and close order') })) {
        isLoading.value = true;
        
        props.params.data.filter(r => r.sale_status == "Submitted" || r.sale_status == "Bill Requested").forEach(async (d) => {
       
            payment_promises.value.push({
                sale:d.name,
                payment_type: sale.setting?.default_payment_type
            })                 
        });
        Promise.all(payment_promises.value).then(async () => {
            await call.get('epos_restaurant_2023.api.api.on_sale_quick_pay', {
                data:JSON.stringify(payment_promises.value)
            }).then((res)=>{
                props.params.data.filter(r => r.sale_status == "Submitted" || r.sale_status == "Bill Requested").forEach(async (d) =>{ 
                    const _sale = res.message.filter((r)=>r.name == d.name)
                    if(_sale.length>0){
                        d.sale_status = "Closed";
                        d.sale_status_color = sale.setting.sale_status.find(r => r.name == 'Closed').background_color;
                        const data = {
                            action: "print_receipt",
                            print_setting:  sale.setting?.default_pos_receipt,
                            setting: sale.setting?.pos_setting,
                            sale: _sale[0]
                        }
                        if (localStorage.getItem("is_window") == "1" && isPrint) {
                            window.chrome.webview.postMessage(JSON.stringify(data));
                        } 
                    }                   
                });


                toaster.success($t('msg.Payment successfully'));
                tableLayout.getSaleList();            
                isLoading.value = false;
                emit('resolve', true);
            }).catch((r)=>{
                toaster.error(r.message); 
                isLoading.value = false;
            }); 
           
        })        
    }
}
async function PrintReceipt(d, r) {
    const resource = createResource({
        url: 'frappe.client.get',
        params: {
            doctype: "Sale",
            name: d.name
        },
        async onSuccess(doc) {
            if (doc.sale_products.length > 0) {
                const data = {
                    action: "print_receipt",
                    print_setting: r,
                    setting: sale.setting?.pos_setting,
                    sale: doc
                }

                if (localStorage.getItem("is_window") == "1") {
                    window.chrome.webview.postMessage(JSON.stringify(data));
                }
            }
            d.sale_status = "Bill Requested";
        },
    });

    await resource.fetch().then(async (doc) => {
        if (doc) {
            const updateResource = createResource({
                url: 'epos_restaurant_2023.api.api.update_print_bill_requested',
                params: {
                    name: doc.name
                }
            });
            await updateResource.fetch();
        }
    });

}



async function onCancelPrintBill() {
    if (props.params.data.filter(r => r.sale_status == "Bill Requested").length == 0) {
        toaster.warning($t('msg.There are no bills to cancel print'));
        return;
    }

    gv.authorize("cancel_print_bill_required_password", "cancel_print_bill", "cancel_print_bill_required_note", "Cancel Print Bill Note").then((v) => {
        if (v) {
            isLoading.value = true;
            const promises = [];
            props.params.data.filter(r => r.sale_status == "Bill Requested").forEach(async (d) => {
                promises.push(submitCancelPrintBill(d));
            });

            Promise.all(promises).then(() => {
                toaster.success($t('msg.Cancel print successfully'));
                tableLayout.getSaleList();
                isLoading.value = false;               
            });
        }
    })

}


async function submitCancelPrintBill(d){
    const resource = createDocumentResource({
        doctype: "Sale",
        name: d.name,
    });
    await resource.get.fetch().then(async (v)=>{
		await resource.setValue.submit({
            sale_status:'Submitted'
        }).then((data)=>{
            d.sale_status = "Submitted";
            d.sale_status_color = sale.setting.sale_status.find(r => r.name == 'Submitted').background_color;
        });
	})
}

async function openOrder(s) {
    if(mobile.value){
        await sale.LoadSaleData(s.name).then(async (v)=>{
            localStorage.setItem('make_order_auth',JSON.stringify(props.params.make_order_auth));
            const result =  await smallViewSaleProductListModal ({title: s.name ? s.name : 'New Sale', data: {from_table: true}});            
        })
    }else{       
        localStorage.setItem('make_order_auth',JSON.stringify(props.params.make_order_auth));
        router.push({ name: "AddSale", params: { name: s.name } });
    }
    emit('resolve', false);
}

async function onNewOrder() {
    emit('resolve', { action: "new_sale" });
}
function onClose() {
    emit("resolve", false);
}
</script>