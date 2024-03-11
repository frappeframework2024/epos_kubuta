<template>
<label class="bold">Sale Note</label>
<ComInput  type="textarea" keyboard v-model="sale.sale.note" placeholder="Add Note"/>

</template>


<script setup>
    import {ref,inject} from "@/plugin"
    const sale =inject("$sale")
   

</script>