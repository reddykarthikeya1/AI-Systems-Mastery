from dataclasses import dataclass

@dataclass
class HldSystem:
    id: int
    filename: str
    title: str
    metaphor: str
    sec1_requirements: str
    sec2_estimates_text: str
    sec2_estimates_py: str
    sec3_api_design: str
    sec4_data_model: str
    sec5_diagram: str
    sec6_deep_dive: str
    sec7_scaling: str
    sec8_failure_modes: str
    sec9_tradeoffs: str
    sec10_cost: str
    sec11_interview_timeline: str
    sec12_followups: str
