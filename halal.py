import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import re
import string
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

@st.cache
def get_data():
    return pd.read_csv("data.csv" ,sep='\t')

def split_query(q):
	qlist=q.lower().split()
	qlist="|".join(qlist)
	return qlist
	
def jaccard_similarity(list1, list2):
	s1 = set(list1)
	s2 = set(list2)
	return float(len(s1.intersection(s2)) / len(s1.union(s2)))

datahalal=get_data()


def get_response(q):
	query=split_query(q)
	mask = datahalal[datahalal['produk'].str.contains(query) | datahalal['perusahaan'].str.contains(query,case=False)]
	mask=mask.reset_index()
	similarity=np.zeros((len(mask)))
	numsort=mask.size
	if (numsort > 20):
		numsort=20
	for ind in mask.index:
		line=mask['produk'][ind]+' '+mask['perusahaan'][ind]
		if (type(line)==str):
			qlist=q.lower().split()
			linelist=line.lower().split()
			similarity[ind]=jaccard_similarity(qlist,linelist)
	idx=(-similarity).argsort()[:numsort]
	data = []
	for y in idx:
    		data.append([mask['produk'][y], mask['perusahaan'][y], mask['sertifikat'][y],mask['tanggal'][y]])
	
	return(data)
    	
st.title("Assalamu 'alaikum di Open Data Halal :)")

cari = st.text_input("Cari Produk/Restaurant Halal", "rawon surabaya")
cariflag=False  
mydata =[]
if(st.button('Submit')):
	result = cari.title()
	if(result):
		st.write("Hasil Pencarian "+result)
		mydata=get_response(result)
		hasil = pd.DataFrame(mydata, columns=['produk', 'perusahaan','sertifikat','tanggal'])
		st.table(hasil)
		cariflag=True
	else:
		st.error("Masukkan input ya")

st.title("Fun Facts about Produk Halal di Indonesia")


st.header("WordCloud Nama Produk tersertifikasi Halal di LPPOM MUI")
st.image("produk.png", width=None)

st.header("Nama Perusahaan tersertifikasi Halal di LPPOM MUI")
values = st.slider("Jumlah Perusahaan", 5, 20, step=5)
st.table(datahalal.groupby(["perusahaan"]).count().sort_values("produk",ascending=False).head(values))

st.header("UMKM Binaan Pusat Kajian Halal ITS")
st.markdown("Kunjungi binaan halal ITS [disini](http://halal.its.ac.id/binaan) ")

st.header("Linked Open Data Halal")
st.markdown("Kunjungi Linked Open Data Halal ITS [disini](http://halal.addi.is.its.ac.id) ")

st.markdown("---")
st.markdown("**Awards**")
st.markdown("- [Best Graphistry app at Tigergraph Hackathon 2021](https://devpost.com/software/halal-food)")
st.markdown("- [Neo4J Graphie Award Winner 2020](https://neo4j.com/graphies/#panel1)")
st.markdown("- Best Paper at International Conference on Halal Innovation in Products and Services 2018")

st.header("Dipersembahkan oleh")
st.image("logo.png")

