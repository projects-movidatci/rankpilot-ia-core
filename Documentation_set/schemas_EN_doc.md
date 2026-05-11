## Overview:
This file defines Pydantic models for structuring submission data for legal ranking directories such as Legal 500, Chambers, and Leaders League. It establishes a hierarchy of models to capture various aspects of a law firm's submission, including identity, department information, client and matter details, nominations, and feedback.

## Classes:
- **`BaseSubmission`**: The base class for all submission types, serving as a common ancestor.
- **`InterviewContact`**: Represents contact details for individuals involved in interviews.
- **`Identity`**: Contains firm identity information, country, practice area, contact persons, current band status, and ranking history trajectory.
- **`HeadOfTeam`**: Represents the head of a specific team or department.
- **`Metrics`**: Captures quantitative metrics for a department, such as partner and non-partner counts.
- **`DepartmentInfo`**: Holds internal department name, heads of team, and associated metrics.
- **`Narratives`**: Stores narrative sections for a submission, including differentiators, innovations, and feedback on rankings.
- **`Barrister`**: Details about an independent barrister or advocate instructed.
- **`Partner`**: Information for a nominated leading partner.
- **`Associate`**: Information for a nominated leading associate or next-gen partner.
- **`ArrivalDeparture`**: Records significant personnel changes (arrivals, departures, promotions).
- **`IndividualNominations`**: Aggregates nominations for leading and next-generation partners and associates.
- **`TeamDynamics`**: Tracks recent significant movements of lawyers within the team.
- **`Client`**: Represents a client, including their status (active, new, publishable).
- **`WorkHighlight`**: A brief, publishable summary of a significant piece of work.
- **`TeamMember`**: Information about a member of a legal team.
- **`ExternalFirm`**: Details about another law firm involved in a matter.
- **`Dates`**: Start and end dates for a matter.
- **`PMatter`**: Represents a publishable matter with detailed attributes.
- **`NPMatter`**: Represents a non-publishable (confidential) matter with detailed attributes.
- **`Legal500Submission`**: The top-level Pydantic model for a Legal 500 submission.
- **`ContactPerson`**: Represents a contact person for a submission.
- **`PreliminaryInformation`**: Contains preliminary details for a Chambers submission.
- **`PartnerStats`**: Statistics related to partners in a department.
- **`DepartmentLawyersRanked`**: Information about lawyers ranked or unranked within a department.
- **`HireDeparture`**: Records lawyer hires and departures for Chambers submissions.
- **`DepartmentInfoFeature`**: The main model for department information in Chambers submissions.
- **`BarristerAdvocate`**: Details about barristers or advocates for Chambers feedback.
- **`FeedbackFeature`**: Aggregates feedback sections for a Chambers submission.
- **`PublishableClient`**: Represents a client whose information is suitable for publication.
- **`PublishableMatter`**: Represents a work highlight intended for publication in Chambers.
- **`PublishableInformationFeature`**: Aggregates all publishable information for a Chambers submission.
- **`ConfidentialMatter`**: Represents a work highlight that is confidential for Chambers submissions.
- **`ConfidentialInformationFeature`**: Aggregates all confidential information for a Chambers submission.
- **`ChambersSubmission`**: The top-level Pydantic model for a Chambers submission.
- **`FirmInformationLL`**: Contains firm-level information for a Leaders League submission.
- **`DepartmentHeadLL`**: Represents a head of department or key partner for Leaders League.
- **`DepartmentChangeLL`**: Records changes within a department for Leaders League.
- **`ActiveClientLL`**: Represents an active client for a Leaders League submission.
- **`DepartmentInformationLL`**: The main model for department information in Leaders League submissions.
- **`EstablishedPractitionerLL`**: Feedback on established practitioners in a Leaders League submission.
- **`RisingStarLL`**: Feedback on rising stars in a Leaders League submission.
- **`PeerFeedbackLL`**: Aggregates peer feedback for a Leaders League submission.
- **`RankingFeedbackLL`**: Stores feedback related to ranking positions for Leaders League.
- **`WorkHighlightLL`**: Represents a work highlight for a Leaders League submission.
- **`LeadersLeagueSubmission`**: The top-level Pydantic model for a Leaders League submission.

## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| `Field` | `None, description="Full name of the interview contact."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Job title of the contact."` | Sets a default value of None and provides a description for the `job_title` field. |
| `Field` | `None, description="Email address. Extract cleanly without mailto: prefixes."` | Sets a default value of None and provides a description for the `email` field. |
| `Field` | `None, description="Telephone number. Keep international codes if present."` | Sets a default value of None and provides a description for the `phone` field. |
| `Field` | `None, description="The official name of the law firm."` | Sets a default value of None and provides a description for the `firm_name` field. |
| `Field` | `None, description="The country for the submission (e.g., 'United States')."` | Sets a default value of None and provides a description for the `country` field. |
| `Field` | `None, description="The specific practice area selected for this submission."` | Sets a default value of None and provides a description for the `practice_area` field. |
| `Field` | `default_factory=list, description="List of contacts to arrange interviews with."` | Initializes an empty list by default and provides a description for the `interview_contacts` field. |
| `Field` | `description="CRITICAL STRATEGY FIELD. The current ranking status of the firm in this specific practice area (e.g., 'Unranked', 'Band 1', 'Band 4')."` | Provides a description for the `current_band_status` field, emphasizing its strategic importance. |
| `Field` | `default="N/A", description="The firm's recent ranking history. Choose 'Ascent' if they recently climbed, 'Descent' if they dropped, 'Stagnation' if they have been in the same band for years, or 'N/A' if unknown."` | Sets a default value of "N/A" and provides a description for the `ranking_history_trajectory` field. |
| `Field` | `None, description="Full name of the team or department head."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Office location or city of the team head."` | Sets a default value of None and provides a description for the `location` field. |
| `Field` | `0, description="Number of partners who spend at least 50% of their time in this department. Return 0 if none."` | Sets a default value of 0 and provides a description for the `partners_count_50_percent_plus` field. |
| `Field` | `0, description="Number of non-partners who spend at least 50% of their time in this department. Return 0 if none."` | Sets a default value of 0 and provides a description for the `non_partners_count_50_percent_plus` field. |
| `Field` | `None, description="The Team or Department Name as used internally by the firm."` | Sets a default value of None and provides a description for the `team_name_internal` field. |
| `Field` | `default_factory=list, description="List of the Head(s) of the Team."` | Initializes an empty list by default and provides a description for the `heads_of_team` field. |
| `Field` | `default_factory=Metrics` | Initializes a default `Metrics` object for the `metrics` field. |
| `Field` | `None, description="Narrative detailing what sets the practice apart from other firms."` | Sets a default value of None and provides a description for the `what_sets_us_apart` field. |
| `Field` | `None, description="Narrative detailing measures introduced or maintained over the last year to benefit clients."` | Sets a default value of None and provides a description for the `initiatives_and_innovation` field. |
| `Field` | `None, description="Feedback regarding existing rankings or commentary. Return null if blank."` | Sets a default value of None and provides a description for the `rankings_feedback` field. |
| `Field` | `None, description="Name of the independent barrister or advocate."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="The Chambers or Firm they belong to."` | Sets a default value of None and provides a description for the `chambers` field. |
| `Field` | `None, description="Location or jurisdiction of the barrister."` | Sets a default value of None and provides a description for the `location` field. |
| `Field` | `None, description="Comments regarding the instruction or their performance."` | Sets a default value of None and provides a description for the `comments` field. |
| `Field` | `None, description="Full name of the leading partner."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Office location or city of the partner."` | Sets a default value of None and provides a description for the `location` field. |
| `Field` | `False, description="Were they ranked in the previous edition? Map 'Yes'/'Y' to true, 'No'/'N' to false."` | Sets a default value of False and provides a description for the `ranked_in_previous_edition` field. |
| `Field` | `None, description="Detailed supporting evidence and narrative for why this partner is pre-eminent. Extract full text."` | Sets a default value of None and provides a description for the `supporting_information` field. |
| `Field` | `None, description="Full name of the leading associate/next gen partner (can include counsel)."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Office location or city of the associate."` | Sets a default value of None and provides a description for the `location` field. |
| `Field` | `None, description="Detailed supporting evidence for this associate/partner. Extract full text."` | Sets a default value of None and provides a description for the `supporting_information` field. |
| `Field` | `None, description="Name of the person who arrived, departed, or was promoted."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="The position or role of the person (e.g., Partner)."` | Sets a default value of None and provides a description for the `position_role` field. |
| `Field` | `None, description="Specify strictly 'Joined', 'Departed', or 'Promoted'."` | Sets a default value of None and provides a description for the `action` field. |
| `Field` | `None, description="The firm they joined from, or the destination firm they departed to."` | Sets a default value of None and provides a description for the `firm_source_destination` field. |
| `Field` | `None, description="The month and year of the action (e.g., 'March 2025')."` | Sets a default value of None and provides a description for the `month_year` field. |
| `Field` | `default_factory=list, description="Nominations for genuinely exceptional, pre-eminent partners."` | Initializes an empty list by default and provides a description for the `leading_partners` field. |
| `Field` | `default_factory=list, description="Nominations for junior/new/younger partners making a material difference."` | Initializes an empty list by default and provides a description for the `next_generation_partners` field. |
| `Field` | `default_factory=list, description="Nominations for junior/new/younger associates or counsels making a material difference."` | Initializes an empty list by default and provides a description for the `leading_associates` field. |
| `Field` | `default_factory=list, description="List of significant recent arrivals, departures, or promotions at the partner level."` | Initializes an empty list by default and provides a description for the `arrivals_and_departures` field. |
| `Field` | `None, description="The official name of the active key client."` | Sets a default value of None and provides a description for the `active_key_client` field. |
| `Field` | `False, description="Determine if this is a new client. Map 'Yes' or 'Y' to true, 'No', 'N' or blank to false."` | Sets a default value of False and provides a description for the `is_new_client` field. |
| `Field` | `False, description="Whether the client is publishable."` | Sets a default value of False and provides a description for the `is_publishable` field. |
| `Field` | `None, description="A brief 1-2 sentence summary of a highlight matter (e.g., 'Advised X on acquisition of Y'). MUST be publishable."` | Sets a default value of None and provides a description for the `publishable_summary` field. |
| `Field` | `None, description="Name of the lead partner or other key team member."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Office location of the team member."` | Sets a default value of None and provides a description for the `office` field. |
| `Field` | `None, description="Specific practice area of the team member."` | Sets a default value of None and provides a description for the `practice_area` field. |
| `Field` | `None, description="Name of the other law firm advising on the matter."` | Sets a default value of None and provides a description for the `firm_name` field. |
| `Field` | `None, description="Description of their role."` | Sets a default value of None and provides a description for the `role_details` field. |
| `Field` | `None, description="The specific firm, company, or individual that this external firm advised."` | Sets a default value of None and provides a description for the `entity_advised` field. |
| `Field` | `None, description="Start date of the matter. Return null if not provided."` | Sets a default value of None and provides a description for the `start` field. |
| `Field` | `None, description="End date of the matter. Return null if not provided."` | Sets a default value of None and provides a description for the `end` field. |
| `Field` | `None, description="Matter ID."` | Sets a default value of None and provides a description for the `id` field. |
| `Field` | `None, description="The name of the client."` | Sets a default value of None and provides a description for the `client_name` field. |
| `Field` | `None, description="The industry sector of the matter/client. Return null if blank."` | Sets a default value of None and provides a description for the `industry_sector` field. |
| `Field` | `None, description="Detailed description of the matter, background, and firm's role. DO NOT include generic marketing text."` | Sets a default value of None and provides a description for the `matter_description` field. |
| `Field` | `None, description="Financial value of the deal/matter. Return null if blank."` | Sets a default value of None and provides a description for the `deal_value` field. |
| `Field` | `False` | Sets a default value of False for the `is_cross_border` field. |
| `Field` | `default_factory=list, description="If cross-border, list the jurisdictions involved."` | Initializes an empty list by default and provides a description for the `jurisdictions_involved` field. |
| `Field` | `default_factory=list, description="List of lead partners working on this specific matter."` | Initializes an empty list by default and provides a description for the `lead_partners` field. |
| `Field` | `default_factory=list, description="List of other key team members (associates, counsels) on the matter."` | Initializes an empty list by default and provides a description for the `other_key_team_members` field. |
| `Field` | `default_factory=list, description="List of other external firms involved in the matter."` | Initializes an empty list by default and provides a description for the `external_firms_advising` field. |
| `Field` | `None, description="Start and end dates for the matter."` | Sets a default value of None and provides a description for the `dates` field. |
| `Field` | `False, description="Whether the matter is publishable. If the text explicitly says 'CONFIDENTIAL', this should be false."` | Sets a default value of False and provides a description for the `is_publishable` field. |
| `Field` | `None` | Sets a default value of None for the `identity` field. |
| `Field` | `None` | Sets a default value of None for the `department_info` field. |
| `Field` | `None` | Sets a default value of None for the `narratives` field. |
| `Field` | `default_factory=list, description="Up to 3 brief summaries of publishable work highlights."` | Initializes an empty list by default and provides a description for the `work_highlights_summaries` field. Sets a maximum length of 3. |
| `Field` | `default_factory=list, description="Up to 20 publishable work highlights."` | Initializes an empty list by default and provides a description for the `publishable_matters` field. Sets a maximum length of 20. |
| `Field` | `default_factory=list, description="Up to 20 confidential work highlights."` | Initializes an empty list by default and provides a description for the `confidential_matters` field. Sets a maximum length of 20. |
| `Field` | `default_factory=list, description="Optional details of independent barristers/advocates instructed in the past year."` | Initializes an empty list by default and provides a description for the `barristers` field. |
| `Field` | `None, description="Full name of the contact person."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Email address. Extract cleanly without mailto: prefixes."` | Sets a default value of None and provides a description for the `email` field. |
| `Field` | `None, description="Telephone number. Keep international codes if present."` | Sets a default value of None and provides a description for the `telephone_number` field. |
| `Field` | `None, description="The official, registered name of the law firm. Strip conversational filler."` | Sets a default value of None and provides a description for the `A1_firm_name` field. |
| `Field` | `None, description="The specific practice area being submitted for (e.g., 'FinTech Legal')."` | Sets a default value of None and provides a description for the `A2_practice_area` field. |
| `Field` | `None, description="The country or jurisdiction the submission applies to."` | Sets a default value of None and provides a description for the `A3_location_jurisdiction` field. |
| `Field` | `default_factory=list, description="List of personnel designated to arrange interviews."` | Initializes an empty list by default and provides a description for the `A4_contact_persons` field. |
| `Field` | `default=None, description="CRITICAL STRATEGY FIELD. The current ranking status of the firm in this specific practice area (e.g., 'Unranked', 'Band 1', 'Band 4'). If not explicitly mentioned, return null."` | Sets a default value of None and provides a description for the `current_band_status` field, emphasizing its strategic importance. |
| `Field` | `default=None, description="The firm's recent ranking history. Choose 'Ascent' if they recently climbed, 'Descent' if they dropped, 'Stagnation' if they have been in the same band for years, or 'First Time' if they have never been ranked before. If the history is not explicitly mentioned, you MUST return null."` | Sets a default value of None and provides a description for the `ranking_history_trajectory` field. |
| `Field` | `None, description="The total raw integer number of lawyers/partners in this category. Return 0 if none."` | Sets a default value of None and provides a description for the `total_number` field. |
| `Field` | `None, description="The percentage of males. Include the '%' sign if present in text."` | Sets a default value of None and provides a description for the `male_ratio_percentage` field. |
| `Field` | `None, description="The percentage of females. Include the '%' sign if present in text."` | Sets a default value of None and provides a description for the `female_ratio_percentage` field. |
| `Field` | `None, description="Full name of the lawyer."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Include the bio URL or specific comments/key areas of focus listed for this lawyer."` | Sets a default value of None and provides a description for the `comments_or_web_link` field. |
| `Field` | `None, description="Evaluate if they are a partner based on the text. You MUST output exactly 'Y' or 'N'."` | Sets a default value of None and provides a description for the `is_partner` field. |
| `Field` | `None, description="Evaluate if they are already ranked based on the text. You MUST output exactly 'Y' or 'N'."` | Sets a default value of None and provides a description for the `is_ranked` field. |
| `Field` | `None, description="Details regarding parental leave or part-time arrangements. Return null if blank."` | Sets a default value of None and provides a description for the `parental_leave_or_part_time` field. |
| `Field` | `None, description="Name of the lawyer who joined or departed."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Specify strictly 'Joined' or 'Departed'."` | Sets a default value of None and provides a description for the `status_joined_departed` field. |
| `Field` | `None, description="The name of the previous firm (if joined) or destination firm (if departed)."` | Sets a default value of None and provides a description for the `from_or_destination_firm` field. |
| `Field` | `None, description="The internal name the firm uses. Usually labeled as B.1"` | Sets a default value of None and provides a description for the `department_name` field. |
| `Field` | `None, description="Total number and gender ratio of partners in the department."` | Sets a default value of None and provides a description for the `B2_partners` field. |
| `Field` | `None, description="Total number and gender ratio of other qualified lawyers (associates, counsels)."` | Sets a default value of None and provides a description for the `B3_other_qualified_lawyers` field. |
| `Field` | `default_factory=list, description="List of Department Head(s) or Key Partners (USA Template)."` | Initializes an empty list by default and provides a description for the `B4_department_heads` field. |
| `Field` | `None, description="Percentage of the team identifying as LGBT+. Must be a raw number/percentage string. Return null if blank."` | Sets a default value of None and provides a description for the `B5_diversity_lgbt_percentage` field. |
| `Field` | `None, description="Percentage of the team with a disability. Must be a raw number/percentage string. Return null if blank."` | Sets a default value of None and provides a description for the `B6_diversity_disability_percentage` field. |
| `Field` | `default_factory=list, description=("CRITICAL: Look for the section identifying the leaders of the practice. It is usually titled 'B4 Department Head(s) or Key Partners' OR 'B7 Head or Heads of department'. Ignore the B4/B7 numbering and look for the keywords 'Head' and 'Department'. The data will likely be a flattened table containing Names, Emails, and Phone numbers. Extract every person listed in this specific section.")` | Initializes an empty list by default and provides a detailed description for the `heads_of_department` field. |
| `Field` | `default_factory=list, description="List of partners who joined or left. Usually labeled as B.8 or similar."` | Initializes an empty list by default and provides a description for the `hires_departures_last_12_months` field. |
| `Field` | `default_factory=list, description="Details regarding ranked and unranked lawyers, including their key areas of focus and standout work."` | Initializes an empty list by default and provides a description for the `B9_lawyers_ranked_unranked` field. |
| `Field` | `None, description=("Narrative text describing what the department is best known for. Note: This is typically labeled as 'B7' or 'B10'. It should include details on industry sector expertise, key types of work, areas of recent growth, and any feedback on previous Chambers coverage. Maximum word count is usually 500 words.")` | Sets a default value of None and provides a detailed description for the `department_best_known_for` field. |
| `Field` | `default_factory=list, description="List of external barristers or advocates used by the firm."` | Initializes an empty list by default and provides a description for the `C1_barristers_advocates` field. |
| `Field` | `None, description="Feedback provided regarding other competing firms or the ranking status of their own lawyers. Return null if blank."` | Sets a default value of None and provides a description for the `C2_feedback_on_other_firms` field. |
| `Field` | `None, description="The official name of the client."` | Sets a default value of None and provides a description for the `name_of_client` field. |
| `Field` | `None, description="Determine if this is a new client within the last 12 months. Map 'Yes' to true, 'No' or blank to false."` | Sets a default value of None and provides a description for the `is_new_client` field. |
| `Field` | `None, description="The internal matter ID or sequential number (e.g., 'Publishable Matter 1')."` | Sets a default value of None and provides a description for the `matter_id` field. |
| `Field` | `None, description="The name of the client. MUST be publishable."` | Sets a default value of None and provides a description for the `D1_name_of_client` field. |
| `Field` | `None, description="Summarizes the publishable matter and the firm's specific role. MUST NOT contain confidential information. If text says 'CONFIDENTIAL', route it to section E instead."` | Sets a default value of None and provides a description for the `D2_summary_of_matter_and_role` field. |
| `Field` | `None, description="The financial value of the matter including currency. Return null if N/A or blank."` | Sets a default value of None and provides a description for the `D3_matter_value` field. |
| `Field` | `None, description="List of jurisdictions involved if cross-border. If it explicitly says 'No', return null."` | Sets a default value of None and provides a description for the `D4_cross_border_jurisdictions` field. |
| `Field` | `None, description="Name(s) of the lead partner(s) on the matter."` | Sets a default value of None and provides a description for the `D5_lead_partner` field. |
| `Field` | `None, description="Names of other associates or team members involved."` | Sets a default value of None and provides a description for the `D6_other_team_members` field. |
| `Field` | `None, description="Names of other law firms involved and their roles. Return null if N/A."` | Sets a default value of None and provides a description for the `D7_other_firms_advising` field. |
| `Field` | `None, description="The current status (e.g., 'Ongoing') or completion date."` | Sets a default value of None and provides a description for the `D8_date_completion_or_status` field. |
| `Field` | `None, description="URLs to press coverage or additional notes. Return null if blank."` | Sets a default value of None and provides a description for the `D9_other_information_links` field. |
| `Field` | `default_factory=list, description="List of clients whose identities can be published. Exclude any client marked confidential."` | Initializes an empty list by default and provides a description for the `D0_publishable_clients_list` field. |
| `Field` | `default_factory=list, description="List of up to 20 publishable work highlights. MUST NOT contain confidential data."` | Initializes an empty list by default and provides a description for the `publishable_matters` field. Sets a maximum length of 20. |
| `Field` | `None, description="The internal matter ID or sequential number (e.g., 'Confidential Matter 1')."` | Sets a default value of None and provides a description for the `matter_id` field. |
| `Field` | `None, description="The name of the client. Treat this as strictly confidential."` | Sets a default value of None and provides a description for the `E1_name_of_client` field. |
| `Field` | `None, description="Summarizes the confidential matter and the firm's role. This text is protected and not for publication."` | Sets a default value of None and provides a description for the `E2_summary_of_matter_and_role` field. |
| `Field` | `None, description="The financial value of the matter. Often marked 'Confidential' or 'Non disclosable'. Extract the text as written."` | Sets a default value of None and provides a description for the `E3_matter_value` field. |
| `Field` | `None, description="List of jurisdictions involved if cross-border. If it explicitly says 'No', return null."` | Sets a default value of None and provides a description for the `E4_cross_border_jurisdictions` field. |
| `Field` | `None, description="Name(s) of the lead partner/lawyer on the matter."` | Sets a default value of None and provides a description for the `E5_lead_lawyer` field. |
| `Field` | `None, description="Names of other associates or team members involved."` | Sets a default value of None and provides a description for the `E6_other_team_members` field. |
| `Field` | `None, description="Names of other law firms involved and their roles. Return null if N/A."` | Sets a default value of None and provides a description for the `E7_other_firms_advising` field. |
| `Field` | `None, description="The current status (e.g., 'Ongoing') or completion date."` | Sets a default value of None and provides a description for the `E8_date_completion_or_status` field. |
| `Field` | `None, description="URLs to press coverage or additional notes. Return null if blank."` | Sets a default value of None and provides a description for the `E9_other_information_links` field. |
| `Field` | `True, description="Always set to true for matters in Section E."` | Sets a default value of True and provides a description for the `is_confidential` field. |
| `Field` | `default_factory=list, description="List of clients whose identities MUST remain strictly confidential."` | Initializes an empty list by default and provides a description for the `E0_confidential_clients_list` field. |
| `Field` | `default_factory=list, description="List of confidential work highlights. These matters are protected and not for publication."` | Initializes an empty list by default and provides a description for the `confidential_matters` field. |
| `Field` | `None` | Sets a default value of None for the `A_preliminary_information` field. |
| `Field` | `None` | Sets a default value of None for the `B_department_information` field. |
| `Field` | `None` | Sets a default value of None for the `C_feedback` field. |
| `Field` | `None` | Sets a default value of None for the `D_publishable_information` field. |
| `Field` | `None` | Sets a default value of None for the `E_confidential_information` field. |
| `Field` | `None, description="The official name of the firm."` | Sets a default value of None and provides a description for the `firm_name` field. |
| `Field` | `None, description="The year the firm was established."` | Sets a default value of None and provides a description for the `year_established` field. |
| `Field` | `None, description="Name of the Managing Partner(s)."` | Sets a default value of None and provides a description for the `managing_partners` field. |
| `Field` | `None, description="Name of the person(s) in charge of Marketing/Business Development."` | Sets a default value of None and provides a description for the `marketing_bd_persons` field. |
| `Field` | `None, description="List of office locations."` | Sets a default value of None and provides a description for the `list_of_offices` field. |
| `Field` | `None, description="Number of Partners in the entire firm."` | Sets a default value of None and provides a description for the `total_partners` field. |
| `Field` | `None, description="Number of Counsels/Associates in the entire firm."` | Sets a default value of None and provides a description for the `total_counsels_associates` field. |
| `Field` | `None, description="Name of the head of the department or key partner."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Email address."` | Sets a default value of None and provides a description for the `email` field. |
| `Field` | `None, description="The year they became a partner."` | Sets a default value of None and provides a description for the `partner_since` field. |
| `Field` | `None, description="Specific specialisms of the partner."` | Sets a default value of None and provides a description for the `specific_specialisms` field. |
| `Field` | `False, description="True if the partner dedicates less than 50% of their time to this department (needs to be highlighted in red)."` | Sets a default value of False and provides a description for the `dedicates_less_than_50_percent` field. |
| `Field` | `None, description="Name of the person."` | Sets a default value of None and provides a description for the `name` field. |
| `Field` | `None, description="Position (e.g., Partner, Counsel, Associate)."` | Sets a default value of None and provides a description for the `position` field. |
| `Field` | `None, description="Action: Arrived, left, promoted, or retired."` | Sets a default value of None and provides a description for the `action` field. |
| `Field` | `None, description="Where they moved to or from."` | Sets a default value of None and provides a description for the `moved_to_from` field. |
| `Field` | `None, description="Month and year of the change."` | Sets a default value of None and provides a description for the `month_year` field. |
| `Field` | `None, description="Name of the company/client."` | Sets a default value of None and provides a description for the `company` field. |
| `Field` | `None, description="Industry sector of the client."` | Sets a default value of None and provides a description for the `sector` field. |
| `Field` | `False, description="True if it is a new client."` | Sets a default value of False and provides a description for the `is_new_client` field. |
| `Field` | `False, description="True if the client is confidential."` | Sets a default value of False and provides a description for the `is_confidential` field. |
| `Field` | `None, description="Type of work performed for the client."` | Sets a default value of None and provides a description for the `type_of_work` field. |
| `Field` | `None, description="Name of the Partner(s) in charge of completing this form."` | Sets a default value of None and provides a description for the `partners_completing_form` field. |
| `Field` | `default_factory=list, description="List of Heads of the department and other key partners."` | Initializes an empty list by default and provides a description for the `department_heads` field. |
| `Field` | `None, description="Number of Male Partners in the department."` | Sets a default value of None and provides a description for the `composition_male_partners` field. |
| `Field` | `None, description="Number of Female Partners in the department."` | Sets a default value of None and provides a description for the `composition_female_partners` field. |
| `Field` | `None, description="Number of Counsels/Associates in the department."` | Sets a default value of None and provides a description for the `composition_counsels_associates` field. |
| `Field` | `default_factory=list, description="Changes in the department over the last 12 months."` | Initializes an empty list by default and provides a description for the `department_changes` field. |
| `Field` | `None, description="Narrative on what the department is best known for (max 500 words)."` | Sets a default value of None and provides a description for the `best_known_for` field. |
| `Field` | `None, description="Number of new cases taken on in the last 12 months."` | Sets a default value of None and provides a description for the `new_cases_last_12_months` field. |
| `Field` | `default_factory=list, max_length=5, description="Top five sectors the department works with."` | Initializes an empty list by default and provides a description for the `top_five_sectors` field. Sets a maximum length of 5. |
| `Field` | `default_factory=list, max_length=30, description="List of active clients (up to 30)."` | Initializes an empty list by default and provides a description for the `active_clients` field. Sets a maximum length of 30. |
| `Field` | `default_factory=list, description="Feedback on leading law firms/lawyers."` | Initializes an empty list by default and provides a description for the `established_practitioners` field. |
| `Field` | `None, description="Name of the leading firm or lawyer."` | Sets a default value of None and provides a description for the `firm_lawyer` field. |
| `Field` | `None, description="Comments supporting their leading status."` | Sets a default value of None and provides a description for the `comments` field. |
| `Field` | `default_factory=list, description="Feedback on rising stars in the practice."` | Initializes an empty list by default and provides a description for the `rising_stars` field. |
| `Field` | `None, description="Name of the rising star law firm."` | Sets a default value of None and provides a description for the `law_firm` field. |
| `Field` | `None, description="Names of the rising star lawyers."` | Sets a default value of None and provides a description for the `lawyers` field. |
| `Field` | `None, description="Main specialty of the rising star."` | Sets a default value of None and provides a description for the `main_specialty` field. |
| `Field` | `None, description="Opinion on the firm's current position in Leaders League ranking."` | Sets a default value of None and provides a description for the `opinion_current_position` field. |
| `Field` | `None, description="Name of the Matter."` | Sets a default value of None and provides a description for the `matter_name` field. |
| `Field` | `False, description="True if the matter is confidential."` | Sets a default value of False and provides a description for the `is_confidential` field. |
| `Field` | `None, description="Name of the Client."` | Sets a default value of None and provides a description for the `client` field. |
| `Field` | `None, description="Value of the matter (specify currency) and/or other key numbers."` | Sets a default value of None and provides a description for the `matter_value` field. |
| `Field` | `None, description="Status of the matter (closed in last year or ongoing)."` | Sets a default value of None and provides a description for the `matter_status` field. |
| `Field` | `None, description="Description of the context in which work was solicited."` | Sets a default value of None and provides a description for the `matter_context` field. |
| `Field` | `None, description="Explanation of what the firm did and strategy used."` | Sets a default value of None and provides a description for the `firm_role_output` field. |
| `Field` | `None, description="Lead Partner(s) on the matter."` | Sets a default value of None and provides a description for the `lead_partners` field. |
| `Field` | `None, description="Other team members involved."` | Sets a default value of None and provides a description for the `other_team_members` field. |
| `Field` | `None, description="Other firms advising on the matter and their role."` | Sets a default value of None and provides a description for the `other_firms_advising` field. |
| `Field` | `None, description="Links to press coverage."` | Sets a default value of None and provides a description for the `press_links` field. |
| `Field` | `default_factory=list, max_length=10, description="Up to 10 work highlights."` | Initializes an empty list by default and provides a description for the `work_highlights` field. Sets a maximum length of 10. |
| `Field` | `None` | Sets a default value of None for the `firm_information` field. |
| `Field` | `None` | Sets a default value of None for the `department_information` field. |
| `Field` | `None` | Sets a default value of None for the `peer_feedback` field. |
| `Field` | `None` | Sets a default value of None for the `ranking_feedback` field. |