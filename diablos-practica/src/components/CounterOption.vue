<template>
   <div class="div-counter">
      <h3>{{ counter }}</h3>
      <button type="button" @click="addCounter" class="btn-add">
         Incrementar
      </button>
      <button type="button" @click="remCounter" class="btn-rem">
         Desincrementar
      </button>
      <button type="button" @click="restCounter" class="btn-restart">Reiniciar</button>
   </div>
</template>

<script >
import { defineComponent } from "vue";
export default defineComponent({
   name: "CounterOption",
   data() {
      let counter = 0;
      return { counter };
   },
   methods: {
      addCounter() {
         this.counter++;
      },
      remCounter() {
         this.counter--;
      },
      restCounter() {
         this.counter = 0;
      }
   },
});
</script>

<style scoped>
.div-counter {
   display: block;
   margin: 5px;
}
button {
   margin-right: 5px;
}
</style>

