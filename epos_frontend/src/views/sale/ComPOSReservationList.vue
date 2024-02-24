<template>
  <ComModal :mobileFullscreen="true" @onClose="onClose()" width="1200px" :hideOkButton="true">
    <template #title>
      {{ $t('Reservation') }}
    </template>
    <template #content>
      <div class="d-flex flex-row justify-space-between my-4">
            <ComInput  style="width:372px"  type="date" v-model="filter_date" :label="`${$t('Arrival Date')}:`"></ComInput>
            <div>
              <v-btn class="mr-1" prepend-icon="mdi-close" @click="onClearSearch" color="error">
                {{$t('Clear')}}
            </v-btn>
              <v-btn class="ml-1" prepend-icon="mdi-magnify" @click="onSearch" color="success">
                {{$t('Search')}}
            </v-btn>
            </div>
           
          </div>
      <ComPlaceholder :loading="isLoading" :is-not-empty="reservationData.length > 0" :text="$t('Empty Data')"
        icon="mdi-note-outline">
        <div>
          
          
          <div class="grid gap-2 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
            <v-card v-for="(s, index) in reservationData" :key="index">
              <v-card-title class="!p-0">
                <v-toolbar height="48">
                  <v-toolbar-title class="text">
                    <span class="font-bold text-sm">#{{ s.name }}</span>
                  </v-toolbar-title>
                  <template v-slot:append>
                    <v-chip size="small" class="ma-2" :color="s.reservation_status_background_color"
                      :text-color="s.reservation_status_color">
                      {{ s.reservation_status }}
                    </v-chip>
                  </template>
                </v-toolbar>
              </v-card-title>
              <v-card-text class="!pt-0 !pr-0 !pb-14 !pl-0">
                <v-list :lines="false" density="compact" class="pa-0">

                  <v-list-item :title="`${$t('Arrival Date')}:`">
                    <template v-slot:append>
                      {{ moment(new Date(`${s.arrival_date} ${s.arrival_time}`)).format('yyyy-MM-DD hh:mm A') }}
                    </template>
                  </v-list-item>

                  <v-list-item :title="`${$t('Table')}#`" v-if="s.table_number">
                    <template v-slot:append>
                      {{ s.table_number }}
                    </template>
                  </v-list-item>

                  <v-list-item :title="`${$t('Total Guest')}:`" v-if="s.total_guest">
                    <template v-slot:append>
                      {{ s.total_guest }} {{$t('Pax')}}
                    </template>
                  </v-list-item>
                  <v-list-item v-if="s.guest" :title="`${$t('Guest Code')}:`">
                    <template v-slot:append>
                      {{ s.guest }}
                    </template>
                  </v-list-item>

                  <v-list-item :title="`${$t('Guest Name')}:`">
                    <template v-slot:append>
                      {{ s.guest_name }}
                    </template>
                  </v-list-item>

                  <v-list-item v-if="s.tour_code" :title="`${$t('Tour')}:`">
                    <template v-slot:append>
                      {{ s.tour_code }}
                      <span v-if="s.tour_code">
                        -
                      </span>
                      {{ s.tour_name }}
                    </template>
                  </v-list-item>
                  <v-list-item v-if="s.guide_name" :title="`${$t('Guide')}:`">
                    <template v-slot:append>
                      {{ s.guide_code }}
                      <span v-if="s.guide_code">
                        -
                      </span>
                        {{ s.guide_name }}
                    </template>
                  </v-list-item>

                  <v-list-item :title="`${$t('Total Qty')}:`" v-if="s.total_quantity > 0">
                    <template v-slot:append>
                      {{ s.total_quantity }}
                    </template>
                  </v-list-item>
                  <v-list-item :title="`${$t('Deposit')}:`" v-if="s.total_deposit > 0">
                    <template v-slot:append>
                      <CurrencyFormat :value="s.total_deposit" />
                    </template>
                  </v-list-item>


                </v-list>
              </v-card-text>
              <v-card-actions class="pt-0 flex items-center justify-between absolute bottom-0 w-full">

                <v-btn v-if="s.arrival_date == current_date" variant="tonal" color="success" @click="onCheckIn(s)">
                  {{ $t('Checked In') }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </div>
      </ComPlaceholder>
    </template>
  </ComModal>
</template>
<script setup>
import { useRouter, defineProps, defineEmits, ref, inject, createToaster, i18n, onMounted } from "@/plugin"
import ComModal from "../../components/ComModal.vue";
import { confirm, changeTableDialog } from '@/utils/dialog';
import ComPlaceholder from "../../components/layout/components/ComPlaceholder.vue";
import { useDisplay } from 'vuetify';
import moment from '@/utils/moment.js';


const { t: $t } = i18n.global;
const { mobile } = useDisplay();

const isLoading = ref(true);
const reservationData = ref([]);

const frappe = inject("$frappe");
const router = useRouter();
const emit = defineEmits(["resolve"])
const gv = inject('$gv');
const sale = inject("$sale");
const toaster = createToaster({ position: "top" });

const db = frappe.db();
const call = frappe.call();
let filter_date = ref(moment(new Date()).format('yyyy-MM-DD'))
let current_date = ref(moment(new Date()).format('yyyy-MM-DD'))


const props = defineProps({
  params: {
    type: Object,
    required: true,
  }
})


onMounted(() => {
  _onInit()
});

function _onInit() {
  isLoading.value = true;
  call.get("epos_restaurant_2023.api.pos_reservation.get_pos_reservation_list",
  {
    "property":gv.setting.business_branch,
    "arrival_date":filter_date.value
  }).then((res)=>{
    reservationData.value = [];
    if(res.message){
      reservationData.value = res.message;
    }else{

    }
    isLoading.value = false;
  }).catch((err)=>  isLoading.value = false);

  // db.getDocList("POS Reservation",
  //   {
  //     fields: ["name"],
  //     filters: [
  //       ["property", "=", gv.setting.business_branch],
  //       ["arrival_date", "=", filter_date.value],
  //       ["reservation_status", "in", "Confirmed"]
  //     ],
  //     limit: 50,
  //     orderBy: {
  //       field: 'arrival_date',
  //       order: 'desc',
  //     },
  //   }).then(doc => {
  //     reservationData.value = [];
  //     doc.forEach(d => {
  //       db.getDoc("POS Reservation", d.name).then(r => {
  //         reservationData.value.push(r);
  //       })
  //     });

  //     isLoading.value = false;
  //   }).catch(err => {
  //     isLoading.value = false;
  //   });
}

function onClearSearch(){
  filter_date.value = moment(new Date()).format('yyyy-MM-DD')
  _onInit()
}
function onSearch(){
  _onInit()
}
async function onCheckIn(reservation) {
  if ((reservation.table_id || "") == "") {
    const result = await changeTableDialog({ "_is_reservation": true });
    if (result) {
      reservation.table_id = result.id;
      reservation.table_number = result.tbl_no;

      onConvertToSale(reservation);
    }
  }
  else if (await confirm({ title: $t("Checked In"), text: $t("msg.are you sure to checked in this reservation") })) {
    onConvertToSale(reservation)
  }
}



async function onConvertToSale(reservation) {
  const params = {
    business_branch: gv.setting?.business_branch,
    pos_profile: localStorage.getItem("pos_profile")
  };

  call.get('epos_restaurant_2023.api.api.get_current_shift_information', params)
    .then(async (_res) => {
      const _data = _res.message;
      if (_data.cashier_shift == null) {
        toaster.warning($t("msg.Please start shift first"));
      } else if (_data.working_day == null) {
        toaster.warning($t("msg.Please start working day first"));
      } else {
        gv.authorize("open_order_required_password", "make_order").then(async (v) => {
          if (v) {
            isLoading.value = true;
            const make_order_auth = { "username": v.username, "name": v.user, discount_codes: v.discount_codes };
            localStorage.setItem('make_order_auth', JSON.stringify(make_order_auth));

            await db.getDoc("Tables Number", reservation.table_id).then(async (table) => {
              sale.newSale();
              sale.sale.from_reservation = reservation.name;

              sale.sale.working_day = _data.working_day.name;
              sale.sale.cashier_shift = _data.cashier_shift.name;
              sale.sale.shift_name = _data.cashier_shift.shift_name;

              sale.sale.guest_cover = (reservation.total_guest || 0);
              sale.sale.table_id = reservation.table_id;
              sale.sale.tbl_number = reservation.table_number;

              sale.sale.customer = reservation.guest;
              sale.sale.customer_photo = reservation.guest_photo;
              sale.sale.customer_name = reservation.guest_name;
              sale.sale.customer_group = reservation.guest_type;
              sale.sale.deposit = reservation.total_deposit;

              if (table.sale_type) {
                sale.sale.sale_type = table.sale_type
              }
              if (table.price_rule) {
                sale.sale.price_rule = table.price_rule;
              }
              if (gv.setting.price_rule != sale.sale.price_rule) {
                toaster.info($t('msg.Your current price rule is', [sale.sale.price_rule]));
              }

              sale.sale.sale_status = "Hold Order";
              sale.action = "hold_order";

              await reservationProductConvert(reservation);


              await sale.onSubmit().then(async (value) => {
                if (value) {
                  sale.sale = value;
                  call.get("epos_restaurant_2023.api.api.update_pos_reservation_and_sale_payment", {
                    reservation_name: reservation.name,
                    reservation_status: "Dine-in",
                    sale: value.name
                  }).then(() => {
                    router.push({
                      name: "AddSale",
                      params: { name: value.name }
                    }).then(() => {
                      onClose();
                    });

                  }).catch((err) => {
                    _onInit()
                  });
                }
              }).catch(() => {
                isLoading.value = false;
              });
            }).catch(() => {
              isLoading.value = false;
            })

          }
        });
      }
    })
    .catch((error) => {
      isLoading.value = false;
    });
}


async function reservationProductConvert(reservation) {

  const now = new Date();
  const make_order_auth = JSON.parse(localStorage.getItem('make_order_auth'));

  for (let p of reservation.reservation_product) {
    let _p = await db.getDoc("Product", p.product_code);
    let printers = [];
    _p.printers.forEach(_printer => {
      printers.push({
        "printer": _printer.printer_name,
        "group_item_type": _printer.group_item_type,
        "is_label_printer": _printer.is_label_printer
      })
    })
    var saleProduct = {
      product_code: p.product_code,
      product_name: p.product_name,
      product_name_kh: p.product_name_kh,
      revenue_group: p.revenue_group,
      unit: p.unit,
      quantity: p.quantity,
      sub_total: 0,
      total_discount: 0,
      total_tax: 0,
      discount_amount: 0,
      sale_discount_amount: 0,
      note: '',
      regular_price: p.price,
      price: p.price,
      modifiers_price: 0,
      product_photo: p.product_photo,
      selected: false,
      modified: moment(now).format('yyyy-MM-DD HH:mm:ss.SSS'),
      creation: moment(now).format('yyyy-MM-DD HH:mm:ss.SSS'),
      append_quantity: _p.append_quantity,
      allow_discount: _p.allow_discount,
      allow_free: _p.allow_free,
      allow_change_price: _p.allow_change_price,
      is_open_product: _p.is_open_product,
      portion: "",
      modifiers: '',
      // modifiers_data: p.modifiers_data,
      is_free: 0,
      sale_product_status: "New",
      discount_type: "Percent",
      discount: 0,
      order_by: make_order_auth.name,
      order_time: moment(now).format('yyyy-MM-DD HH:mm:ss.SSS'),
      printers: JSON.stringify(printers),
      product_variants: [],
      is_combo_menu: _p.is_combo_menu,
      use_combo_group: _p.use_combo_group,
      product_tax_rule: "",
      is_require_employee: _p.is_require_employee,
      pos_reservation: reservation.name
    }

    sale.updateSaleProduct(saleProduct);
    sale.sale.sale_products.push(saleProduct);
    sale.updateSaleProduct(saleProduct);
  }

  sale.updateSaleSummary();
}

function onClose() {
  emit('resolve', false);
}
</script>