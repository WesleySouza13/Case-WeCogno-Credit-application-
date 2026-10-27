# %%
import os 
import pandas as pd 
import numpy as np
sub_path = os.path.join('..','..', 'data', 'raw', 'base_submissao.parquet')
df = pd.read_parquet(sub_path)
# %%
# tratando algumas colunas 
df['data_solicitacao'] = pd.to_datetime(df['data_solicitacao'], format='%Y-%m-%d', errors='coerce')
# %%
# classe para carregamento de tabelas 
class tables_load():
    def table_base_cadastral(self, verbose=True):
        if verbose == True: 
            data_path = os.path.join('..', '..','data', 'raw', 'base_cadastral.parquet')
            if os.path.exists(data_path) != True:
                raise AttributeError('Arquivo nao encontrado')
            df = pd.read_parquet(data_path)
            print('==='*50)
            print(f'Dimensoes da tabela de cadastro:')
            print('==='*50)
            print(f'linhas: {df.shape[0]}')
            print(f'colunas: {df.shape[1]}')
            return df.set_index('id_cliente')
        
    def table_base_emprestimos(self, verbose=True):
        if verbose == True:
            data_path = os.path.join('..','..', 'data', 'raw', 'historico_emprestimos.parquet')
            if os.path.exists(data_path) != True:
                    raise AttributeError('Arquivo nao encontrado')
            df = pd.read_parquet(data_path)
            print('==='*50)
            print(f'Dimensoes da tabela de emprestimos:')
            print('==='*50)
            print(f'linhas: {df.shape[0]}')
            print(f'colunas: {df.shape[1]}')
            return df.set_index(['id_cliente', 'id_contrato'])

df_cad = tables_load().table_base_cadastral()
df_cad=df_cad.reset_index()
# tratando idades irreais 
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
# %%
# %%
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
    return df_merge

# Identifica colunas terminadas em _x
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
# %%
path_data = os.path.join('..', '..', 'data', 'processed', 'base_submissao_tratada.parquet')
df_final.to_parquet(path_data)
# %%
