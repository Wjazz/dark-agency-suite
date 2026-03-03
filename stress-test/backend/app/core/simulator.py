"""
Institutional Stress Test - Process Simulation Engine

Uses Dark Agency agent model to identify bottlenecks in 
organizational processes by simulating how Dark Agents
navigate bureaucracy vs Normal Agents.

Key insight: Where Dark Agents break rules most frequently
= Where the process has unnecessary friction.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random
import json


class NodeType(Enum):
    """Types of nodes in a process map"""
    START = "start"
    END = "end"
    TASK = "task"                    # Normal work step
    GATEWAY_XOR = "gateway_xor"      # Decision point (exclusive)
    GATEWAY_AND = "gateway_and"      # Parallel split/join
    APPROVAL = "approval"            # Bureaucratic checkpoint (WALL)
    SUBPROCESS = "subprocess"        # Nested process


class AgentType(Enum):
    DARK_AGENT = "dark"      # High S_Agency, will break rules strategically
    NORMAL_AGENT = "normal"  # Follows rules, waits at approvals
    TOXIC_AGENT = "toxic"    # High G, causes damage without progress


@dataclass
class ProcessNode:
    """A node in the organizational process"""
    id: str
    name: str
    node_type: NodeType
    
    # Execution time (ticks)
    base_time: int = 1
    
    # For approvals (bureaucracy)
    approval_probability: float = 0.8  # Chance of passing
    wait_time: int = 5                 # Ticks to wait
    
    # Connections
    next_nodes: List[str] = field(default_factory=list)
    
    # Analytics
    visits: int = 0
    transgressions: int = 0  # Times Dark Agents bypassed
    total_wait: int = 0


@dataclass
class ProcessMap:
    """An organizational process loaded from JSON/BPMN"""
    name: str
    nodes: Dict[str, ProcessNode]
    start_node: str
    end_node: str
    
    @classmethod
    def from_json(cls, data: dict) -> 'ProcessMap':
        """Load process from JSON format"""
        nodes = {}
        for n in data['nodes']:
            nodes[n['id']] = ProcessNode(
                id=n['id'],
                name=n['name'],
                node_type=NodeType(n['type']),
                base_time=n.get('base_time', 1),
                approval_probability=n.get('approval_probability', 0.8),
                wait_time=n.get('wait_time', 5),
                next_nodes=n.get('next', [])
            )
        return cls(
            name=data['name'],
            nodes=nodes,
            start_node=data['start'],
            end_node=data['end']
        )


@dataclass
class SimAgent:
    """An agent navigating the process"""
    id: int
    agent_type: AgentType
    
    # Personality (simplified Bifactor)
    s_agency: float = 0.5
    g_factor: float = 0.2
    
    # State
    current_node: str = ""
    ticks_at_node: int = 0
    completed: bool = False
    total_time: int = 0
    
    # Behavior tracking
    rules_broken: int = 0
    approvals_waited: int = 0
    nodes_visited: List[str] = field(default_factory=list)


class ProcessSimulator:
    """
    Simulates agents navigating organizational processes
    to identify bottlenecks and friction points.
    """
    
    def __init__(self, process: ProcessMap):
        self.process = process
        self.agents: List[SimAgent] = []
        self.tick = 0
        self.max_ticks = 500
        
    def create_population(
        self, 
        n_dark: int = 10, 
        n_normal: int = 30,
        n_toxic: int = 5
    ) -> None:
        """Create agent population for simulation"""
        agent_id = 0
        
        # Dark Agents (High S_Agency)
        for _ in range(n_dark):
            self.agents.append(SimAgent(
                id=agent_id,
                agent_type=AgentType.DARK_AGENT,
                s_agency=random.uniform(0.7, 0.95),
                g_factor=random.uniform(0.1, 0.35),
                current_node=self.process.start_node
            ))
            agent_id += 1
        
        # Normal Agents (Low everything)
        for _ in range(n_normal):
            self.agents.append(SimAgent(
                id=agent_id,
                agent_type=AgentType.NORMAL_AGENT,
                s_agency=random.uniform(0.2, 0.45),
                g_factor=random.uniform(0.1, 0.25),
                current_node=self.process.start_node
            ))
            agent_id += 1
        
        # Toxic Agents (High G)
        for _ in range(n_toxic):
            self.agents.append(SimAgent(
                id=agent_id,
                agent_type=AgentType.TOXIC_AGENT,
                s_agency=random.uniform(0.3, 0.5),
                g_factor=random.uniform(0.7, 0.95),
                current_node=self.process.start_node
            ))
            agent_id += 1
    
    def step(self) -> bool:
        """Execute one simulation tick. Returns False when done."""
        self.tick += 1
        
        all_done = True
        for agent in self.agents:
            if not agent.completed:
                all_done = False
                self._process_agent(agent)
        
        return not all_done and self.tick < self.max_ticks
    
    def _process_agent(self, agent: SimAgent) -> None:
        """Process one agent's decision and movement"""
        node = self.process.nodes[agent.current_node]
        node.visits += 1
        
        # Check if at end
        if node.node_type == NodeType.END:
            agent.completed = True
            return
        
        agent.ticks_at_node += 1
        agent.total_time += 1
        
        # Handle different node types
        if node.node_type == NodeType.APPROVAL:
            self._handle_approval(agent, node)
        elif node.node_type == NodeType.TASK:
            self._handle_task(agent, node)
        elif node.node_type in (NodeType.GATEWAY_XOR, NodeType.GATEWAY_AND):
            self._handle_gateway(agent, node)
        elif node.node_type == NodeType.START:
            self._move_to_next(agent, node)
    
    def _handle_approval(self, agent: SimAgent, node: ProcessNode) -> None:
        """Handle bureaucratic approval checkpoint"""
        
        if agent.agent_type == AgentType.DARK_AGENT:
            # Dark Agent: Calculate if worth bypassing
            bypass_probability = agent.s_agency * 0.7
            
            if random.random() < bypass_probability:
                # Bypass the approval (transgression)
                node.transgressions += 1
                agent.rules_broken += 1
                self._move_to_next(agent, node)
                return
        
        elif agent.agent_type == AgentType.TOXIC_AGENT:
            # Toxic: Complain but don't progress efficiently
            if agent.ticks_at_node > node.wait_time * 2:
                # Eventually gives up or causes problems
                if random.random() < 0.3:
                    self._move_to_next(agent, node)
            return
        
        # Normal behavior: Wait for approval
        if agent.ticks_at_node >= node.wait_time:
            if random.random() < node.approval_probability:
                agent.approvals_waited += 1
                node.total_wait += agent.ticks_at_node
                self._move_to_next(agent, node)
            else:
                # Rejected - wait more
                agent.ticks_at_node = 0
    
    def _handle_task(self, agent: SimAgent, node: ProcessNode) -> None:
        """Handle normal task node"""
        if agent.ticks_at_node >= node.base_time:
            self._move_to_next(agent, node)
    
    def _handle_gateway(self, agent: SimAgent, node: ProcessNode) -> None:
        """Handle decision gateway"""
        # For XOR: Choose random path
        # For AND: In reality would spawn parallel, but simplified here
        self._move_to_next(agent, node)
    
    def _move_to_next(self, agent: SimAgent, node: ProcessNode) -> None:
        """Move agent to next node"""
        if node.next_nodes:
            next_node = random.choice(node.next_nodes)
            agent.nodes_visited.append(agent.current_node)
            agent.current_node = next_node
            agent.ticks_at_node = 0
    
    def run(self) -> 'SimulationResult':
        """Run complete simulation"""
        while self.step():
            pass
        return self.get_results()
    
    def get_results(self) -> 'SimulationResult':
        """Compile simulation results"""
        return SimulationResult(
            process_name=self.process.name,
            total_ticks=self.tick,
            agents=self.agents,
            nodes=self.process.nodes
        )


@dataclass
class BottleneckReport:
    """A detected bottleneck in the process"""
    node_id: str
    node_name: str
    severity: float  # 0-1, how bad
    transgression_rate: float  # How often Dark Agents bypass
    avg_wait_time: float
    recommendation: str


@dataclass
class SimulationResult:
    """Results from a stress test simulation"""
    process_name: str
    total_ticks: int
    agents: List[SimAgent]
    nodes: Dict[str, ProcessNode]
    
    def get_bottlenecks(self) -> List[BottleneckReport]:
        """Analyze results to find bottlenecks"""
        bottlenecks = []
        
        for node_id, node in self.nodes.items():
            if node.node_type != NodeType.APPROVAL:
                continue
            
            if node.visits == 0:
                continue
            
            transgression_rate = node.transgressions / max(1, node.visits)
            avg_wait = node.total_wait / max(1, node.visits - node.transgressions)
            
            # High transgression = Dark Agents found this node unnecessary
            if transgression_rate > 0.3:
                severity = min(1.0, transgression_rate + avg_wait / 20)
                
                bottlenecks.append(BottleneckReport(
                    node_id=node_id,
                    node_name=node.name,
                    severity=severity,
                    transgression_rate=transgression_rate,
                    avg_wait_time=avg_wait,
                    recommendation=self._get_recommendation(transgression_rate, avg_wait)
                ))
        
        return sorted(bottlenecks, key=lambda x: x.severity, reverse=True)
    
    def _get_recommendation(self, transgression_rate: float, avg_wait: float) -> str:
        if transgression_rate > 0.7:
            return "ELIMINATE: This approval adds friction without value. Dark Agents routinely bypass it successfully."
        elif transgression_rate > 0.5:
            return "STREAMLINE: Convert to async approval or delegate to department level."
        elif avg_wait > 10:
            return "ACCELERATE: Reduce SLA or add parallel approval paths."
        else:
            return "MONITOR: Some friction detected, continue observing."
    
    def get_summary(self) -> dict:
        """Get summary statistics"""
        dark_agents = [a for a in self.agents if a.agent_type == AgentType.DARK_AGENT]
        normal_agents = [a for a in self.agents if a.agent_type == AgentType.NORMAL_AGENT]
        
        dark_completed = [a for a in dark_agents if a.completed]
        normal_completed = [a for a in normal_agents if a.completed]
        
        return {
            "process_name": self.process_name,
            "total_ticks": self.total_ticks,
            "dark_agents": {
                "total": len(dark_agents),
                "completed": len(dark_completed),
                "avg_time": sum(a.total_time for a in dark_completed) / max(1, len(dark_completed)),
                "avg_rules_broken": sum(a.rules_broken for a in dark_agents) / max(1, len(dark_agents))
            },
            "normal_agents": {
                "total": len(normal_agents),
                "completed": len(normal_completed),
                "avg_time": sum(a.total_time for a in normal_completed) / max(1, len(normal_completed)),
                "avg_approvals_waited": sum(a.approvals_waited for a in normal_agents) / max(1, len(normal_agents))
            },
            "efficiency_gap": self._calculate_efficiency_gap(dark_completed, normal_completed),
            "bottleneck_count": len(self.get_bottlenecks())
        }
    
    def _calculate_efficiency_gap(
        self, 
        dark_completed: List[SimAgent], 
        normal_completed: List[SimAgent]
    ) -> float:
        """Calculate how much faster Dark Agents complete vs Normal"""
        if not dark_completed or not normal_completed:
            return 0.0
        
        dark_avg = sum(a.total_time for a in dark_completed) / len(dark_completed)
        normal_avg = sum(a.total_time for a in normal_completed) / len(normal_completed)
        
        if normal_avg == 0:
            return 0.0
        
        return (normal_avg - dark_avg) / normal_avg


def run_stress_test(process_json: dict, n_dark: int = 20, n_normal: int = 50) -> SimulationResult:
    """
    Run a complete stress test simulation
    
    Args:
        process_json: Process map in JSON format
        n_dark: Number of Dark Agents to simulate
        n_normal: Number of Normal Agents to simulate
    
    Returns:
        SimulationResult with bottleneck analysis
    """
    process = ProcessMap.from_json(process_json)
    simulator = ProcessSimulator(process)
    simulator.create_population(n_dark=n_dark, n_normal=n_normal, n_toxic=5)
    return simulator.run()
