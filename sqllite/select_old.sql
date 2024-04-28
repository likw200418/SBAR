-- query.sql

SELECT
    --id as '病人ID',
    Patient.bed_ID '历史床位号',
    --bed_number as '床位编号',
    Patient.`name` as '病人姓名',
    Patient.gender as '病人性别',
    Patient.age as '病人年龄',
    --contact_phone as '联系电话',
    --Patient.admission_number as '入院号',
    Patient.admission_date as '入院日期',
    --Patient.discharge_date as '出院日期',
    --Patient.status as '病人状态',
    Patient.chief_complaint as '主诉',
    Patient.important_disposal as '重要处置',
    Patient.medical_history as '既往史',
    Patient.positive_results as '阳性结果',
    Patient.physical_examination as '体征',
    Patient.critical_value as '危急值',
    Patient.vital_signs as '生命体征',
    Patient.bleeding as '出血',
    Patient.pain as '疼痛',
    Patient.urinarycatheter as '尿管',
    Patient.drainagetube as '引流管',
    Patient.stoma as '造瘘',
    Patient.intake_output as '出入量',
    Patient.self_care as '自理',
    Patient.falls as '跌倒',
    Patient.pressure_ulcers as '压疮',
    Patient.VYE as 'VYE',
    Patient.note as '建议'
   -- custom_integer_field as '自定义整数字段',
   -- custom_float_field as '自定义浮点数字段',
   -- created_at as '创建时间'
FROM Patient
WHERE Patient.bed_ID IS NOT NULL and Patient.bed_ID!='';

