import Enumerable from 'linq'
import { keyboardDialog, createResource } from "@/plugin"
import { createToaster } from "@meforma/vue-toaster";
import moment from '@/utils/moment.js';
import { FrappeApp } from 'frappe-js-sdk';
import CryptoJS from 'crypto-js';  

const frappe = new FrappeApp();

const key =CryptoJS.enc.Latin1.parse('NiQNF6jOiU7Kf4GaW4Y5Htb18sO3zWrf');
const iv = CryptoJS.enc.Latin1.parse('KiKlmSo2wWmdKXAs');

const toaster = createToaster({ position: "top" });

export default class POSLicense {
    constructor() { 
        this.web_platform = false,
        this.license = null
    }


    async  onPOSLicenseCheck(device_id){
        const call = frappe.call();
        return await  call.get("epos_restaurant_2023.api.pos_license.station_license",{"device_id":device_id,"platform":"Web"})
        .then(res=>{  
            const res_data = res.message;  
            if((res_data.name||"") == "" || res_data.name ==undefined){
                this.license = {
                    "status":false,
                    "show_license_msg":true,
                    "message":"Invalid device station. Please contact to system administrator for solve."
                };
                return this.license;
            } else{ 
                if ((res_data.license||"") == "" || res_data.license==undefined){
                    this.license =   {
                        "status":false,
                        "show_license_msg":true,
                        "message":`Invalid license on ${res_data.name}. Please contact to system administrator for solve.`
                    };
                    return this.license;
                }else{ 
                    let response = { "status":false,"invalid_license": true,"show_license_msg":true, "device_name":res_data.name,"message":`Invalid license on ${res_data.name}`};
                    const _license =  this.decryptAES(this.decryptAES(res_data.license));
                    let arr = _license.split('|'); 
                    if(arr.length>0){
                        if(arr[0]== device_id){
                            if(arr.length > 1){
                                const _now =  new Date();                 
                                let _date = `${_now.getFullYear()}-${_now.getMonth()+1}-${_now.getDate()}`; 
                                const now = new Date (_date);
                                const expired_date = new Date(arr[1]);  
                                if(expired_date < now){ 
                                     response = { 
                                        "status":true, 
                                        "device_name":res_data.name,
                                        "show_license_msg":true,
                                        "message":`${res_data.name} expired ${ Math.floor((now - expired_date) / (1000 * 60 * 60 * 24))+1}day(s) ago. Please contact to system administrator for solve.` 
                                    };
                                }else{
                                    const total_day_license = Math.floor((expired_date - now ) / (1000 * 60 * 60 * 24));                                    
                                    if(arr[2]=="True"){                
                                        response = { 
                                            "status":true, 
                                            "is_trail":true,
                                            "show_license_msg":true,
                                            "device_name":res_data.name,
                                            "message":`${res_data.name} trail license ${total_day_license}day(s).`
                                        };

                                    }else{ 
                                      if(total_day_license==0){
                                        response = { 
                                            "status":true, 
                                            "show_license_msg":true,
                                            "device_name":res_data.name,
                                            "message":`${res_data.name} license expired today.`
                                        }; 
                                      }else if (total_day_license<=7){
                                        response = { 
                                            "status":true, 
                                            "show_license_msg":true,
                                            "device_name":res_data.name,
                                            "message":`${res_data.name} license will expired in ${total_day_license}day(s) more. Expired on ${moment(expired_date).format("DD-MMM-yyyy")}`
                                        };  
                                      }else{
                                        response = { 
                                            "status":true, 
                                            "show_license_msg":false,
                                            "device_name":res_data.name,
                                            "message":``
                                        }; 
                                      }
                                    }
                                }
                            }else{
                                response = { 
                                    "status":true, 
                                    "device_name":res_data.name,
                                    "message":``
                                }; 
                            }
                        }else{
                             response = { 
                                    "status":true, 
                                    "device_name":res_data.name,
                                    "show_license_msg":true,
                                    "message":`Invalid device station. Please contact to system administrator for solve.`
                                }; 
                        }
                    }
                    this.license = response;
                    return response;
                }
            }
        }).catch(error=>{
            this.license = {
                "status":false,
                "show_license_msg":true,
                "message":"Invalid Device id"
            };
            return this.license;
        })

    }

    decryptAES(cipher_text){ 
        var ctx = CryptoJS.enc.Base64.parse(cipher_text);
        var enc = CryptoJS.lib.CipherParams.create({ciphertext:ctx});
        let data  = CryptoJS.AES.decrypt(enc, key,{iv:iv}); 
        return data.toString(CryptoJS.enc.Utf8);
    }
}