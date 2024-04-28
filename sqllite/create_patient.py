import sqlite3

class DatabaseManager:
    def __init__(self, db_name='DB_SBAR.db'):
        self.db_name = db_name

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # 创建 Patient 表
        c.execute('''CREATE TABLE IF NOT EXISTS Patient (
                        id INTEGER PRIMARY KEY,
                        bed_ID TEXT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        gender TEXT,
                        contact_phone TEXT,
                        admission_number TEXT,
                        admission_date DATE,
                        discharge_date DATE,
                        status TEXT,
                        note TEXT,
                        chief_complaint TEXT,
                        important_disposal TEXT,
                        medical_history TEXT,
                        positive_results TEXT,
                        physical_examination TEXT,
                        critical_value TEXT,
                        urinarycatheter TEXT,
                        drainagetube TEXT,
                        stoma TEXT,
                        vital_signs TEXT,
                        bleeding TEXT,
                        pain TEXT,
                        intake_output TEXT,
                        self_care TEXT,
                        falls TEXT,
                        pressure_ulcers TEXT,
                        VYE TEXT,
                        custom_integer_field TEXT,
                        custom_float_field TEXT,
                        created_at timestamp not null default(datetime(CURRENT_TIMESTAMP,'localtime'))
                        )''')

        # 创建 Bed 表
        c.execute('''CREATE TABLE IF NOT EXISTS Bed (
                        id INTEGER PRIMARY KEY,
                        bed_number INTEGER NOT NULL,
                        room_number INTEGER,
                        patient_id INTEGER,
                        status TEXT,
                        note TEXT,
                        custom_integer_field INTEGER,
                        custom_float_field FLOAT,
                        FOREIGN KEY (patient_id) REFERENCES Patient (id)
                        )''')

        # 提交更改并关闭连接
        conn.commit()
        conn.close()
