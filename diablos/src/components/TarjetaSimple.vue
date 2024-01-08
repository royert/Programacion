<template>
   <div class="container-card">
      <img
         class="container-card__container-img"
         src="../assets/logo.png"
         alt="Logo de tarjeta"
      />
      <h2 class="container-card__container-title">Tittle</h2>
      <h5 class="container-card__container-subtitle">Subtitle</h5>
      <p class="container-card__container-text">
         Lorem ipsum dolor sit amet consectetur adipisicing elit. Quasi quaerat
         sint dicta rem accusamus eaque! Iure ipsam eum harum laudantium,
         obcaecati temporibus sed facilis dolorem assumenda consectetur, quo,
         incidunt quam?
      </p>
      <button type="button" class="container-card__container-button">
         Visit
      </button>
   </div>
</template>

<script setup>
</script>

<style lang="css" scoped>
.container-card {
   width: 25%;
   border: 1px solid gray;
   text-align: center;
   margin-right: 5%;
}
.container-card__container-title {
   font-size: 20px;
   font-weight: bold;
}
.container-card__container-img {
   width: 100%;
}
.container-card__container-subtitle {
   font-size: 15px;
   color: coral;
}
.container-card__container-button {
   background: rgba(0, 128, 0, 0.575);
   width: 5em;
   border-radius: 0.3em;
}
.container-card__container-button:hover {
   background-color: bisque;
   font-weight: bold;
}
</style>