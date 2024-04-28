from datetime import datetime
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from patient_ui.patient_ui import Ui_PatientViewer  # 导入通过 Qt Designer 创建的主窗口界面类
from patient_ui.patientUI import Ui_addPatientViewer  # 导入通过 Qt Designer 创建的副窗口界面类
from patient_ui.ksgh_ui import Ui_kshc
from sqllite.create_patient import DatabaseManager  # 导入用于创建数据库的类
import sqlite3
import os
import re
from PyQt5.QtGui import QFont,QColor
import openpyxl

class PatientViewerApp(QtWidgets.QMainWindow, Ui_PatientViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('SBAR系统')
        self.setMouseTracking(True)
        self.setWindowIcon(QtGui.QIcon('./static/hsz.png'))
        self.context_menu = QtWidgets.QMenu(self)
        font4 = QFont("微软雅黑", 13)
        self.detail_action1 = self.context_menu.addAction("查看病人信息")
        self.detail_action1.setFont(font4)
        self.detail_action1.triggered.connect(self.show_detail)

        self.detail_action2 = self.context_menu.addAction("增加病人到床位")
        self.detail_action2.setFont(font4)
        self.detail_action2.triggered.connect(self.add_detail)

        self.detail_action3 = self.context_menu.addAction("移除该床位病人")
        self.detail_action3.setFont(font4)
        self.detail_action3.triggered.connect(self.del_detail)

        self.detail_action4 = self.context_menu.addAction("修改病人信息")
        self.detail_action4.setFont(font4)
        self.detail_action4.triggered.connect(self.put_detail)

        self.detail_action5 = self.context_menu.addAction("快速换床")
        self.detail_action5.setFont(font4)
        self.detail_action5.triggered.connect(self.ks_bed)
        conn = sqlite3.connect('DB_SBAR.db')
        my_list = []
        try:
            cursor = conn.execute("select bed_number from Bed;")
            results = cursor.fetchall()
            for row in results:
                my_list.append(str(row[0])+"号床")
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
            return
        self.comboBox.addItem("全部")
        self.comboBox.setStyleSheet("font: 12pt \"宋体\";")
        self.comboBox.addItems(my_list)#查看所有床位
        self.add_button.clicked.connect(self.add_beds)#点击增加床位按钮
        self.del_button.clicked.connect(self.del_beds)#点击删除床位按钮
        self.search_button.clicked.connect(self.def_beds)
        self.comboBox.currentIndexChanged.connect(self.search_beds)#选择后立马触发
        self.search_button.setEnabled(False)
        self.tableView.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightblue; black: white; font-weight: bold;font:12pt \"微软雅黑\";\n }")
        self.export_button.clicked.connect(self.export_all)
        self.export_button2.clicked.connect(self.export_old)
    def export_to_excel(self, results, template_path, output_filename):
        try:
            # 打开 Excel 模板文件
            wb = openpyxl.load_workbook(template_path)
            ws = wb.active
            # 定义数据填充的起始行和列
            start_row = 4  # 假设第一行是标题
            start_col = 1  # 假设第一列是数据起始列
            # 将数据填充到模板中
            row_num = start_row
            for row_data in results:
                col_num = start_col
                for cell_value in row_data:
                    ws.cell(row=row_num, column=col_num).value = cell_value
                    col_num += 1
                row_num += 1
            # 获取当前用户的桌面路径
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            # 拼接完整的输出文件路径
            output_path = os.path.join(desktop_path, output_filename)
            # 保存填充后的 Excel 文件
            wb.save(output_path)
            QMessageBox.warning(self, "成功", f"数据已成功导出到 {output_path}", QMessageBox.Ok)
            # 自动打开导出的 Excel 文件
            os.startfile(output_path)
        except Exception as e:
            print(f"导出到 Excel 时出现错误：{str(e)}")



    def export_old(self):
        try:
            conn = sqlite3.connect('DB_SBAR.db')
            query_path = "./sqllite/select_old.sql"
            query = read_query_file(query_path)
            cursor = conn.execute(query)
            results = cursor.fetchall()
            # 获取当前日期
            current_date = datetime.now()
            # 将日期格式化为 YYYY-MM-DD
            formatted_date = current_date.strftime("%Y-%m-%d")
            # 定义模板和输出路径
            template_path = './Template/Template_old.xlsx'
            output_path =f"SBAR报表-历史记录-{formatted_date}.xlsx"
            # 导出数据到 Excel
            self.export_to_excel(results, template_path, output_path)
            conn.close()
        except sqlite3.Error as e:
            print(f"数据库错误：{str(e)}")
        except FileNotFoundError as e:
            print(f"文件未找到：{str(e)}")
        except Exception as e:
            print(f"发生未知错误：{str(e)}")
    def export_all(self):
        try:
            conn = sqlite3.connect('DB_SBAR.db')
            query_path = "./sqllite/select.sql"
            query = read_query_file(query_path)
            cursor = conn.execute(query)
            results = cursor.fetchall()
            # 获取当前日期
            current_date = datetime.now()
            # 将日期格式化为 YYYY-MM-DD
            formatted_date = current_date.strftime("%Y-%m-%d")
            # 定义模板和输出路径
            template_path = './Template/Template.xlsx'
            output_path =f"SBAR报表-{formatted_date}.xlsx"
            # 导出数据到 Excel
            self.export_to_excel(results, template_path, output_path)
            conn.close()
        except sqlite3.Error as e:
            print(f"数据库错误：{str(e)}")
        except FileNotFoundError as e:
            print(f"文件未找到：{str(e)}")
        except Exception as e:
            print(f"发生未知错误：{str(e)}")
    def ks_bed(self):
        self.ks_bes = ksPatientViewer(self)
        self.ks_bes.show()
        selected_index = self.tableView.currentIndex()
        conn = sqlite3.connect('DB_SBAR.db')
        my_lists = []
        if self.tableView.model().item(selected_index.row(), 0) is not None:
            beds_number = self.tableView.model().item(selected_index.row(), 0).text()
            beds_id = re.search(r'\d+', beds_number).group()
            try:
                cursor = conn.execute("select bed_number from Bed;")
                results = cursor.fetchall()
                for row in results:
                    my_lists.append(str(row[0]) + "号床")
                self.ks_bes.comboBox_dq.addItems(my_lists)
                self.ks_bes.comboBox_gh.addItems(my_lists)
                self.ks_bes.comboBox_dq.setCurrentIndex(int(beds_id)-1 if int(beds_id) >= 1 else int(beds_id))
                self.ks_bes.pushButton.clicked.connect(self.ks_bes.Oks)
                self.ks_bes.pushButton_2.clicked.connect(self.ks_bes.cls)
                self.ks_bes.comboBox_dq.setEnabled(False)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
                return
        conn.close()
    def def_beds(self):
        self.load_data()
        self.comboBox.setCurrentIndex(0)
    def search_beds(self):
        #搜索功能,获取床位号，要用新的model模型
        text = self.comboBox.currentText()
        if text=="全部":
            self.detail_window = AddPatientViewer(self)
            self.load_data()
        else:
            conn = sqlite3.connect('DB_SBAR.db')
            try:
                self.search_button.setEnabled(True)
                beds_id = re.search(r'\d+', text).group()
                query_path = "./sqllite/ser_select.sql"
                query = read_query_file(query_path)
                cursor = conn.execute(query, (beds_id,))
                models = QtGui.QStandardItemModel()
                header = [description[0] for description in cursor.description]
                models.setHorizontalHeaderLabels(header)
                font = QFont("微软雅黑", 13)  # 设置字体样式
                font2 = QFont("宋体", 12)  # 设置字体样式
                for row_num, row_data in enumerate(cursor, start=1):
                    for col_num, col_data in enumerate(row_data):
                        if col_data is not None:
                            item = QtGui.QStandardItem(str(col_data))
                            if col_num == 0:
                                item.setText(f"{col_data}号床")
                                item.setFont(font)
                                # item.setBackground(QColor("lightblue"))
                            item.setToolTip(str(col_data))
                            item.setFont(font2)
                            models.setItem(row_num - 1, col_num, item)
                self.tableView.setModel(models)
                self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
            conn.close()
    def del_beds(self):
        #直接删除最大的床位号，有病人不能删
        conn = sqlite3.connect('DB_SBAR.db')
        try:
            cursor = conn.execute("SELECT MAX(id) FROM Bed;")
            results = cursor.fetchall()
            # 输出结果
            for row in results:
                beds_id = row[0]
            cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (beds_id,))
            results = cursor.fetchall()
            for row in results:
                res = row[0]
        except Exception as e:
            QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
            return
        if beds_id is None:
            QMessageBox.warning(self, "错误", f"没有床位可以移除", QMessageBox.Ok)
        else:
            if res  is None:
                try:
                    cur = conn.execute("DELETE FROM Bed WHERE bed_number=?;", (beds_id,))
                    conn.commit()
                    QMessageBox.information(self, "成功", f"成功删除床位：{beds_id}号床！", QMessageBox.Ok)
                    self.load_data()
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"插入床位信息时出错：{str(e)}", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "错误", f"请先移除病人信息", QMessageBox.Ok)
        conn.close()
    def add_beds(self):
        #增加空床位
        conn = sqlite3.connect('DB_SBAR.db')
        try:
            cursor = conn.execute("SELECT MAX(id) FROM Bed;")
            results = cursor.fetchall()
            # 输出结果
            for row in results:
                beds_id = row[0]
        except Exception as e:
            QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
            return
        if beds_id is None:
            beds_id = 1
        else:
            beds_id=beds_id+1
        try:
            cur = conn.execute("INSERT INTO Bed (bed_number) VALUES (?);", (beds_id,))
            conn.commit()
            QMessageBox.information(self, "成功", f"成功增加床位：{beds_id}号床！", QMessageBox.Ok)
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"插入床位信息时出错：{str(e)}", QMessageBox.Ok)
        conn.close()
    def add_detail(self):
        #增加病人
        self.detail_window = AddPatientViewer(self)
        selected_index = self.tableView.currentIndex()
        if self.tableView.model().item(selected_index.row(), 0) is not None:
            beds_number = self.tableView.model().item(selected_index.row(), 0).text()
            beds_id = re.search(r'\d+', beds_number).group()
            conn = sqlite3.connect('DB_SBAR.db')
            cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;",(beds_id,))
            results = cursor.fetchall()
            self.detail_window.ui.pushButton.setText("确认添加")
            for row in results:
                print(row[0])
                #判断该床位不能有人
            if row[0] is None:
                #把实例化对象传给on——submit_clicked方法中
                self.detail_window.ui.label.setText(beds_number)
                self.detail_window.ui.pushButton.clicked.connect(self.detail_window.on_submit_clicked)  # 调用方法,当使用 clicked.connect() 连接槽函数时，你不能直接传递参数给槽函数。相反，你需要使用 lambda 函数
                self.detail_window.show()
            else:
                QMessageBox.information(self, "错误", f"{beds_number}位已有病人，你可以试试查看/修改/移除", QMessageBox.Ok)
            conn.close()

    def put_detail(self):
        selected_index = self.tableView.currentIndex()
        self.detail_window = AddPatientViewer(self)
        # self.detail_window.ui.pushButton.hide()
        self.detail_window.ui.pushButton.setText("确认修改")
        if self.tableView.model().item(selected_index.row(), 0) is not None:
            beds_number = self.tableView.model().item(selected_index.row(), 0).text()
            number_only = re.search(r'\d+', beds_number).group()
            self.detail_window.ui.label.setText(beds_number)
            conn = sqlite3.connect('DB_SBAR.db')
            cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (number_only,))
            results = cursor.fetchall()
            for row in results:
                print(row[0])
            if row[0] is not None:
                query_path = "./sqllite/select_bed_id.sql"
                query = read_query_file(query_path)
                cursor = conn.execute(query, (number_only,))
                rows = cursor.fetchall()
                result_list = []
                columns = [description[0] for description in cursor.description]
                # 遍历每一行
                for row in rows:
                    # 将每一行的数据与字段名组合成字典
                    row_dict = dict(zip(columns, row))
                    # 将字典添加到结果列表中
                    result_list.append(row_dict)
                if result_list[0]['name'] is not None:
                    self.detail_window.ui.username.setText(result_list[0]['name'])
                if result_list[0]['age'] is not None:
                    self.detail_window.ui.age.setText(str(result_list[0]['age']))
                if result_list[0]['gender'] is not None:
                    self.detail_window.ui.gender.setText(result_list[0]['gender'])
                if result_list[0]['admission_date'] is not None:
                    text_date = result_list[0]['admission_date']
                    self.detail_window.ui.admission_date.setDate(datetime.strptime(text_date, "%Y-%m-%d"))
                if result_list[0]['chief_complaint'] is not None:
                    self.detail_window.ui.chief_complaint.setText(result_list[0]['chief_complaint'])
                if result_list[0]['note'] is not None:
                    self.detail_window.ui.note.setText(result_list[0]['note'])
                if result_list[0]['important_disposal'] is not None:
                    self.detail_window.ui.important_disposal.setText(result_list[0]['important_disposal'])
                if result_list[0]['medical_history'] is not None:
                    self.detail_window.ui.medical_history.setText(result_list[0]['medical_history'])
                if result_list[0]['positive_results'] is not None:
                    self.detail_window.ui.positive_results.setText(result_list[0]['positive_results'])
                if result_list[0]['physical_examination'] is not None:
                    self.detail_window.ui.physical_examination.setText(result_list[0]['physical_examination'])
                if result_list[0]['critical_value'] is not None:
                    self.detail_window.ui.critical_value.setText(result_list[0]['critical_value'])
                if result_list[0]['vital_signs'] is not None:
                    self.detail_window.ui.vital_signs.setText(result_list[0]['vital_signs'])
                if result_list[0]['bleeding'] is not None:
                    self.detail_window.ui.bleeding.setText(result_list[0]['bleeding'])
                if result_list[0]['pain'] is not None:
                    self.detail_window.ui.pain.setText(result_list[0]['pain'])
                if result_list[0]['urinarycatheter'] is not None:
                    self.detail_window.ui.urinarycatheter.setText(result_list[0]['urinarycatheter'])
                if result_list[0]['drainagetube'] is not None:
                    self.detail_window.ui.drainagetube.setText(result_list[0]['drainagetube'])
                if result_list[0]['stoma'] is not None:
                    self.detail_window.ui.stoma.setText(result_list[0]['stoma'])
                if result_list[0]['self_care'] is not None:
                    self.detail_window.ui.self_care.setText(result_list[0]['self_care'])
                if result_list[0]['falls'] is not None:
                    self.detail_window.ui.falls.setText(result_list[0]['falls'])
                if result_list[0]['VYE'] is not None:
                    self.detail_window.ui.VYE.setText(result_list[0]['VYE'])
                if result_list[0]['pressure_ulcers'] is not None:
                    self.detail_window.ui.pressure_ulcers.setText(result_list[0]['pressure_ulcers'])
                if result_list[0]['intake_output'] is not None:
                    self.detail_window.ui.intake_output.setText(result_list[0]['intake_output'])
                self.detail_window.show()
                if self.tableView.model().item(selected_index.row(), 0) is not None:
                    beds_number = self.tableView.model().item(selected_index.row(), 0).text()
                    beds_id = re.search(r'\d+', beds_number).group()
                    conn = sqlite3.connect('DB_SBAR.db')
                    cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (beds_id,))
                    results = cursor.fetchall()
                    self.detail_window.ui.pushButton.setText("确认修改")
                    for row in results:
                        print(row[0])
                    # 把实例化对象传给on——submit_clicked方法中
                    self.detail_window.ui.label.setText(beds_number)
                    self.detail_window.ui.pushButton.clicked.connect(
                    self.detail_window.on_submit_clicked)  # 调用方法,当使用 clicked.connect() 连接槽函数时，你不能直接传递参数给槽函数。相反，你需要使用 lambda 函数
                    self.detail_window.show()
            else:
                QMessageBox.information(self, "错误", f"{beds_number}位还没有病人，你可以试试添加", QMessageBox.Ok)
        conn.close()

        print("修改")

    def del_detail(self):
        #移除床位关联病人的ID--使ID填到字段历史ID中。增加移除时间，空出床位
        selected_index = self.tableView.currentIndex()
        beds_number = self.tableView.model().item(selected_index.row(), 0).text()
        beds_id = re.search(r'\d+', beds_number).group()
        conn = sqlite3.connect('DB_SBAR.db')
        cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (beds_id,))
        results = cursor.fetchall()
        for row in results:
            print(row[0])
        if row[0] is not None:
            reply = QMessageBox.question(self, '错误', f'即将移除{beds_id}号床位的病人,是否继续',
                                         QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            # 判断用户的响应
            if reply == QMessageBox.Ok:
                # 用户点击了确认按钮
                # 执行相应的操作
                try:
                    conn.execute("UPDATE patient SET bed_ID =? where id=(SELECT patient_id FROM Bed b LEFT JOIN Patient a ON b.patient_id = a.id WHERE b.id = ?);", (beds_id+"号床",beds_id))
                    conn.commit()
                    try:
                        cursor = conn.execute("UPDATE Bed SET patient_id = NULL WHERE bed_number =?;", (beds_id,))
                        conn.commit()
                        self.load_data()
                    except Exception as e:
                        QMessageBox.information(self, "错误", f"删除病人错误！", QMessageBox.Ok)
                except Exception as e:
                    QMessageBox.information(self, "错误", f"更新历史床位错误！", QMessageBox.Ok)
                    pass

            else:
                return
        else:
            QMessageBox.information(self, "错误", f"{beds_number}位还没有病人，你可以试试添加", QMessageBox.Ok)
        conn.close()
    #右键查看病人信息
    def show_detail(self):
        selected_index = self.tableView.currentIndex()
        self.detail_window = AddPatientViewer(self)
        self.detail_window.ui.pushButton.hide()
        if self.tableView.model().item(selected_index.row(), 0) is not None:
            beds_number = self.tableView.model().item(selected_index.row(), 0).text()
            number_only = re.search(r'\d+', beds_number).group()
            self.detail_window.ui.label.setText(beds_number)
            conn = sqlite3.connect('DB_SBAR.db')
            cursor = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (number_only,))
            results = cursor.fetchall()
            for row in results:
                print(row[0])
            if row[0] is not None:
                query_path = "./sqllite/select_bed_id.sql"
                query = read_query_file(query_path)
                cursor = conn.execute(query,(number_only,))
                rows = cursor.fetchall()
                result_list = []
                columns = [description[0] for description in cursor.description]
                # 遍历每一行
                for row in rows:
                    # 将每一行的数据与字段名组合成字典
                    row_dict = dict(zip(columns, row))
                    # 将字典添加到结果列表中
                    result_list.append(row_dict)
                if result_list[0]['name'] is not None:
                    self.detail_window.ui.username.setText(result_list[0]['name'])
                if result_list[0]['age'] is not None:
                    self.detail_window.ui.age.setText(str(result_list[0]['age']))
                if result_list[0]['gender'] is not None:
                    self.detail_window.ui.gender.setText(result_list[0]['gender'])
                if result_list[0]['admission_date'] is not None:
                    text_date=result_list[0]['admission_date']
                    self.detail_window.ui.admission_date.setDate(datetime.strptime(text_date, "%Y-%m-%d"))
                if result_list[0]['chief_complaint'] is not None:
                    self.detail_window.ui.chief_complaint.setText(result_list[0]['chief_complaint'])
                if result_list[0]['note'] is not None:
                    self.detail_window.ui.note.setText(result_list[0]['note'])
                if result_list[0]['important_disposal'] is not None:
                    self.detail_window.ui.important_disposal.setText(result_list[0]['important_disposal'])
                if result_list[0]['medical_history'] is not None:
                    self.detail_window.ui.medical_history.setText(result_list[0]['medical_history'])
                if result_list[0]['positive_results'] is not None:
                    self.detail_window.ui.positive_results.setText(result_list[0]['positive_results'])
                if result_list[0]['physical_examination'] is not None:
                    self.detail_window.ui.physical_examination.setText(result_list[0]['physical_examination'])
                if result_list[0]['critical_value'] is not None:
                    self.detail_window.ui.critical_value.setText(result_list[0]['critical_value'])
                if result_list[0]['vital_signs'] is not None:
                    self.detail_window.ui.vital_signs.setText(result_list[0]['vital_signs'])
                if result_list[0]['bleeding'] is not None:
                    self.detail_window.ui.bleeding.setText(result_list[0]['bleeding'])
                if result_list[0]['pain'] is not None:
                    self.detail_window.ui.pain.setText(result_list[0]['pain'])
                if result_list[0]['urinarycatheter'] is not None:
                    self.detail_window.ui.urinarycatheter.setText(result_list[0]['urinarycatheter'])
                if result_list[0]['drainagetube'] is not None:
                    self.detail_window.ui.drainagetube.setText(result_list[0]['drainagetube'])
                if result_list[0]['stoma'] is not None:
                    self.detail_window.ui.stoma.setText(result_list[0]['stoma'])
                if result_list[0]['self_care'] is not None:
                    self.detail_window.ui.self_care.setText(result_list[0]['self_care'])
                if result_list[0]['falls'] is not None:
                    self.detail_window.ui.falls.setText(result_list[0]['falls'])
                if result_list[0]['VYE'] is not None:
                    self.detail_window.ui.VYE.setText(result_list[0]['VYE'])
                if result_list[0]['pressure_ulcers'] is not None:
                    self.detail_window.ui.pressure_ulcers.setText(result_list[0]['pressure_ulcers'])
                if result_list[0]['intake_output'] is not None:
                    self.detail_window.ui.intake_output.setText(result_list[0]['intake_output'])
                self.detail_window.show()
            else:
                QMessageBox.information(self, "错误", f"{beds_number}位还没有病人，你可以试试添加", QMessageBox.Ok)
        conn.close()
        print("查看")
    #用于处理右键菜单事件
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())
    def load_data(self):
        if os.path.exists('./sqllite/DB_SBAR.db'):
            conn = sqlite3.connect('DB_SBAR.db')
        else:
            db_manager = DatabaseManager()
            db_manager.create_database()
            conn = sqlite3.connect('DB_SBAR.db')
        query_path = "./sqllite/select.sql"
        query = read_query_file(query_path)
        model = QtGui.QStandardItemModel()
        cursor = conn.execute(query)
        header = [description[0] for description in cursor.description]
        model.setHorizontalHeaderLabels(header)
        font = QFont("微软雅黑", 13)  # 设置字体样式
        font2 = QFont("宋体", 12)  # 设置字体样式
        for row_num, row_data in enumerate(cursor, start=1):
            for col_num, col_data in enumerate(row_data):
                if col_data is not None:
                    item = QtGui.QStandardItem(str(col_data))
                    if col_num == 0:
                        item.setText(f"{col_data}号床")
                        item.setFont(font)
                        # item.setBackground(QColor("lightblue"))
                    item.setToolTip(str(col_data))
                    item.setFont(font2)
                    model.setItem(row_num - 1, col_num, item)
        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        conn.close()
class AddPatientViewer(QtWidgets.QMainWindow, Ui_addPatientViewer):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_addPatientViewer()
        self.ui.setupUi(self)
        self.main_window = main_window
    def on_submit_clicked(self):
        bed_number = self.ui.label.text()
        bed_id_value = re.search(r'\d+', bed_number).group()
        # 获取各个输入框的内容并打印出来
        name_value = self.ui.username.toPlainText()
        # 加判断，添加的人名字不能为空
        if name_value=='':
            QMessageBox.information(self, "错误", f"病人姓名不能为空", QMessageBox.Ok)
        else:
            age_value = self.ui.age.toPlainText()
            gender_value = self.ui.gender.toPlainText()
            admission_date_value = self.ui.admission_date.date().toString("yyyy-MM-dd")
            chief_complaint_value = self.ui.chief_complaint.toPlainText()
            important_disposal_value = self.ui.important_disposal.toPlainText()
            physical_examination_value = self.ui.physical_examination.toPlainText()
            critical_value_value = self.ui.critical_value.toPlainText()
            positive_results_value = self.ui.positive_results.toPlainText()
            medical_history_value = self.ui.medical_history.toPlainText()
            vital_signs_value = self.ui.vital_signs.toPlainText()
            self_care_value = self.ui.self_care.toPlainText()
            pressure_ulcers_value = self.ui.pressure_ulcers.toPlainText()
            falls_value = self.ui.falls.toPlainText()
            VYE_value = self.ui.VYE.toPlainText()
            bleeding_value = self.ui.bleeding.toPlainText()
            pain_value = self.ui.pain.toPlainText()
            urinarycatheter_value = self.ui.urinarycatheter.toPlainText()
            drainagetube_value = self.ui.drainagetube.toPlainText()
            stoma_value = self.ui.stoma.toPlainText()
            intake_output_value = self.ui.intake_output.toPlainText()
            note_value = self.ui.note.toPlainText()
            conn = sqlite3.connect('DB_SBAR.db')
            try:
                conn.execute(
                    "INSERT INTO Patient (`name`, age, gender, admission_date, note, chief_complaint, important_disposal, medical_history, positive_results, physical_examination, critical_value, vital_signs, bleeding, pain, urinarycatheter, drainagetube, stoma, intake_output, self_care, falls, pressure_ulcers, VYE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name_value, age_value, gender_value, admission_date_value, note_value, chief_complaint_value,
                     important_disposal_value, medical_history_value, positive_results_value, physical_examination_value,
                     critical_value_value, vital_signs_value, bleeding_value, pain_value, urinarycatheter_value,
                     drainagetube_value, stoma_value, intake_output_value, self_care_value, falls_value, pressure_ulcers_value,
                     VYE_value))
                conn.commit()  # 提交事务
                print("插入成功")
                # 执行查询
                cursor = conn.execute("SELECT MAX(id) FROM Patient;")
                # 获取所有行
                results = cursor.fetchall()
                # 输出结果
                for row in results:
                    print(row[0], bed_id_value)
                conn.execute("UPDATE Bed SET patient_id =? WHERE id =?", (row[0], bed_id_value))
                conn.commit()  # 提交事务
                conn.close()
                self.main_window.load_data()
                self.close()
            #还要刷新表格
            except sqlite3.Error as e:
                print("插入失败:", e)
        conn.close()
class ksPatientViewer(QtWidgets.QMainWindow,Ui_kshc):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_kshc()
        self.ui.setupUi(self)
        self.main_window = main_window
        # 访问comboBox_dq
        self.comboBox_dq = self.ui.comboBox_dq
        self.comboBox_gh = self.ui.comboBox_gh
        self.pushButton = self.ui.pushButton
        self.pushButton_2 = self.ui.pushButton_2
        self.comboBox_gh.setStyleSheet("font: 12pt \"宋体\";")
        self.comboBox_dq.setStyleSheet("font: 12pt \"宋体\";")
    def Oks(self):
        #同床位不能换，其中一个没选不能换
        conn = sqlite3.connect('DB_SBAR.db')
        dq = self.comboBox_dq.currentText()
        gh = self.comboBox_gh.currentText()
        if gh == "--请选择--":
            QMessageBox.information(self, "错误", f"你还没有选择床位！", QMessageBox.Ok)
        elif dq==gh:
            QMessageBox.information(self, "错误", f"当前床位不能和更换床位一样", QMessageBox.Ok)
        else:
            try:
                beds_id_dq = re.search(r'\d+', dq).group()
                cursor_dq = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (beds_id_dq,))
                results = cursor_dq.fetchall()
                # 输出结果
                for row in results:
                    row_dq = row[0]
                beds_id_gh = re.search(r'\d+', gh).group()
                cursor_gh = conn.execute("SELECT patient_id FROM Bed WHERE id=?;", (beds_id_gh,))
                results = cursor_gh.fetchall()
                for row in results:
                    row_gh = row[0]
                print("当前病人",row_dq,"更换病人",row_gh,"当前床位",beds_id_dq,"更换床位",beds_id_gh)
                if row_gh is None and row_dq is None:
                    QMessageBox.warning(self, "错误", f"两个床位不能都没有病人", QMessageBox.Ok)
                elif row_gh is None and row_dq is not None:
                    #更换为空，当前有人，需要把当前床位的病人移到 更换床位
                    conn.execute("UPDATE Bed SET patient_id=? where id=?;", (row_dq, beds_id_gh))
                    conn.execute("UPDATE Bed SET patient_id=NULL where id=?;", (beds_id_dq))
                    conn.commit()
                    self.main_window.load_data()
                    pass
                elif row_dq is None and row_gh is not None:
                    #当前床位为空，更换有人，需要把更换的移到当前
                    conn.execute("UPDATE Bed SET patient_id=? where id=?;", (row_gh, beds_id_dq))
                    conn.execute("UPDATE Bed SET patient_id=NULL where id=?;", (beds_id_gh))
                    conn.commit()
                    self.main_window.load_data()
                    pass
                elif row_dq is not  None and row_gh is not None:
                    #当前有人，更换有人，需要互相移动
                    conn.execute("UPDATE Bed SET patient_id=? where id=?;", (row_dq, beds_id_gh))
                    conn.execute("UPDATE Bed SET patient_id=? where id=?;", (row_gh, beds_id_dq))
                    conn.commit()
                    self.main_window.load_data()
                else:
                    QMessageBox.warning(self, "错误", f"触发隐藏BUG", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"查询床位信息时出错：{str(e)}", QMessageBox.Ok)
                return
        conn.close()
        self.close()
    def cls(self):
        self.close()

def read_query_file(query_path):
    with open(query_path, 'r', encoding='utf-8') as file:
        return file.read()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = PatientViewerApp()
    main_window.load_data()
    main_window.show()
    sys.exit(app.exec_())
