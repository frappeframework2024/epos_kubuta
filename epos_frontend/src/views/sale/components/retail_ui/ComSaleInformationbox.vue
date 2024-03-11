<template>
    <div class="v-col rounded-lg mx-1 p-1" :class="bgColor">
        <div class="flex items-center h-100">
            <div class="v-row px-2">
                <div class="v-col text-white" style="padding: 0 !important;">
                    <small>
                        {{ title }}
                    </small>
                    <div>
                        {{ value }}
                    </div>
                </div>
                <div class="v-col-auto flex justify-center align-center v-ps-5" style="padding: 0 !important;">
                    <v-icon :size="size" :icon="icon" color="white"></v-icon>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps, inject } from 'vue'
const emit = defineEmits(["onClick"])
const props = defineProps({
    title: String,
    value: String,
    bgColor: String,
    icon: String,
    size: String
})
function onClick() {
    emit('onClick')
}
</script>

<style lang="">

</style>