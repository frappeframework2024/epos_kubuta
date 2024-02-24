<template>    
    <v-dialog :scrollable="false" v-model="open" :fullscreen="mobile"
        :style="mobile ? '' : 'width: 100%;max-width:800px'">
        <v-card>
            <ComToolbar @onClose="onClose">
                <template #title>
                   {{ `${(params._is_reservation||false) ?$t('Assign Table') : $t('Change or Merge Table')}`  }}
                </template>
            </ComToolbar>
            <div class="overflow-auto p-3 h-full">
                <v-tabs align-tabs="center"
                    v-if="tableLayout.table_groups && tableLayout.table_groups.length > 1"
                    v-model="tableLayout.tab">
                    <v-tab v-for="g in tableLayout.table_groups" :key="g.key" :value="g.key">
                        {{ g.table_group }}
                    </v-tab>
                </v-tabs>
                <template v-if="tableLayout.table_groups">
                    <v-window v-model="tableLayout.tab">
                        <template v-for="g in tableLayout.table_groups"> 
                            <v-window-item :value="g.key">
                                <div class="pa-4">
                                    <ComInput 
                                    v-model="g.search_table_keyword"
                                    autofocus
                                    ref="searchTextField"
                                    keyboard
                                    class="my-2 mb-4"
                                    :placeholder="$t('Search')" />
                                    <div class="grid gap-4 grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-5 xl:grid-cols-5 2xl:grid-cols-6">
                                    <template v-for="(t, index) in getTable(g.tables, g.search_table_keyword)" :key="index">
                                        <template v-if="(params._is_reservation||false)">
                                            <v-btn  color="rgb(79, 157, 217)" @click="onSelectTable(t)" width="100%" height="100">
                                                <span class = "text-white"> {{ t.tbl_no }}  </span>    
                                                
                                            </v-btn>
                                        </template>
                                        <template v-else>
                                            <v-badge :content="t.sales?.length" color="error" v-if="t.sales?.length>0">
                                                <v-btn  :color="t.background_color" @click="onSelectTable(t)" width="100%" height="100">
                                                {{ t.tbl_no }}
                                                </v-btn>
                                            </v-badge>
                                            <v-btn v-else   :color="t.background_color" @click="onSelectTable(t)" width="100%" height="100">
                                                {{ t.tbl_no }}                                              
                                            </v-btn>
                                        </template>
                                    </template>
                                </div>
                            </div>
                            </v-window-item>
                        </template>
                    </v-window>
                </template>
            </div>
        </v-card>
    </v-dialog>
</template>
  
<script setup>
import { ref, defineEmits, inject,changeTableSelectSaleOrderDialog,i18n } from '@/plugin'
import ComToolbar from '@/components/ComToolbar.vue';
import { createToaster } from '@meforma/vue-toaster';
import ComInput from '../../../components/form/ComInput.vue';
import { useDisplay } from 'vuetify';
const { t: $t } = i18n.global;  

const { mobile } = useDisplay()

const tableLayout = inject("$tableLayout");
const sale = inject("$sale");
const toaster = createToaster({ position: "top" })

const props = defineProps({
    params: {
        type: Object,
        require: true
    }
})

 

const emit = defineEmits(["resolve", "reject"])

let open = ref(true);
tableLayout.getSaleList();


function onClose() {
    emit("resolve", false)
}

function getTable(tables,keyword) {
    if((props.params?._is_reservation||false) ){
        tables = tables.filter((r)=> {
            return   (r.sales?.length||0) ==0
        });
    }     
    
    if (keyword == "") {
        return tables;
    } else {
        return tables.filter((r) => {
            return   String(r.tbl_no).toLocaleLowerCase().includes(keyword.toLocaleLowerCase());
        });
    }
}



async function onSelectTable(t) {
    if((props.params?._is_reservation||false) )
    {
        emit("resolve", t);
    }
    else{
        if(t.sales?.length==0){  
                generateProductPrinterChangeTable(sale.sale.sale_products,  sale.sale.name, sale.sale.tbl_number); 
                sale.sale.sale_products?.forEach((r)=>{
                    r.move_from_table = sale.sale.tbl_number;
                });
                sale.sale.table_id = t.id;
                sale.sale.tbl_number = t.tbl_no;
                toaster.success($t('msg.Change to table')+": " + t.tbl_no);
                emit("resolve", true)
        }
        else {
                const result = await changeTableSelectSaleOrderDialog({data:t});
                if(result){
                    if(result.action=="create_new_bill"){
                        //
                        generateProductPrinterChangeTable(sale.sale.sale_products,  sale.sale.name, sale.sale.tbl_number);

                        sale.sale.sale_products?.forEach((r)=>{
                            r.move_from_table = sale.sale.tbl_number;
                        });
                        sale.sale.table_id = t.id;
                        sale.sale.tbl_number = t.tbl_no;
                        toaster.success($t('msg.Change to table')+": " + t.tbl_no);
                        emit("resolve", true);
                        
                    }else if(result.action=="reload_sale"){
                        emit("resolve", result)
                    }
                }
        }
    }
}


function generateProductPrinterChangeTable(sale_products, old_sale,old_table){
    if(sale.setting.pos_setting.print_sale_product_change_table){            
        sale_products?.forEach((r) => {
            const pritners = JSON.parse(r.printers);
            pritners.forEach((p) => {
                sale.changeTableSaleProducts.push({
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
                    is_free: r.is_free == 1,
                    order_by: r.order_by,
                    creation: r.creation,
                    modified: r.modified,
                    move_from_table:old_table,
                    move_from_sale: old_sale,
                });
            });
        });
        
    }
}


</script>