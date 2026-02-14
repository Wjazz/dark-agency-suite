"""
Founder Risk Assessment AI - IVR Engine

Institutional Void Readiness (IVR) Algorithm for evaluating
startup founders in emerging markets (Latam, Africa, SEA).

Key insight: In institutional voids, a "good and obedient" founder
fails. You need a founder with Dark Agency to navigate corruption,
bureaucracy, and informality - without being a criminal.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class FounderClassification(Enum):
    """Founder investment classification"""
    HIGH_POTENTIAL_MAVERICK = "HIGH_POTENTIAL_MAVERICK"  # 🔵 Ideal for LatAm
    ADAPTABLE_INNOVATOR = "ADAPTABLE_INNOVATOR"         # 🟢 Good potential
    STRUCTURED_OPERATOR = "STRUCTURED_OPERATOR"         # 🟡 Better for stable markets
    RED_FLAG_MONITOR = "RED_FLAG_MONITOR"              # 🟠 Needs due diligence
    CRIMINAL_RISK = "CRIMINAL_RISK"                    # 🔴 Do not invest


class InvestmentRecommendation(Enum):
    STRONG_INVEST = "STRONG_INVEST"
    INVEST = "INVEST"
    CONDITIONAL = "CONDITIONAL"
    PASS = "PASS"
    REJECT = "REJECT"


@dataclass
class FounderProfile:
    """Founder's psychometric profile"""
    # Core Dark Tetrad (normalized 0-1)
    narcissism: float
    machiavellianism: float
    psychopathy: float
    sadism: float
    
    # Thesis constructs
    vigilance: float          # VEE - Environmental sensing
    psycap: float             # Psychological Capital (resilience)
    pops: float               # Political navigation ability
    
    # Business context
    market_chaos: float       # How chaotic is the target market (0-1)
    regulatory_burden: float  # How much red tape (0-1)
    corruption_index: float   # Transparency International inverse


@dataclass
class IVRResult:
    """Institutional Void Readiness Assessment Result"""
    # Core scores
    ivr_score: float          # 0-1, main output
    g_factor: float           # Toxicity risk
    s_agency: float           # Strategic darkness
    
    # Classification
    classification: FounderClassification
    recommendation: InvestmentRecommendation
    confidence: float
    
    # Risk flags
    risk_flags: List[str]
    
    # Narrative for VC report
    narrative: str
    
    @property
    def semaphore_color(self) -> str:
        return {
            FounderClassification.HIGH_POTENTIAL_MAVERICK: "cyan",
            FounderClassification.ADAPTABLE_INNOVATOR: "green",
            FounderClassification.STRUCTURED_OPERATOR: "yellow",
            FounderClassification.RED_FLAG_MONITOR: "orange",
            FounderClassification.CRIMINAL_RISK: "red"
        }[self.classification]


class IVREngine:
    """
    Institutional Void Readiness Engine
    
    Evaluates founders for their ability to navigate institutional
    voids in emerging markets.
    """
    
    # IVR Formula weights (from thesis)
    # IVR = 0.35*S + 0.25*VEE + 0.20*PsyCap + 0.15*POPS - 0.30*G
    WEIGHT_S_AGENCY = 0.35
    WEIGHT_VEE = 0.25
    WEIGHT_PSYCAP = 0.20
    WEIGHT_POPS = 0.15
    WEIGHT_G = -0.30
    
    # Thresholds
    G_THRESHOLD_CRITICAL = 0.75
    G_THRESHOLD_HIGH = 0.60
    S_THRESHOLD_HIGH = 0.65
    IVR_THRESHOLD_HIGH = 0.70
    IVR_THRESHOLD_MODERATE = 0.50
    
    def extract_g_factor(self, profile: FounderProfile) -> float:
        """Extract G-factor (antagonistic core)"""
        g = (0.45 * profile.psychopathy +
             0.40 * profile.sadism +
             0.10 * profile.machiavellianism +
             0.05 * profile.narcissism)
        return max(0.0, min(1.0, g))
    
    def calculate_s_agency(self, profile: FounderProfile, g: float) -> float:
        """Calculate S_Agency (Dark Agency)"""
        raw_agency = 0.50 * profile.machiavellianism + 0.50 * profile.narcissism
        s_agency = raw_agency - (g * 0.35)
        
        # VEE amplifies S_Agency expression
        s_agency *= (1.0 + profile.vigilance * 0.2)
        
        return max(0.0, min(1.0, s_agency))
    
    def calculate_ivr(self, profile: FounderProfile, g: float, s: float) -> float:
        """
        Calculate Institutional Void Readiness score
        
        IVR = (0.35 × S_Agency) + (0.25 × VEE) + (0.20 × PsyCap) 
            + (0.15 × POPS) - (0.30 × G)
        """
        ivr = (self.WEIGHT_S_AGENCY * s +
               self.WEIGHT_VEE * profile.vigilance +
               self.WEIGHT_PSYCAP * profile.psycap +
               self.WEIGHT_POPS * profile.pops +
               self.WEIGHT_G * g)
        
        # Adjust for market chaos - higher chaos needs higher IVR
        market_adjustment = profile.market_chaos * 0.1
        
        return max(0.0, min(1.0, ivr + market_adjustment + 0.2))  # +0.2 base
    
    def classify(
        self, 
        g: float, 
        s: float, 
        ivr: float,
        profile: FounderProfile
    ) -> Tuple[FounderClassification, InvestmentRecommendation, float]:
        """Classify founder and generate recommendation"""
        
        # Criminal risk: High G, regardless of other factors
        if g > self.G_THRESHOLD_CRITICAL:
            return (
                FounderClassification.CRIMINAL_RISK,
                InvestmentRecommendation.REJECT,
                0.90
            )
        
        # Red flag: Moderate-high G with concerning patterns
        if g > self.G_THRESHOLD_HIGH:
            return (
                FounderClassification.RED_FLAG_MONITOR,
                InvestmentRecommendation.PASS,
                0.75
            )
        
        # High Potential Maverick: High S, High IVR, Low G
        if s > self.S_THRESHOLD_HIGH and ivr > self.IVR_THRESHOLD_HIGH and g < 0.35:
            return (
                FounderClassification.HIGH_POTENTIAL_MAVERICK,
                InvestmentRecommendation.STRONG_INVEST,
                0.85
            )
        
        # Adaptable Innovator: Good S, Moderate-High IVR
        if s > 0.50 and ivr > self.IVR_THRESHOLD_MODERATE:
            return (
                FounderClassification.ADAPTABLE_INNOVATOR,
                InvestmentRecommendation.INVEST,
                0.75
            )
        
        # Structured Operator: Low S, Low G - better for stable markets
        if s < 0.45 and g < 0.35 and ivr < self.IVR_THRESHOLD_MODERATE:
            return (
                FounderClassification.STRUCTURED_OPERATOR,
                InvestmentRecommendation.CONDITIONAL,
                0.70
            )
        
        # Default: Needs more analysis
        return (
            FounderClassification.STRUCTURED_OPERATOR,
            InvestmentRecommendation.CONDITIONAL,
            0.60
        )
    
    def detect_risk_flags(self, profile: FounderProfile, g: float, s: float) -> List[str]:
        """Detect specific risk flags for due diligence"""
        flags = []
        
        if profile.psychopathy > 0.70:
            flags.append("HIGH_PSYCHOPATHY: May have difficulty with long-term commitments and team loyalty")
        
        if profile.sadism > 0.50:
            flags.append("SADISM_INDICATOR: Monitor for toxic leadership patterns")
        
        if g > 0.50 and s < 0.40:
            flags.append("TOXIC_WITHOUT_STRATEGY: High antagonism without productive channeling")
        
        if profile.psycap < 0.30:
            flags.append("LOW_RESILIENCE: May struggle with startup stress and pivots")
        
        if profile.vigilance < 0.35:
            flags.append("LOW_AWARENESS: May miss market signals and pivot opportunities")
        
        if profile.pops < 0.30 and profile.market_chaos > 0.70:
            flags.append("POLITICAL_MISMATCH: Low political skill in highly political market")
        
        return flags
    
    def generate_narrative(
        self, 
        profile: FounderProfile,
        classification: FounderClassification,
        ivr: float,
        g: float,
        s: float,
        risk_flags: List[str]
    ) -> str:
        """Generate narrative report for VC partners"""
        
        narratives = {
            FounderClassification.HIGH_POTENTIAL_MAVERICK: f"""
High-potential founder with exceptional institutional navigation capability.
IVR Score: {ivr:.2f} indicates strong ability to operate in chaotic markets.
S_Agency ({s:.2f}) suggests strategic rule-bending for productive outcomes.
Low G-factor ({g:.2f}) indicates this is strategic, not antisocial.
RECOMMENDATION: Strong investment candidate for emerging market plays.
""",
            FounderClassification.ADAPTABLE_INNOVATOR: f"""
Solid founder profile with good adaptability markers.
IVR Score: {ivr:.2f} shows adequate void navigation capability.
Balanced S_Agency ({s:.2f}) suggests pragmatic approach to obstacles.
RECOMMENDATION: Good investment candidate with standard due diligence.
""",
            FounderClassification.STRUCTURED_OPERATOR: f"""
Founder profile indicates preference for structured environments.
Lower IVR Score ({ivr:.2f}) may struggle in highly chaotic markets.
Lower S_Agency ({s:.2f}) suggests rule-following tendency.
RECOMMENDATION: Better suited for Series B+ or stable market expansion.
""",
            FounderClassification.RED_FLAG_MONITOR: f"""
WARNING: Profile shows concerning patterns requiring deep due diligence.
Elevated G-factor ({g:.2f}) indicates potential for counterproductive behavior.
{len(risk_flags)} risk flags detected.
RECOMMENDATION: Do not proceed without extensive reference checks.
""",
            FounderClassification.CRIMINAL_RISK: f"""
ALERT: Profile indicates high risk of unethical/illegal behavior.
G-factor ({g:.2f}) exceeds critical threshold.
Strong indicators of antisocial tendencies that cannot be productively channeled.
RECOMMENDATION: Pass on investment. Document concerns for future reference.
"""
        }
        
        return narratives.get(classification, "Assessment inconclusive.").strip()
    
    def assess(self, profile: FounderProfile) -> IVRResult:
        """
        Full founder assessment pipeline
        
        Takes founder profile, returns complete IVR assessment.
        """
        g = self.extract_g_factor(profile)
        s = self.calculate_s_agency(profile, g)
        ivr = self.calculate_ivr(profile, g, s)
        
        classification, recommendation, confidence = self.classify(g, s, ivr, profile)
        risk_flags = self.detect_risk_flags(profile, g, s)
        narrative = self.generate_narrative(
            profile, classification, ivr, g, s, risk_flags
        )
        
        return IVRResult(
            ivr_score=round(ivr, 4),
            g_factor=round(g, 4),
            s_agency=round(s, 4),
            classification=classification,
            recommendation=recommendation,
            confidence=round(confidence, 4),
            risk_flags=risk_flags,
            narrative=narrative
        )


# Global engine instance
engine = IVREngine()


def assess_founder(profile: FounderProfile) -> IVRResult:
    """Convenience function for founder assessment"""
    return engine.assess(profile)
