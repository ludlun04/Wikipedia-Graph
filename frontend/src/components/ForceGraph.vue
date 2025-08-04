<script setup lang="ts">
import * as d3 from "d3"
import {onMounted, ref, defineProps, watch} from "vue";
import type { GraphNode, GraphLink } from "../types.ts"

const props = defineProps<{
  nodes: GraphNode[]
  links: GraphLink[]
}>()


const graphContainer = ref(null)

onMounted(() => {
  renderGraph(props.nodes, props.links);
})

watch(props, () => {
  renderGraph(props.nodes, props.links)
})

const renderGraph = (nodes: GraphNode[], links: GraphLink[]) => {
  console.log('Rendering graph', nodes, links)
  const width = 800;
  const height = 600;

  const svg = d3.select(graphContainer.value)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const simulation = d3.forceSimulation<GraphNode>(nodes)
    .force("link", d3.forceLink<GraphNode, GraphLink>(links).id((n: GraphNode) => n.id))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.append("g")
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .attr("stroke", "#999")
    .attr("stroke-width", 2);

  const node = svg.append("g")
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", 10)
    .attr("fill", "#69b3a2");

  const label = svg.append("g")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .text((n: GraphNode) => n.name)
    .attr("font-size", 12)
    .attr("dx", 15)
    .attr("dy", 4);

  simulation.on("tick", () => {
    link
      .attr("x1", ((l: GraphLink) => l.source.x ?? 0))
      .attr("y1", ((l: GraphLink) => l.source.y ?? 0))
      .attr("x2", ((l: GraphLink) => l.target.x ?? 0))
      .attr("y2", ((l: GraphLink) => l.target.y ?? 0));

    node
      .attr("cx", ((d: GraphNode) => d.x ?? 0))
      .attr("cy", ((d: GraphNode) => d.y ?? 0));

    label
      .attr("x", ((d: GraphNode) => d.x ?? ''))
      .attr("y", ((d: GraphNode) => d.y ?? ''));
  });
};

</script>

<template>
  <div
    ref="graphContainer"
    class="graph-container"
  />
</template>

<style>
.graph-container {
  width: 100%;
  height: 100vh;
}
</style>
