SELECT T1.id_cliente, 
T1.sexo, T1.idade, 
T1.qtd_filhos,
T1.possui_imovel, 
T1.possui_carro, 
AVG(T1.renda_anual) AS renda_anual, 
T2.tipo_contrato, 
T2.valor_credito, 
T2.valor_parcela, 
T2.qtd_parcelas_planejadas,
T2.finalidade_emprestimo,
T2.categoria_bem
FROM tabela_cadastral_tratada AS T1
LEFT JOIN tabela_emprestimos_tratada AS T2
ON T1.id_cliente = T2.id_cliente
GROUP BY renda_anual
