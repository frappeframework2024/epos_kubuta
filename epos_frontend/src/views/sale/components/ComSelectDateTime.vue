<template>
    <ComModal @onClose="onClose" @onOk="onClick()" titleOKButton="Set Time In">
        <template #title>
            {{ $t('Timer') }}
        </template>
        <template #content>  
            <div> 
                <!-- Please enter the time when the player started playing the game. If the player has not started playing yet, please click on the ‘Set Time In Later’ button. -->
                <v-alert type="info"
                    :text="$t('msg.Timer Alert Message')"
                ></v-alert>
            </div>
            <div class="w-100 text-center">
                <input class="calendar-custom mt-5" type="datetime-local" v-model="date" >
            </div>
        </template> 
        <template #action>
                <v-btn variant="flat" type="button" color="primary" :disabled="loading" v-if="!hideOkButton" @click="setTimeLaterClick()">
                       {{$t("Set Time In Later")  }}
                    </v-btn>
        </template>
    </ComModal>
</template>
<script setup>
import { ref,computed } from '@/plugin'
import { defineEmits } from 'vue';
import { useDisplay } from 'vuetify';
import moment from '@/utils/moment.js';
const { mobile } = useDisplay()

const props = defineProps({
    params:Object
})



// const date = ref("2024-01-09 13:49");
const default_date = moment(new Date).format('YYYY-MM-DD HH:mm')

const date =  ref(default_date + ":00")

if (props.params?.time_in){
    
    date.value = props.params.time_in
} 
const emit = defineEmits(["click"])




function onClick() {
    emit("resolve",moment(date.value).format('yyyy-MM-DD HH:mm:ss'));
}
function setTimeLaterClick() {
    emit("resolve",'Set Later');
}
function onClose() {
    emit("resolve", false);
}
</script> 
<style scoped>
    .calendar-custom{ 
        font-size: 42px;
        color: #3468C0;
        text-align: center;
        border: 2px solid;
        border-radius: 5px;
    }
    .calendar-custom:focus-visible{
        outline: 0;
    }
    @media (max-width: 768px) {
        .calendar-custom{
            font-size: 18px;
        }
    }
</style>