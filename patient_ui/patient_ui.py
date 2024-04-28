from PyQt5 import QtCore, QtWidgets


class Ui_PatientViewer(object):
    def setupUi(self, PatientViewer):
        PatientViewer.setObjectName("PatientViewer")
        PatientViewer.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(PatientViewer)
        self.centralwidget.setObjectName("centralwidget")

        # 垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # 添加水平布局1
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.verticalLayout.addLayout(self.horizontalLayout_1)

        # 添加下拉框
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        # 添加自定义数据源
        # self.comboBox.addItems([])  # 自定义数据源
        self.comboBox.setFixedWidth(150)
        self.horizontalLayout_1.addWidget(self.comboBox)

        # 添加搜索按钮
        self.search_button = QtWidgets.QPushButton("恢复默认", self.centralwidget)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_1.addWidget(self.search_button)

        self.add_button = QtWidgets.QPushButton("增加空床位", self.centralwidget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_1.addWidget(self.add_button)

        self.del_button = QtWidgets.QPushButton("移除空床位", self.centralwidget)
        self.del_button.setObjectName("del_button")
        self.horizontalLayout_1.addWidget(self.del_button)

        # 添加弹性容器
        spacerItem = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem)

        # 添加导出按钮
        self.export_button = QtWidgets.QPushButton("导出为Excel", self.centralwidget)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout_1.addWidget(self.export_button)
        self.export_button2 = QtWidgets.QPushButton("导出为Excel(历史记录)", self.centralwidget)
        self.export_button2.setObjectName("export_button")
        self.horizontalLayout_1.addWidget(self.export_button2)

        # 添加水平布局2
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # 添加表格视图
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.tableView.setAlternatingRowColors(True)  # 启用交替行颜色
        self.horizontalLayout_2.addWidget(self.tableView)

        PatientViewer.setCentralWidget(self.centralwidget)
        self.retranslateUi(PatientViewer)
        QtCore.QMetaObject.connectSlotsByName(PatientViewer)

        # 设置表格头样式和列移动功能
        self.setupTableStylesAndFeatures()

    def setupTableStylesAndFeatures(self):
        # 设置横向表格头样式
        self.tableView.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                border-top: 0px solid #E5E5E5;
                border-left: 0px solid #E5E5E5;
                border-right: 0.5px solid #E5E5E5;
                border-bottom: 0.5px solid #E5E5E5;
                background-color: white;
                padding: 4px;
            }
        """)
        # 设置纵向表格头样式
        self.tableView.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                border-top: 0px solid #E5E5E5;
                border-left: 0px solid #E5E5E5;
                border-right: 0.5px solid #E5E5E5;
                border-bottom: 0.5px solid #E5E5E5;
                background-color: white;
                padding: 4px;
            }
        """)
        # 设置左上角格子样式
        self.tableView.verticalHeader().setStyleSheet("""
            QTableCornerButton::section {
                border-top: 0px solid #E5E5E5;
                border-left: 0px solid #E5E5E5;
                border-right: 0.5px solid #E5E5E5;
                border-bottom: 0.5px solid #E5E5E5;
                background-color: white;
            }
        """)

    def retranslateUi(self, PatientViewer):
        _translate = QtCore.QCoreApplication.translate
        PatientViewer.setWindowTitle(_translate("PatientViewer", "SBAR系统"))
