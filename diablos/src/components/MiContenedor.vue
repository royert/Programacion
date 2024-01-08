<template>
   <div class="container-flex">
      <TarjetaSimple />
      <TarjetaDosVue />
   </div>
</template>

<script setup>
import TarjetaSimple from "./TarjetaSimple.vue";
import TarjetaDosVue from "./TarjetaDos.vue";
</script>

<style lang="css" scoped>
.container-flex{
    display: flex;
}
</style>