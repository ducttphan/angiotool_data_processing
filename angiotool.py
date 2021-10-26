import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from pandas.core.reshape.concat import concat 
import streamlit as st 
import os


datalist = []
angiotool_header = ['Image_Name', 'Date', 'Time', 'File_Location', 'Low_Threshold', 'High_Threshold', 
    'Vessel_Thickness', 'Small_Particles', 'Fill_Holes', 'Scaling_Factor', 'NA', 'Explant_Area', 
    'Vessels_Area', 'Vessels_Percentage_Area', 'Total_Branchpoints', 'Junctions_Density', 'Total_Vessels_Length', 
    'Average_Vessels_Length', 'Total_Endpoints', 'Average_Lacunarity']

keylist_header = ['Group', 'File_Location', 'Image_Name']

st.header('Processing AngioTool Output File')
st.markdown("""**Instructions:**  
    1. Upload AngioTool combined_report.xls file.  
    2. Upload a keylist .csv file that can be used to sort data by group.  
    3. Information from the keylist (e.g., Group, File_Location) will be appended 
    to the raw dataframe for sorting purpose.       
    """)

uploaded_angiotool_file = st.file_uploader("Upload your Angiotool .xls report file:")
uploaded_xls = pd.read_excel(uploaded_angiotool_file, header= 3, names= angiotool_header) 

uploaded_keylist_file = st.file_uploader("Upload your keylist .csv file to sort data by group:")
uploaded_keylist_csv = pd.read_csv(uploaded_keylist_file, header= 0, names= keylist_header)

image_name = pd.DataFrame(uploaded_xls['Image_Name'])
vessels_area = pd.DataFrame(uploaded_xls['Vessels_Area'])
vessels_length = pd.DataFrame(uploaded_xls['Total_Vessels_Length'])
branchpoints = pd.DataFrame(uploaded_xls['Total_Branchpoints'])
lacunarity = pd.DataFrame(uploaded_xls['Average_Lacunarity'])
angiotool_df = pd.concat([image_name, vessels_area, vessels_length, branchpoints, lacunarity], axis= 1)
df = pd.merge(uploaded_keylist_csv, angiotool_df, on= ['Image_Name'])

st.write("""### _Raw Data_  """)
st.write(df)
st.write('___')

st.header('Sorting Data')
st.markdown("""**Instructions:**  
    1. Type in name of group to extract data.  
    2. Vessel morphometry data in pixel units (vessel area, total vessel length, number of branchpoints, lacunarity) 
    belong to this group will be sorted and tabulated into a new dataframe.  
    3. Statistical summary (Mean, SD, SEM, N) will be generated based on the tabulated dataframe.  
    4. Type in directory path to save .csv files. (e.g. _/Users/a/Desktop/data/_).       
    """)
group_name = st.text_input('Name of group to extract data:')
group_rawdata = df[df["Group"] == group_name]
n_row = len(group_rawdata.index)

mean_vessels_area = group_rawdata['Vessels_Area'].mean()
std_vessels_area = group_rawdata['Vessels_Area'].std()
sem_vessels_area = group_rawdata['Vessels_Area'].sem()
group_vessels_area_summary = pd.Series([mean_vessels_area, std_vessels_area, sem_vessels_area, n_row], 
    index= ['Mean', 'SD', 'SEM', 'N'], name= 'Vessels_Area')

mean_vessels_length = group_rawdata['Total_Vessels_Length'].mean()
std_vessels_length = group_rawdata['Total_Vessels_Length'].std()
sem_vessels_length = group_rawdata['Total_Vessels_Length'].sem()
group_vessels_length_summary = pd.Series([mean_vessels_length, std_vessels_length, sem_vessels_length, n_row], 
    index= ['Mean', 'SD', 'SEM', 'N'], name= 'Vessels_Length')

mean_branchpoints = group_rawdata['Total_Branchpoints'].mean()
std_branchpoints = group_rawdata['Total_Branchpoints'].std()
sem_branchpoints = group_rawdata['Total_Branchpoints'].sem()
group_branchpoints_summary = pd.Series([mean_branchpoints, std_branchpoints, sem_branchpoints, n_row], 
    index= ['Mean', 'SD', 'SEM', 'N'], name= 'Vessel_Branchpoints')

mean_lacunarity = group_rawdata['Average_Lacunarity'].mean()
std_lacunarity = group_rawdata['Average_Lacunarity'].std()
sem_lacunarity = group_rawdata['Average_Lacunarity'].sem()
group_lacunarity_summary = pd.Series([mean_lacunarity, std_lacunarity, sem_lacunarity, n_row], 
    index= ['Mean', 'SD', 'SEM', 'N'], name= 'Average_Lacunarity')

group_summary = pd.concat([group_vessels_area_summary, group_vessels_length_summary, 
    group_branchpoints_summary, group_lacunarity_summary], axis= 1)

st.write("""### _Tabulated Data_  """)
st.write(group_rawdata)
st.write("""### _Data Summary_  """)
st.write(group_summary)

with st.form('save_csv_files') :
    save_dir = st.text_input('Type directory to save tabulated dataframe and summary .csv files:')
    group_df_csv = os.path.join(save_dir, group_name + '_tabulated_dataframe.csv')
    group_summary_csv = os.path.join(save_dir, group_name + '_data_summary.csv')
    saved = st.form_submit_button('Save')
    if saved:
        group_rawdata.to_csv(group_df_csv)
        group_summary.to_csv(group_summary_csv)
        st.write('_Files saved_')