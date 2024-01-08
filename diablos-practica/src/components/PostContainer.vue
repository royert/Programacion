<template>
   <div class="post-container">
      <PostCard />
      <CounterOptionVue />
      <CounterComposition />
      <ExampleSelective />
      <vOn />
      <ModelForm />

   </div>
</template>

<script setup>
import PostCard from "./PostCard.vue";
import CounterOptionVue from "./CounterOption.vue";
import CounterComposition from "./CounterComposition.vue";
import ExampleSelective from "./ExampleSelective.vue";
import vOn from "./v-On.vue";
import ModelForm from "./ModelForm.vue";
</script>

<style scoped>
.post-container {
   width: 100%;
   display: block;
}
</style>