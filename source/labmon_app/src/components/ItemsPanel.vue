<template>

    <ItemToggle :itemData="potion" :onSelect="handleItemSelected" />

</template>

<script setup>
import ItemToggle from './ItemToggle.vue'

function handleItemSelected(itemId) {
  console.log('Selected item ID:', itemId)
}

const potion = {
  id: 42,
  name: 'Potion',
  quantity: 3,
  sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/potion.png'
}

</script>