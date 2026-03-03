"""
SD4 Assessment Items
Short Dark Tetrad Scale for Maverick Hunter
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class Construct(Enum):
    NARCISSISM = "narcissism"
    MACHIAVELLIANISM = "machiavellianism"
    PSYCHOPATHY = "psychopathy"
    SADISM = "sadism"
    VIGILANCE = "vigilance"      # VEE
    PSYCAP = "psycap"            # Psychological Capital


@dataclass
class AssessmentItem:
    code: str
    text: str
    text_es: str
    construct: Construct
    reverse_scored: bool = False


# SD4 Items (adapted for workplace context)
SD4_ITEMS: List[AssessmentItem] = [
    # Narcissism (7 items)
    AssessmentItem("NARC_01", "I tend to want others to admire me", 
                   "Tiendo a querer que otros me admiren", Construct.NARCISSISM),
    AssessmentItem("NARC_02", "I tend to want others to pay attention to me",
                   "Tiendo a querer que otros me presten atención", Construct.NARCISSISM),
    AssessmentItem("NARC_03", "I have been compared to famous people",
                   "Me han comparado con personas famosas", Construct.NARCISSISM),
    AssessmentItem("NARC_04", "I am an average person", 
                   "Soy una persona promedio", Construct.NARCISSISM, reverse_scored=True),
    AssessmentItem("NARC_05", "I insist on getting the respect I deserve",
                   "Insisto en obtener el respeto que merezco", Construct.NARCISSISM),
    AssessmentItem("NARC_06", "I like to show off every now and then",
                   "Me gusta presumir de vez en cuando", Construct.NARCISSISM),
    AssessmentItem("NARC_07", "I have a natural talent for influencing people",
                   "Tengo un talento natural para influir en las personas", Construct.NARCISSISM),
    
    # Machiavellianism (9 items)
    AssessmentItem("MACH_01", "I believe in being strategic when dealing with people",
                   "Creo en ser estratégico al tratar con personas", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_02", "Whatever it takes, you must get the important people on your side",
                   "Cueste lo que cueste, debes tener a las personas importantes de tu lado", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_03", "I avoid direct conflict with others because they may be useful in the future",
                   "Evito conflictos directos porque las personas pueden ser útiles en el futuro", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_04", "It's wise to keep track of information that you can use against people later",
                   "Es sabio guardar información que puedas usar contra las personas después", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_05", "I wait for the right time to get back at people",
                   "Espero el momento adecuado para vengarme de las personas", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_06", "There are things you should hide from others because they don't need to know",
                   "Hay cosas que debes ocultar porque otros no necesitan saberlas", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_07", "Make sure your plans benefit yourself, not others",
                   "Asegúrate de que tus planes te beneficien a ti, no a otros", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_08", "Most people can be manipulated",
                   "La mayoría de las personas pueden ser manipuladas", Construct.MACHIAVELLIANISM),
    AssessmentItem("MACH_09", "People see me as a natural leader",
                   "Las personas me ven como un líder natural", Construct.MACHIAVELLIANISM),
    
    # Psychopathy (7 items)
    AssessmentItem("PSYC_01", "I feel bad when my actions hurt others",
                   "Me siento mal cuando mis acciones lastiman a otros", Construct.PSYCHOPATHY, reverse_scored=True),
    AssessmentItem("PSYC_02", "People often say I'm out of control",
                   "La gente suele decir que estoy fuera de control", Construct.PSYCHOPATHY),
    AssessmentItem("PSYC_03", "I tend to fight against authorities and their rules",
                   "Tiendo a luchar contra las autoridades y sus reglas", Construct.PSYCHOPATHY),
    AssessmentItem("PSYC_04", "I've been in trouble with the law",
                   "He tenido problemas con la ley", Construct.PSYCHOPATHY),
    AssessmentItem("PSYC_05", "I sometimes get into dangerous situations",
                   "A veces me meto en situaciones peligrosas", Construct.PSYCHOPATHY),
    AssessmentItem("PSYC_06", "People who mess with me always regret it",
                   "Las personas que se meten conmigo siempre lo lamentan", Construct.PSYCHOPATHY),
    AssessmentItem("PSYC_07", "I have never gotten into trouble with the law",
                   "Nunca he tenido problemas con la ley", Construct.PSYCHOPATHY, reverse_scored=True),
    
    # Sadism (7 items)
    AssessmentItem("SAD_01", "I enjoy seeing people hurt",
                   "Disfruto ver a las personas sufrir", Construct.SADISM),
    AssessmentItem("SAD_02", "I would never hurt another person",
                   "Nunca lastimaría a otra persona", Construct.SADISM, reverse_scored=True),
    AssessmentItem("SAD_03", "Hurting people would be exciting",
                   "Lastimar personas sería emocionante", Construct.SADISM),
    AssessmentItem("SAD_04", "I have daydreams about hurting people",
                   "He tenido fantasías sobre lastimar personas", Construct.SADISM),
    AssessmentItem("SAD_05", "I think about hurting people who irritate me",
                   "Pienso en lastimar a las personas que me irritan", Construct.SADISM),
    AssessmentItem("SAD_06", "I have humiliated others to keep them in line",
                   "He humillado a otros para mantenerlos en línea", Construct.SADISM),
    AssessmentItem("SAD_07", "I enjoy making jokes at the expense of others",
                   "Disfruto hacer bromas a costa de otros", Construct.SADISM),
]

# Vigilance (VEE) items
VEE_ITEMS: List[AssessmentItem] = [
    AssessmentItem("VEE_01", "I'm always alert to opportunities in my environment",
                   "Siempre estoy alerta a las oportunidades en mi entorno", Construct.VIGILANCE),
    AssessmentItem("VEE_02", "I quickly notice when organizational rules change",
                   "Rápidamente noto cuando las reglas organizacionales cambian", Construct.VIGILANCE),
    AssessmentItem("VEE_03", "I can sense when there's a power shift in my workplace",
                   "Puedo sentir cuando hay un cambio de poder en mi trabajo", Construct.VIGILANCE),
    AssessmentItem("VEE_04", "I pay attention to the informal networks in organizations",
                   "Presto atención a las redes informales en las organizaciones", Construct.VIGILANCE),
]

# PsyCap items (abbreviated)
PSYCAP_ITEMS: List[AssessmentItem] = [
    AssessmentItem("PC_01", "I can get through difficult times because I've experienced difficulty before",
                   "Puedo superar tiempos difíciles porque he experimentado dificultades antes", Construct.PSYCAP),
    AssessmentItem("PC_02", "I usually take stressful things at work in stride",
                   "Usualmente tomo las cosas estresantes del trabajo con calma", Construct.PSYCAP),
    AssessmentItem("PC_03", "I feel confident presenting information to colleagues",
                   "Me siento seguro presentando información a mis colegas", Construct.PSYCAP),
    AssessmentItem("PC_04", "If I should find myself in a difficult situation, I could think of many ways to get out",
                   "Si me encuentro en una situación difícil, podría pensar en muchas formas de salir", Construct.PSYCAP),
]

# All items combined
ALL_ITEMS = SD4_ITEMS + VEE_ITEMS + PSYCAP_ITEMS


def get_items_by_construct(construct: Construct) -> List[AssessmentItem]:
    """Get all items for a specific construct"""
    return [item for item in ALL_ITEMS if item.construct == construct]


def calculate_construct_score(responses: Dict[str, int], construct: Construct) -> float:
    """
    Calculate normalized score (0-1) for a construct
    
    responses: Dict mapping item code to response (1-5 Likert scale)
    """
    items = get_items_by_construct(construct)
    if not items:
        return 0.5
    
    total = 0.0
    count = 0
    
    for item in items:
        if item.code in responses:
            score = responses[item.code]
            if item.reverse_scored:
                score = 6 - score  # Reverse 1-5 scale
            # Normalize to 0-1
            normalized = (score - 1) / 4.0
            total += normalized
            count += 1
    
    return total / count if count > 0 else 0.5


def calculate_all_scores(responses: Dict[str, int]) -> Dict[str, float]:
    """Calculate all construct scores from responses"""
    return {
        "narcissism": calculate_construct_score(responses, Construct.NARCISSISM),
        "machiavellianism": calculate_construct_score(responses, Construct.MACHIAVELLIANISM),
        "psychopathy": calculate_construct_score(responses, Construct.PSYCHOPATHY),
        "sadism": calculate_construct_score(responses, Construct.SADISM),
        "vigilance": calculate_construct_score(responses, Construct.VIGILANCE),
        "psycap": calculate_construct_score(responses, Construct.PSYCAP),
    }
