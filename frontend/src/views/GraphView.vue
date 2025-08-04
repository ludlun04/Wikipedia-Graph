<script setup lang="ts">
import Graph from '@/components/Graph.vue';
import type {GraphLink, GraphNode} from '@/types';
import { ref } from 'vue'

const nodes = ref<GraphNode[]>([
  {name: 'A', id: 1},
  {name: 'B', id: 2},
  {name: 'C', id: 3},
  {name: 'D', id: 4},
  {name: 'E', id: 5}
])

const links = ref<GraphLink[]>([
  {source: nodes.value[1], target: nodes.value[2]},
  {source: nodes.value[2], target: nodes.value[3]},
  {source: nodes.value[3], target: nodes.value[1]},
  {source: nodes.value[4], target: nodes.value[0]},
  {source: nodes.value[0], target: nodes.value[1]},
])

const updateLinks = () => {
  links.value[0] = {source: nodes.value[1], target: nodes.value[4]}
}

</script>

<template>
  <h1>Graph</h1>
  <Graph
    :nodes="nodes"
    :links="links"
  />
  <button @click="updateLinks">
    Change graph
  </button>
</template>
