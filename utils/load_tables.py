import pandas as pd 
import os 
from pathlib import Path
class tables_load():
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

    def table_base_cadastral(self, verbose=True):
        data_path = self.base_dir / 'data' / 'raw' / 'base_cadastral.parquet'
        if not data_path.is_file():
            raise FileNotFoundError('Arquivo nao encontrado')
        df = pd.read_parquet(data_path)
        if verbose:
            print('==='*50)
            print('Dimensoes da tabela de cadastro:')
            print('==='*50)
            print(f'linhas: {df.shape[0]}')
            print(f'colunas: {df.shape[1]}')
        return df.set_index('id_cliente')
        
    def table_base_emprestimos(self, verbose=True):
            data_path = self.base_dir / 'data' / 'raw' / 'base_cadastral.parquet'
            if not data_path.is_file():
                        raise FileNotFoundError('Arquivo nao encontrado')
            df = pd.read_parquet(data_path)
            if verbose:
                print('==='*50)
                print('Dimensoes da tabela de emprestimos:')
                print('==='*50)
                print(f'linhas: {df.shape[0]}')
                print(f'colunas: {df.shape[1]}')
            return df.set_index(['id_cliente', 'id_contrato'])