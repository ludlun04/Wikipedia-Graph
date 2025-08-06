<script setup lang="ts">
import type {GraphEdge, GraphNode} from '@/types/types';
import { Network } from "vue3-visjs"
import { ref } from 'vue'

const nodes = ref<GraphNode[]>([
  {name: 'A', id: 1},
  {name: 'B', id: 2},
  {name: 'C', id: 3},
  {name: 'D', id: 4},
  {name: 'E', id: 5}
])

const edges = ref<GraphEdge[]>([
  {from: 1, to: 2},
  {from: 2, to: 3},
  {from: 3, to: 1},
  {from: 4, to: 0},
  {from: 0, to: 1},
])

const updateLinks = () => {
  //links.value[0] = {source: nodes.value[1], target: nodes.value[4]}
  //links.value[5] = {source: nodes.value[1], target: nodes.value[4]}
  nodes.value.push({name: 'F', id: 6})
}

</script>

<template>
  <h1>Graph</h1>
  <Network
    class="network"
    :nodes="nodes"
    :edges="edges"
  />
  <button @click="updateLinks">
    Change graph
  </button>
</template>

<style>
.network {
  width: 100vw;
  height: 80vh;
}
</style>
