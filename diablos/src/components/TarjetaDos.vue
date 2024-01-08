<template>
   <div class="container-card">
      <img src="../assets/logo.png" alt="Mi foto" class="container-card__img" />
      <h2 class="container-card__title">Mi nombre es</h2>
      <p class="container-card__subtitle">Soy de Venezuela</p>
      <button class="container-card__container-button-btn btn1">BTN1</button>
      <button class="container-card__container-button-btn btn2">BTN2</button>
   </div>
</template>

<script setup>
</script>

<style lang="css" scoped>
.container-card {
   width: 25%;
   padding-top: 10px;
   text-align: center;
   border: 1px solid gray;
}
.container-card__img {
   width: 90%;
   border: 1px solid #335ab2;
   border-radius: 50%;
}
.container-card__title {
   font-size: 25px;
}
.container-card__container-button-btn {
   width: 60px;
   margin: 5%;
}
.btn1{
    background: #15aefa;
    width: 35%;
    border-radius: 15%;
}
.btn2{
    background: #f25cce;
    width: 35%;
    border-radius: 15%;
}
</style>