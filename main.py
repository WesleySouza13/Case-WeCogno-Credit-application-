import streamlit as st 
import os 
from utils.load_tables import tables_load
from utils.prepros_func import col_transform
import pandas as pd 
from predict.api_predict import model_predict
import numpy as np 
import seaborn as sns 
import plotly.express as px

logo_path = os.path.join('images', 'wecogno_cover.jpg')
st.image(logo_path)

# apresentaçao do app 
st.text('Esse app foi desenvolvido com o intuito de fazer previsões em batch para mensuração de risco de crédito para novos clientes.')
st.markdown('Desenvolvido por Wesley de Souza Matos')

df_uploader= st.file_uploader('Insira os dados', type=['parquet'])
if df_uploader is not None:
    df = pd.read_parquet(df_uploader)
    df_cad = tables_load().table_base_cadastral()
    df_cad=df_cad.reset_index()
    df_emp = tables_load().table_base_emprestimos()
    df_cad['data_nascimento'] = pd.to_datetime(df_cad['data_nascimento'], format='%Y-%m-%d', errors='coerce')
    data_hoje = pd.Timestamp.today().normalize()
    df_cad['idade'] = (data_hoje.year - df_cad['data_nascimento'].dt.year-((df_cad['data_nascimento'].dt.month > data_hoje.month) | ((df_cad['data_nascimento'].dt.month == data_hoje.month) & (df_cad['data_nascimento'].dt.day > data_hoje.day))).astype('Int64'))
    df_cad.drop('data_nascimento', axis=1, inplace=True)
    # %%
    # primeiro merge (base cadastro)
    df_merge1 = pd.merge(df, df_cad, how='left', on='id_cliente') 
    # %%
    # segundo merge (base emprestimo)
    df_emp = tables_load().table_base_emprestimos()
    df_emp= df_emp.reset_index()
    df_emp = df_emp.drop_duplicates(subset='id_cliente',keep='first')
    # %%
    df_merge2 = pd.merge(df_merge1, df_emp, how='left', on='id_cliente')
    print(df_merge2.shape)
    cols_x = [ col for col in df_merge2.columns if col.endswith('_x')]
    # remove as colunas _y correspondentes
    cols_y = [col[:-2] + '_y' for col in cols_x if col[:-2] + '_y' in df_merge2.columns]
    df_merge2 = df_merge2.drop(columns=cols_y)
    # retirando o sufixo _x
    df_merge2 = df_merge2.rename(columns={col: col[:-2] for col in cols_x})
    # %%
    df_final = col_transform(df_merge2)
    # %%
    # selecionando especificamente as colunas usadas na modelagem 
    df_final = df_final[['dia_semana_solicitacao', 'hora_solicitacao', 'tipo_contrato',
            'valor_credito', 'valor_bem', 'valor_parcela', 'valor_bem_ausente',
            'valor_parcela_ausente', 'qtd_filhos', 'qtd_membros_familia',
            'renda_anual', 'tipo_renda', 'ocupacao', 'tipo_organizacao',
            'nivel_educacao', 'estado_civil', 'tipo_moradia', 'possui_carro',
            'possui_imovel', 'nota_regiao_cliente', 'nota_regiao_cliente_cidade',
            'idade', 'pct_valor_credito_bem', 'flag_credito_maior_bem',
            'pct_parcela_bem', 'pct_valor_bem_renda_anual',
            'pct_valor_credito_renda', 'prazo_implicito',
            'valor_bem_maior_que_renda', 'diff_valor_bem_credito',
            'renda_per_capta', 'flag_sem_filhos', 'aposentado', 'servidor_publico',
            'nota_max_regiao_cliente', 'periodo_dia', 'flag_final_de_semana']]
    st.dataframe(df_final)
    
    # fazendo prediçao 
    proba = model_predict(df_final)
    st.markdown('Predições:')
    df_pivot = df_final.reset_index().copy()
    pred_data = pd.DataFrame()
    pred_data['id_cliente'] = df_pivot['id_cliente']
    pred_data['data_solicitacao'] = df_pivot['data_solicitacao']
    pred_data['probabilidade'] = proba
    pred_data['RENDA'] = df_pivot['renda_anual']
    #pred_data['RENDA'] = df_final['renda_anual']
    # separaçao de grupos 
    pred_data['RISCO'] = faixas_risco = np.select([proba <= 0.10, proba <= 0.17],['BAIXO','MÉDIO'],default='ALTO')
    st.dataframe(pred_data)
    
    fig_prob_time = px.histogram(pred_data, 'probabilidade', color_discrete_sequence=['#27F579'], title='Histograma das Probabilidades')
    box_prob = px.box(pred_data, 'probabilidade', color_discrete_sequence=['#27F579'], title='Boxplot das Probabilidades')
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_prob_time)
    with col2:
        st.plotly_chart(box_prob)
    mean_clientes = pred_data[pred_data['RISCO']=='MÉDIO']
    # faixas de renda: classe D, C, B, A
    mean_clientes['FAIXA_RENDA'] = np.select([mean_clientes['RENDA'] <= 20000, (mean_clientes['RENDA'] > 20000) & (mean_clientes['RENDA'] < 30000), (mean_clientes['RENDA'] >= 30000) & (mean_clientes['RENDA'] < 50000)],
                                            ['D', 'C', 'B'],default='A')        
    st.markdown('Clientes com risco médio (avaliação humana):')
    st.dataframe(mean_clientes)
    median_clients_box = px.box(data_frame=mean_clientes,y='probabilidade', color='FAIXA_RENDA')
    st.plotly_chart(median_clients_box)
else:
    raise FileNotFoundError('insira um arquivo válido')
# %%
