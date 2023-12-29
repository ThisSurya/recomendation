import streamlit as st
import pandas as pd
import Backend.Apriori as Apr
import Backend.Order as Order
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
st.set_option('deprecation.showPyplotGlobalUse', False)
def Recomendation():
    col1, col2, col3 = st.tabs(["Preprocessing", "Describe","Model"])
    
    upload_file = st.file_uploader("Upload CSV", type={"csv"})
    
    if upload_file is not None:
        with col1:
            upload_file = pd.read_csv(upload_file)
            upload_file['PESAN'] = upload_file['PESAN'].abs()
            data_raw = Apr.Import_data(upload_file)
            kode_city = data_raw['KOTA'].unique()
            kode_city = kode_city.astype(str)

            option = st.selectbox(
                'Pilih daerah yang tersebar: ',
                (kode_city)
            )

            support = st.slider(
                'Pilih nominal nilai support mu: ',
                0.05, 0.95, 0.3, 0.05
            )

            st.write(f'Daerah yang ingin kamu analisa: {option}')
            data_cook = Apr.Choose_City(data_raw, option)

            date_awal = st.date_input(
                'Pilih tanggal awal yang ingin kamu analisa: ',
                format="MM/DD/YYYY",
                min_value = data_cook['TGL'][0],
                max_value = data_cook['TGL'][len(data_cook)-1],
                value = data_cook['TGL'][0],
            )
            date_akhir = st.date_input(
                'pilih tanggal akhir yang ingin dianalisa: ',
                min_value= date_awal,
                format="MM/DD/YYYY",
                max_value = data_cook['TGL'][len(data_cook)-1],
                value = data_cook['TGL'][len(data_cook)-1],
            )
    
        with col2:
            st.write("# Visual data")
            upload_file = upload_file.loc[upload_file['KOTA'] == option]
            st.write(upload_file['PESAN'].describe())

            product = upload_file['PRODUK GROUP'].unique()
            product = pd.DataFrame(product, columns=['PRODUK GROUP'])
            total_penjual_per_produk = upload_file.groupby('PRODUK GROUP')['PESAN'].sum().reset_index()
            
            total_penjual_per_produk = pd.concat([product, total_penjual_per_produk])
            total_penjual_per_produk = total_penjual_per_produk.sort_values(by='PESAN', ascending=False)
            total_penjual_per_produk = total_penjual_per_produk.head(8)

            fig = make_subplots(
                rows=1, cols=2,
                specs=[[{'type': 'bar'}, {'type': 'domain'}]]
            )
            fig.add_trace(go.Bar(y=total_penjual_per_produk['PESAN'], x=total_penjual_per_produk['PRODUK GROUP']), row=1, col=1)
            fig.add_trace(go.Pie(values=total_penjual_per_produk['PESAN'], labels=total_penjual_per_produk['PRODUK GROUP']), row=1, col=2)
            
            st.plotly_chart(fig)

        with col3:
            data_cook = Apr.Time_Frame(data_cook, date_awal, date_akhir)
            data_apriori = Apr.Row2Column(data_cook)
            frequent, result = Apr.Modelling(data_apriori, support)
            st.write('Data Sudah dianalisis berikut adalah hasil nya:  ')

            if len(frequent) >= 1 :
                list_itemsets = Apr.Frozen2List(frequent)

                frequent2 = {'itemsets': list_itemsets, 'support': frequent['support']}
                frequent2 = pd.DataFrame(frequent2)
                st.bar_chart(frequent2, x='itemsets', y='support')
                st.write(frequent2.head())

                frequent2 = Apr.RemoveFrozenset_Frequent(frequent)
                frequent2 = frequent2['itemsets'].drop_duplicates()
            
            filter = st.slider(
                'Pilih nominal nilai support mu: ',
                0.05, 0.98, 0.5, 0.01
            )
            filtered_result = result[result['support'] > filter]
            display_result = Apr.RemoveFronzenset_Assoc(filtered_result)
            st.write("Rules: ")
            st.write(display_result)
            recomendation = display_result.head(4)
            st.write("Rekomendasi dari algoritma: ")
            
            for x in recomendation.index:
                antecedent = recomendation['antecedents'][x]
                consequent = recomendation['consequents'][x]

                st.write(f"{x+1}. produk {consequent} bisa direkomendasikan dengan produk {antecedent}")

            st.write("## Pencarian manual")
            option_antecedent = st.selectbox(
                'antecedent',
                frequent2,
                index=0
            )
            option_consequent = st.selectbox(
                'consequent',
                frequent2,
                index=1
            )

            decision = Order.Decision(filtered_result, option_antecedent, option_consequent)
            another_recomendation = False
            try:
                if(decision['support'][0] >= 0.7 or decision['confidence'][0] >= 0.7):
                    st.write(f"{decision['antecedents'][0]} dan produk {decision['consequents'][0]} memiliki korelasi yang bagus")
                elif((decision['support'][0] >= 0.4 and decision['support'][0] < 0.7) or (decision['confidence'][0] >= 0.4 and decision['confidence'][0] < 0.7)):
                    st.write(f"{decision['antecedents'][0]} dan produk {decision['consequents'][0]} memiliki korelasi yang cukup")
                elif((decision['support'][0] < 0.4) or (decision['confidence'][0] < 0.4)):
                    another_recomendation = True
                    st.write(f"{decision['antecedents'][0]} dan produk {decision['consequents'][0]} memiliki korelasi yang kurang")
                
                
            except:
                st.write(
                        """
                        Maaf tidak ada korelasi! kamu bisa mengurangi nilai support, supaya hasil korelasi terlihat,
                        jika tetap tak terlihat brarti model kami belum memiliki data yang kamu punya!
                        silahkan chat admin jika ingin menambahkan data
                        """
                )
            if another_recomendation :
                st.write("Berikut adalah rekomendasi produk lainnya: ")
                recomendation = Order.Recomendation(display_result, option_antecedent)
                for index, x in enumerate(recomendation):
                    st.write(f"{index+1}. {x}")
    else:
        st.write("Harap upload file terlebih dahulu untuk melanjutkan!")  

def list2Column(result_model):
    st.data_editor(
    result_model,
    column_config={
        "sales": st.column_config.ListColumn(
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            width="medium",
        ),
    },
    hide_index=True,
)


st.write('## Analysis')
Recomendation()