<template>
    <ComModal @onOk="onOK()" @onClose="onClose">
        <template #title>{{ $t("Change Shift Name") }}</template>
        <template #content>
            <v-select :label="$t('Shift')" item-title="name" item-value="name" variant="solo" v-model="shift_type"
                    density="compact" :items="gv.setting.shift_types.filter(shift_name => shift_name.show_in_pos == 1)"></v-select>
        </template>
    </ComModal>
</template>
<script setup>
import { i18n,ref,inject,defineEmits } from '@/plugin'

const props = defineProps({
    params:{
        type:Object,
        default:{}
    }
})
const emit = defineEmits(["resolve"])
const gv = inject("$gv")
const { t: $t } = i18n.global;
const frappe = inject('$frappe')
const db = frappe.db()
const shift_type = ref(props.params.data.shift_name)


function onOK(){
    db.updateDoc('Cashier Shift', props.params.data.name, {
        shift_name:shift_type.value,
    })
    .then((doc) => {
        emit('resolve', doc)
    })
    .catch((error) => console.error(error));
}

function onClose() {
  emit('resolve', false);
}
</script>
<style lang="">
    
</style>