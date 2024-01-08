<template>
   <h4 v-if="edad >= 18" :class="{ 'MayorEdad' : control }">
      Eres Mayor de edad
   </h4>
   <h4 v-else :class="{'MenorEdad' : control }">Eres menor de edad</h4>
</template>

<script setup>
let edad = 17;
let control = true;

</script>

<style scoped>
.MayorEdad {
   color: lime;
}
.MenorEdad {
   color: red;
}
</style>