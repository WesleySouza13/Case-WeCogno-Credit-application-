WITH tb_emp AS (SELECT id_cliente,id_contrato, dia_semana_solicitacao,hora_solicitacao,
tipo_contrato, valor_bem, valor_credito, valor_parcela,  valor_bem_ausente, valor_parcela_ausente, data_decisao
FROM tabela_emprestimos_tratada
), 
tb_cad AS (
SELECT id_cliente,qtd_filhos,  qtd_membros_familia, 
renda_anual, tipo_renda, ocupacao, tipo_organizacao, nivel_educacao, estado_civil, 
tipo_moradia, possui_carro, possui_imovel, nota_regiao_cliente, nota_regiao_cliente_cidade,idade 
FROM tabela_cadastral_tratada
),
tb_emp_cad AS (
SELECT T1.*, 
T2.qtd_filhos, T2.qtd_membros_familia, T2.renda_anual,T2.tipo_renda, T2.ocupacao,
T2.tipo_organizacao, T2.nivel_educacao, T2.estado_civil, T2.tipo_moradia, 
T2.possui_carro, T2.possui_imovel, T2.nota_regiao_cliente, T2.nota_regiao_cliente_cidade, T2.idade
FROM tb_emp AS T1
iNNER JOIN tb_cad AS T2
ON T1.id_cliente = T2.id_cliente
),
tb_parcelas AS (
    SELECT id_contrato,
    MAX(TARGET) AS TARGET FROM tabela_parcelas
    GROUP BY id_contrato
),
tb_agg AS (
SELECT 
T1.id_cliente,T1.id_contrato, strftime('%Y-%m', T1.data_decisao) as safra_decisao, T1.dia_semana_solicitacao, 
CAST(strftime('%H', T1.hora_solicitacao)AS INTEGER) AS hora_solicitacao, T1.tipo_contrato, T1.valor_credito, T1.valor_bem, T1.valor_parcela,
T1.valor_bem_ausente, T1.valor_parcela_ausente,  T1.qtd_filhos, T1.qtd_membros_familia,T1.renda_anual,
T1.tipo_renda, T1.ocupacao, T1.tipo_organizacao, T1.nivel_educacao, T1.estado_civil, T1.tipo_moradia, T1.possui_carro, 
T1.possui_imovel, T1.nota_regiao_cliente, T1.nota_regiao_cliente_cidade, T1.idade, T2.TARGET
FROM tb_emp_cad AS T1 
LEFT JOIN tb_parcelas AS T2
ON T1.id_contrato = T2.id_contrato
),
tb_geral AS (
SELECT * FROM tb_agg
WHERE TARGET IS NOT NULL
)

SELECT *, ROUND((valor_credito/ valor_bem),2) AS pct_valor_credito_bem,
CASE WHEN valor_credito > valor_bem THEN 1 
ELSE 0 END AS flag_credito_maior_bem, 
ROUND((valor_parcela/valor_bem),2) AS pct_parcela_bem,
ROUND((valor_bem/renda_anual),2) AS pct_valor_bem_renda_anual,
ROUND((valor_credito/renda_anual),2) AS pct_valor_credito_renda,
ROUND((valor_credito/valor_parcela)) AS prazo_implicito,
CASE WHEN valor_bem > renda_anual THEN 1
ELSE 0 END AS valor_bem_maior_que_renda,
ROUND((valor_bem - valor_credito),2) AS diff_valor_bem_credito,
ROUND((renda_anual/qtd_membros_familia),2) AS renda_per_capta,
CASE WHEN qtd_filhos = 0 THEN 1 
ELSE 0 END AS flag_sem_filhos,
CASE WHEN tipo_renda = 'aposentado' THEN 1
ELSE 0 END AS aposentado,
CASE WHEN tipo_renda = 'servidor público' THEN 1
ELSE 0 END AS servidor_publico,
CASE WHEN nota_regiao_cliente >=3 THEN 1 
ELSE 0 END AS nota_max_regiao_cliente,
-- tempo
CASE  WHEN hora_solicitacao BETWEEN 0  AND 5  THEN 'madrugada'
WHEN hora_solicitacao BETWEEN 6  AND 11 THEN 'manha'
WHEN hora_solicitacao BETWEEN 12 AND 17 THEN 'tarde'
WHEN hora_solicitacao BETWEEN 18 AND 23 THEN 'noite'
ELSE NULL END  periodo_dia,
CASE WHEN dia_semana_solicitacao IN('sábado' , 'domingo') THEN 1
ELSE 0 END AS flag_final_de_semana
FROM tb_geral
