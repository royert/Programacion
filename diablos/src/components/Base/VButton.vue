<template>
   <a href="#">{{ props.Texto }}</a>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
   
      Texto: String,
      ColorTexto: String,
      ColorFondo: String,
  
});
</script>

<style lang="scss" scoped>
</style>