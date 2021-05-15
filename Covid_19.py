  
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
#package
def prepare_df(df_name):
	df=pd.read_csv(df_name)
	df=df.T
	Dict=dict(df.loc['StateOrUT'])
	df=df.rename(columns = Dict)

	l=[]
	for i in range(1,27):
  		if i<10:
  			l.append("0"+str(i)+"-Feb")
  		else:
  			l.append(str(i)+"-Feb")

	df.drop(['StateOrUT','30-Jan','31-Jan'],axis=0,inplace=True)
	df.drop(l,axis=0,inplace=True)
	df.drop(['Cases being reassigned to states','Total#'],axis=1,inplace=True)

	if df_name=='Deaths.csv':
		df.loc['24-May','Puducherry']=0

	df=df.astype("int64")
	return df

def all(df_t,df_r,df_d):
	total_cases = df_t.sum(axis=1)
	total_recover = df_r.sum(axis=1)
	total_deaths = df_d.sum(axis=1)
	new={ 'Cases' : total_cases, 'Recovered' : total_recover, 'Deaths' : total_deaths}
	df_all=pd.DataFrame(new)
	return df_all

def stream_lit(df_all,df_t,df_r,df_d):

	st.title("COVID-19 DATA ANALYSIS TILL 20-JUNE")
	month = st.selectbox('Select the Month',('Jun', 'Apr', 'Mar'))
	if  month=='Jun':
		date = st.slider('Select the Date', 1, 20,20)
	elif month=='Mar':
		date = st.slider('Select the Date', 1,31,31)
	else:
		date = st.slider('Select the Date', 1,30,30)
	if date<10:
		dat='0'+str(date)+'-'+month
	else:
		dat=str(date)+'-'+month
	st.write("You selected:",dat)

	st.header("CASES : "+str(df_all.loc[dat,'Cases']))
	st.header("RECOVERED : "+str(df_all.loc[dat,'Recovered']))
	st.header("DEATHS : "+str(df_all.loc[dat,'Deaths']))

	st.subheader("Pie Chart of Cases, Recovered and Deaths according to date :")
	fig= px.pie(names=df_all.columns,values=df_all.loc[dat])
	st.plotly_chart(fig)
	st.subheader("Bar Chart of Cases, Recovered and Deaths according to date :")
	fig = px.bar(x=df_all.columns,y=df_all.loc[dat],color=df_all.columns, labels={
                     "y": "People",
                     "x": "Cases",
                     "color" : "DataFrame"})
	st.plotly_chart(fig)

	st.subheader('Comparsion between Total Cases, Recovered Cases and Deaths')
	fig = px.line(df_all,labels={
                     "value": "People",
                     "index": "Date",
                     "variable" : "DataFrame"})
	st.plotly_chart(fig)

	st.subheader('Comparsion between States or Union Territories according to DataFrame')
	data_f = st.selectbox('Select the DataFrame',('Total', 'Recovered', 'Deaths'))
	options = st.multiselect('Select States or Union Territories',list(df_r.columns),['Rajasthan', 'Punjab'])
	if data_f=='Total':
		fig = px.line(df_t[options],labels={
                     "value": "People",
                     "index": "Date",
                     "variable" : "States or Union Territories"})
	elif data_f=='Recovered':
		fig = px.line(df_r[options],labels={
                     "value": "People",
                     "index": "Date",
                     "variable" : "States or Union Territories"})
	else:
		fig = px.line(df_d[options],labels={
                     "value": "People",
                     "index": "Date",
                     "variable" : "States or Union Territories"})
	st.plotly_chart(fig)

	st.subheader('Bar-Chart-Race')
	data_r = st.selectbox('Select the DataFrame :',('Total', 'Recovered', 'Deaths'))
	if data_r=='Total':
		video_file = open('total.mp4', 'rb')
		video_bytes = video_file.read()
		st.video(video_bytes)
	elif data_r=='Recovered':
		video_file = open('recover.mp4', 'rb')
		video_bytes = video_file.read()
		st.video(video_bytes)
	else:
		video_file = open('death.mp4', 'rb')
		video_bytes = video_file.read()
		st.video(video_bytes)
	





df_r=prepare_df('Recovered.csv')
df_d=prepare_df('Deaths.csv')
df_t=prepare_df('Total.csv')
df_all=all(df_t,df_r,df_d)

stream_lit(df_all,df_t,df_r,df_d)
