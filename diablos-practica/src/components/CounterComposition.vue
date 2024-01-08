<template>
   <div class="div-composition">
      <h3>{{ counter }}</h3>
      <button type="button" @click="addCounter" class="btn-add">
         Incrementa la Composicion
      </button>
      <button type="button" @click="remCounter" class="btn-rem">Restar</button>
      <button type="button" @click="restCounter" class="btn-rest">
         Reiniciar
      </button>
   </div>
</template>

<script setup>
import { ref } from "vue";

let counter = ref(0);
const addCounter = () => {
   counter.value++;
};
const remCounter = () => {
   counter.value--;
};
const restCounter = () => {
   counter.value = 0;
};
</script>

<style scoped>
.div-composition {
   display: block;
   border: 3px solid #ccc;
   border-radius: 3px;
   padding: 3px;
}
</style>