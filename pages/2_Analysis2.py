import streamlit as st
from Backend import Apriori2 as Apr
from Backend import Rules2 as Rule

def main():
    data_raw = Apr.Import_data()
    data_cooked = Apr.Preprocessing1(data_raw)

    kode_class = data_cooked['KELASPRODUK'].unique()
    
    option_class = st.selectbox(
        'pilih produk: ',
        (kode_class)
    )

    data_apriori_1 = Apr.Class_Product(data_cooked, option_class)
    st.write(data_apriori_1.head())
    data_apriori_1= Apr.Row2Column(data_apriori_1, 'KOTA')

    st.write('Hasil Analisa: ')
    frequent = Apr.AprioriModel(data_apriori_1)

    st.write(frequent.head(len(frequent)))

    st.write('Dari hasil olahan tersebut daerah yang paling memiliki potensi: ')
    filtered_frequent = Apr.Recomendation_Place(frequent)
    filtered_frequent = Apr.Frozen2List(filtered_frequent)
    filtered_frequent = Apr.Flat1Dimesion(filtered_frequent)
    i = 0
    for x in filtered_frequent:
        i+=1
        st.write(f'{i}. {x}')

    st.write('Analisa lbih lanjut tentang daerah')
    option_city = st.selectbox(
        'Pilih daerah sesuai hasil analisa: ',
        (filtered_frequent)
    )
    data_apriori_2 = Apr.Preprocessing2(data_raw)
    data_apriori_2 = Apr.City_Filter(data_apriori_2, option_city)
    data_apriori_2 = Apr.Row2Column(data_apriori_2, 'KELASPRODUK')
    frequent2 = Apr.AprioriModel(data_apriori_2)

    rules = Rule.Rules(frequent2)
    result = Rule.Combination(rules, option_class)
    # rules = Apr.Recomendation_Place(frequent2)
    st.write('Hasil analisa rules: ')
    st.write(result)
    st.write(rules.head(len(rules.head())))

main()