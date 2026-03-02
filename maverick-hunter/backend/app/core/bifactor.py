"""
Maverick Hunter - HR Tech SaaS
Bifactor S-1 Core Engine

Identifies Dark Innovators vs Toxic candidates using 
the thesis model: "Dark Agency in Institutional Voids"
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple
import math


class Classification(Enum):
    """Candidate classification based on Bifactor model"""
    MAVERICK = "MAVERICK"           # 🔵 High S_Agency, Low G - HIRE for innovation
    PERFORMER = "PERFORMER"         # 🟢 Moderate S_Agency, Low G - HIRE
    RELIABLE = "RELIABLE"           # 🟡 Low S_Agency, Low G - HIRE for structured roles
    MONITOR = "MONITOR"             # 🟠 Moderate G, High S_Agency - HIRE with coaching
    RISK = "RISK"                   # 🔴 High G - DO NOT HIRE


@dataclass
class PsychometricScores:
    """Raw scores from SD4 assessment (0-1 normalized)"""
    narcissism: float
    machiavellianism: float
    psychopathy: float
    sadism: float
    
    # Additional constructs
    vigilance: float = 0.5      # VEE
    psycap: float = 0.5         # Psychological Capital
    pops: float = 0.5           # Perceived Org Politics


@dataclass 
class BifactorResult:
    """Output from Bifactor S-1 model"""
    g_factor: float             # General Antagonistic Factor
    s_agency: float             # Dark Agency (residual)
    classification: Classification
    confidence: float
    
    # Predictions
    eib_prediction: float       # Intrapreneurial Behavior
    cwb_o_risk: float           # Organizational transgression risk
    cwb_i_risk: float           # Interpersonal damage risk
    
    # Semaphore color for UI
    @property
    def semaphore_color(self) -> str:
        return {
            Classification.MAVERICK: "cyan",
            Classification.PERFORMER: "green", 
            Classification.RELIABLE: "yellow",
            Classification.MONITOR: "orange",
            Classification.RISK: "red"
        }[self.classification]
    
    @property
    def hire_recommendation(self) -> str:
        return {
            Classification.MAVERICK: "STRONGLY RECOMMEND - Innovation/Leadership roles",
            Classification.PERFORMER: "RECOMMEND - High growth potential",
            Classification.RELIABLE: "RECOMMEND - Structured/Process roles",
            Classification.MONITOR: "CONDITIONAL - Requires coaching/supervision",
            Classification.RISK: "DO NOT RECOMMEND - High toxicity risk"
        }[self.classification]


class BifactorEngine:
    """
    Bifactor S-1 Model Implementation
    
    Extracts G (general antagonistic factor) and S_Agency (dark agency)
    from Dark Tetrad scores to classify candidates.
    """
    
    # Factor loadings from thesis
    LOADING_PSYCHOPATHY = 0.45
    LOADING_SADISM = 0.40
    LOADING_MACH = 0.10
    LOADING_NARC = 0.05
    
    # Thresholds
    G_THRESHOLD_HIGH = 0.70
    G_THRESHOLD_MODERATE = 0.50
    S_AGENCY_THRESHOLD_HIGH = 0.65
    S_AGENCY_THRESHOLD_MODERATE = 0.45
    
    def extract_g_factor(self, scores: PsychometricScores) -> float:
        """
        Extract G-factor (antagonistic core)
        
        G represents the shared variance of psychopathy and sadism -
        the destructive elements of the Dark Tetrad.
        """
        g = (self.LOADING_PSYCHOPATHY * scores.psychopathy +
             self.LOADING_SADISM * scores.sadism +
             self.LOADING_MACH * scores.machiavellianism +
             self.LOADING_NARC * scores.narcissism)
        return max(0.0, min(1.0, g))
    
    def calculate_s_agency(self, scores: PsychometricScores, g: float) -> float:
        """
        Calculate S_Agency (Dark Agency) as residual
        
        S_Agency = strategic darkness after removing G contamination.
        This is what predicts intrapreneurial behavior (EIB).
        """
        raw_agency = 0.50 * scores.machiavellianism + 0.50 * scores.narcissism
        
        # Remove G contamination
        s_agency = raw_agency - (g * 0.35)
        
        # VEE amplifies expression
        s_agency *= (1.0 + scores.vigilance * 0.2)
        
        return max(0.0, min(1.0, s_agency))
    
    def predict_eib(self, scores: PsychometricScores, g: float, s: float) -> float:
        """Predict Intrapreneurial Behavior score"""
        effective_vee = scores.vigilance * (1.0 + scores.pops * s * 0.5)
        
        eib = (0.30 * s +           # H1a: S_Agency → EIB (+)
               -0.20 * g +          # H1c: G → EIB (-)
               0.25 * effective_vee +
               0.15 * scores.psycap +
               0.10 * (s * scores.psycap))
        
        return max(0.0, min(1.0, eib + 0.3))
    
    def predict_cwb_o(self, g: float, s: float) -> float:
        """Predict CWB-O (organizational transgression) risk"""
        return max(0.0, min(1.0, 0.30 * s + 0.25 * g))
    
    def predict_cwb_i(self, g: float, s: float) -> float:
        """Predict CWB-I (interpersonal damage) risk"""
        return max(0.0, min(1.0, 0.70 * g + 0.05 * s))
    
    def classify(self, g: float, s: float) -> Tuple[Classification, float]:
        """
        Classify candidate based on G and S_Agency
        
        Returns (Classification, confidence)
        """
        # High G = RISK (regardless of S_Agency)
        if g > self.G_THRESHOLD_HIGH:
            return Classification.RISK, 0.85 + (g - 0.7) * 0.5
        
        # High S_Agency + Low G = MAVERICK
        if s > self.S_AGENCY_THRESHOLD_HIGH and g < self.G_THRESHOLD_MODERATE:
            return Classification.MAVERICK, 0.80 + (s - 0.65) * 0.5
        
        # High S_Agency + Moderate G = MONITOR
        if s > self.S_AGENCY_THRESHOLD_HIGH and g >= self.G_THRESHOLD_MODERATE:
            return Classification.MONITOR, 0.70
        
        # Moderate S_Agency + Low G = PERFORMER
        if s > self.S_AGENCY_THRESHOLD_MODERATE and g < self.G_THRESHOLD_MODERATE:
            return Classification.PERFORMER, 0.75
        
        # Low S_Agency + Low G = RELIABLE
        return Classification.RELIABLE, 0.85
    
    def analyze(self, scores: PsychometricScores) -> BifactorResult:
        """
        Full analysis pipeline
        
        Takes raw psychometric scores, returns full classification result.
        """
        g = self.extract_g_factor(scores)
        s = self.calculate_s_agency(scores, g)
        
        classification, confidence = self.classify(g, s)
        
        return BifactorResult(
            g_factor=round(g, 4),
            s_agency=round(s, 4),
            classification=classification,
            confidence=round(min(1.0, confidence), 4),
            eib_prediction=round(self.predict_eib(scores, g, s), 4),
            cwb_o_risk=round(self.predict_cwb_o(g, s), 4),
            cwb_i_risk=round(self.predict_cwb_i(g, s), 4)
        )


# Global engine instance
engine = BifactorEngine()


def analyze_candidate(scores: PsychometricScores) -> BifactorResult:
    """Convenience function for analyzing a candidate"""
    return engine.analyze(scores)
