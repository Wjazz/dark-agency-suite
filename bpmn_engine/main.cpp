#include "Process.h"
#include "MetricsExporter.h"
#include <iostream>

/**
 * Motor BPMN - Simulación del Proceso de Reclutamiento
 * 
 * Este programa demuestra BPMN en código vs gráfico (Bizagi)
 * Aplica POO, polimorfismo, y People Analytics
 */

int main() {
    std::cout << "=========================================================\n";
    std::cout << "       MOTOR BPMN - PROCESO DE RECLUTAMIENTO           \n";
    std::cout << "   De Grafico (Bizagi) a Codigo (C++ con OOP)          \n";
    std::cout << "=========================================================\n";
    
    // Crear proceso
    Process reclutamiento("Proceso de Reclutamiento y Selección");
    
    // Configurar recursos (mismos que en Bizagi)
    reclutamiento.addResource("AnalistaJR", 5, 10.0);  // 5 analistas, $10/hora
    reclutamiento.addResource("GerenteLider", 5, 50.0); // 5 gerentes, $50/hora
    
    std::cout << "\n[CONFIG] Configuracion de Recursos:\n";
    std::cout << "  - Analista JR: 5 personas a $10/hora\n";
    std::cout << "  - Gerente Lider: 5 personas a $50/hora\n";
    
    // ==================== CONSTRUIR EL PROCESO ====================
    
    // Start Event
    auto* start = reclutamiento.addStartEvent("start", "Postulante");
    
    // Lane: RECLUTAMIENTO
    auto* hojaVida = reclutamiento.addActivity("hojaVida", "Recibir hoja de vida", 
                                               60, "AnalistaJR");
    
    auto* gw1 = reclutamiento.addExclusiveGateway("gw1", "¿Cumple requisitos?", 0.85);
    auto* rechazado1 = reclutamiento.addEndEvent("end1", "Rechazado - No cumple perfil");
    
    // Lane: SELECCIÓN
    auto* testResiliencia = reclutamiento.addActivity("testRes", 
                                                      "Ejecutar test de resiliencia", 
                                                      1, "AnalistaJR");
    
    auto* evaluarAmbicion = reclutamiento.addActivity("evalAmb", 
                                                      "Evaluar ambición", 
                                                      1, "AnalistaJR");
    
    auto* gw2 = reclutamiento.addExclusiveGateway("gw2", "Primera selección", 0.60);
    auto* rechazado2 = reclutamiento.addEndEvent("end2", "Rechazado - No superó evaluaciones");
    
    auto* entrevistaPsico = reclutamiento.addActivity("entPsico", 
                                                      "Entrevistas psicotécnicas", 
                                                      30, "AnalistaJR");
    
    auto* evaluacion360 = reclutamiento.addActivity("eval360", 
                                                    "Evaluación 360", 
                                                    60, "AnalistaJR");
    
    auto* entrevistaFinal = reclutamiento.addActivity("entFinal", 
                                                      "Entrevista final", 
                                                      60, "AnalistaJR");
    
    auto* gw3 = reclutamiento.addExclusiveGateway("gw3", "¿Aprobó entrevista?", 0.70);
    
    auto* assessmentCenter = reclutamiento.addActivity("assessment", 
                                                       "Assessment Center", 
                                                       240, "GerenteLider");
    
    auto* gw4 = reclutamiento.addExclusiveGateway("gw4", "¿Segunda oportunidad?", 0.20);
    auto* rechazado3 = reclutamiento.addEndEvent("end3", "Rechazado - Segundo filtro (cultura)");
    auto* referido = reclutamiento.addEndEvent("end4", "Referido a otro puesto");
    
    // Lane: BÚSQUEDA
    auto* induccion = reclutamiento.addActivity("induccion", 
                                                "Inducción", 
                                                2520, "AnalistaJR"); // 6 días × 7h × 60min
    
    auto* gw5 = reclutamiento.addExclusiveGateway("gw5", "¿Aceptó oferta?", 0.90);
    auto* noAcepto = reclutamiento.addEndEvent("end5", "No aceptó oferta");
    
    auto* verificacionAntecedentes = reclutamiento.addActivity("verif", 
                                                               "Verificación de antecedentes Offline", 
                                                               1260, "GerenteLider"); // 3 días × 7h × 60min
    
    auto* contratacion = reclutamiento.addActivity("contrato", 
                                                   "Contratación del agente", 
                                                   30, "AnalistaJR");
    
    auto* finalExitoso = reclutamiento.addEndEvent("end6", "Contratado exitosamente");
    
    // ==================== CONECTAR FLUJOS ====================
    
    // Flujo principal de RECLUTAMIENTO
    start->connectTo(hojaVida);
    hojaVida->connectTo(gw1);
    gw1->connectTo(testResiliencia);  // Salida "Sí" (índice 0)
    gw1->connectTo(rechazado1);       // Salida "No" (índice 1)
    
    // Flujo de SELECCIÓN
    testResiliencia->connectTo(evaluarAmbicion);
    evaluarAmbicion->connectTo(gw2);
    gw2->connectTo(entrevistaPsico);  // Salida "Aprobado"
    gw2->connectTo(rechazado2);       // Salida "Rechazado"
    
    entrevistaPsico->connectTo(evaluacion360);
    evaluacion360->connectTo(entrevistaFinal);
    entrevistaFinal->connectTo(gw3);
    
    gw3->connectTo(induccion);        // Salida "Aprobado"
    gw3->connectTo(gw4);              // Salida "No aprobado"
    
    gw4->connectTo(referido);         // Salida "Sí, segunda oportunidad"
    gw4->connectTo(rechazado3);       // Salida "No"
    
    // Flujo de BÚSQUEDA/CONTRATACIÓN
    induccion->connectTo(assessmentCenter);
    assessmentCenter->connectTo(gw5);
    
    gw5->connectTo(verificacionAntecedentes); // Salida "Aceptó"
    gw5->connectTo(noAcepto);                 // Salida "No aceptó"
    
    verificacionAntecedentes->connectTo(contratacion);
    contratacion->connectTo(finalExitoso);
    
    // ==================== EJECUTAR SIMULACIÓN ====================
    
    std::cout << "\n[SIMULACION] Iniciando simulacion con 100 candidatos...\n";
    std::cout << "-----------------------------------------------------\n";
    
    reclutamiento.simulate(100, 1.0); // 100 candidatos, 1 min de intervalo
    
    // ==================== EXPORTAR MÉTRICAS ====================
    
    std::cout << "\n[EXPORT] Exportando metricas a CSV...\n";
    MetricsExporter exporter("simulacion_reclutamiento");
    exporter.exportAll(reclutamiento.getContext(), reclutamiento.getTokens());
    
    // Abrir dashboard en navegador
    std::cout << "\n[DASHBOARD] Abriendo dashboard en navegador...\n";
    system("start dashboard.html");
    
    std::cout << "\n\n=========================================================\n";
    std::cout << "              COMPARACION CON BIZAGI                  \n";
    std::cout << "=========================================================\n";
    std::cout << "\nEste motor BPMN replica el diseno de Bizagi en codigo.\n";
    std::cout << "Ventajas del codigo:\n";
    std::cout << "  [OK] Control de versiones (Git)\n";
    std::cout << "  [OK] Logica de negocio compleja\n";
    std::cout << "  [OK] Integracion con APIs/DB\n";
    std::cout << "  [OK] Testing automatizado\n";
    std::cout << "  [OK] Simulaciones reproducibles\n";
    std::cout << "\nAmbos enfoques son complementarios:\n";
    std::cout << "  * Bizagi: Diseno visual y validacion rapida\n";
    std::cout << "  * Codigo: Implementacion y automatizacion\n";
    std::cout << "\n[INSIGHT] Para People Analytics: dominar ambos es el diferenciador.\n";
    std::cout << "\n[PERFECT] Dashboard creado con agencia\n";
    
    return 0;
}
