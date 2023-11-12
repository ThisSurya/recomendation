import streamlit as st
import pandas as pd
import Backend.Apriori as Apr
import Backend.Order as Order

def Recomendation():
    data = Apr.Import_data()

    kode_customer = data['CUSTOMERID'].unique()
    kode_customer = kode_customer.astype(int)

    option = st.selectbox(
        'Pelanggan: ',
        (kode_customer)
    )

    timeframe = st.selectbox(
        'TimeFrame: ',
        (3, 6, 9, 12)
    )

    st.write(f'Nama Customer: {option}')
    data_apriori = Apr.Choose_Customer(data, option)
    data_apriori = Apr.Time_Frame(data_apriori, timeframe)

    data_apriori = Apr.Row2Column(data_apriori)
    frequent, result = Apr.Modelling(data_apriori)

    st.write('Data Sudah dianalisis berikut adalah hasil nya:  ')
    st.write(frequent.head())
    st.write(result.head())

    
    best_seller = Order.BestSeller(frequent)
    st.write(f'## Produk yang sering dibeli: ', best_seller[0])
    key_class = Order.ClassProduct(data, best_seller[0])
    recomendation_best = Order.Recomendation_Best(data, key_class)
    st.write('Rekomendasi produk yang serupa (1 kelas) ', recomendation_best)
    
    product = Order.PickProduct(frequent)
    product_select = st.selectbox('Produk: ', (product))
    recomendation = Order.Recomendation(result, product_select)
    recomendation = pd.DataFrame(recomendation)
    if recomendation.empty:
        st.write('Belum memiliki rekomendasi, buat customer untuk membeli lebih banyak! ')
    else:
        st.write(f'Jangan lupa tawarkan produk ini jika customer membeli {product_select}')
        list2Column(recomendation)

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


st.write('## Kebutuhan Konsumen')
Recomendation()