SELECT 
T2.id_contrato,
T1.id_cliente,
T1.sexo,
T1.qtd_filhos,
T1.qtd_membros_familia, 
T1.renda_anual, 
T1.estado_civil, 
T1.idade,
T1.nivel_educacao, 
T1.possui_carro, 
T1.possui_imovel,
T2.TARGET,
T2.dias_atraso,
T2.valor_previsto_parcela,
T2.valor_pago_parcela
FROM tabela_cadastral_tratada as T1
LEFT JOIN tabela_parcelas AS T2
ON T1.id_cliente = T2.id_cliente
