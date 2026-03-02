import { useState } from 'react'

// Demo assessment items (subset for quick testing)
const DEMO_ITEMS = [
    { code: "NARC_01", text: "I tend to want others to admire me", text_es: "Tiendo a querer que otros me admiren", construct: "narcissism" },
    { code: "NARC_05", text: "I insist on getting the respect I deserve", text_es: "Insisto en obtener el respeto que merezco", construct: "narcissism" },
    { code: "MACH_01", text: "I believe in being strategic when dealing with people", text_es: "Creo en ser estratégico al tratar con personas", construct: "machiavellianism" },
    { code: "MACH_02", text: "Whatever it takes, you must get the important people on your side", text_es: "Cueste lo que cueste, debes tener a las personas importantes de tu lado", construct: "machiavellianism" },
    { code: "PSYC_01", text: "I feel bad when my actions hurt others", text_es: "Me siento mal cuando mis acciones lastiman a otros", construct: "psychopathy", reverse: true },
    { code: "PSYC_03", text: "I tend to fight against authorities and their rules", text_es: "Tiendo a luchar contra las autoridades y sus reglas", construct: "psychopathy" },
    { code: "SAD_01", text: "I enjoy seeing people hurt", text_es: "Disfruto ver a las personas sufrir", construct: "sadism" },
    { code: "SAD_02", text: "I would never hurt another person", text_es: "Nunca lastimaría a otra persona", construct: "sadism", reverse: true },
    { code: "VEE_01", text: "I'm always alert to opportunities in my environment", text_es: "Siempre estoy alerta a las oportunidades en mi entorno", construct: "vigilance" },
    { code: "PC_01", text: "I can get through difficult times because I've experienced difficulty before", text_es: "Puedo superar tiempos difíciles porque he experimentado dificultades antes", construct: "psycap" },
]

const LIKERT_LABELS = ["Totally Disagree", "Disagree", "Neutral", "Agree", "Totally Agree"]

// Classification colors and emojis
const CLASSIFICATION_CONFIG = {
    MAVERICK: { color: "cyan", emoji: "🚀", label: "MAVERICK" },
    PERFORMER: { color: "green", emoji: "⭐", label: "PERFORMER" },
    RELIABLE: { color: "yellow", emoji: "✓", label: "RELIABLE" },
    MONITOR: { color: "orange", emoji: "⚠️", label: "MONITOR" },
    RISK: { color: "red", emoji: "⛔", label: "RISK" }
}

// Simulate Bifactor analysis (frontend demo)
function analyzeBifactor(responses) {
    const scores = { narcissism: 0, machiavellianism: 0, psychopathy: 0, sadism: 0, vigilance: 0, psycap: 0 }
    const counts = { narcissism: 0, machiavellianism: 0, psychopathy: 0, sadism: 0, vigilance: 0, psycap: 0 }

    DEMO_ITEMS.forEach((item, idx) => {
        let score = responses[idx]
        if (item.reverse) score = 6 - score
        scores[item.construct] += (score - 1) / 4
        counts[item.construct]++
    })

    // Average scores
    Object.keys(scores).forEach(k => {
        scores[k] = counts[k] > 0 ? scores[k] / counts[k] : 0.5
    })

    // Bifactor calculations
    const g = 0.45 * scores.psychopathy + 0.40 * scores.sadism + 0.10 * scores.machiavellianism + 0.05 * scores.narcissism
    const rawAgency = 0.50 * scores.machiavellianism + 0.50 * scores.narcissism
    const s = Math.max(0, Math.min(1, rawAgency - g * 0.35))

    // Classification
    let classification
    if (g > 0.70) classification = "RISK"
    else if (s > 0.65 && g < 0.50) classification = "MAVERICK"
    else if (s > 0.65 && g >= 0.50) classification = "MONITOR"
    else if (s > 0.45 && g < 0.50) classification = "PERFORMER"
    else classification = "RELIABLE"

    // Predictions
    const eib = Math.max(0, Math.min(1, 0.30 * s - 0.20 * g + 0.25 * scores.vigilance + 0.15 * scores.psycap + 0.3))
    const cwb_o = Math.max(0, Math.min(1, 0.30 * s + 0.25 * g))
    const cwb_i = Math.max(0, Math.min(1, 0.70 * g + 0.05 * s))

    return {
        g_factor: g.toFixed(2),
        s_agency: s.toFixed(2),
        classification,
        confidence: 0.85,
        eib_prediction: eib.toFixed(2),
        cwb_o_risk: cwb_o.toFixed(2),
        cwb_i_risk: cwb_i.toFixed(2)
    }
}

function App() {
    const [screen, setScreen] = useState('welcome') // welcome, assessment, result
    const [currentQuestion, setCurrentQuestion] = useState(0)
    const [responses, setResponses] = useState(Array(DEMO_ITEMS.length).fill(null))
    const [result, setResult] = useState(null)

    const handleResponse = (value) => {
        const newResponses = [...responses]
        newResponses[currentQuestion] = value
        setResponses(newResponses)

        // Auto-advance after short delay
        setTimeout(() => {
            if (currentQuestion < DEMO_ITEMS.length - 1) {
                setCurrentQuestion(currentQuestion + 1)
            }
        }, 300)
    }

    const handleSubmit = () => {
        const analysisResult = analyzeBifactor(responses)
        setResult(analysisResult)
        setScreen('result')
    }

    const restart = () => {
        setScreen('welcome')
        setCurrentQuestion(0)
        setResponses(Array(DEMO_ITEMS.length).fill(null))
        setResult(null)
    }

    // Welcome Screen
    if (screen === 'welcome') {
        return (
            <div className="app">
                <div className="header">
                    <h1>🎯 Maverick Hunter</h1>
                    <p className="tagline">Hire the people who break the right rules</p>
                </div>

                <div className="demo-banner">
                    DEMO MODE - Bifactor S-1 Talent Assessment
                </div>

                <div className="card">
                    <h2>What is Maverick Hunter?</h2>
                    <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '1.5rem' }}>
                        Traditional hiring tests reject "conflictive" candidates. But <strong style={{ color: 'var(--color-maverick)' }}>Dark Innovators</strong> -
                        people who strategically break rules to drive innovation - are often mislabeled as troublemakers.
                    </p>
                    <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '2rem' }}>
                        Using the <strong>Bifactor S-1 Model</strong>, we distinguish between <strong style={{ color: 'var(--color-maverick)' }}>S_Agency</strong> (strategic darkness that drives innovation)
                        and <strong style={{ color: 'var(--color-risk)' }}>G Factor</strong> (destructive toxicity).
                    </p>

                    <div className="metrics-grid">
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-maverick)' }}>🔵</div>
                            <div className="metric-label">Maverick</div>
                        </div>
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-performer)' }}>🟢</div>
                            <div className="metric-label">Performer</div>
                        </div>
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-reliable)' }}>🟡</div>
                            <div className="metric-label">Reliable</div>
                        </div>
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-monitor)' }}>🟠</div>
                            <div className="metric-label">Monitor</div>
                        </div>
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-risk)' }}>🔴</div>
                            <div className="metric-label">Risk</div>
                        </div>
                    </div>

                    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                        <button className="btn btn-primary" onClick={() => setScreen('assessment')}>
                            Start Demo Assessment
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    // Assessment Screen
    if (screen === 'assessment') {
        const item = DEMO_ITEMS[currentQuestion]
        const progress = ((currentQuestion + 1) / DEMO_ITEMS.length) * 100
        const allAnswered = responses.every(r => r !== null)

        return (
            <div className="app">
                <div className="card">
                    <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                    </div>

                    <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
                        Question {currentQuestion + 1} of {DEMO_ITEMS.length}
                    </p>

                    <div className="question">
                        <p className="question-text">{item.text}</p>
                        <p className="question-text-es">{item.text_es}</p>

                        <div className="likert-scale">
                            {[1, 2, 3, 4, 5].map(value => (
                                <div
                                    key={value}
                                    className={`likert-option ${responses[currentQuestion] === value ? 'selected' : ''}`}
                                    onClick={() => handleResponse(value)}
                                >
                                    <div className="number">{value}</div>
                                    <div className="label">{LIKERT_LABELS[value - 1]}</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="nav-buttons">
                        <button
                            className="btn"
                            style={{ background: 'var(--bg-input)' }}
                            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                            disabled={currentQuestion === 0}
                        >
                            ← Previous
                        </button>

                        {currentQuestion < DEMO_ITEMS.length - 1 ? (
                            <button
                                className="btn btn-primary"
                                onClick={() => setCurrentQuestion(currentQuestion + 1)}
                                disabled={responses[currentQuestion] === null}
                            >
                                Next →
                            </button>
                        ) : (
                            <button
                                className="btn btn-primary"
                                onClick={handleSubmit}
                                disabled={!allAnswered}
                            >
                                Get Results 🎯
                            </button>
                        )}
                    </div>
                </div>
            </div>
        )
    }

    // Result Screen
    if (screen === 'result' && result) {
        const config = CLASSIFICATION_CONFIG[result.classification]

        const recommendations = {
            MAVERICK: "Ideal for leadership, innovation, and entrepreneurial roles. Will push boundaries productively.",
            PERFORMER: "Strong candidate with growth potential. Suitable for roles requiring initiative.",
            RELIABLE: "Dependable team member. Best for structured, process-oriented positions.",
            MONITOR: "Potential mixed. Consider with mentorship program and clear boundaries.",
            RISK: "High probability of counterproductive behaviors. Not recommended for hire."
        }

        return (
            <div className="app">
                <div className="card result-card">
                    <div className={`semaphore ${config.color}`}>
                        <span style={{ color: 'var(--bg-dark)' }}>{config.emoji}</span>
                    </div>

                    <h2 className={`classification-name ${config.color}`}>
                        {config.label}
                    </h2>

                    <p className="recommendation">{recommendations[result.classification]}</p>

                    <div className="metrics-grid">
                        <div className="metric">
                            <div className="metric-value" style={{ color: 'var(--color-maverick)' }}>{result.s_agency}</div>
                            <div className="metric-label">S_Agency</div>
                        </div>
                        <div className="metric">
                            <div className={`metric-value ${parseFloat(result.g_factor) > 0.5 ? 'negative' : 'positive'}`}>
                                {result.g_factor}
                            </div>
                            <div className="metric-label">G Factor</div>
                        </div>
                        <div className="metric">
                            <div className="metric-value positive">{result.eib_prediction}</div>
                            <div className="metric-label">EIB Potential</div>
                        </div>
                        <div className="metric">
                            <div className={`metric-value ${parseFloat(result.cwb_i_risk) > 0.4 ? 'negative' : 'neutral'}`}>
                                {result.cwb_i_risk}
                            </div>
                            <div className="metric-label">CWB-I Risk</div>
                        </div>
                    </div>

                    <div style={{ marginTop: '2rem' }}>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                            Confidence: {(result.confidence * 100).toFixed(0)}%
                        </p>
                        <div className="confidence-bar">
                            <div className="confidence-fill" style={{ width: `${result.confidence * 100}%` }}></div>
                        </div>
                    </div>

                    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                        <button className="btn btn-primary" onClick={restart}>
                            Start New Assessment
                        </button>
                    </div>
                </div>

                <div className="card" style={{ textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                        Based on <strong>Bifactor S-1 Model</strong> from thesis:
                        <em>"Dark Agency in Institutional Voids"</em>
                    </p>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                        "La rebeldía calculada es rentabilidad"
                    </p>
                </div>
            </div>
        )
    }

    return null
}

export default App
