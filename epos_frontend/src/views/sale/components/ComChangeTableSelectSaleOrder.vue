
<template>
    <ComModal :mobileFullscreen="true" @onClose="onClose" :hideOkButton="true" :hideCloseButton="true">
        <template #title>
            {{ $t('msg.Change to table') }} - {{ params?.data?.tbl_no }} - {{ $t('Bill') }} #{{ sale.sale.name }}
        </template>
        <template #content>
            <ComLoadingDialog v-if="isLoading" />
            <v-alert type="info"
                :text="$t('msg.Press on existing order if you want to merge order or press on button Create New Bill to create order in the same table')"
                variant="tonal"></v-alert>
            <v-btn @click="onSaleOrderClick(s)" v-for="(s, index) in params.data.sales" :key="index" height="100"
                :color="s.sale_status_color" class="ma-2">
                {{ s.name }}
                <br />
                <CurrencyFormat :value="s.grand_total" />
            </v-btn>
        </template>
        <template #action>
            <v-btn variant="flat" color="primary" @click="onCreateNewBill()">{{ $t('Create New Bill') }}</v-btn>
        </template>
    </ComModal>
</template>
  
<script setup>
import { ref, defineEmits, inject, useRouter, createDocumentResource,confirm,i18n } from '@/plugin'
import { createToaster } from '@meforma/vue-toaster';
import ComLoadingDialog from '@/components/ComLoadingDialog.vue';

const { t: $t } = i18n.global;  
const emit = defineEmits(["resolve", "reject"])
const sale = inject("$sale");

const router = useRouter();
const isLoading = ref(false);
const toaster = createToaster({ position: "top" })
const frappe = inject("$frappe");
const props = defineProps({
    params: {
        type: Object,
        require: true
    }
})


//frappe api call
const call = frappe.call();



function onCreateNewBill() {
    emit("resolve", { action: "create_new_bill" });
}

async function onSaleOrderClick(s) {
    if (s.sale_status == "Bill Requested") {
        toaster.warning($t("msg.You cannot merge order to the bill requested"));
        return;
    }
    if (s.name == sale.sale.name) {
        toaster.warning($t('msg.You cannot merge order to the current order'));
        return;
    }
  

    if (await confirm({ title: $t('Merge Order'), text: $t("msg.are sure you to merge this order")})) {
        isLoading.value = true;  
        const params = {
            old_sale: sale.sale.name,
            new_sale: s.name,
        };
        call.get('epos_restaurant_2023.api.change_merge_table.on_merge_order', params)
        .then((res) =>{ 
            isLoading.value = false;
            if(res.message.alert!=""){
                toaster.success($t(`msg.${res.message.alert}`,[res.message.data.name]))
            }
            router.push({
                name: "AddSale", params: {
                name: res.message.data.name
                }});
            isLoading.value = false;
            emit("resolve", { action: "reload_sale", name: res.message.data.name })   


             // check if print items merge bill
            if(sale.setting.pos_setting.print_sale_product_merged_table){                  
                sale.sale.sale_products.filter(r => (r.move_from_sale||"") != "" && (r.move_from_sale_printed||0)==0 && JSON.parse(r.printers).length > 0)
                .forEach((r) => {          
                    const pritners = JSON.parse(r.printers);
                    pritners.forEach((p) => {
                        sale.productPrinters.push({
                            move_from_sale_printed: 1,
                            printer: p.printer,
                            group_item_type: p.group_item_type,
                            is_label_printer: p.is_label_printer==1,
                            product_code: r.product_code,
                            product_name_en: r.product_name,
                            product_name_kh: r.product_name_kh,
                            portion: r.portion,
                            unit: r.unit,
                            modifiers: r.modifiers,
                            note: r.note,
                            quantity: r.quantity,
                            is_deleted: false,
                            is_free: r.is_free == 1,
                            combo_menu:r.combo_menu,
                            order_by:r.order_by,
                            creation:r.creation,
                            modified:r.modified,
                            move_from_sale: r.move_from_sale,
                            move_from_table:r.move_from_table,
                            is_timer_product: (r.is_timer_product||0),
                            reference_sale_product: r.reference_sale_product,
                            duration: r.duration,
                            time_stop: (r.time_stop||0),
                            time_in: r.time_in,
                            time_out_price: r.time_out_price,
                            time_out: r.time_out
                        });
                    });
                });

                sale.onPrintToKitchen(sale.sale);
            }


            
        }).catch((error) => {
       
            isLoading.value = false;
        });
    }

}

function onClose() {
    emit("resolve", false)
}

</script>