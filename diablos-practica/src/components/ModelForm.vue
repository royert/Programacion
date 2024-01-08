<template>
   <form action="">
      <input type="text" v-model="valor" />
   </form>
   <h4>{{ valor }}</h4>
</template>

<script setup>
import { ref } from "vue";

let valor = ref("");
</script>

<style scoped>
</style>