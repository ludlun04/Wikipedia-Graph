
export interface GraphNode extends d3.SimulationNodeDatum {
  id: number
  name: string
}

export interface GraphLink extends d3.SimulationLinkDatum<GraphNode> {
  source: GraphNode
  target: GraphNode
}

