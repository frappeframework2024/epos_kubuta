<template>
<PageLayout icon="" title="">
     <v-btn @click="encrypt">
        test
     </v-btn>
     encrypted = {{ encrypted }}
</PageLayout>
</template>
<script setup>
import {ref,confirmDialog} from "@/plugin"
import PageLayout from '../components/layout/PageLayout.vue';
import CryptoJS from 'crypto-js';
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({position:"top"});
const todoList = ref([]);
const toDo = ref("")

const iv = 'sinasinasisinaaa'
const key= ref('82f2ceed4c503896c8a291e560bd4325')
const text= ref('HELLO')
let encrypted=ref('')
  function encrypt(){
    encrypted.value = CryptoJS.AES.encrypt(text.value, CryptoJS.enc.Utf8.parse(key.value),{
      iv: CryptoJS.enc.Utf8.parse(iv),
        mode: CryptoJS.mode.CBC
    })
  }
  function decrypt() {
    console.log(encrypted.value)
    text.value = CryptoJS.AES.decrypt(encrypted.value, CryptoJS.enc.Utf8.parse(key.value),{
      iv: CryptoJS.enc.Utf8.parse(iv),
        mode: CryptoJS.mode.CBC
    })
  }

function addToDo(){
    todoList.value.push(
        {
            title:toDo.value,
            status:0,
            is_edit:0
        }
    )
}

function onDone(myTodo){
    myTodo.status = 1;
}
function onEdit(myTodo){
    myTodo.is_edit = 1;
}
function onEditSave(myTodo){
    myTodo.is_edit = 0;
}
async function onDelete(index){
    if(await confirmDialog({title:"Delete to do",text:"Are you sure?"})){ 
    todoList.value.splice(index,1);
    toaster.success("Delete to successfully")
    }
}
</script>