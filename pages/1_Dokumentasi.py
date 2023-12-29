import streamlit as st
from PIL import Image

def Documentation():

    documentation_2 = Image.open('Images/Doc_2.PNG')
    documentation_3 = Image.open('Images/Tampilan_awal_analysis.PNG')
    documentation_4 = Image.open('Images/Doc_4.PNG')
    documentation_5 = Image.open('Images/Doc_5.PNG')
    documentation_6 = Image.open('Images/Doc_6.PNG')
    documentation_7 = Image.open('Images/Doc_7.PNG')
    documentation_8 = Image.open('Images/Doc_8.PNG')
    documentation_9 = Image.open('Images/Doc_9.PNG')
    documentation_10 = Image.open('Images/Doc_10.PNG')
    documentation_11 = Image.open('Images/Doc_11.PNG')


    pass
    st.write('# Terimakasih!')
    st.write(
        """
            Ini aplikasi apa sih?
            Kami memberikan rekomendasi produk yang sesuai dengan 
            kebutuhan dan preferensi Anda, berdasarkan pola pembelian Anda dari periode sebelumnya. 
            Dengan demikian, kami membantu Anda membuat keputusan yang lebih baik dan meningkatkan 
            pembelian dari customer yang loyal dan puas. :)
        """
    )
    st.write('# Arti dari setiap input: ')
    st.write('Customer, Input pelanggan yang ingin dilihat pola pembeliannya')
    st.image(documentation_5, caption='Panel Customer')

    st.write('Timeframe, Waktu pola pembeliannya dalam timeframe 3/6/9/12 bulan')
    st.image(documentation_7, caption='Panel Customer')

    st.write('Product, Product yang pernah dibeli oleh customer supaya bisa mencari tahu dengan produk tersebut dia membeli apa saja')
    st.image(documentation_11, caption='Panel Customer')

    st.write('# Tutorial penggunaan')
    st.write('Tampilan Aplikasi awal')
    
    st.write('1. Buka Navbar aplikasi')

    st.write('2. Pilih Analysis')
    st.image(documentation_2, caption='Navbar')

    st.write('3. Tampilan awal')
    st.image(documentation_3, caption='Nilai awal customer dan timeframe sudah terisi default')

    st.write('4. Pilih panel Customer dan akan muncul list customer yang pernah membeli')
    st.image(documentation_4, caption='Panel Customer')

    st.write('5. Disini saya pilih customer dengan ID 1017866')
    st.image(documentation_5)

    st.write('6. Buka panel Timeframe dan akan memiliki tampilan berikut')
    st.image(documentation_6, caption='Timeframe panel')

    st.write('7. saya akan memilih Timeframe 12 bulan ya')
    st.image(documentation_7, caption='Timeframe 12 bulan')

    st.write('8. Hasil nya: ')
    st.image(documentation_8, caption='tes')

    st.write('9. Jika di scroll kebawah, kita bisa menganalysis produk apa yang sering dibeli customer tersebut')
    st.image(documentation_9, caption='Hasil analysis')

    st.write('10. Isi panel product yang pernah dibeli customer')
    st.image(documentation_10, caption='Panel Product')

    st.write('11. pilih TPODA dan sistem akan mencari produk apa yang sering dibeli dengan TPODA')
    st.image(documentation_11, caption='Hasil akhir')

    

Documentation()