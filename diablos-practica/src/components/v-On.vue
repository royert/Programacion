<template>
   <p :style="{color : c}">Texto que cambiara</p>
   <button type="button" @click="changeColor()" class="btn-Color">
      Click para cambiar color
   </button>
   <button type="button" @click="changeColorI()" class="btn-Color">
      Color Inicial
   </button>
</template>

<script setup>
import { ref } from "vue";

let c = ref("lime");

const changeColor = () => {
   c.value = "blue";
};

const changeColorI = () => {
   c.value = "lime";
};

</script>

<style scoped>
</style>