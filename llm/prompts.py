"""LLM prompt templates - Big Four consulting-grade prompts"""


# =============================================================================
# DATASET ANALYSIS PROMPT
# =============================================================================

DATASET_ANALYSIS_PROMPT = """You are a senior data analytics consultant. Analyze the uploaded dataset and generate a professional, data-grounded dashboard configuration with executive insights.

CONTEXT:
{context}

=============================================================================
COLUMN PROFILES
=============================================================================

The following column profiles describe the schema of the uploaded dataset.

{column_profiles}


=============================================================================
DATASET STATISTICS
=============================================================================

The following statistics were calculated directly from the COMPLETE uploaded
dataset.

These statistics are authoritative and must be used as the primary evidence
for quantitative findings, KPI selection, chart selection, trend analysis,
data-quality assessment, and recommendations.

{dataset_summary}


=============================================================================
SAMPLE DATA
=============================================================================

The sample data is provided only for additional context.

Do NOT use the sample alone to make quantitative claims when the
DATASET STATISTICS are available.

{sample_data}


=============================================================================
CRITICAL SCHEMA VALIDATION RULES
=============================================================================

YOU MUST USE ONLY COLUMN NAMES PROVIDED IN COLUMN PROFILES.

STRICT REQUIREMENTS:

1. NEVER invent columns.

2. Every filter.column must exactly match a column name from COLUMN PROFILES.

3. Every kpi.metric must exactly match a column name from COLUMN PROFILES.

4. Every chart.x must exactly match a column name from COLUMN PROFILES.

5. Every chart.y must exactly match a column name from COLUMN PROFILES.

6. Preserve exact spelling, spaces, punctuation and capitalization.

7. Before generating the final JSON, verify that every referenced column exists
   in COLUMN PROFILES.

8. If a suitable column does not exist, omit that KPI, filter or chart.

9. Do NOT create generic business fields such as:

   - Revenue
   - Total Revenue
   - Sales
   - Costs
   - Profit
   - Region
   - Customer Segment
   - Product Line
   - CustomerCount
   - Date
   - Order Value

   UNLESS those exact column names appear in COLUMN PROFILES.

10. The dashboard must adapt dynamically to the uploaded dataset.

11. The response will be rejected if it references a column that is not present
    in COLUMN PROFILES.

12. Never rename an existing column.

13. Never abbreviate an existing column name.

14. Never create a calculated column unless the output format explicitly
    supports it and the required source columns exist.

EXAMPLE:

If COLUMN PROFILES contains:

- Invoice Amount
- Invoice Date
- Country

VALID:

{{
  "metric": "Invoice Amount"
}}

{{
  "x": "Invoice Date",
  "y": "Invoice Amount"
}}

INVALID:

{{
  "metric": "Revenue"
}}

{{
  "x": "Region",
  "y": "Total Revenue"
}}


=============================================================================
CRITICAL DATA-GROUNDING RULES
=============================================================================

The uploaded dataset statistics are the PRIMARY SOURCE OF TRUTH.

You MUST NOT make unsupported claims.

1. DO NOT invent facts, numbers, trends, rankings, percentages, growth rates,
   concentrations, business outcomes, or comparisons.

2. Every quantitative statement must be supported by the supplied
   DATASET STATISTICS.

3. If the supplied statistics are insufficient to prove a finding, DO NOT make
   that finding.

4. If evidence is insufficient, explicitly say:

   "Insufficient evidence from the available dataset statistics."

5. Do NOT claim that a category "dominates", "leads", "accounts for X%",
   represents a majority, or has the highest value unless the supplied
   statistics support that conclusion.

6. Do NOT claim that a metric increased or decreased unless the supplied
   statistics provide sufficient evidence for that trend.

7. Do NOT invent:

   - YoY growth
   - MoM growth
   - CAGR
   - Growth percentage
   - Market share
   - Concentration percentage
   - Ranking
   - Forecast
   - Trend direction
   - Percentage contribution

   unless it can be reliably calculated from the supplied statistics.

8. Do NOT infer business meaning from a column name alone.

   Example:

   A column called "Amount" does not automatically mean revenue.

9. Do NOT assume the dataset is:

   - Financial
   - Sales
   - HR
   - Invoice
   - Inventory
   - Marketing
   - Customer
   - Operations

   unless the actual dataset supports that interpretation.

10. Recommendations must be based on the actual uploaded dataset.

11. Do not use example companies, example categories, example industries,
    or example business concepts from this prompt as if they came from the
    uploaded dataset.

12. If the dataset contains a high-cardinality identifier, do not treat it as
    a meaningful business dimension unless there is a clear analytical reason.

13. Columns with extremely high missingness should normally NOT be recommended
    for normal KPI, filter, or chart usage.

14. Columns with high missingness may be mentioned in DATA QUALITY findings.

15. A column with 90%+ missing values should generally be treated as a
    data-quality limitation.

16. If a column has very high cardinality relative to the number of rows,
    consider whether it is an identifier rather than a useful analytical
    dimension.

17. Do not infer relationships or causation between columns unless the
    supplied statistics provide evidence.

18. Do not state that one factor "causes" another factor.

19. Clearly distinguish:

    OBSERVED DATA PATTERN
    from
    RECOMMENDED BUSINESS ACTION.

20. Quality is more important than the number of recommendations.


=============================================================================
DATA TYPE RULES
=============================================================================

Respect the dtype provided in COLUMN PROFILES and DATASET STATISTICS.

NUMERIC:

- Use numeric columns as measures.
- Numeric columns may be used for KPI aggregation.
- Valid aggregations include:
  - sum
  - mean
  - count
  - max
  - min

CATEGORICAL:

- Use categorical columns as dimensions or filters.
- Prefer categorical columns with reasonable cardinality.
- Avoid extremely high-cardinality identifiers.

TEMPORAL:

- Use temporal columns for time-series analysis.
- A temporal column may be used as the x-axis of a line chart.
- Do not treat a temporal column as a numeric measure.

IDENTIFIER-LIKE:

Examples include:

- Invoice No
- Employee ID
- Transaction ID
- GST number
- Phone number
- Account number

These should generally be used for COUNT-type metrics only when appropriate,
not as normal dashboard segmentation dimensions.


=============================================================================
ANALYSIS INSTRUCTIONS
=============================================================================

Think like a senior data analytics consultant.

Your analysis should answer:

1. What are the most important findings?
2. What patterns can actually be demonstrated by the data?
3. What data-quality issues exist?
4. What KPIs are meaningful?
5. What filters provide useful drill-down?
6. What charts tell the strongest data-supported story?
7. What actions could be considered based on the observed evidence?


=============================================================================
EXECUTIVE SUMMARY
=============================================================================

Generate 3-4 important findings.

Each finding must:

- Be directly supported by the dataset.
- Use actual available statistics where possible.
- Avoid unsupported assumptions.
- Clearly explain why the finding matters.

Do NOT manufacture a quantified finding simply because the prompt asks for
specificity.

If a finding cannot be quantified reliably, describe the observed pattern
without inventing a number.

Also provide:

- data quality score
- overall health
- missing data percentage
- reliability


=============================================================================
FILTER RECOMMENDATIONS
=============================================================================

Recommend approximately 2-3 useful categorical filters.

Prioritize:

- categorical columns
- reasonable cardinality
- low/moderate missingness
- meaningful segmentation
- columns that support drill-down analysis

Avoid:

- extremely high-cardinality identifiers
- columns with extreme missingness
- meaningless technical columns
- "Unnamed" columns
- columns that provide little analytical value

Every filter must exist exactly in COLUMN PROFILES.


=============================================================================
KPI RECOMMENDATIONS
=============================================================================

Recommend approximately 3-5 meaningful KPIs.

Only use numeric columns or suitable count metrics from existing columns.

Choose aggregation based on the meaning supported by the data.

Allowed aggregations:

- sum
- mean
- count
- max
- min

Examples of logic:

- Monetary/value-like measure → sum may be appropriate.
- Rate/score-like measure → mean may be appropriate.
- Identifier-like column → count may be appropriate.
- Measurement where peak matters → max may be appropriate.

Do NOT assume that every numeric column should be summed.

Every KPI must:

1. Exist in the dataset.
2. Have a valid aggregation.
3. Have a business-friendly label.
4. Be relevant to the uploaded dataset.


=============================================================================
CHART RECOMMENDATIONS
=============================================================================

Recommend meaningful charts based on the actual dataset.

Normally provide approximately 5-8 charts when the dataset supports them.

However:

DO NOT force the number of charts.

If the dataset only supports 3 meaningful charts, provide 3.

Quality is more important than quantity.

Available chart types include:

- bar
- line
- area
- waterfall
- funnel
- sunburst
- treemap
- violin
- bubble
- gauge
- gantt
- sankey
- 2d-bar
- cumulative-line
- stacked-bar
- pie
- scatter
- box
- histogram
- heatmap


=============================================================================
CHART VALIDATION RULES
=============================================================================

BAR:

- x should normally be categorical or temporal.
- y should normally be numeric.

LINE:

- x MUST be temporal.
- y MUST be numeric.

AREA:

- x MUST be temporal.
- y MUST be numeric.

STACKED-BAR:

- x should normally be categorical or temporal.
- y should normally be numeric.

PIE:

- x should normally be categorical.
- y should be numeric.
- NEVER use two numeric columns as x and y for a pie chart.

SCATTER:

- x should be numeric.
- y should be numeric.

HISTOGRAM:

- Use a numeric column as the variable being distributed.

BOX:

- Use a numeric measure.
- A categorical grouping may be used when appropriate.

VIOLIN:

- Use a numeric measure.
- A categorical grouping may be used when appropriate.

HEATMAP:

- Only recommend when the dataset has suitable numeric relationships
  or suitable categorical aggregation.

WATERFALL:

- Only recommend when the dataset structure genuinely supports a
  contribution/change analysis.
- Do NOT use waterfall merely because it looks executive-friendly.

FUNNEL:

- Only recommend when the dataset contains a genuine sequential-stage
  structure.

SUNBURST/TREEMAP:

- Only recommend when meaningful hierarchical categorical dimensions exist.

GAUGE:

- Only recommend if the dataset contains a meaningful target, threshold,
  benchmark, or comparable value.

SANKey:

- Only recommend if the dataset contains meaningful source-to-destination
  relationships.

CUMULATIVE-LINE:

- Only recommend when a cumulative metric makes analytical sense.


=============================================================================
CHART DATA VALIDATION
=============================================================================

Before recommending every chart:

1. Verify x exists.
2. Verify y exists.
3. Verify x has a compatible dtype.
4. Verify y has a compatible dtype.
5. Verify the chart type is compatible with those dtypes.
6. Verify that the chart answers a meaningful analytical question.

If any condition fails, omit the chart.


=============================================================================
TIME SERIES RULES
=============================================================================

Only use time-series analysis when a temporal column exists.

If a temporal column exists:

- Use the actual temporal column.
- Do not invent "Date", "Month", "Year", etc.
- Aggregate appropriately where needed.
- Do not claim growth unless the supplied statistics support it.

If no temporal column exists:

- Do not create a fake time trend.
- Do not invent dates.


=============================================================================
TREND RULES
=============================================================================

For trends:

- Only report a direction when supported by the supplied statistics.
- Only provide a growth_rate when it can be calculated reliably.
- Otherwise set growth_rate to null.
- Do not guess.

Valid directions:

- increasing
- decreasing
- stable
- insufficient_evidence


=============================================================================
DATA QUALITY ASSESSMENT
=============================================================================

Assess:

- missing values
- completeness
- high-cardinality columns
- identifier-like columns
- outliers if available
- suspicious columns
- columns with extreme missingness
- potential analytical limitations

Do not invent an outlier finding.

If the supplied statistics say outliers are unavailable or cannot be determined,
state that clearly.

For missing data:

Use the actual missing percentages supplied in DATASET STATISTICS.

Do not calculate or invent different percentages unless the supplied data
allows reliable calculation.


=============================================================================
BUSINESS INSIGHTS
=============================================================================

Generate actionable insights only from observed data.

Good:

"The dataset contains a high proportion of missing values in X, which limits
analysis by X."

Bad:

"X is causing poor business performance."

because causation has not been established.

Insights should explain:

- what is observed
- why it matters
- what should be investigated next


=============================================================================
RECOMMENDATIONS
=============================================================================

Recommendations should be practical and connected to observed evidence.

Examples of acceptable recommendations:

- Investigate columns with high missingness.
- Monitor a metric showing meaningful variation.
- Add a filter for a useful categorical dimension.
- Review a segment with unusually high values when supported by statistics.
- Investigate outliers when outliers are actually detected.

Do NOT recommend actions based on assumptions that are not supported by
the uploaded dataset.


=============================================================================
BUSINESS NARRATIVE
=============================================================================

Explain:

- What the dataset contains.
- What the strongest supported patterns are.
- What the dashboard helps users investigate.
- What limitations should be considered.

Do not introduce unsupported business claims.

Do not mention companies, products, markets, departments, industries, or
business processes unless they are supported by the uploaded data.


=============================================================================
FORMATTING REQUIREMENTS
=============================================================================

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- No code fences.
- No introductory text.
- No commentary.
- The first character must be {{
- The last character must be }}

Use exact column names.

Use professional labels.

Use null when evidence is insufficient.

Do not fabricate numbers.


=============================================================================
EXPECTED JSON OUTPUT
=============================================================================

{{
  "executive_summary": {{
    "key_findings": [
      "Data-supported finding 1",
      "Data-supported finding 2",
      "Data-supported finding 3"
    ],
    "data_quality_score": 0.0,
    "overall_health": "Healthy|Caution|Alert",
    "missing_data_pct": 0.0,
    "reliability": "High|Medium|Low"
  }},

  "trends": [
    {{
      "column": "EXACT_EXISTING_COLUMN_NAME",
      "direction": "increasing|decreasing|stable|insufficient_evidence",
      "growth_rate": null,
      "evidence": "Evidence from supplied dataset statistics"
    }}
  ],

  "data_quality": {{
    "missing_values": {{
      "EXACT_COLUMN_NAME": 0.0
    }},
    "outliers_detected": false,
    "data_completeness": 0.0,
    "recommendation": "Data-quality recommendation based only on supplied statistics"
  }},

  "insights": [
    "Data-supported business insight 1",
    "Data-supported business insight 2",
    "Data-supported business insight 3"
  ],

  "recommendations": [
    "Evidence-based recommendation 1",
    "Evidence-based recommendation 2",
    "Evidence-based recommendation 3"
  ],

  "filters": [
    {{
      "column": "EXACT_EXISTING_CATEGORICAL_COLUMN",
      "filter_type": "dropdown",
      "label": "Professional Display Name"
    }}
  ],

  "kpis": [
    {{
      "metric": "EXACT_EXISTING_NUMERIC_COLUMN",
      "aggregation": "sum",
      "label": "Professional KPI Label"
    }}
  ],

  "charts": [
    {{
      "chart_id": "chart-0",
      "type": "bar",
      "x": "EXACT_EXISTING_CATEGORICAL_COLUMN",
      "y": "EXACT_EXISTING_NUMERIC_COLUMN",
      "title": "Business-focused title",
      "size": "1/2"
    }}
  ],

  "layout_grid": "2-col",

  "narrative": "Data-grounded strategic summary explaining what the dashboard reveals and what users should investigate."
}}


=============================================================================
FINAL VALIDATION BEFORE RESPONSE
=============================================================================

Before returning the JSON, perform these checks internally:

CHECK 1:
Does every referenced column exist exactly in COLUMN PROFILES?

CHECK 2:
Does every KPI use an appropriate existing column?

CHECK 3:
Does every filter use an existing categorical column?

CHECK 4:
Does every line/area chart use a temporal x-axis?

CHECK 5:
Does every pie chart use a categorical dimension and numeric measure?

CHECK 6:
Does every scatter chart use numeric x and y?

CHECK 7:
Are high-missingness columns avoided for normal analysis?

CHECK 8:
Are high-cardinality identifier columns avoided as normal dimensions?

CHECK 9:
Are all quantitative findings supported by DATASET STATISTICS?

CHECK 10:
Have all unsupported trends, rankings, growth rates, and percentages been
removed or marked as insufficient evidence?

CHECK 11:
Have you avoided assuming the business domain?

CHECK 12:
Is the final response valid JSON only?

Return ONLY the JSON object.
"""


# =============================================================================
# BIG FOUR PROMPT
# =============================================================================

def build_big_four_prompt(
    col_summary: str,
    sample_str: str,
    n_rows: int,
    n_cols: int,
    n_kpis: int,
    n_filters: int,
    objective: str = ''
) -> str:
    """Build the Big Four analyst prompt, optionally scoped to a user objective."""

    objective = (objective or '').strip()[:500].strip()

    objective_section = ''

    if objective:
        objective_section = (
            f'USER OBJECTIVE: {objective}\n\n'
            f'Use this objective to prioritise chart types, KPI selection, '
            f'and the strategic narrative.\n'
            f'Focus recommendations on answering: "{objective}"\n\n'
        )

    return f"""{objective_section}
You are a Senior Data Analytics Partner at a leading analytics consulting
firm with extensive experience turning raw data into C-suite insights.

A client has shared a dataset and needs a rigorous, specific, and actionable
analysis.

=============================================================================
DATASET OVERVIEW
=============================================================================

- Rows: {n_rows:,}
- Columns: {n_cols}
- User has pre-selected {n_kpis} KPIs
- User has pre-selected {n_filters} filters


=============================================================================
COLUMN PROFILES
=============================================================================

{col_summary}


=============================================================================
SAMPLE DATA
=============================================================================

{sample_str}


=============================================================================
STRICT DATA-GROUNDING RULES
=============================================================================

1. Use only columns that exist in the supplied column profiles.

2. Never invent columns.

3. Never invent numerical findings.

4. Never invent percentages.

5. Never invent rankings.

6. Never invent growth rates.

7. Never claim a category dominates unless the available data supports it.

8. Never claim causation unless the data explicitly supports it.

9. If evidence is insufficient, say so.

10. High-cardinality identifiers should generally not be used as normal
    analytical dimensions.

11. Columns with high missingness should be treated as data-quality concerns.

12. Recommendations must adapt to the actual dataset.

13. Do not assume the business domain.


=============================================================================
ANALYSIS
=============================================================================

Provide:

1. EXECUTIVE FINDINGS

Generate 3-4 important findings based on the supplied data.

2. KPI RECOMMENDATIONS

Recommend 3-5 meaningful metrics.

For each:

- exact column name
- aggregation
- business label
- rationale

3. CHART RECOMMENDATIONS

Recommend 5-7 meaningful charts when supported by the data.

For each:

- chart type
- x-column
- y-column
- business title
- analytical rationale

Do not force charts that the dataset cannot support.

4. FILTER RECOMMENDATIONS

Recommend 2-3 meaningful categorical filters.

5. STRATEGIC NARRATIVE

Provide a concise data-grounded summary for leadership.


=============================================================================
CHART COMPATIBILITY
=============================================================================

- Bar: categorical/temporal x + numeric y
- Line: temporal x + numeric y
- Pie: categorical x + numeric y
- Scatter: numeric x + numeric y
- Histogram: numeric distribution
- Box: numeric measure, optional categorical grouping
- Heatmap: suitable numeric relationships or aggregated matrix
- Funnel: only for genuine sequential stages
- Treemap: only for meaningful hierarchical categories


=============================================================================
OUTPUT
=============================================================================

Return ONLY valid JSON.

No markdown.
No explanations.
No code fences.
No commentary.

{{
  "executive_summary": {{
    "key_findings": [
      "Data-supported finding 1",
      "Data-supported finding 2",
      "Data-supported finding 3"
    ],
    "narrative": "2-3 sentence data-grounded narrative.",
    "risk_flags": [
      "Evidence-based risk or data-quality issue"
    ],
    "priority_action": "Evidence-based priority for further investigation"
  }},

  "data_quality_score": 0.0,

  "kpis": [
    {{
      "column": "EXACT_EXISTING_COLUMN",
      "aggregation": "sum",
      "label": "Business Label",
      "rationale": "Why this metric matters based on the dataset"
    }}
  ],

  "charts": [
    {{
      "type": "bar",
      "x": "EXACT_EXISTING_COLUMN",
      "y": "EXACT_EXISTING_NUMERIC_COLUMN",
      "title": "Business Title",
      "rationale": "What this chart reveals"
    }}
  ],

  "filters": [
    {{
      "column": "EXACT_EXISTING_CATEGORICAL_COLUMN",
      "label": "Display Name",
      "rationale": "Why this segmentation is useful"
    }}
  ],

  "narrative": "2-3 sentence strategic summary based only on the supplied data."
}}"""









# """LLM prompt templates - Big Four consulting-grade prompts"""

# DATASET_ANALYSIS_PROMPT = """You are a McKinsey-level data analytics consultant. Analyze this dataset comprehensively and generate a professional dashboard configuration with executive insights.

# CONTEXT: {context}

# COLUMN PROFILES:
# {column_profiles}

# SAMPLE DATA (first 100 rows):
# {sample_data}


# =============================================================================
# CRITICAL SCHEMA VALIDATION RULES
# =============================================================================

# YOU MUST USE ONLY THE COLUMN NAMES PROVIDED IN COLUMN PROFILES.

# STRICT REQUIREMENTS:

# 1. NEVER invent columns.

# 2. Every filter.column must exactly match a column name from COLUMN PROFILES.

# 3. Every kpi.metric must exactly match a column name from COLUMN PROFILES.

# 4. Every chart.x and chart.y must exactly match a column name from COLUMN PROFILES.

# 5. Preserve exact spelling, spaces, punctuation and capitalization.

# 6. Before generating the final JSON, verify that every referenced column exists in COLUMN PROFILES.

# 7. If a suitable column does not exist, omit that KPI, filter or chart.

# 8. Do NOT create generic business fields such as:
#   - Revenue
#   - Total Revenue
#   - Sales
#   - Costs
#   - Profit
#   - Region
#   - Customer Segment
#   - Product Line
#   - CustomerCount
#   - Date
#   - Order Value

#    UNLESS those exact column names appear in COLUMN PROFILES.

# 9. The dashboard must adapt dynamically to any uploaded dataset.

# 10. The response will be rejected if it references any column that is not present in COLUMN PROFILES.

# EXAMPLE:

# If COLUMN PROFILES contains:

# - Invoice Amount
# - Invoice Date
# - Country

# VALID:

# {{
#   "metric": "Invoice Amount"
# }}

# {{
#   "x": "Invoice Date",
#   "y": "Invoice Amount"
# }}

# INVALID:

# {{
#   "metric": "Revenue"
# }}

# {{
#   "x": "Region",
#   "y": "Total Revenue"
# }}


# =============================================================================
# ANALYSIS INSTRUCTIONS - Big Four Standards
# =============================================================================

# You are designing an executive dashboard that tells a data story. Think like a management consultant:
# 1. What are the 3-4 most important findings? (executive summary)
# 2. What trends or patterns emerge? (time-series, growth, seasonality)
# 3. What data quality issues exist? (missing data, outliers, reliability)
# 4. What actionable insights can we extract? (business implications)
# 5. What drill-downs would executives want? (filters for deeper analysis)
# 6. What metrics matter most? (KPIs that drive decisions)

# DETAILED REQUIREMENTS:

# 1. **Executive Summary** (CRITICAL for Big Four style):
#    - Identify 3-4 key findings that a CEO would care about
#    - Be specific: "Revenue declined 12% YoY in Q3" not "Sales are down"
#    - Include data quality assessment (e.g., "95% data completeness")
#    - State the overall health of the dataset (Healthy/Caution/Alert)

# 2. **Filters** (Enable meaningful drill-downs):
#    - Select 2-3 categorical columns with cardinality 5-50
#    - Prioritize only columns that actually exist in COLUMN PROFILES.
#    - Choose the most useful categorical columns available in the dataset.
#    - These should be columns executives naturally ask: "What about if we filter by...?"
#    - Format label as readable: "Region", "Customer Segment", "Product Line"

# 3. **KPIs** (Key business metrics):
#    - Select only numeric columns that exist in COLUMN PROFILES.
#    - The metric field must exactly match an existing column name.
#    - Recommend AGGREGATION STRATEGY:
#      * sum: Total revenue, total volume, total cost
#      * mean: Average transaction, average rating
#      * count: Number of records, customers, transactions
#      * max: Peak value, highest transaction
#    - Label should be business-friendly: "$Total Revenue" not "sum_of_amount"
#    - Prioritize metrics that answer: "Are we healthy? Growing? Profitable?"

# 4. **Charts** (Tell the data story - 5-8 charts):
#    - Start with the "so what?" - what insight do you want to convey?
#    - Recommend diverse chart types based on data semantics:
#      * TIME SERIES: Use 'line' or 'area' (shows trends, seasonality)
#      * COMPOSITION: Use 'stacked-bar', 'pie' (shows part-to-whole)
#      * DISTRIBUTION: Use 'box', 'violin', 'histogram' (shows spread, outliers)
#      * COMPARISON: Use 'bar' (top 10, side-by-side comparison)
#      * HIERARCHY: Use 'sunburst', 'treemap' (drill-down structure)
#      * CORRELATION: Use 'scatter', 'heatmap' (relationships)
#      * TRENDS: Use 'cumulative-line' (running totals, growth)
#      * PERFORMANCE: Use 'waterfall' (profit drivers), 'funnel' (conversion)
#    - Advanced types for impactful presentations:
#      * 'waterfall': Perfect for profit/cost breakdowns
#      * 'funnel': Ideal for pipeline/conversion analysis
#      * 'sunburst': Best for hierarchical drill-down
#      * 'treemap': Great for portfolio/market share analysis
#      * 'bubble': Shows 3 dimensions simultaneously
#      * 'gauge': Perfect for target progress metrics
#    - Each chart needs a BUSINESS-FOCUSED title:
#      ✓ "Top 5 Revenue Sources by Region"
#      ✗ "Bar Chart - Amount by Category"
#    - Layout: Use 'full' for key insight, '1/2' for 2-per-row, '1/3' for 3-per-row

# 5. **Business Narrative** (Why this dashboard design?):
#    - Explain the story: "This dashboard reveals X, highlights Y, enables Z"
#    - Connect to business impact: "Allows quick identification of underperforming regions"
#    - Format numbers professionally: "$2.4M" not "$2400000"

# 6. **Data Quality Assessment**:
#    - Report missing data % by column
#    - Flag any outliers or data quality concerns
#    - Assess overall reliability: High/Medium/Low
#    - Recommend caution areas (e.g., "2023 data incomplete")

# FORMATTING REQUIREMENTS:

# - Numbers: Use abbreviated scale ($2.4M, 45.2%, 1.2K)
# - Dates: Use "YYYY-MM-DD" format in descriptions
# - Labels: PascalCase for readable titles ("Total Revenue", not "total_revenue")
# - Return ONLY valid JSON with no markdown, no explanations, no code blocks, no wrapping text

# =============================================================================
# EXPECTED JSON OUTPUT FORMAT
# =============================================================================

# {{
#   "executive_summary": {{
#     "key_findings": [
#       "Key insight 1 (be specific with metrics)",
#       "Key insight 2 (quantified impact)",
#       "Key insight 3 (business implication)"
#     ],
#     "data_quality_score": 0.92,
#     "overall_health": "Healthy",
#     "missing_data_pct": 2.1,
#     "reliability": "High"
#   }},
#   "trends": [
#     {{"column": "existing_numeric_column", "direction": "increasing", "growth_rate": 0.12}},
#     {{"column": "another_existing_numeric_column", "direction": "stable", "growth_rate": 0.0}}
#   ],
#   "data_quality": {{
#     "missing_values": {{"Column1": 0.5, "Column2": 1.2}},
#     "outliers_detected": false,
#     "data_completeness": 0.98,
#     "recommendation": "Data quality is high; proceed with confidence"
#   }},
#   "insights": [
#     "Business insight 1 that explains what the data means",
#     "Business insight 2 with actionable implications"
#   ],
#   "recommendations": [
#     "Recommended action or focus area 1",
#     "Recommended action or focus area 2"
#   ],
#   "filters": [
#     {{"column": "col_name", "filter_type": "dropdown", "label": "Display Name"}}
#   ],
#   "kpis": [
#     {{"metric": "col_name", "aggregation": "sum|mean|count|max", "label": "Professional Label"}}
#   ],
#   "charts": [
#     {{
#       "chart_id": "chart-0",
#       "type": "bar|line|waterfall|funnel|sunburst|treemap|violin|bubble|gauge|gantt|sankey|2d-bar|cumulative-line|stacked-bar|pie|scatter|box|histogram",
#       "x": "x_column",
#       "y": "y_column",
#       "title": "Business-focused title explaining the insight",
#       "size": "1/3|1/2|full"
#     }}
#   ],
#   "layout_grid": "2-col|3-col",
#   "narrative": "Executive summary of why this dashboard design tells the data story"
# }}

# CRITICAL:
# Return ONLY valid JSON.
# Do not explain your answer.
# Do not add markdown.
# Do not add code fences.
# Do not add introductory text.
# Do not add commentary.
# The first character of the response must be {{
# The last character of the response must be}}
# """


# def build_big_four_prompt(col_summary: str, sample_str: str, n_rows: int,
#                            n_cols: int, n_kpis: int, n_filters: int,
#                            objective: str = '') -> str:
#     """Build the Big Four analyst prompt, optionally scoped to a user objective."""
#     objective = (objective or '').strip()[:500].strip()

#     objective_section = ''
#     if objective:
#         objective_section = (
#             f'USER OBJECTIVE: {objective}\n\n'
#             f'Use this objective to prioritise chart types, KPI selection, and the strategic narrative.\n'
#             f'Focus your recommendations on answering: "{objective}"\n\n'
#         )

#     return f"""{objective_section}You are a Senior Data Analytics Partner at McKinsey & Company with 15 years of experience turning raw data into C-suite insights. A client has just shared their dataset and needs your expert analysis.

# DATASET OVERVIEW:
# - Rows: {n_rows:,}  |  Columns: {n_cols}
# - User has pre-selected {n_kpis} KPIs and {n_filters} filters

# COLUMN PROFILES (name [type] cardinality missing% top_values):
# {col_summary}

# SAMPLE DATA (5 rows):
# {sample_str}

# INSTRUCTIONS:
# As a Big Four senior analyst, provide a rigorous, specific, and actionable diagnostic. Do NOT be generic.

# 1. EXECUTIVE FINDINGS (3-4 bullet points)
#    - Start each with a quantified statement: "X% of...", "Top 3... account for Y%", "Critical gap in..."
#    - Flag any data quality red flags (high cardinality IDs, high missing%, sparse columns)
#    - State what business question each column can answer

# 2. KPI RECOMMENDATIONS (3-5 metrics)
#    - For each: column name, aggregation (sum/mean/count/max), business label, and WHY it matters
#    - Focus on metrics that drive operational or financial decisions

# 3. CHART RECOMMENDATIONS (5-7 charts)
#    - For each chart: type, x-column, y-column, business title, and 1-line analytical rationale
#    - Prioritise: distribution analysis (bar/pie), trend decomposition (line if temporal),
#      concentration analysis (treemap/funnel), outlier detection (box plot),
#      cross-dimensional analysis (heatmap if multiple numerics)
#    - Be specific about which columns to use and what insight the chart reveals

# 4. FILTER RECOMMENDATIONS (2-3 filters)
#    - Identify the 2-3 categorical columns that segment the data most meaningfully for drill-down

# 5. STRATEGIC NARRATIVE (2-3 sentences)
#    - What story does this data tell? What should leadership focus on first?

# Return ONLY valid JSON - no markdown, no explanation text:

# {{
#   "executive_summary": {{
#     "key_findings": [
#       "Quantified finding 1 — e.g. Top 3 categories account for 78% of total volume",
#       "Quantified finding 2 — e.g. 23% of records show incomplete data in 4 key fields",
#       "Quantified finding 3 — e.g. Revenue concentration risk: single vendor drives 45% of spend"
#     ],
#     "narrative": "2-3 sentence Big Four analyst narrative. What does this data tell leadership? What should they focus on first? Frame it as a Senior Partner presenting to the C-suite.",
#     "risk_flags": ["Risk or data quality issue 1", "Risk or data quality issue 2"],
#     "priority_action": "Single most important action leadership should take based on this data"
#   }},
#   "data_quality_score": 0.0,
#   "kpis": [
#     {{"column": "col", "aggregation": "sum", "label": "Business Label", "rationale": "why it matters"}}
#   ],
#   "charts": [
#     {{"type": "bar|pie|line|histogram|box|heatmap|funnel|treemap|scatter", "x": "col", "y": "col", "title": "Business Title", "rationale": "what insight this reveals"}}
#   ],
#   "filters": [
#     {{"column": "col", "label": "Display Name", "rationale": "segmentation value"}}
#   ],
#   "narrative": "2-3 sentence strategic summary for leadership"
# }}"""
