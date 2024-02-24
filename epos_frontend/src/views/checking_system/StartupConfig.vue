<template lang="">
    <ComToolbar :isClose="((is_window||0)==1 )" @onClose="onExitWindow()">
        <template #title>
            POS Configuration
        </template>
    </ComToolbar>
    
    <v-container>
        <v-card
            class="mx-auto mt-12"
            color="grey-lighten-3"
            max-width="400"
        > {{check}}  
            <v-card-title v-if="(is_startup_device||0)==0">
                <div class="text-center p-4">
                    ePOS System
                </div>
            </v-card-title>
            <v-card-text>                
                <form @submit.prevent="onSave()">
                    <div v-if="(is_startup_device||0)==0">
                        <ComInput
                            class="mb-2"
                            density="compact"
                            variant="solo"
                            label="ID"
                            prepend-inner-icon="mdi-cellphone-link"
                            single-line
                            hide-details
                            v-model="state.uid"
                            keyboard >
                        </ComInput> 
                        <!-- <ComInput
                            class="mb-2"
                            density="compact"
                            variant="solo"
                            label="Device Name"
                            prepend-inner-icon="mdi-cellphone-link"
                            single-line
                            hide-details
                            v-model="state.device_name"
                            keyboard >
                        </ComInput>  -->
                    </div>
                    <v-card-title v-else>
                        <div class="text-center p-4">
                            {{state.device_name}}
                        </div>
                    </v-card-title>
                    
                    <ComInput
                        class="mb-6"
                        density="compact"
                        variant="solo"
                        label="POS Profile"
                        prepend-inner-icon="mdi-account"
                        single-line
                        hide-details
                        v-model="state.pos_profile"
                        keyboard
                    ></ComInput>
                    <div class="text-right">
                        <v-btn type="sumbit" class="w-full" color="primary" :loading="store.state.isLoading">Save</v-btn>
                    </div>
                </form>
            </v-card-text>
        </v-card>
    </v-container>
</template>
<script setup>
    import {reactive, createResource, createToaster, useStore, inject,onMounted,ref,computed} from '@/plugin';
    import ComToolbar from '@/components/ComToolbar.vue'; 
    import CryptoJS from 'crypto-js';    
    const pos_license = inject('$pos_license');

    const frappe = inject('$frappe');
    const call = frappe.call();

    const auth = inject('$auth');
    const toast = createToaster();
    const store = useStore(); 

    const state = reactive({
        valid: true,
        device_name: '',
        uid:'',
        pos_profile: 'Main POS Profile',
        loading: true
    });

    const is_startup_device = ref(false); 
    function onExitWindow() {
        const data = {
            action: "exit",
        }
        window.chrome.webview.postMessage(JSON.stringify(data));
    }

    if(auth.isLoggedIn){
        auth.logout()
    }

    const is_window = localStorage.getItem("is_window");
    const is_apk_ipa = localStorage.getItem("apkipa");
    
    const check = computed(()=>{
        pos_license.web_platform  = false;
        is_startup_device.value = false;
        if((is_window||0)==1 || (is_apk_ipa||0)==1){
            pos_license.web_platform  = true;
            state.device_name = localStorage.getItem("__startup_device");
            is_startup_device.value = true;
        }      
   }) ;

 
   async function onSave() {
        pos_license.web_platform  = false;
        if((is_window||0) == 0 && (is_apk_ipa||0)==0){
            pos_license.web_platform = true;
            if(!state.uid || !state.pos_profile){
                toast.warning('Field(s) cannot be blank.',{ position: 'top'});
                return;
            }
            is_startup_device.value = false;
            await pos_license.onPOSLicenseCheck(state.uid).then((_res)=>{
                if(!_res.status){
                    toast.warning(_res.message,{ position: 'top'});
                    return;
                }
                if(_res.is_used){
                    toast.warning(`${_res.device_name} is already used on other device.`,{ position: 'top'});
                    return
                }
                localStorage.setItem('_webuid',state.uid);
                state.device_name = _res.device_name;
                _onSave();
            }) ;
        }
        else if((is_window||0) == 0 && (is_apk_ipa||0)!=0){
            _onSave()
        } else if((is_window||0) != 0 && (is_apk_ipa||0)==0){
            _onSave()
        }
    }

    function _onSave(){        
        if(!state.device_name || !state.pos_profile)
        {
            toast.warning('Field(s) cannot be blank.',{ position: 'top'});
            return
        }
        store.dispatch('startLoading')
        createResource({
            url: 'epos_restaurant_2023.api.api.check_pos_profile',
            params:{
                pos_profile_name:state.pos_profile,
                device_name:state.device_name,
                is_used_validate: !is_startup_device.value
            },
            auto:true,
            onSuccess(doc){
                localStorage.setItem('device_name',state.device_name);
                localStorage.setItem('device_setting', JSON.stringify( doc));
                localStorage.setItem('pos_profile',state.pos_profile);
                location.reload();
            },
            onError(){
                store.dispatch('endLoading')
            }
        })
    }

    </script>