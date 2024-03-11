<template>
    <div class="px-2">
        <div class="flex justify-between my-1 border-b">
            <div v-if="label">{{ $t(label) }}</div>
            <div v-else><slot name="label"></slot></div>
            <div class="text-subtitle-1">
                <template v-if="value">
                    {{ value }}
                </template>    
                <slot v-else></slot> 
                
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    label: String,
    value: String
})

import { i18n } from '@/i18n';
const { t: $t } = i18n.global;
</script>