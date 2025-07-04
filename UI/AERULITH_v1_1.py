from PySide6.QtCore import (QMetaObject, QRect, QSize, Qt, QTimer)
from PySide6.QtGui import (QFont, QIcon, QPixmap)
from PySide6.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QLCDNumber, QLabel, QPlainTextEdit, QProgressBar, QScrollArea, 
                               QSizePolicy, QDoubleSpinBox, QStatusBar, QVBoxLayout, QWidget)
import random

# U I    F R A M E W O R K
class MainWindow(object):
    def UI_Setup(self, Main_Window):
        Main_Window.resize(1182,462)

        #F O N T S
        font_ul = QFont()
        font_ul.setFamilies(["Terminal"])
        font_ul.setPointSize(12)
        font_ul.setUnderline(True)

        font_nl = QFont()
        font_nl.setFamilies(["Terminal"])
        font_nl.setPointSize(12)
        font_nl.setUnderline(False)
        #I M A G E  F R A M E S
        self.blink_frames = [QPixmap(f"Animations/Blink/{i}.png").copy(113,40,160,215).scaled(300,403) for i in range(5)]

        #I C O N
        icon = QIcon()
        icon.addFile("Icons/Tamicon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Main_Window.setWindowIcon(icon)
    
        #O U T E R     H O R I Z O N T A L     L A Y O U T
        self.outer_widget = QWidget(Main_Window)
        self.main_horizontal_layout = QHBoxLayout(self.outer_widget)
        
        #L E F T    C O L U M N
        self.left_column = QWidget(self.outer_widget)
        self.left_inner_vertical_layout = QVBoxLayout(self.left_column)
        self.image_label = QGroupBox(self.left_column)
        self.image_label.setFont(font_ul)
        self.image = QLabel(self.image_label)
        self.image.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setGeometry(QRect(75,20,300,403))
        self.stats_label = QGroupBox(self.left_column)
        self.stats_label.setFont(font_ul)
        self.stats_layout = QGridLayout(self.stats_label)
        self.level_label = QLabel(self.stats_label)
        self.level_label.setFont(font_ul)
        self.level_lcd = QLCDNumber(self.stats_label)
        self.level_lcd.setFont(font_nl)
        self.level_progress = QProgressBar(self.stats_label)
        self.mood_label = QLabel(self.stats_label)
        self.mood_label.setFont(font_ul)
        self.mood_value = QLabel(self.stats_label)
        self.mood_value.setFont(font_nl)
        self.action_label = QLabel(self.stats_label)
        self.action_label.setFont(font_ul)
        self.action_value = QLabel(self.stats_label)
        self.action_value.setFont(font_nl)
        self.persona_label = QLabel(self.stats_label)
        self.persona_label.setFont(font_ul)
        self.persona_value = QLabel(self.stats_label)
        self.persona_value.setFont(font_nl)
    
        self.stats_layout.addWidget(self.level_label,0,0,1,1)
        self.stats_layout.addWidget(self.level_lcd,0,1,1,1)
        self.stats_layout.addWidget(self.level_progress,1,0,1,2)
        self.stats_layout.addWidget(self.mood_label,2,0,1,1)
        self.stats_layout.addWidget(self.mood_value,2,1,1,1)
        self.stats_layout.addWidget(self.action_label,3,0,1,1)
        self.stats_layout.addWidget(self.action_value,3,1,1,1)
        self.stats_layout.addWidget(self.persona_label,4,0,1,1)
        self.stats_layout.addWidget(self.persona_value,4,1,1,1)
        self.stats_layout.setColumnStretch(0, 1)
        self.stats_layout.setColumnStretch(1, 2)

        self.left_inner_vertical_layout.addWidget(self.image_label)
        self.left_inner_vertical_layout.addWidget(self.stats_label)

        #C E N T E R    C O L U M N
        self.center_column = QWidget(self.outer_widget)
        self.center_vertical_layout = QVBoxLayout(self.center_column)
        self.output_label = QGroupBox(self.center_column)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.output_label.setFont(font_ul)
        self.output_inner_layout = QVBoxLayout(self.output_label)
        self.chatbox = QScrollArea(self.output_label)
        self.chatbox.setFont(font_nl)
        self.chatbox.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setFont(font_nl)
        self.scroll_widget.setGeometry(QRect(0,0,344,269))
        self.chatbox.setWidget(self.scroll_widget)
        self.output_inner_layout.addWidget(self.chatbox)

        self.input_label = QGroupBox(self.center_column)
        self.input_label.setFont(font_ul)
        self.center_input_inner_layout = QVBoxLayout(self.input_label)
        self.input_value = QPlainTextEdit(self.input_label)
        self.input_value.setFont(font_nl)
        self.center_input_inner_layout.addWidget(self.input_value)

        self.center_vertical_layout.addWidget(self.output_label)
        self.center_vertical_layout.addWidget(self.input_label)
        self.center_vertical_layout.setStretch(0, 4)
        self.center_vertical_layout.setStretch(1, 1)

        #C H A T H E L P E R
        #self.chat_helper()


        #R I G H T      C O L U M N
        self.right_column = QWidget(self.outer_widget)
        self.right_grid_layout = QGridLayout(self.right_column)
        
        self.error_label = QLabel(self.right_column)
        self.error_label.setFont(font_ul)
        self.error_value = QLCDNumber(self.right_column)
        self.error_value.setFont(font_nl)

        self.model_label = QLabel(self.right_column)
        self.model_label.setFont(font_ul)
        self.model_value = QLabel(self.right_column)
        self.model_value.setFont(font_nl)

        self.confidence_label = QLabel(self.right_column)
        self.confidence_label.setFont(font_ul)
        self.confidence_value = QLCDNumber(self.right_column)
        self.confidence_value.setFont(font_nl)

        self.temp_label = QLabel(self.right_column)
        self.temp_label.setFont(font_ul)
        self.temp_value = QDoubleSpinBox(self.right_column)
        self.temp_value.setMinimumWidth(100)
        self.temp_value.setRange(0.0, 1.0)
        self.temp_value.setSingleStep(0.05)
        self.temp_value.setDecimals(2)

        self.top_p_label = QLabel(self.right_column)
        self.top_p_label.setFont(font_ul)
        self.top_p_value = QDoubleSpinBox(self.right_column)
        self.top_p_value.setMinimumWidth(100)
        self.top_p_value.setRange(0.0, 1.0)
        self.top_p_value.setSingleStep(0.05)
        self.top_p_value.setDecimals(2)

        self.module_box = QGroupBox(self.right_column)
        self.module_box.setFont(font_ul)
        self.module_box_layout = QHBoxLayout(self.module_box)
        self.modules_value = QScrollArea(self.module_box)
        self.modules_value.setFont(font_nl)
        self.module_scroll = QWidget()
        self.module_scroll.setFont(font_nl)
        self.module_scroll.setGeometry(QRect(0,0,344,54))
        self.modules_value.setWidget(self.module_scroll)
        self.module_box_layout.addWidget(self.modules_value)

        self.CTL_box = QGroupBox(self.right_column)
        self.CTL_box.setFont(font_ul)
        self.CTL_horizontal_layout = QHBoxLayout(self.CTL_box)
        self.CTL_value = QScrollArea(self.CTL_box)
        self.CTL_value.setFont(font_nl)
        self.CTL_value.setWidgetResizable(True)
        self.CTL_scrollbox = QWidget()
        self.CTL_scrollbox.setFont(font_nl)
        self.CTL_scrollbox.setGeometry(0,0,344,133)
        self.CTL_value.setWidget(self.CTL_scrollbox)
        self.CTL_horizontal_layout.addWidget(self.CTL_value)

        self.right_grid_layout.addWidget(self.CTL_box,0,0,1,2)
        self.right_grid_layout.addWidget(self.model_label,1,0,1,1)
        self.right_grid_layout.addWidget(self.model_value,1,1,1,1)
        self.right_grid_layout.addWidget(self.confidence_label,2,0,1,1)
        self.right_grid_layout.addWidget(self.confidence_value,2,1,1,1)
        self.right_grid_layout.addWidget(self.error_label,3,0,1,1)
        self.right_grid_layout.addWidget(self.error_value,3,1,1,1)
        self.right_grid_layout.addWidget(self.temp_label,4,0,1,1)
        self.right_grid_layout.addWidget(self.temp_value,4,1,1,1)
        self.right_grid_layout.addWidget(self.top_p_label,5,0,1,1)
        self.right_grid_layout.addWidget(self.top_p_value,5,1,1,1)
        self.right_grid_layout.addWidget(self.module_box,6,0,1,2)
        
        self.right_grid_layout.setRowStretch(0,10)
        self.right_grid_layout.setColumnStretch(0, 1)

        self.main_horizontal_layout.addWidget(self.left_column)
        self.main_horizontal_layout.addWidget(self.center_column)
        self.main_horizontal_layout.addWidget(self.right_column)
        self.main_horizontal_layout.setStretch(0,1)
        self.main_horizontal_layout.setStretch(1,1)
        self.main_horizontal_layout.setStretch(2,1)
        Main_Window.setCentralWidget(self.outer_widget)
        self.statusbar = QStatusBar(Main_Window)
        Main_Window.setStatusBar(self.statusbar)
        self.UI_Namer(Main_Window)
        QMetaObject.connectSlotsByName(Main_Window)


    # def next_frame(self,typeframe):
    #     self.image.setPixmap(typeframe[self.image_index])
    #     if self.image_index == len(typeframe)-1:
    #         self.image_animation_timer.stop()
    #         QTimer.singleShot(1500+random.randint(500,1000),self.image_animation_timer.start)

    #     self.image_index = (self.image_index + 1) % len(typeframe)

    def UI_Namer(self, Main_Window):
        Main_Window.setWindowTitle("AERULITH | A Phazite™ Construct")
        self.image_label.setTitle("T.A.M.A")
        self.stats_label.setTitle("Stats:")
        self.level_label.setText("Level:")
        self.mood_label.setText("Mood:")
        self.mood_value.setText("Happy")
        self.persona_label.setText("Behavioral Core:")
        self.persona_value.setText("Sentrix v1.0")
        self.action_label.setText("Current Action:")
        self.action_value.setText("Browsing")
        self.output_label.setTitle("Core Output")
        self.input_label.setTitle("Enter Your Prompt")
        self.error_label.setText("Error%")
        self.confidence_label.setText("Confidence%")
        self.model_value.setText("NACJAC Series v1.3")
        self.temp_label.setText("Temp")
        self.module_box.setTitle("Current Modules")
        self.CTL_box.setTitle("Cognitive Track Log")
        self.model_label.setText("Current Model")
        self.top_p_label.setText("Top P")
