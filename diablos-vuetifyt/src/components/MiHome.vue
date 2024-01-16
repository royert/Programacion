<template>
<v-container>
      <v-carousel :show-arrows="false">
         <v-carousel-item
            v-for="(item, i) in items"
            :key="i"
            :src="item.src"
            cover
         ></v-carousel-item>
      </v-carousel>

</template>

<script >
export default {
   data() {
      return {
         items: [
            {
               src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
            },
            {
               src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
            },
            {
               src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
            },
            {
               src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
            },
         ],
      };
   },
};
</script>

<style lang="css" scoped>
v-carousel{
    width: 100vw;
    height: 100vh;
}
</style>