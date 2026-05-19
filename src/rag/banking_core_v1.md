Banking Intelligence Core v1

Este documento es el cerebro de clasificación (Knowledge Base) para extraer metadatos de los asuntos de Banking & Finance de Chambers. Debes usar estas reglas para llenar los campos del esquema de extracción.

1. PRIMARY CATEGORY (primary_category)

Tu objetivo es seleccionar EXACTAMENTE UNA categoría principal de la siguiente lista oficial. Lee la descripción del matter y busca los "Triggers". Si el asunto abarca múltiples categorías (ej. un préstamo sindicado para una adquisición), utiliza la Regla de Prioridad: El propósito del crédito (Acquisition/Leveraged) o el tipo de activo (Fund/Real Estate) SIEMPRE tiene prioridad sobre el mecanismo de entrega (Syndicated/Corporate).

Lista Oficial de Categorías Primarias:

    Acquisition Finance

        Concepto: Financiamiento estructurado específicamente para la compra de una empresa, línea de negocio, activo o portafolio.

        Triggers: "Financing linked to M&A", "purchase price", "target acquisition", "buyer/seller", "takeover".

        Boundary Rule: Si el comprador es un fondo de Private Equity y la deuda es de alto riesgo, clasifícalo como Leveraged Finance.

    Leveraged Finance

        Concepto: Préstamos de grado sub-inversión (sub-investment grade), casi siempre vinculados a fondos de Private Equity (Sponsors), LBOs (Leveraged Buyouts) o corporativos con alta carga de deuda.

        Triggers: "LBO", "sponsor-backed", "senior/mezzanine debt", "unitranche", "direct lending", "high-yield crossover", "debt stack".

        Boundary Rule: Las transacciones apalancadas que involucran prestatarios corporativos DEBEN ir aquí, no en Corporate Finance.

    Corporate Finance / Investment Grade Lending

        Concepto: Préstamos generales a prestatarios corporativos o de grado de inversión para su operativa diaria.

        Triggers: "Revolving credit facility (RCF)", "term loan", "working capital", "corporate treasury", "public company borrower".

    Syndicated Lending

        Concepto: Préstamo otorgado por un sindicato o grupo de prestamistas bajo un mismo acuerdo de facilidad.

        Triggers: "Mandated lead arrangers (MLA)", "bookrunners", "agent bank", "syndicate", "security agent".

        Boundary Rule: Úsalo como categoría principal solo si el texto enfatiza la mecánica de la sindicación sobre el propósito del préstamo.

    Structured Finance

        Concepto: Financiamientos altamente sofisticados que involucran transferencia de riesgo, re-empaquetado de deuda o instrumentos híbridos.

        Triggers: "Securitisation-style mechanics", "risk transfer", "structured notes", "hybrid instruments", "payment waterfall".

    Asset-Based Lending (ABL)

        Concepto: Préstamos garantizados dinámicamente por los activos operativos del prestatario.

        Triggers: "Accounts receivable", "inventory", "equipment", "borrowing base", "collateral pool".

    Fund Finance

        Concepto: Financiamiento otorgado directamente a un fondo de inversión (Private Equity, Credit, Real Estate, etc.).

        Triggers: "Subscription line", "capital call facility", "NAV facility", "continuation fund", "GP financing", "feeder structure".

    Trade Finance

        Concepto: Financiamiento diseñado para respaldar flujos comerciales internacionales y cadenas de suministro.

        Triggers: "Commodity finance", "export/import finance", "supply chain finance", "factoring", "ECA-backed finance".

    Real Estate Finance

        Concepto: Financiamiento para la adquisición, desarrollo o inversión en bienes raíces a nivel institucional.

        Triggers: "Portfolio acquisition finance", "development finance", "institutional real estate".

    Project Finance

        Concepto: Financiamiento atado a los ingresos futuros de un proyecto de infraestructura, energía o similar.

        Triggers: "Energy", "renewables", "infrastructure", "mining", "utilities".

        Boundary Rule: Clasifica como tal, pero advierte (flag) que esto usualmente pertenece a la tabla separada de Project Finance.

    Refinancing

        Concepto: Sustitución o reestructuración de deuda existente fuera de un contexto de insolvencia/quiebra.

        Triggers: "Maturity extension", "covenant reset", "replacement of existing facilities".

    Debt Restructuring / Distressed Finance

        Concepto: Rework de acuerdos de deuda en situaciones de crisis financiera, estrés o insolvencia inminente.

        Triggers: "Distressed asset", "creditor committee", "debtor-in-possession (DIP)", "standstill agreement", "rescue package".

    Islamic Finance

        Concepto: Estructuras financieras que cumplen estrictamente con la ley Sharia.

        Triggers: "Ijarah", "Murabaha", "Sukuk", "Wakalah", "Sharia-compliant".

2. ADJACENT TABLE RISK (adjacent_table_risk)

Tu objetivo es evaluar si el asunto realmente pertenece a la práctica de Banking & Finance o si debería ser enviado a una tabla o ranking especializado.

Categorías Adyacentes:

    Capital Markets (Mercado de Capitales)

        Concepto: Levantamiento de fondos a través de la emisión de valores bursátiles o instrumentos de mercado, no mediante préstamos bancarios privados.

        Triggers: "IPO", "equity offering", "bond issuance", "high-yield bond", "MTN programme", "securitisation", "CLO", "derivatives", "structured products".

        Boundary Rule: Si el asunto involucra un préstamo bancario junto con una emisión de bonos, el riesgo sigue siendo True porque Chambers prefiere ver la emisión en Capital Markets, a menos que el texto se enfoque exclusivamente en la negociación de la facilidad de crédito bancario.

    Project Finance (Financiamiento de Proyectos)

        Concepto: Financiamiento dependiente estricta y exclusivamente del flujo de caja futuro de un proyecto de infraestructura, energía o industrial (Non-recourse / Limited recourse).

        Triggers: "Infrastructure", "energy", "renewables", "mining", "oil and gas", "transport/toll roads", "utilities", "social infrastructure".

    Asset Finance (Financiamiento de Activos Especializados)

        Concepto: Financiamiento atado a la compra o arrendamiento de activos de transporte pesado (no inventario ni equipo de fábrica regular).

        Triggers: "Aircraft", "aviation finance", "ships / shipping finance", "rolling stock / rail finance", "sale and leaseback", "operating leases", "JOLCOs".

    Restructuring & Insolvency (Reestructuración e Insolvencia)

        Concepto: Casos formales de quiebra, insolvencia o liquidación de activos.

        Triggers: "Insolvency proceedings", "bankruptcy", "liquidation", "Chapter 11".

        Boundary Rule: Retorna False (es decir, déjalo en Banking) si es puramente un refinanciamiento de deuda en estrés (Distressed Finance) o un standstill sin entrar en un proceso judicial de insolvencia.

    Financial Services Regulatory (Regulatorio Financiero)

        Concepto: Asesoría pura sobre cumplimiento y regulación, sin una transacción de préstamo adjunta.

        Triggers: "Regulatory compliance", "financial services directives", "bank licensing", "fintech regulation", "prudential regulation".

    Banking Litigation (Litigio Bancario)

        Concepto: Disputas legales y juicios relacionados con actividades bancarias.

        Triggers: "Litigation", "disputes", "mis-selling", "professional negligence", "bank failures", "civil fraud", "breach of warranty".

3. CLIENT SIDE (client_side)

Tu objetivo es identificar de qué lado de la mesa se sentó la firma legal. Extrae EXACTAMENTE UNO de los siguientes roles principales. Si la firma representó a múltiples partes (ej. Lenders y Arrangers al mismo tiempo), selecciona el rol de mayor jerarquía financiera (ej. Arranger).

Roles Principales:

    Lender (Prestamista)

        Concepto: Entidades que proveen los fondos. Pueden ser bancos comerciales, fondos de crédito privado, prestamistas alternativos, instituciones financieras de desarrollo (DFIs) o agencias de crédito a la exportación (ECAs).

        Triggers: "Lender", "syndicate of banks", "credit fund", "alternative lender", "development finance institution", "ECA", "financier".

        Boundary Rule: Para Chambers Global y LatAm, la representación de Lenders es una señal de alto ranking (High-ranking signal). Asegúrate de capturar esto correctamente.

    Borrower (Prestatario / Deudor)

        Concepto: La empresa corporativa, corporación cotizada en bolsa, o el vehículo de propósito especial (SPV) que recibe el préstamo y asume la deuda.

        Triggers: "Borrower", "corporate client", "debtor", "public company", "target company" (si ya fue adquirida).

        Boundary Rule: Si el cliente es un fondo de inversión que está pidiendo dinero prestado para comprar una empresa, NO uses Borrower, usa Sponsor.

    Sponsor (Patrocinador Financiero)

        Concepto: Fondos de capital privado (Private Equity), fondos de infraestructura o inversionistas institucionales que respaldan la adquisición o inyectan el capital (Equity) para que el vehículo pida la deuda.

        Triggers: "Private equity sponsor", "financial sponsor", "investment firm backing the acquisition", "LBO sponsor", "fund".

        Boundary Rule: Altamente prevalente en los casos de Leveraged Finance y Acquisition Finance.

    Arranger / Agent (Estructurador / Agente)

        Concepto: Bancos que no solo prestan dinero, sino que organizan el sindicato, estructuran el trato o administran las garantías (colateral).

        Triggers: "Mandated lead arranger (MLA)", "bookrunner", "facility agent", "administrative agent", "security agent", "collateral agent".

    Guarantor (Garante)

        Concepto: La entidad (usualmente una empresa matriz o subsidiaria) que provee garantías pero no es el receptor primario de los fondos.

        Triggers: "Guarantor", "parent company providing security", "sponsor providing a guarantee".

4. FIRM ROLE TAXONOMY (firm_role_taxonomy)

Tu objetivo es clasificar el nivel de protagonismo y fuerza estratégica de la firma legal en la transacción. Evalúa el texto y extrae EXACTAMENTE UNA de las siguientes etiquetas estandarizadas.

Etiquetas de Rol:

    Very Strong (Lead/Structuring Counsel)

        Concepto: La firma tuvo un rol central y directivo en la transacción. Lideraron la estructuración, negociaron los documentos principales o coordinaron a múltiples firmas.

        Triggers: "Lead counsel", "lender counsel" (en financiamientos mayores), "sponsor counsel", "borrower counsel" (en financiamientos estratégicos), "coordinating counsel", "structuring counsel", "agent counsel", "security agent counsel", "led negotiations", "drafted the facility agreement".

        Boundary Rule: Si la firma representó al Agente de Seguridad (Security Agent) o al Sindicato completo de Bancos (Lender Syndicate), asume un rol Very Strong por defecto debido a la complejidad de la coordinación.

    Moderate (Specialized/Local Counsel with substance)

        Concepto: La firma jugó un rol importante pero no directivo. Manejaron una "rebanada" específica y compleja de la transacción, como las garantías locales o un tramo particular de la deuda.

        Triggers: "Local counsel advising on security package", "regulatory counsel with strategic input", "counsel on one financing tranche", "counsel on collateral aspects".

        Boundary Rule: Si el texto dice "Local counsel" PERO explica explícitamente que redactaron documentos de garantía locales, resolvieron problemas de aplicabilidad transfronteriza (enforceability) o manejaron aprobaciones regulatorias críticas para el cierre, clasifícalo aquí, NO como Weak.

    Weak (Execution/Support Counsel)

        Concepto: La firma realizó tareas de apoyo rutinarias, ejecución básica (commoditized) o asesoría auxiliar sin complejidad descrita.

        Triggers: "Local counsel" (sin explicación adicional), "due diligence support", "document review", "limited legal opinion", "ancillary advice", "routine regulatory input", "assisted with", "advised on a loan" (texto genérico).

        Boundary Rule: Ante descripciones vagas como "advised the company on a financing" sin especificar qué hicieron exactamente, asume Weak. El rol debe ser demostrado, no solo reclamado.

5. COMPLEXITY INDICATORS (complexity_indicators)

Tu objetivo es identificar y extraer una lista de etiquetas que describan los elementos de sofisticación técnica, legal o estratégica del asunto.

Instrucciones de extracción:

    Retorna una lista de strings (List[str]).

    Usa preferiblemente las etiquetas en negrita de la lista de abajo.

    No inventes complejidades: Si el texto solo describe una ejecución simple, retorna una lista vacía.

    Un asunto "Strong" para Chambers suele tener 2 o más de estos indicadores.

Catálogo de Indicadores de Complejidad:
A. Sofisticación Estructural

    Multi-tranche structure: Presencia de diferentes niveles de deuda con distintos perfiles de riesgo.

        Triggers: "Senior secured", "Mezzanine layer", "Unitranche", "Second lien", "Subordinated debt", "Bridge-to-bond structure".

    Intercreditor arrangements: Acuerdos complejos que regulan la relación y prioridad entre distintos grupos de acreedores.

        Triggers: "Intercreditor agreement", "Subordination deed", "Creditor committee", "Coordinating committee".

    Bespoke collateral / Security package: Estructuras de garantía diseñadas a medida o sobre activos inusuales.

        Triggers: "Borrowing base mechanism", "Floating charges", "Security over receivables/inventory", "Waterfall payment structure", "Complex perfection requirements".

B. Sofisticación Jurisdiccional y Regulatoria

    Cross-border / Multi-jurisdictional: Transacciones que involucran leyes, activos o partes en más de un país.

        Triggers: "Cross-border security", "International lender syndicate", "Multi-currency facility", "Foreign law finance documents", "Coordination of local counsel".

    Regulatory overlay: El financiamiento enfrenta restricciones legales o requiere aprobaciones de entes gubernamentales.

        Triggers: "Prudential regulation", "Banking licensing issues", "Public sector approvals", "Tax-driven structuring", "Implementation of directives".

C. Contexto Estratégico y Financiero

    Strategic M&A / LBO context: El financiamiento es una pieza crítica para una adquisición o transformación corporativa.

        Triggers: "Acquisition-related financing", "Leveraged buyout (LBO)", "Sponsor-backed transaction", "Public takeover financing".

    Distressed context / Debt restructuring: La transacción ocurre en un escenario de crisis financiera o insolvencia inminente.

        Triggers: "Standstill agreement", "Covenant reset/renegotiation", "Maturity extension", "New money financing", "Debtor-in-possession (DIP)".

D. Sofisticación por Producto / Innovación

    Sustainability-linked / ESG features: Inclusión de mecanismos de financiamiento sostenible.

        Triggers: "ESG-linked margin adjustments", "Sustainability KPIs", "Green loans", "Emissions reduction targets".

    NAV / Hybrid fund finance: Financiamiento sofisticado a nivel de fondos de inversión.

        Triggers: "NAV facility", "Subscription lines", "Levered feeder structure", "Asset-based fund facility".

    ECA / Trade sophistication: Involucramiento de agencias oficiales o estructuras comerciales complejas.

        Triggers: "ECA-backed financing", "Structured trade finance", "Commodity-linked credit".

    First-of-kind / Novel structure: Transacciones que introducen un producto o estructura nunca antes vista en el mercado local.

        Triggers: "First sustainability-linked loan in the sector", "Market-first structure", "Innovative collateral package".