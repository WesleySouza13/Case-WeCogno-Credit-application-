import pandas as pd 
import numpy as np 

def col_transform(data:pd.DataFrame):
    df_merge = data.copy()
    # tranformando renda_anual em uma coluna numerica
    df_merge['renda_anual'] = df_merge['renda_anual'].str.replace('.', '', regex=False).str.replace(',','.')
    df_merge['renda_anual'] = pd.to_numeric(df_merge['renda_anual'], errors='coerce')
    # index
    df_merge = df_merge.set_index(['id_cliente', 'data_solicitacao'])
    # hora de solicitacao
    df_merge['hora_solicitacao'] = pd.to_datetime(df_merge['hora_solicitacao'],format='%H:%M:%S',errors='coerce').dt.hour.astype('Int64')
    df_merge['tipo_contrato'] = df_merge['tipo_contrato'].str.lower()
    df_merge['valor_bem_ausente'] = np.where(df_merge['valor_bem'].isna(), 1,0)
    df_merge['valor_parcela_ausente'] = np.where(df_merge['valor_parcela'].isna(), 1,0)
    df_merge['pct_valor_credito_bem'] = round(df_merge['valor_credito']/df_merge['valor_bem'],2)
    df_merge['flag_credito_maior_bem'] = np.where(df_merge['valor_credito']>df_merge['valor_bem'],1,0)
    df_merge['pct_parcela_bem'] = round(df_merge['valor_parcela']/df_merge['valor_bem'],2)
    df_merge['pct_valor_bem_renda_anual'] = round(df_merge['valor_bem']/df_merge['renda_anual'],2)
    df_merge['pct_valor_credito_renda'] = round(df_merge['valor_credito']/df_merge['renda_anual'],2)
    df_merge['prazo_implicito'] = round(df_merge['valor_credito']/df_merge['valor_parcela'],2)
    df_merge['valor_bem_maior_que_renda'] = np.where(df_merge['valor_bem']>df_merge['renda_anual'],1,0)
    df_merge['diff_valor_bem_credito'] = round(df_merge['valor_bem'] - df_merge['valor_credito'],2)
    df_merge['renda_per_capta'] = round(df_merge['renda_anual']/df_merge['qtd_membros_familia'],2)
    df_merge['flag_sem_filhos'] = np.where(df_merge['qtd_filhos']==0,1,0)
    df_merge['aposentado'] = np.where(df_merge['tipo_renda']=='aposentado',1,0)
    df_merge['servidor_publico'] = np.where(df_merge['tipo_renda']=='servidor público',1,0)
    df_merge['nota_max_regiao_cliente'] = np.where(df_merge['nota_regiao_cliente']>=3,1,0)
    hora = df_merge['hora_solicitacao']
    df_merge['periodo_dia'] = np.select([hora.between(0, 5).fillna(False).to_numpy(dtype=bool),hora.between(6, 11).fillna(False).to_numpy(dtype=bool),hora.between(12, 17).fillna(False).to_numpy(dtype=bool),
            hora.between(18, 23).fillna(False).to_numpy(dtype=bool)],['madrugada', 'manha', 'tarde', 'noite'],default=None)
    df_merge['flag_final_de_semana'] = (df_merge['dia_semana_solicitacao'].isin(['sábado', 'domingo']).astype('int8')) 
    
    # deixando algumas colunas em caixa baixa
    labels_count = ['possui_imovel', 'possui_carro']
    for labels_lower in labels_count:
        print(f'modificando coluna: {labels_lower}')
        df_merge[labels_lower] = df_merge[labels_lower].str.strip().str.lower().replace({'nao':'não', 'Sim':'sim',
                                                                                        'SIM':'sim','Não':'não' })
        print('coluna modificada com sucesso')
        print('----'*50)
    df_merge['tipo_renda'] = df_merge['tipo_renda'].str.lower()
    # tratando linhas com possiveis inf 
    df_merge['prazo_implicito'] = np.where(df_merge['prazo_implicito']==np.inf,df_merge['prazo_implicito'].median(), df_merge['prazo_implicito'] )
    df_merge.loc[df_merge['renda_anual'] < 0,'renda_anual'] *= -1    
    df_merge['ocupacao'] = df_merge['ocupacao'].fillna('Não informado')
    return df_merge