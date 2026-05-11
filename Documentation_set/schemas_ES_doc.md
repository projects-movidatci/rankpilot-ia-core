```markdown
## Resumen:
Este archivo define modelos Pydantic para estructurar los datos de presentación para directorios de clasificación legal como Legal 500, Chambers y Leaders League. Establece una jerarquía de modelos para capturar varios aspectos de la presentación de un bufete de abogados, incluida la identidad, la información del departamento, los detalles del cliente y el asunto, las nominaciones y los comentarios.

## Clases:
- **`BaseSubmission`**: La clase base para todos los tipos de presentación, que sirve como un ancestro común.
- **`InterviewContact`**: Representa los detalles de contacto de las personas involucradas en las entrevistas.
- **`Identity`**: Contiene información de identidad de la firma, país, área de práctica, personas de contacto, estado de clasificación actual y trayectoria del historial de clasificación.
- **`HeadOfTeam`**: Representa al jefe de un equipo o departamento específico.
- **`Metrics`**: Captura métricas cuantitativas para un departamento, como recuentos de socios y no socios.
- **`DepartmentInfo`**: Contiene el nombre interno del departamento, los jefes de equipo y las métricas asociadas.
- **`Narratives`**: Almacena secciones narrativas para una presentación, que incluyen diferenciadores, innovaciones y comentarios sobre las clasificaciones.
- **`Barrister`**: Detalles sobre un abogado o consejero independiente contratado.
- **`Partner`**: Información para un socio principal nominado.
- **`Associate`**: Información para un asociado principal o socio emergente nominado.
- **`ArrivalDeparture`**: Registra cambios significativos de personal (llegadas, salidas, promociones).
- **`IndividualNominations`**: Agrega nominaciones para socios y asociados principales y de próxima generación.
- **`TeamDynamics`**: Rastrea movimientos significativos recientes de abogados dentro del equipo.
- **`Client`**: Representa a un cliente, incluido su estado (activo, nuevo, publicable).
- **`WorkHighlight`**: Un resumen breve y publicable de un trabajo importante.
- **`TeamMember`**: Información sobre un miembro de un equipo legal.
- **`ExternalFirm`**: Detalles sobre otro bufete de abogados involucrado en un asunto.
- **`Dates`**: Fechas de inicio y fin de un asunto.
- **`PMatter`**: Representa un asunto publicable con atributos detallados.
- **`NPMatter`**: Representa un asunto no publicable (confidencial) con atributos detallados.
- **`Legal500Submission`**: El modelo Pydantic de nivel superior para una presentación de Legal 500.
- **`ContactPerson`**: Representa a una persona de contacto para una presentación.
- **`PreliminaryInformation`**: Contiene detalles preliminares para una presentación de Chambers.
- **`PartnerStats`**: Estadísticas relacionadas con los socios en un departamento.
- **`DepartmentLawyersRanked`**: Información sobre abogados clasificados o no clasificados dentro de un departamento.
- **`HireDeparture`**: Registra contrataciones y salidas de abogados para presentaciones de Chambers.
- **`DepartmentInfoFeature`**: El modelo principal para la información del departamento en presentaciones de Chambers.
- **`BarristerAdvocate`**: Detalles sobre abogados o consejeros para comentarios de Chambers.
- **`FeedbackFeature`**: Agrega secciones de comentarios para una presentación de Chambers.
- **`PublishableClient`**: Representa a un cliente cuya información es adecuada para su publicación.
- **`PublishableMatter`**: Representa un resumen de trabajo destinado a su publicación en Chambers.
- **`PublishableInformationFeature`**: Agrega toda la información publicable para una presentación de Chambers.
- **`ConfidentialMatter`**: Representa un resumen de trabajo confidencial para presentaciones de Chambers.
- **`ConfidentialInformationFeature`**: Agrega toda la información confidencial para una presentación de Chambers.
- **`ChambersSubmission`**: El modelo Pydantic de nivel superior para una presentación de Chambers.
- **`FirmInformationLL`**: Contiene información a nivel de firma para una presentación de Leaders League.
- **`DepartmentHeadLL`**: Representa a un jefe de departamento o socio clave para Leaders League.
- **`DepartmentChangeLL`**: Registra cambios dentro de un departamento para Leaders League.
- **`ActiveClientLL`**: Representa a un cliente activo para una presentación de Leaders League.
- **`DepartmentInformationLL`**: El modelo principal para la información del departamento en presentaciones de Leaders League.
- **`EstablishedPractitionerLL`**: Comentarios sobre profesionales establecidos en una presentación de Leaders League.
- **`RisingStarLL`**: Comentarios sobre estrellas emergentes en una presentación de Leaders League.
- **`PeerFeedbackLL`**: Agrega comentarios de pares para una presentación de Leaders League.
- **`RankingFeedbackLL`**: Almacena comentarios relacionados con las posiciones de clasificación para Leaders League.
- **`WorkHighlightLL`**: Representa un resumen de trabajo para una presentación de Leaders League.
- **`LeadersLeagueSubmission`**: El modelo Pydantic de nivel superior para una presentación de Leaders League.

## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `Field` | `None, description="Full name of the interview contact."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Job title of the contact."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `job_title`. |
| `Field` | `None, description="Email address. Extract cleanly without mailto: prefixes."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `email`. |
| `Field` | `None, description="Telephone number. Keep international codes if present."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `phone`. |
| `Field` | `None, description="The official name of the law firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_name`. |
| `Field` | `None, description="The country for the submission (e.g., 'United States')."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `country`. |
| `Field` | `None, description="The specific practice area selected for this submission."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `practice_area`. |
| `Field` | `default_factory=list, description="List of contacts to arrange interviews with."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `interview_contacts`. |
| `Field` | `description="CRITICAL STRATEGY FIELD. The current ranking status of the firm in this specific practice area (e.g., 'Unranked', 'Band 1', 'Band 4')."` | Proporciona una descripción para el campo `current_band_status`, enfatizando su importancia estratégica. |
| `Field` | `default="N/A", description="The firm's recent ranking history. Choose 'Ascent' if they recently climbed, 'Descent' if they dropped, 'Stagnation' if they have been in the same band for years, or 'N/A' if unknown."` | Establece un valor predeterminado de "N/A" y proporciona una descripción para el campo `ranking_history_trajectory`. |
| `Field` | `None, description="Full name of the team or department head."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Office location or city of the team head."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `location`. |
| `Field` | `0, description="Number of partners who spend at least 50% of their time in this department. Return 0 if none."` | Establece un valor predeterminado de 0 y proporciona una descripción para el campo `partners_count_50_percent_plus`. |
| `Field` | `0, description="Number of non-partners who spend at least 50% of their time in this department. Return 0 if none."` | Establece un valor predeterminado de 0 y proporciona una descripción para el campo `non_partners_count_50_percent_plus`. |
| `Field` | `None, description="The Team or Department Name as used internally by the firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `team_name_internal`. |
| `Field` | `default_factory=list, description="List of the Head(s) of the Team."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `heads_of_team`. |
| `Field` | `default_factory=Metrics` | Inicializa un objeto `Metrics` predeterminado para el campo `metrics`. |
| `Field` | `None, description="Narrative detailing what sets the practice apart from other firms."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `what_sets_us_apart`. |
| `Field` | `None, description="Narrative detailing measures introduced or maintained over the last year to benefit clients."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `initiatives_and_innovation`. |
| `Field` | `None, description="Feedback regarding existing rankings or commentary. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `rankings_feedback`. |
| `Field` | `None, description="Name of the independent barrister or advocate."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="The Chambers or Firm they belong to."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `chambers`. |
| `Field` | `None, description="Location or jurisdiction of the barrister."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `location`. |
| `Field` | `None, description="Comments regarding the instruction or their performance."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `comments`. |
| `Field` | `None, description="Full name of the leading partner."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Office location or city of the partner."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `location`. |
| `Field` | `False, description="Were they ranked in the previous edition? Map 'Yes'/'Y' to true, 'No'/'N' to false."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `ranked_in_previous_edition`. |
| `Field` | `None, description="Detailed supporting evidence and narrative for why this partner is pre-eminent. Extract full text."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `supporting_information`. |
| `Field` | `None, description="Full name of the leading associate/next gen partner (can include counsel)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Office location or city of the associate."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `location`. |
| `Field` | `None, description="Detailed supporting evidence for this associate/partner. Extract full text."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `supporting_information`. |
| `Field` | `None, description="Name of the person who arrived, departed, or was promoted."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="The position or role of the person (e.g., Partner)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `position_role`. |
| `Field` | `None, description="Specify strictly 'Joined', 'Departed', or 'Promoted'."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `action`. |
| `Field` | `None, description="The firm they joined from, or the destination firm they departed to."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_source_destination`. |
| `Field` | `None, description="The month and year of the action (e.g., 'March 2025')."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `month_year`. |
| `Field` | `default_factory=list, description="Nominations for genuinely exceptional, pre-eminent partners."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `leading_partners`. |
| `Field` | `default_factory=list, description="Nominations for junior/new/younger partners making a material difference."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `next_generation_partners`. |
| `Field` | `default_factory=list, description="Nominations for junior/new/younger associates or counsels making a material difference."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `leading_associates`. |
| `Field` | `default_factory=list, description="List of significant recent arrivals, departures, or promotions at the partner level."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `arrivals_and_departures`. |
| `Field` | `None, description="The official name of the active key client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `active_key_client`. |
| `Field` | `False, description="Determine if this is a new client. Map 'Yes' or 'Y' to true, 'No', 'N' or blank to false."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_new_client`. |
| `Field` | `False, description="Whether the client is publishable."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_publishable`. |
| `Field` | `None, description="A brief 1-2 sentence summary of a highlight matter (e.g., 'Advised X on acquisition of Y'). MUST be publishable."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `publishable_summary`. |
| `Field` | `None, description="Name of the lead partner or other key team member."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Office location of the team member."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `office`. |
| `Field` | `None, description="Specific practice area of the team member."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `practice_area`. |
| `Field` | `None, description="Name of the other law firm advising on the matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_name`. |
| `Field` | `None, description="Description of their role."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `role_details`. |
| `Field` | `None, description="The specific firm, company, or individual that this external firm advised."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `entity_advised`. |
| `Field` | `None, description="Start date of the matter. Return null if not provided."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `start`. |
| `Field` | `None, description="End date of the matter. Return null if not provided."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `end`. |
| `Field` | `None, description="Matter ID."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `id`. |
| `Field` | `None, description="The name of the client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `client_name`. |
| `Field` | `None, description="The industry sector of the matter/client. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `industry_sector`. |
| `Field` | `None, description="Detailed description of the matter, background, and firm's role. DO NOT include generic marketing text."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_description`. |
| `Field` | `None, description="Financial value of the deal/matter. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `deal_value`. |
| `Field` | `False` | Establece un valor predeterminado de False para el campo `is_cross_border`. |
| `Field` | `default_factory=list, description="If cross-border, list the jurisdictions involved."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `jurisdictions_involved`. |
| `Field` | `default_factory=list, description="List of lead partners working on this specific matter."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `lead_partners`. |
| `Field` | `default_factory=list, description="List of other key team members (associates, counsels) on the matter."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `other_key_team_members`. |
| `Field` | `default_factory=list, description="List of other external firms involved in the matter."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `external_firms_advising`. |
| `Field` | `None, description="Start and end dates for the matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `dates`. |
| `Field` | `False, description="Whether the matter is publishable. If the text explicitly says 'CONFIDENTIAL', this should be false."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_publishable`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `identity`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `department_info`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `narratives`. |
| `Field` | `default_factory=list, description="Up to 3 brief summaries of publishable work highlights."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `work_highlights_summaries`. Establece una longitud máxima de 3. |
| `Field` | `default_factory=list, description="Up to 20 publishable work highlights."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `publishable_matters`. Establece una longitud máxima de 20. |
| `Field` | `default_factory=list, description="Up to 20 confidential work highlights."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `confidential_matters`. Establece una longitud máxima de 20. |
| `Field` | `default_factory=list, description="Optional details of independent barristers/advocates instructed in the past year."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `barristers`. |
| `Field` | `None, description="Full name of the contact person."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Email address. Extract cleanly without mailto: prefixes."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `email`. |
| `Field` | `None, description="Telephone number. Keep international codes if present."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `telephone_number`. |
| `Field` | `None, description="The official, registered name of the law firm. Strip conversational filler."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `A1_firm_name`. |
| `Field` | `None, description="The specific practice area being submitted for (e.g., 'FinTech Legal')."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `A2_practice_area`. |
| `Field` | `None, description="The country or jurisdiction the submission applies to."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `A3_location_jurisdiction`. |
| `Field` | `default_factory=list, description="List of personnel designated to arrange interviews."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `A4_contact_persons`. |
| `Field` | `default=None, description="CRITICAL STRATEGY FIELD. The current ranking status of the firm in this specific practice area (e.g., 'Unranked', 'Band 1', 'Band 4'). If not explicitly mentioned, return null."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `current_band_status`, enfatizando su importancia estratégica. |
| `Field` | `default=None, description="The firm's recent ranking history. Choose 'Ascent' if they recently climbed, 'Descent' if they dropped, 'Stagnation' if they have been in the same band for years, or 'First Time' if they have never been ranked before. If the history is not explicitly mentioned, you MUST return null."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `ranking_history_trajectory`. |
| `Field` | `None, description="The total raw integer number of lawyers/partners in this category. Return 0 if none."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `total_number`. |
| `Field` | `None, description="The percentage of males. Include the '%' sign if present in text."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `male_ratio_percentage`. |
| `Field` | `None, description="The percentage of females. Include the '%' sign if present in text."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `female_ratio_percentage`. |
| `Field` | `None, description="Full name of the lawyer."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Include the bio URL or specific comments/key areas of focus listed for this lawyer."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `comments_or_web_link`. |
| `Field` | `None, description="Evaluate if they are a partner based on the text. You MUST output exactly 'Y' or 'N'."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `is_partner`. |
| `Field` | `None, description="Evaluate if they are already ranked based on the text. You MUST output exactly 'Y' or 'N'."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `is_ranked`. |
| `Field` | `None, description="Details regarding parental leave or part-time arrangements. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `parental_leave_or_part_time`. |
| `Field` | `None, description="Name of the lawyer who joined or departed."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Specify strictly 'Joined' or 'Departed'."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `status_joined_departed`. |
| `Field` | `None, description="The name of the previous firm (if joined) or destination firm (if departed)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `from_or_destination_firm`. |
| `Field` | `None, description="The internal name the firm uses. Usually labeled as B.1"` | Establece un valor predeterminado de None y proporciona una descripción para el campo `department_name`. |
| `Field` | `None, description="Total number and gender ratio of partners in the department."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `B2_partners`. |
| `Field` | `None, description="Total number and gender ratio of other qualified lawyers (associates, counsels)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `B3_other_qualified_lawyers`. |
| `Field` | `default_factory=list, description="List of Department Head(s) or Key Partners (USA Template)."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `B4_department_heads`. |
| `Field` | `None, description="Percentage of the team identifying as LGBT+. Must be a raw number/percentage string. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `B5_diversity_lgbt_percentage`. |
| `Field` | `None, description="Percentage of the team with a disability. Must be a raw number/percentage string. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `B6_diversity_disability_percentage`. |
| `Field` | `default_factory=list, description=("CRITICAL: Look for the section identifying the leaders of the practice. It is usually titled 'B4 Department Head(s) or Key Partners' OR 'B7 Head or Heads of department'. Ignore the B4/B7 numbering and look for the keywords 'Head' and 'Department'. The data will likely be a flattened table containing Names, Emails, and Phone numbers. Extract every person listed in this specific section.")` | Inicializa una lista vacía por defecto y proporciona una descripción detallada para el campo `heads_of_department`. |
| `Field` | `default_factory=list, description="List of partners who joined or left. Usually labeled as B.8 or similar."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `hires_departures_last_12_months`. |
| `Field` | `default_factory=list, description="Details regarding ranked and unranked lawyers, including their key areas of focus and standout work."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `B9_lawyers_ranked_unranked`. |
| `Field` | `None, description=("Narrative text describing what the department is best known for. Note: This is typically labeled as 'B7' or 'B10'. It should include details on industry sector expertise, key types of work, areas of recent growth, and any feedback on previous Chambers coverage. Maximum word count is usually 500 words.")` | Establece un valor predeterminado de None y proporciona una descripción detallada para el campo `department_best_known_for`. |
| `Field` | `default_factory=list, description="List of external barristers or advocates used by the firm."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `C1_barristers_advocates`. |
| `Field` | `None, description="Feedback provided regarding other competing firms or the ranking status of their own lawyers. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `C2_feedback_on_other_firms`. |
| `Field` | `None, description="The official name of the client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name_of_client`. |
| `Field` | `None, description="Determine if this is a new client within the last 12 months. Map 'Yes' to true, 'No' or blank to false."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `is_new_client`. |
| `Field` | `None, description="The internal matter ID or sequential number (e.g., 'Publishable Matter 1')."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_id`. |
| `Field` | `None, description="The name of the client. MUST be publishable."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D1_name_of_client`. |
| `Field` | `None, description="Summarizes the publishable matter and the firm's specific role. MUST NOT contain confidential information. If text says 'CONFIDENTIAL', route it to section E instead."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D2_summary_of_matter_and_role`. |
| `Field` | `None, description="The financial value of the matter including currency. Return null if N/A or blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D3_matter_value`. |
| `Field` | `None, description="List of jurisdictions involved if cross-border. If it explicitly says 'No', return null."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D4_cross_border_jurisdictions`. |
| `Field` | `None, description="Name(s) of the lead partner(s) on the matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D5_lead_partner`. |
| `Field` | `None, description="Names of other associates or team members involved."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D6_other_team_members`. |
| `Field` | `None, description="Names of other law firms involved and their roles. Return null if N/A."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D7_other_firms_advising`. |
| `Field` | `None, description="The current status (e.g., 'Ongoing') or completion date."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D8_date_completion_or_status`. |
| `Field` | `None, description="URLs to press coverage or additional notes. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `D9_other_information_links`. |
| `Field` | `default_factory=list, description="List of clients whose identities can be published. Exclude any client marked confidential."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `D0_publishable_clients_list`. |
| `Field` | `default_factory=list, description="List of up to 20 publishable work highlights. MUST NOT contain confidential data."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `publishable_matters`. Establece una longitud máxima de 20. |
| `Field` | `None, description="The internal matter ID or sequential number (e.g., 'Confidential Matter 1')."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_id`. |
| `Field` | `None, description="The name of the client. Treat this as strictly confidential."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E1_name_of_client`. |
| `Field` | `None, description="Summarizes the confidential matter and the firm's role. This text is protected and not for publication."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E2_summary_of_matter_and_role`. |
| `Field` | `None, description="The financial value of the matter. Often marked 'Confidential' or 'Non disclosable'. Extract the text as written."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E3_matter_value`. |
| `Field` | `None, description="List of jurisdictions involved if cross-border. If it explicitly says 'No', return null."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E4_cross_border_jurisdictions`. |
| `Field` | `None, description="Name(s) of the lead partner/lawyer on the matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E5_lead_lawyer`. |
| `Field` | `None, description="Names of other associates or team members involved."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E6_other_team_members`. |
| `Field` | `None, description="Names of other law firms involved and their roles. Return null if N/A."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E7_other_firms_advising`. |
| `Field` | `None, description="The current status (e.g., 'Ongoing') or completion date."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E8_date_completion_or_status`. |
| `Field` | `None, description="URLs to press coverage or additional notes. Return null if blank."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `E9_other_information_links`. |
| `Field` | `True, description="Always set to true for matters in Section E."` | Establece un valor predeterminado de True y proporciona una descripción para el campo `is_confidential`. |
| `Field` | `default_factory=list, description="List of clients whose identities MUST remain strictly confidential."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `E0_confidential_clients_list`. |
| `Field` | `default_factory=list, description="List of confidential work highlights. These matters are protected and not for publication."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `confidential_matters`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `A_preliminary_information`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `B_department_information`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `C_feedback`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `D_publishable_information`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `E_confidential_information`. |
| `Field` | `None, description="The official name of the firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_name`. |
| `Field` | `None, description="The year the firm was established."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `year_established`. |
| `Field` | `None, description="Name of the Managing Partner(s)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `managing_partners`. |
| `Field` | `None, description="Name of the person(s) in charge of Marketing/Business Development."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `marketing_bd_persons`. |
| `Field` | `None, description="List of office locations."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `list_of_offices`. |
| `Field` | `None, description="Number of Partners in the entire firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `total_partners`. |
| `Field` | `None, description="Number of Counsels/Associates in the entire firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `total_counsels_associates`. |
| `Field` | `None, description="Name of the head of the department or key partner."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Email address."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `email`. |
| `Field` | `None, description="The year they became a partner."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `partner_since`. |
| `Field` | `None, description="Specific specialisms of the partner."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `specific_specialisms`. |
| `Field` | `False, description="True if the partner dedicates less than 50% of their time to this department (needs to be highlighted in red)."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `dedicates_less_than_50_percent`. |
| `Field` | `None, description="Name of the person."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `name`. |
| `Field` | `None, description="Position (e.g., Partner, Counsel, Associate)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `position`. |
| `Field` | `None, description="Action: Arrived, left, promoted, or retired."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `action`. |
| `Field` | `None, description="Where they moved to or from."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `moved_to_from`. |
| `Field` | `None, description="Month and year of the change."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `month_year`. |
| `Field` | `None, description="Name of the company/client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `company`. |
| `Field` | `None, description="Industry sector of the client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `sector`. |
| `Field` | `False, description="True if it is a new client."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_new_client`. |
| `Field` | `False, description="True if the client is confidential."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_confidential`. |
| `Field` | `None, description="Type of work performed for the client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `type_of_work`. |
| `Field` | `None, description="Name of the Partner(s) in charge of completing this form."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `partners_completing_form`. |
| `Field` | `default_factory=list, description="List of Heads of the department and other key partners."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `department_heads`. |
| `Field` | `None, description="Number of Male Partners in the department."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `composition_male_partners`. |
| `Field` | `None, description="Number of Female Partners in the department."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `composition_female_partners`. |
| `Field` | `None, description="Number of Counsels/Associates in the department."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `composition_counsels_associates`. |
| `Field` | `default_factory=list, description="Changes in the department over the last 12 months."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `department_changes`. |
| `Field` | `None, description="Narrative on what the department is best known for (max 500 words)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `best_known_for`. |
| `Field` | `None, description="Number of new cases taken on in the last 12 months."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `new_cases_last_12_months`. |
| `Field` | `default_factory=list, max_length=5, description="Top five sectors the department works with."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `top_five_sectors`. Establece una longitud máxima de 5. |
| `Field` | `default_factory=list, max_length=30, description="List of active clients (up to 30)."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `active_clients`. Establece una longitud máxima de 30. |
| `Field` | `default_factory=list, description="Feedback on leading law firms/lawyers."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `established_practitioners`. |
| `Field` | `None, description="Name of the leading firm or lawyer."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_lawyer`. |
| `Field` | `None, description="Comments supporting their leading status."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `comments`. |
| `Field` | `default_factory=list, description="Feedback on rising stars in the practice."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `rising_stars`. |
| `Field` | `None, description="Name of the rising star law firm."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `law_firm`. |
| `Field` | `None, description="Names of the rising star lawyers."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `lawyers`. |
| `Field` | `None, description="Main specialty of the rising star."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `main_specialty`. |
| `Field` | `None, description="Opinion on the firm's current position in Leaders League ranking."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `opinion_current_position`. |
| `Field` | `None, description="Name of the Matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_name`. |
| `Field` | `False, description="True if the matter is confidential."` | Establece un valor predeterminado de False y proporciona una descripción para el campo `is_confidential`. |
| `Field` | `None, description="Name of the Client."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `client`. |
| `Field` | `None, description="Value of the matter (specify currency) and/or other key numbers."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_value`. |
| `Field` | `None, description="Status of the matter (closed in last year or ongoing)."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_status`. |
| `Field` | `None, description="Description of the context in which work was solicited."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `matter_context`. |
| `Field` | `None, description="Explanation of what the firm did and strategy used."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `firm_role_output`. |
| `Field` | `None, description="Lead Partner(s) on the matter."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `lead_partners`. |
| `Field` | `None, description="Other team members involved."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `other_team_members`. |
| `Field` | `None, description="Other firms advising on the matter and their role."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `other_firms_advising`. |
| `Field` | `None, description="Links to press coverage."` | Establece un valor predeterminado de None y proporciona una descripción para el campo `press_links`. |
| `Field` | `default_factory=list, max_length=10, description="Up to 10 work highlights."` | Inicializa una lista vacía por defecto y proporciona una descripción para el campo `work_highlights`. Establece una longitud máxima de 10. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `firm_information`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `department_information`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `peer_feedback`. |
| `Field` | `None` | Establece un valor predeterminado de None para el campo `ranking_feedback`. |
```