<template>
    <ComModal width="1000px" :loading="is_loading" @onClose="onClose" @onOk="onStopClick" titleOKButton="Stop Timer">
        
        <template #title>
            {{ $t('Stop Timer') }}
        </template>
        <template #content>
            <div class="d-block d-md-flex mb-3" style="justify-content: space-between;">
                <div>
                    <span class="ttl-size">{{ $t("Time In") }}: </span>
                    <input class="calendar-custom p-1 w-100" type="datetime-local" v-model="data.time_in" >
                </div>
                <div>
                    <span class="ttl-size">{{$t("Time Out")}}: </span>
                    <input class="calendar-custom p-1 w-100" type="datetime-local" v-model="data.time_out" >
                </div>
            </div> 
            <hr/>
            <div class="v-table__wrapper mt-3">
                <table class="w-100">
                <thead>
                    <tr style="border: 1px solid #ccc">
                        <th class="text-left">{{$t("Time In")}}</th>
                        <th class="text-left">{{$t("Time Out")}}</th>
                        <th class="text-center">{{$t("Duration")}}</th>
                        <th class="text-center">{{$t("Total Minutes")}}</th>
                        <th class="text-right">{{$t("Price")}}</th>
                        <th class="text-right">{{$t("Amount")}}</th>
                    </tr>
                    
                </thead>
                <tbody>
                    <tr  v-for="data in breakdownData">
                        <td>
                            {{ moment(data.time_in).format('DD-MM-YYYY') }}
                            <br/>
                            {{ moment(data.time_in).format('hh:mm A') }}
                        </td>
                        <td>
                            {{ moment(data.time_out_price).format('DD-MM-YYYY') }}
                            <br/>
                            {{ moment(data.time_out_price).format('hh:mm A') }}
                        </td>
                        <td class="text-center">{{ data.duration }}</td>
                        <td class="text-center">{{ data.total_minute }}</td>
                        <td class="text-right"><CurrencyFormat :value="data.price" /></td>
                        <td class="text-right"><CurrencyFormat :value="data.amount" /></td>
                    </tr>
                    <tr>
                        <td class="text-right" colspan="5"><strong>{{$t("Total")}}:</strong></td>
                        <td class="text-right"><strong><CurrencyFormat :value="breakdownData.reduce((n, d) => n + (d.amount || 0), 0)" /> </strong></td>
                       
                    </tr>
                </tbody>
            </table>
            </div>
            
        </template>

    </ComModal>
</template>
<script setup>
import { ref,inject,onMounted,watch,createToaster ,i18n} from '@/plugin'
import { defineEmits } from 'vue';
import { useDisplay } from 'vuetify';
import moment from '@/utils/moment.js';
import { computed } from 'vue';
const sale = inject("$sale")

const frappe = inject("$frappe")
const call = frappe.call()
const { mobile } = useDisplay()
const props = defineProps({
    params: Object
})

const breakdownData = ref([])
const toaster = createToaster({ position: 'top' });

const emit = defineEmits(["click"])
const { t: $t } = i18n.global;

const data = ref(JSON.parse(JSON.stringify(props.params)))
let is_loading=ref(false)

if (!data.value.time_out){
    data.value.time_out=moment(new Date).format('YYYY-MM-DD HH:mm')
}

watch(() => data.value.time_in, (newValue, oldValue) => {
    getBreakdownData()
});

watch(() => data.value.time_out, (newValue, oldValue) => {
    getBreakdownData()
});

function onStopClick() {
    is_loading.value=true
    call.post("epos_restaurant_2023.api.timer_product.stop_timer", { sale_product: data.value  }).then((result) => {
        sale.sale = result.message
        emit("resolve",
            { 
                time_in: moment(data.value.time_in).format('yyyy-MM-DD HH:mm:ss'),
                time_out: moment(data.value.time_out).format('yyyy-MM-DD HH:mm:ss'),
        });
        is_loading.value=false
    }).catch((err)=>{
        is_loading.value=false
        if (err._server_messages){
            const errors = JSON.parse(err._server_messages)
           
            if(errors && errors.length>0){
                const error = JSON.parse(errors[0])
                toaster.warning($t('msg.' + error.message));
            }

            
        }
    })
    
}

function onClose() {
    emit("resolve", false);
}

function getBreakdownData(){
    is_loading.value=true
    data.value.price_rule = sale.sale.price_rule 
    data.value.time_in = moment(data.value.time_in).format('YYYY-MM-DD HH:mm:ss')
    data.value.time_out = moment(data.value.time_out).format('YYYY-MM-DD HH:mm:ss')
    call.post("epos_restaurant_2023.api.timer_product.get_timer_product_breakdown", { sale_product: data.value  }).then((result) => {
        breakdownData.value = result.message
        is_loading.value=false
    }).catch((res)=>{
        is_loading.value=false
    })
}
onMounted(() => {
    getBreakdownData()
})

</script>
<style scoped>
    .calendar-custom{ 
        font-size: 24px;
        color: #3468C0; 
        border: 2px solid;
        border-radius: 5px;
    }
    .calendar-custom:focus-visible{
        outline: 0;
    }
    .ttl-size{
        font-size: 24px;
        color: #D63484;
    }
    table, th, td {
        border: 1px solid #E5E1DA;
    } 
    td, th{
        padding: 3px;
    }
    @media (max-width: 768px) {
        .calendar-custom{
            font-size: 18px;
        }
    }
</style>