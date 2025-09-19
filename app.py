#!/usr/bin/env python
# coding: utf-8

# Import libraries/packages

# In[1]:


import pandas as pd
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc


# Create tables

# In[2]:


def no_geometry():
    df_drug_mort_mapped = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/drug_mortality/refs/heads/main/drug_mort_mapped.csv')
    df_drug_mort_mapped = df_drug_mort_mapped.set_index('HBCode')
    df_hb_table = df_drug_mort_mapped.drop('geometry', axis=1)
    return df_hb_table

df_hb_table = no_geometry()
df_numeric_columns = df_hb_table.select_dtypes('number')


# Create app layout

# In[3]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
app.layout = dbc.Container([
    html.H1("Drug Related Mortality in Scotland by Regional Health Board 2024/25", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays open source drug mortality related data from the National Records of Scotland (NRS) for each of the Scottish Health Board Regions. Click on or hover over your Health Board for an insight into the factors affecting drug mortality in your area:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
    dbc.Row([dbc.Col(html.Iframe(id='my_output', height=600, width=1000, srcDoc=open('drugmortmap.html', 'r').read()))], style={'text-align':'center'}),
    html.Figcaption("Figure 1: Map of the latest drug mortality open data for the Scottish Health Board Regions", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    html.H4("Potential Data Relationships", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("The LDP drug standard in Scotland is a target requiring that 90% of people referred for drug or alcohol treatment start it within three weeks of their referral. This standard aims to ensure fast access to recovery-focused specialist treatment for problematic drug and alcohol use", className='mb-2'),
    html.Summary("People with addiction often have one or more associated health issues or drug related disorders. This could include increased risk of lung or heart disease, stroke, cancer, or mental health conditions", className='mb-2'),
    html.Summary("Opiates or opioids are drugs used to treat pain. They are very addictive and can be misused illegally. Opiates are derived from plants and opioids are synthetic drugs that have the same actions as opiates", className='mb-2'),
    html.Summary("Benzodiazepines are a type of sedative medication. This means they slow down the body and brain's functions. They can be used to help with anxiety and insomnia (difficult getting to sleep or staying asleep). They are also highly addictive", className='mb-2'),
    html.Summary("Gabapentinoids are a class of highly addictive medications, such as gabapentin and pregabalin, primarily used to treat neuropathic pain (nerve pain) from conditions like shingles or diabetes, and also used for epilepsy and anxiety", className='mb-2'),
    html.Summary("Cocaine is a powerfully addictive and dangerous stimulant drug made from the leaves of the coca plant. As a central nervous system stimulant, it produces an intense, short-lived euphoric rush by flooding the brain's reward system with dopamine. Cocaine is illegal in most countries and carries severe risks for both physical and mental health", className='mb-2'),
    html.Summary("Ecstasy is a stimulant drug that may increase feelings of empathy as it is a hallucinogen. It is a designer drug and is both illegal and addictive in nature", className='mb-2'),
    html.Summary("Amphetamines are central nervous system stimulants that are used in the treatment of attention deficit hyperactivity disorder, narcolepsy, and obesity. They should not be taken without a prescription and they are highly addictive", className='mb-2'),
    html.Summary("When combined, ketamine and xylazine are used in veterinary medicine for sedation and anesthesia, but their illicit use as a 'tranq dope' has led to dangerous health consequences in humans", className='mb-2'),
    html.Summary("Alcohol addiction is a chronic relapsing disorder associated with compulsive alcohol drinking, the loss of control over intake, and the emergence of a negative emotional state when alcohol is no longer available", className='mb-2'),
    html.Summary("Polydrug use is the use of more than one drug at a time. Polydrug use increases the risk of drug harms and death. This includes mixing alcohol with other drugs", className='mb-2'),
    html.Summary("Drug use is far more common among younger people, however the median age of those who are taking drugs is increasing", className='mb-2'),
    html.Summary("Poverty and inequality are consistently highlighted as primary drivers of problematic drug use and related deaths in Scotland. People in the most deprived areas are significantly more likely to die from drug misuse compared to those in the least deprived areas", className='mb-2'),
    html.Figcaption("Table 1: Latest open drug mortality related data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark grey", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_hb_table.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_hb_table.columns],
    style_cell={'textAlign': 'center'},
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_data_conditional=
    [
            {
                'if': {
                    'filter_query': '{{{}}} > {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#808080',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.1).items()
        ] +       
        [
            {
                'if': {
                    'filter_query': '{{{}}} <= {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#C0C0C0',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.5).items()
        ]
    ))
    ]),
    html.H4("Open Data References", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.nrscotland.gov.uk/publications/drug-related-deaths-in-scotland-2024/")),
    html.Summary("Public Health Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/drug-related-hospital-statistics-scotland")),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/drug-and-alcohol-treatment-waiting-times")),
    html.Summary("Scotland's Census 2022 - National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml")),
    html.Summary("Scottish Surveys Core Questions 2023 - Scottish Government", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2023/documents/")),
    ])


# Run app

# In[4]:


if __name__ == "__main__":
    app.run()

