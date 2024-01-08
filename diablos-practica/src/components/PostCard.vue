<template>
    <div class="post-card">
        <h3>Carta de envio</h3>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni provident quibusdam deleniti nobis qui hic? Quasi,
            ipsum, magnam quisquam dolorem nobis assumenda, aliquid odio totam aut id ipsam neque minus!</p>
        <PostButton />
    </div>
</template>

<script setup>
import PostButton from './PostButton.vue';
</script>

<style scoped>
.post-card {
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    border: 1px solid #ccc;
}
</style>