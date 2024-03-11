<template>

  <div :class="sale.sale?.sale_products?.length > 0 ? 'table-sale-product-scroll' : ' empty-no-scroll'"
    :style="sale.sale?.sale_products?.length > 0 ? 'max-height:calc(-424px + 100vh)' : ''">
    <v-table>
      <thead>
        <tr>
          <th class="text-left">
            មុខទំនិញ <br />
            Product Description
          </th>
          <th class="text-center">
            ចំនួន <br />
            Quantity
          </th>
          <th class="text-center">
            ឯកតា <br />
            Unit
          </th>
          <th class="text-right">
            តម្លៃ <br />
            Price
          </th>
          <th class="text-right">
            បញ្ចុះតម្លៃ <br />
            Discount
          </th>
          <th class="text-right">
            សរុបតម្លៃ <br />
            Amount
          </th>
          <th class="text-center">
          </th>

        </tr>
      </thead>
      <tbody class="table-pro">
        <template v-if="sale.sale?.sale_products?.length > 0">
          <tr v-for="sp  in sale.getSaleProducts(undefined)" @click="sale.onSelectSaleProduct(sp)"
            :class="sp.selected ? 'selected' : ''">
            <td>
              <div class="d-flex align-center gap-3">
                <div>
                  <v-avatar :image="sp?.product_photo" v-bind="props" v-if="sp?.product_photo"
                    class="cursor-pointer"></v-avatar>
                  <avatar v-else :name="sp.product_name || 'No Name'" v-bind="props" class="cursor-pointer mr-2"
                    size="40"></avatar>
                </div>
                <div>
                  
                  <p>{{ sp.product_code }} </p>
                  <p>{{ sp.product_name }} <v-chip v-if="sp.quantity<0" variant="outlined" color="red">
                      {{ $t("Return") }}
                    </v-chip></p>
                  <p v-if="sp.product_name != sp.product_name_kh">{{ sp.product_name_kh }}</p>
                 
                  <p v-if="!sp.note" class="italic underline" style="color:#ccc;" @click="sale.onSaleProductNote(sp)">
                    {{ $t("Add Note") }}</p>
                  <p v-else class="italic" @click="sale.onSaleProductNote(sp)">{{ sp.note }}</p>
                </div>
              </div>
            </td>
            <td class="text-center">
              <div class="flex justify-center">
                <div class="flex gap-2 border rounded justify-center py-1" style="width:5rem">
                  <div><v-icon icon="mdi-minus-circle-outline" color="red" @click="onUpdateQuantity(sp, -1)"></v-icon>
                  </div>
                  <div>{{ sp.quantity }}</div>
                  <div><v-icon icon="mdi-plus-circle-outline" color="green" @click="onUpdateQuantity(sp, 1)"></v-icon>
                  </div>

                </div>

              </div>
            </td>
            <td class="text-center">
                  
              <ComProductUnit :sale_product="sp" />
            </td>
            <td class="text-end">
              
              <span class="link_line_action overflow-hidden pa-0"  style="min-width:4rem"
                @click="sale.onChangePrice(sp, gv, numberFormat)">
                  <div style="padding:0 5px">
                    <CurrencyFormat :value="sp.price" />
                    
                    
                </div>
                <div  style="padding:0 5px;background-color: #d9d9d9;color: #040259">
                      <CurrencyFormat :currency="gv.setting.pos_setting.second_currency_name" :value="sp.price * sale.exchange_rate" />
                  </div>
              </span>
            </td>
            <td class="text-end">
              <span class="link_line_action overflow-hidden" style="min-width:4rem">
                <template v-if="sp.discount">
                  <span v-if="sp.discount_type == 'Percent'">
                    {{ sp.discount }} % /
                  </span>


                  <CurrencyFormat :value="sp.discount_amount" />
                </template>

                <template v-else>{{ $t("Apply Discount") }}</template>

                <v-menu activator="parent">
                  <v-list>
                    <v-list-item @click="onSaleProductDiscount(sp, 'Percent')">
                      <v-list-item-title>{{ $t("Discount Percent") }} (%)</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="onSaleProductDiscount(sp, 'Amount')">
                      <v-list-item-title>{{ $t("Discount Amount") }} ($)</v-list-item-title>
                    </v-list-item>
                    <v-divider v-if="sp.discount > 0" inset></v-divider>
                    <v-list-item v-if="sp.discount > 0" @click="onSaleProductCancelDiscount(sp)">
                      <v-list-item-title class="text-orange-700">{{ $t("Cancel Discount") }}</v-list-item-title>
                    </v-list-item>

                  </v-list>
                </v-menu>
              </span>
            </td>
            <td class="text-end">
              <span style="min-width:4rem">
                <CurrencyFormat :value="sp.amount" />
                <br/>
                <span style="color: #040259">
                  <CurrencyFormat :currency="gv.setting.pos_setting.second_currency_name" :value="sp.price * sale.exchange_rate" />
                </span>
                
              </span>
            </td>
            <td class="text-center"><v-icon icon="mdi-delete" color="red"
                @click="sale.onRemoveItem(sp, gv, numberFormat)"></v-icon>

              <v-menu>
                <template v-slot:activator="{ props }">

                  <v-btn class="ma-2" icon="mdi-dots-vertical" variant="text"  v-bind="props">
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item v-if="sp.quantity > 0" @click="onReturn(sp)">
                    <v-list-item-title>{{ $t("Mark as Return Product") }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item v-else @click="onReturn(sp)">
                    <v-list-item-title>{{ $t("Mark as Selling Product") }}</v-list-item-title>
                  </v-list-item>


                </v-list>
              </v-menu>

 

            </td>
          </tr>
        </template>

        <template v-else>
          <tr class="empty-data-st">
            <td colspan="6">
              <div class="text-center"><v-icon icon="mdi-cart-outline" color="blue"></v-icon></div>
              <div class="text-center">There is no product selected, please search or scan barcode</div>
            </td>
          </tr>
        </template>
      </tbody>
    </v-table>
  </div>
</template>

<script setup>
import { ref, inject } from "@/plugin"
import ComCurrentUserAvatar from '@/components/layout/components/ComCurrentUserAvatar.vue'
import ComProductUnit from '@/views/sale/components/retail_ui/ComProductUnit.vue'
import { createToaster } from '@meforma/vue-toaster';


import { i18n } from '@/i18n';

const { t: $t } = i18n.global;

const numberFormat = inject('$numberFormat');
const sale = inject('$sale');
const product = inject('$product');
const gv = inject('$gv');

const toaster = createToaster({ position: 'top-right', maxToasts: 2, duration: 3000 });
const frappe = inject('$frappe');
const db = frappe.db()




function onUpdateQuantity(sp, param) {

  param = param * ((sp.is_return || 0) == 0 ? 1 : -1)


  if (!sp.is_return) {
    if (sp.quantity <= 1 && param == -1) {
      return
    }
  } else {
    if (sp.quantity == -1 && param == 1) {
      return
    }
  }

  sale.updateQuantity(sp, sp.quantity + param)
}

function onReturn(sp) {
  sp.is_return = !sp.is_return 
  sale.updateQuantity(sp, sp.quantity * -1)

}

function onSaleProductDiscount(sp, discount_type) {
  if (sp.allow_discount) {
    if (!sale.isBillRequested()) {
      gv.authorize("discount_item_required_password", "discount_item", "discount_item_required_note", "Discount Item Note", "", true).then((v) => {
        if (v) {
          sp.temp_discount_by = v.user;
          sp.temp_discount_note = v.note;

          sale.onDiscount(
            gv,
            `${sp.product_name} Discount`,
            sp.amount,
            sp.discount,
            discount_type,
            v.discount_codes,
            sp.discount_note,
            sp,
            v.category_note_name
          );
        }
      });
    }
  }
  else {
    toaster.warning($t('msg.This item is not allow to discount'));
  }
}



function onSaleProductCancelDiscount(sp) {

  sp.discount = 0;
  sp.discount_type = 'Percent'
  sp.happy_hour_promotion = ''
  sp.happy_hours_promotion_title = ''
  sale.updateSaleProduct(sp)
  sale.updateSaleSummary();

}







</script>

<style>
.selected,
.item-list:hover {
  background-color: #ffebcc !important;
}


.link_line_action {
  border: 1px dashed #4338ca;
  border-radius: 10px;
  padding: 0 5px;
  color: var(--bg-purple-cs);
  cursor: pointer;
  display: inline-block;
  width: 100%;
  white-space: nowrap;
  text-overflow: ellipsis;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table-sale-product-scroll {
  overflow-y: auto;
  position: relative;
}

.empty-data-st {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.empty-data-st .mdi-cart-outline {
  font-size: 5rem;
}

.empty-no-scroll {
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.table-sale-product-scroll .v-table>.v-table__wrapper>table {
  overflow: hidden !important;
}
</style>