SELECT id_contrato, 
count(*) as freq_contratos,
round(avg(valor_previsto_parcela),2) as media_valor_parcela,
ROUND(AVG(dias_atraso)) AS media_dias_atrasos, 
max(numero_parcela) as numero_max_parcelas
FROM tabela_parcelas
GROUP by id_contrato
