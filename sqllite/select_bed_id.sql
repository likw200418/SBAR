SELECT
    Bed.bed_number,
    Patient.`name`,
    Patient.gender,
    Patient.age,
    Patient.admission_date,
    Patient.chief_complaint,
    Patient.important_disposal,
    Patient.medical_history,
    Patient.positive_results,
    Patient.physical_examination,
    Patient.critical_value,
    Patient.vital_signs,
    Patient.bleeding,
    Patient.pain,
    Patient.urinarycatheter,
    Patient.drainagetube,
    Patient.stoma,
    Patient.intake_output,
    Patient.self_care,
    Patient.falls,
    Patient.pressure_ulcers,
    Patient.VYE,
    Patient.note
FROM Bed
LEFT JOIN Patient ON Patient.id = Bed.patient_id
WHERE Bed.bed_number =?;
