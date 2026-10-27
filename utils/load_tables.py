import pandas as pd 
import os 

class tables_load():
    def table_base_cadastral(self, verbose=True):
        if verbose == True: 
            data_path = os.path.join('data', 'raw', 'base_cadastral.parquet')
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
            data_path = os.path.join('data', 'raw', 'historico_emprestimos.parquet')
            if os.path.exists(data_path) != True:
                    raise AttributeError('Arquivo nao encontrado')
            df = pd.read_parquet(data_path)
            print('==='*50)
            print(f'Dimensoes da tabela de emprestimos:')
            print('==='*50)
            print(f'linhas: {df.shape[0]}')
            print(f'colunas: {df.shape[1]}')
            return df.set_index(['id_cliente', 'id_contrato'])