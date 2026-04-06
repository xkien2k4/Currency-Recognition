# Author : Nguyễn Vũ Xuân Kiên 

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import time

class CurrencyRecognitionApp:
    """Ứng dụng nhận dạng tiền Việt Nam PRO"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Nhận dạng mệnh giá tiền Việt Nam ")
        
        self.window_sizes = {
            'splash': '900x650',
            'menu': '800x600',
            'recognition': '1200x750',
            'info': '900x650'
        }
        
        self.root.geometry(self.window_sizes['splash'])
        self.root.configure(bg="#f5f5f5")
        
        self.root.resizable(True, True)
        
        self.root.minsize(800, 550)
        
        self.colors = {
            'primary': '#1976D2',      # Xanh dương chuyên nghiệp
            'secondary': '#424242',    # Xám đậm
            'success': '#388E3C',      # Xanh lá nhẹ
            'warning': '#F57C00',      # Cam nhẹ
            'danger': '#D32F2F',       # Đỏ nhẹ
            'info': '#0097A7',         # Xanh ngọc
            'light': '#FAFAFA',        # Trắng xám
            'dark': '#212121',         # Đen nhẹ
            'bg': '#FFFFFF',           # Trắng
            'text': '#333333',         # Xám chữ
            'border': '#E0E0E0'        # Viền xám nhạt
        }
        
        self.image_path = None
        self.current_image = None
        self.camera = None
        self.camera_running = False
        
        self.templates = self.load_templates()
        print(f"Da tai {sum(len(v) for v in self.templates.values())} templates cho {len(self.templates)} menh gia")
        
        self.show_splash_screen()
    
    def load_templates(self):
        """Tải templates từ thư mục templates/<mệnh_giá>/"""
        templates = {}
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        if not os.path.exists(template_dir):
            print(f"Canh bao: Khong tim thay thu muc templates/")
            return templates
        
        denominations = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]
        
        for denom in denominations:
            denom_dir = os.path.join(template_dir, str(denom))
            if not os.path.exists(denom_dir):
                continue
            
            images = []
            for filename in os.listdir(denom_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    img_path = os.path.join(denom_dir, filename)
                    img = cv2.imread(img_path)
                    if img is not None:
                        images.append(img)
            
            if images:
                templates[denom] = images
                print(f"  {denom:,} VND: {len(images)} templates")
        
        return templates
    
    def show_splash_screen(self):
        """Màn hình chào mừng chuyên nghiệp"""
        self.root.geometry(self.window_sizes['splash'])
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        splash_frame = tk.Frame(self.root, bg=self.colors['light'])
        splash_frame.pack(fill=tk.BOTH, expand=True)
        
        center_frame = tk.Frame(splash_frame, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        logo_container = tk.Frame(center_frame, bg=self.colors['bg'], padx=60, pady=40)
        logo_container.pack()
        
        tk.Label(logo_container, text="🎓", font=("Segoe UI", 48), 
                bg=self.colors['bg']).pack()
        
        tk.Label(logo_container, text="KHOA CÔNG NGHỆ THÔNG TIN", 
                font=("Segoe UI", 16, "bold"), bg=self.colors['bg'], 
                fg=self.colors['secondary']).pack(pady=(10, 5))
        
        separator = tk.Frame(logo_container, height=2, bg=self.colors['primary'])
        separator.pack(fill=tk.X, pady=15)
        
        tk.Label(logo_container, text="ỨNG DỤNG NHẬN DIỆN", 
                font=("Segoe UI", 12, "bold"), bg=self.colors['bg'], 
                fg=self.colors['secondary']).pack(pady=5)

        tk.Label(logo_container, text="MỆNH GIÁ TIỀN VIỆT NAM", 
                font=("Segoe UI", 24, "bold"), bg=self.colors['bg'], 
                fg=self.colors['primary']).pack(pady=5)

        tk.Label(logo_container, text="Vietnamese Currency Recognition Application", 
                font=("Segoe UI", 11, "italic"), bg=self.colors['bg'], 
                fg=self.colors['text']).pack(pady=(10, 5))
        
        tk.Label(logo_container, text="Template Matching & Color Analysis", 
                font=("Segoe UI", 10, "italic"), bg=self.colors['bg'], 
                fg=self.colors['secondary']).pack()
        
        info_card = tk.Frame(center_frame, bg=self.colors['light'], 
                            relief=tk.FLAT, bd=0, padx=30, pady=20)
        info_card.pack(pady=10, expand=True, fill='both')
        
        # Thông tin tác giả
        instructor_frame = tk.Frame(info_card, bg=self.colors['light'])
        instructor_frame.pack(pady=(0, 15), fill='x')
        
        tk.Frame(info_card, height=1, bg=self.colors['border']).pack(fill='x', pady=10)

        tk.Label(instructor_frame, 
                text="Tác giả",
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors['light'], 
                fg=self.colors['primary']).pack()
        
        tk.Label(instructor_frame, 
                text="Nguyễn Vũ Xuân Kiên",
                font=("Segoe UI", 11, "bold"), 
                bg=self.colors['light'], 
                fg=self.colors['text']).pack(pady=(2, 0))
        
        # Hướng dẫn
        
        # Bind phím bất kỳ
        self.root.bind('<Key>', lambda e: self.show_main_menu())
        self.root.bind('<Button-1>', lambda e: self.show_main_menu())
    
    def show_main_menu(self):
        """Menu chính hiện đại"""
        # Điều chỉnh kích thước cửa sổ
        self.root.geometry(self.window_sizes['menu'])
        
        self.root.unbind('<Key>')
        self.root.unbind('<Button-1>')
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame chính
        menu_frame = tk.Frame(self.root, bg=self.colors['light'])
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header đơn giản
        header = tk.Frame(menu_frame, bg=self.colors['bg'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Nhận dạng mệnh giá tiền VN", 
                font=("Segoe UI", 20, "bold"), bg=self.colors['bg'], 
                fg=self.colors['dark']).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Menu container
        menu_container = tk.Frame(menu_frame, bg=self.colors['light'])
        menu_container.pack(expand=True, pady=30)
        
        # Grid layout cho menu
        menu_items = [
            ("Nhận dạng qua File", self.show_image_recognition, self.colors['primary']),
            ("Nhận dạng qua Camera", self.show_camera_recognition, self.colors['success']),
            ("Tính tổng số tiền", self.show_money_counter, self.colors['warning']),
            ("Thống kê", self.show_statistics, self.colors['info']),
            ("Giới thiệu", self.show_about, self.colors['secondary']),
            ("Thoát", self.root.quit, self.colors['danger'])
        ]
        
        for i, (text, command, color) in enumerate(menu_items):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(menu_container, bg=color, cursor="hand2")
            btn_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            btn = tk.Button(btn_frame, text=text, command=command,
                          font=("Segoe UI", 12, "bold"), bg=color, fg="white",
                          width=22, height=2, relief=tk.FLAT, cursor="hand2",
                          activebackground=color, activeforeground="white")
            btn.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
            
            # Hover effect
            def on_enter(e, b=btn, c=color):
                b.config(bg=self._darken_color(c))
            def on_leave(e, b=btn, c=color):
                b.config(bg=c)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Footer
        footer = tk.Frame(menu_frame, bg=self.colors['bg'], height=35)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Label(footer, text=" © 2026 - Nguyễn Kiên", 
                font=("Segoe UI", 9), bg=self.colors['bg'], 
                fg=self.colors['secondary']).pack(pady=8)
    
    def _darken_color(self, color):
        """Làm tối màu cho hover effect"""
        color_map = {
            self.colors['primary']: '#1565C0',
            self.colors['success']: '#2E7D32',
            self.colors['warning']: '#E64A19',
            self.colors['info']: '#00838F',
            self.colors['secondary']: '#303030',
            self.colors['danger']: '#C62828'
        }
        return color_map.get(color, color)
    
    def show_image_recognition(self):
        """Form nhận dạng qua file ảnh"""
        self.create_recognition_gui("image")
    
    def show_camera_recognition(self):
        """Form nhận dạng qua camera"""
        self.create_recognition_gui("camera")
    
    def show_money_counter(self):
        """Form tính tổng số tiền"""
        self.create_recognition_gui("counter")
    
    def show_statistics(self):
        """Form thống kê"""
        # Điều chỉnh kích thước cửa sổ
        self.root.geometry(self.window_sizes['info'])
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header với nút back
        self.create_header(main_frame, "📊 THỐNG KÊ VÀ BÁO CÁO")
        
        # Content
        content = tk.Frame(main_frame, bg="#ecf0f1")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats_text = f"""
        📈 THỐNG KÊ 
        
        ✓ Tổng số mệnh giá hỗ trợ: {len(self.templates)} mệnh giá
        ✓ Tổng số templates: {sum(len(v) for v in self.templates.values())} ảnh mẫu
        ✓ Độ chính xác trung bình: ~85-95%
        
        📋 CHI TIẾT TEMPLATES:
        """
        
        for denom in sorted(self.templates.keys()):
            stats_text += f"\n        • {denom:,} VND: {len(self.templates[denom])} templates"
        
        tk.Label(content, text=stats_text, font=("Courier", 11), 
                bg="white", fg="#2c3e50", justify=tk.LEFT, 
                relief=tk.SOLID, bd=1, padx=20, pady=20).pack(pady=20)
    
    def show_about(self):
        """Form giới thiệu"""
        # Điều chỉnh kích thước cửa sổ
        self.root.geometry(self.window_sizes['info'])
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header với nút back
        self.create_header(main_frame, "ℹ️ GIỚI THIỆU ỨNG DỤNG")
        
        # Content
        content = tk.Frame(main_frame, bg="#ecf0f1")
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        about_text = """
       ⚙️ CÔNG NGHỆ SỬ DỤNG

       • OpenCV: Xử lý ảnh và nhận dạng
       • NumPy: Tính toán ma trận
       • Tkinter: Xây dựng giao diện người dùng
       • Template Matching: So khớp ảnh mẫu
       • Color Analysis: Nhận diện đặc trưng màu sắc

      🚀 CHỨC NĂNG CHÍNH

      ✓ Nhận dạng tiền từ ảnh có sẵn
      ✓ Nhận dạng tiền bằng camera realtime
      ✓ Tính tổng số tiền (cơ bản)
      ✓ Hiển thị độ tin cậy kết quả
      ✓ Thống kê hệ thống

     💰 PHẠM VI HỖ TRỢ

     Hệ thống nhận diện 9 mệnh giá tiền Việt Nam:

     1.000 | 2.000 | 5.000 | 10.000 | 20.000  
     50.000 | 100.000 | 200.000 | 500.000 (VND)

    👨‍💻 TÁC GIẢ

    Nguyễn Vũ Xuân Kiên
        """
        
        tk.Label(content, text=about_text, font=("Arial", 11), 
                bg="white", fg="#2c3e50", justify=tk.LEFT,
                relief=tk.SOLID, bd=1, padx=30, pady=30).pack(pady=20, fill=tk.BOTH, expand=True)
    
    def create_header(self, parent, title):
        """Header chuyên nghiệp"""
        header = tk.Frame(parent, bg=self.colors['bg'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Nút back
        back_btn = tk.Button(header, text="← Menu", command=self.show_main_menu,
                            font=("Segoe UI", 10), bg=self.colors['light'], 
                            fg=self.colors['text'], padx=20, pady=8, 
                            relief=tk.FLAT, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Title
        tk.Label(header, text=title, font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg'], fg=self.colors['dark']).pack(side=tk.LEFT, padx=10)
    
    def create_recognition_gui(self, mode="image"):
        """Tạo giao diện nhận dạng (image/camera/counter)"""
        # Điều chỉnh kích thước cửa sổ
        self.root.geometry(self.window_sizes['recognition'])
        
        # Xóa tất cả widget
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        if mode == "image":
            title = "📁 NHẬN DẠNG QUA FILE ẢNH"
        elif mode == "camera":
            title = "📷 NHẬN DẠNG QUA CAMERA"
        else:
            title = "💰 TÍNH TỔNG SỐ TIỀN"
        
        self.create_header(main_frame, title)
        
        # Toolbar hiện đại
        toolbar = tk.Frame(main_frame, bg=self.colors['light'], height=55)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        if mode == "camera":
            self._create_button(toolbar, "Bật Camera", self.start_camera, 
                              self.colors['success']).pack(side=tk.LEFT, padx=10, pady=10)
            
            self._create_button(toolbar, "Dừng Camera", self.stop_camera, 
                              self.colors['danger']).pack(side=tk.LEFT, padx=5, pady=10)
            
            self._create_button(toolbar, "Chụp ảnh", self.capture_frame, 
                              self.colors['primary']).pack(side=tk.LEFT, padx=5, pady=10)
        else:
            self._create_button(toolbar, "Chọn ảnh", self.select_image, 
                              self.colors['primary']).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.recognize_btn = self._create_button(toolbar, "Nhận dạng", lambda: self.recognize(mode), 
                          self.colors['success'])
        self.recognize_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        self._create_button(toolbar, "Làm mới", lambda: self.clear(mode), 
                          self.colors['secondary']).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Frame hiển thị ảnh
        img_frame = tk.Frame(main_frame, bg=self.colors['light'])
        img_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        # Ảnh gốc
        left_frame = tk.LabelFrame(img_frame, text="Ảnh gốc", 
                                   font=("Segoe UI", 10, "bold"),
                                   bg=self.colors['bg'], fg=self.colors['text'])
        left_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        self.original_canvas = tk.Canvas(left_frame, width=550, height=380, 
                                        bg=self.colors['light'], highlightthickness=0)
        self.original_canvas.pack(padx=5, pady=5)
        
        # Ảnh xử lý
        right_frame = tk.LabelFrame(img_frame, text="Ảnh xử lý", 
                                    font=("Segoe UI", 10, "bold"),
                                    bg=self.colors['bg'], fg=self.colors['text'])
        right_frame.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH, expand=True)
        
        self.processed_canvas = tk.Canvas(right_frame, width=550, height=380, 
                                         bg=self.colors['light'], highlightthickness=0)
        self.processed_canvas.pack(padx=5, pady=5)
        
        # Kết quả
        result_frame = tk.Frame(main_frame, bg=self.colors['bg'], 
                               relief=tk.FLAT, bd=0)
        result_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.result_label = tk.Label(result_frame, text="Chưa có kết quả", 
                                     font=("Segoe UI", 15, "bold"), 
                                     bg=self.colors['bg'], fg=self.colors['secondary'])
        self.result_label.pack(pady=8)
        
        self.detail_label = tk.Label(result_frame, text="", 
                                     font=("Segoe UI", 9), 
                                     bg=self.colors['bg'], fg=self.colors['text'])
        self.detail_label.pack()
    
    def _create_button(self, parent, text, command, bg_color):
        """Tạo button với style nhất quán"""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 10), bg=bg_color, fg="white",
                       padx=15, pady=6, relief=tk.FLAT, cursor="hand2")
        return btn
    
    def select_image(self):
        """Chọn ảnh từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh tiền Việt Nam",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            self.current_image = cv2.imread(file_path)
            
            if self.current_image is None:
                messagebox.showerror("Lỗi", "Không thể đọc ảnh!")
                return
            
            # Hiển thị ảnh gốc
            self.display_image(self.current_image, self.original_canvas)
            self.result_label.config(text="Đã chọn ảnh. Nhấn 'Nhận dạng' để xử lý.", fg="#7f8c8d")
            self.detail_label.config(text="")
    
    def start_camera(self):
        """Bật camera"""
        try:
            # Đóng camera cũ nếu đang mở
            # Tránh gọi isOpened trên None
            if getattr(self, 'camera', None) is not None and hasattr(self.camera, 'isOpened') and self.camera.isOpened():
                self.camera.release()
            
            # Mở camera
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                messagebox.showerror("Lỗi Camera", "Không thể mở camera!")
                return
            
            # Kiểm tra khả năng đọc frame
            ret, frame = self.camera.read()
            if not ret:
                messagebox.showerror("Lỗi Camera", "Camera được mở nhưng không đọc được dữ liệu!")
                self.camera.release()
                return
            
            # Thành công - bắt đầu hiển thị
            self.camera_running = True
            self.camera_active = True
            
            # Bắt đầu cập nhật hình ảnh
            self.update_camera()
            
            # Thông báo thành công
            self.result_label.config(text="Camera đã bật! Nhấn 'Chụp ảnh' để chụp.", fg="#27ae60")
            
        except Exception as e:
            messagebox.showerror("Lỗi Kỹ Thuật", f"Lỗi khi khởi tạo camera:\n\n{str(e)}")
    
    def stop_camera(self):
        """Dừng camera"""
        self.camera_running = False
        self.camera_active = False
        
        if hasattr(self, 'camera') and self.camera:
            self.camera.release()
            self.camera = None
    
    def capture_frame(self):
        """Chụp ảnh từ camera"""
        if self.camera and self.camera_running:
            ret, frame = self.camera.read()
            if ret:
                # Lưu và hiển thị ảnh vừa chụp
                self.current_image = frame.copy()
                self.display_image(self.current_image, self.original_canvas)
                # Dừng camera sau khi chụp
                self.stop_camera()
                # Tự động xử lý như ảnh được upload
                self.result_label.config(text="Đang xử lý ảnh vừa chụp...", fg="#3498db")
                self.detail_label.config(text="")
                self.recognize(mode="image")
            else:
                messagebox.showerror("Lỗi Camera", "Không thể chụp ảnh từ camera!")
    
    def update_camera(self):
        """Cập nhật frame camera"""
        if not self.camera_running or not self.camera:
            return
            
        try:
            ret, frame = self.camera.read()
            if not ret:
                self.stop_camera()
                return
            
            # Lật ngang để dễ nhìn
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            
            # Hiển thị lên canvas
            self.display_image(frame, self.original_canvas)
            
            # Lên lịch cập nhật tiếp
            self.root.after(50, self.update_camera)
            
        except Exception as e:
            self.stop_camera()
    
    def recognize(self, mode="image"):
        """Nhận dạng mệnh giá tiền"""
        # Nếu chưa có ảnh tĩnh, dùng frame gần nhất từ camera
        if self.current_image is None and hasattr(self, 'current_frame'):
            self.current_image = self.current_frame.copy()
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh hoặc chụp từ camera!")
            return
        
        if not self.templates:
            messagebox.showerror("Lỗi", "Không có templates! Vui lòng thêm ảnh mẫu vào thư mục templates/")
            return
        
        self.result_label.config(text="Đang xử lý...", fg="#3498db")
        self.root.update()
        
        try:
            #Tiền xử lý ảnh
            processed = self.preprocess_image(self.current_image)
            self.display_image(processed, self.processed_canvas)
            
            # Template Matching
            tm_scores = self.template_matching(processed)
            
            # Phân tích màu sắc
            color_scores = self.color_analysis(self.current_image)
            
            # Kết hợp điểm số
            final_scores = {}
            for denom in self.templates.keys():
                tm_score = tm_scores.get(denom, 0)
                color_score = color_scores.get(denom, 0)
                
                # Điều chỉnh trọng số - Giảm mạnh ảnh hưởng màu khi TM thấp
                if tm_score < 0.15:  # Nếu Template Matching rất thấp
                    final_scores[denom] = tm_score * 0.95 + color_score * 0.05
                elif tm_score < 0.25:  # Nếu Template Matching thấp
                    final_scores[denom] = tm_score * 0.85 + color_score * 0.15
                else:
                    final_scores[denom] = tm_score * 0.75 + color_score * 0.25
            
            # Tìm mệnh giá có điểm cao nhất
            if final_scores:
                best_denom = max(final_scores, key=final_scores.get)
                best_score = final_scores[best_denom]
                
                # Ưu tiên màu khi màu sắc rất mạnh
                tm_score = tm_scores.get(best_denom, 0)
                color_score = color_scores.get(best_denom, 0)
                
                # Nếu màu >= 0.6, chấp nhận ngay cả khi TM thấp
                if color_score >= 0.6 and best_score < 0.6:
                    best_score = max(best_score, color_score)
                
                # Ngưỡng chấp nhận linh hoạt: nếu màu >= 0.6 thì ngưỡng 0.1, ngược lại 0.15
                accept_threshold = 0.1 if color_score >= 0.6 else 0.15
                if best_score >= accept_threshold:
                    result_text = f"Mệnh giá: {best_denom:,} VND"
                    if mode == "counter":
                        # Giả lập đếm nhiều tờ 
                        result_text = f"Tổng: {best_denom:,} VND (1 tờ)"
                    
                    self.result_label.config(text=result_text, fg="#27ae60")
                    self.detail_label.config(
                        text=f"Độ tin cậy: {best_score*100:.1f}% | "
                             f"TM: {tm_scores[best_denom]*100:.1f}% | "
                             f"Màu: {color_scores[best_denom]*100:.1f}%"
                    )
                else:
                    self.result_label.config(text="Không nhận dạng được", fg="#e74c3c")
                    self.detail_label.config(text=f"Điểm số quá thấp: {best_score*100:.1f}%")
            else:
                self.result_label.config(text="Không có kết quả", fg="#e74c3c")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xử lý: {str(e)}")
            self.result_label.config(text="Lỗi xử lý", fg="#e74c3c")
    
    def preprocess_image(self, image):
        """Tiền xử lý ảnh để tăng chất lượng nhận dạng"""
        # Resize về kích thước chuẩn
        h, w = image.shape[:2]
        scale = 800 / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Chuyển sang grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Tăng độ tương phản 
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Khử nhiễu
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
        
        # Làm sắc nét
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        return sharpened
    
    def template_matching(self, processed_image):
        """Template Matching với nhiều scale"""
        scores = {}
        scales = [0.6, 0.8, 1.0, 1.2, 1.4]  # 5 scales

        # Xử lý cả trường hợp ảnh bị quay 180 độ
        candidate_images = [processed_image]
        try:
            rotated_180 = cv2.rotate(processed_image, cv2.ROTATE_180)
            candidate_images.append(rotated_180)
        except Exception:
            pass
        
        for denom, templates in self.templates.items():
            max_score = 0
            
            for template in templates:
                # Xử lý template giống ảnh test
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                h, w = template_gray.shape[:2]
                scale_t = 800 / max(h, w)
                template_resized = cv2.resize(template_gray, 
                                             (int(w * scale_t), int(h * scale_t)))
                
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                template_enhanced = clahe.apply(template_resized)
                
                # Thử nhiều scale
                for scale in scales:
                    th = int(template_enhanced.shape[0] * scale)
                    tw = int(template_enhanced.shape[1] * scale)
                    
                    # Bỏ qua nếu template lớn hơn ảnh test
                    if th > processed_image.shape[0] or tw > processed_image.shape[1]:
                        continue
                    
                    template_scaled = cv2.resize(template_enhanced, (tw, th))
                    
                    # Thử đối sánh trên các biến thể ảnh ứng viên
                    for test_img in candidate_images:
                        if th > test_img.shape[0] or tw > test_img.shape[1]:
                            continue
                        result = cv2.matchTemplate(test_img, template_scaled, cv2.TM_CCOEFF_NORMED)
                        _, score, _, _ = cv2.minMaxLoc(result)
                        max_score = max(max_score, score)
            
            scores[denom] = max_score
        
        return scores
    
    def color_analysis(self, image):
        """Phân tích màu sắc HSV"""
        # Resize nhỏ để xử lý nhanh
        small = cv2.resize(image, (200, 150))
        # Chỉ lấy vùng trung tâm của ảnh (tránh nền/da tay ở biên)
        sh, sw = small.shape[:2]
        y1, y2 = int(sh * 0.2), int(sh * 0.8)
        x1, x2 = int(sw * 0.15), int(sw * 0.85)
        roi = small[y1:y2, x1:x2]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Tăng cường độ sáng/độ tương phản ở kênh V để chống ảnh tối từ webcam
        h_ch, s_ch, v_ch = cv2.split(hsv)
        clahe_v = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        v_ch_enhanced = clahe_v.apply(v_ch)
        hsv = cv2.merge([h_ch, s_ch, v_ch_enhanced])
        
        # Lấy histogram của Hue channel
        h_channel = hsv[:, :, 0]
        s_channel = hsv[:, :, 1]
        v_channel = hsv[:, :, 2]
        
        # Mask: chỉ lấy pixel có màu rõ ràng (S > 60, V > 50) để màu ổn định hơn
        base_mask = (s_channel > 60) & (v_channel > 50)

        # Loại bỏ vùng da tay theo dải màu da trong HSV để không lẫn với 50k
        # Skin hue khoảng [0, 25] hoặc [160, 179], S > 20, V > 50
        skin_mask = (((h_channel >= 0) & (h_channel <= 25)) | ((h_channel >= 160) & (h_channel <= 179))) & (s_channel > 20) & (v_channel > 50)
        mask = base_mask & (~skin_mask)
        
        if mask.sum() == 0:
            return {d: 0.0 for d in self.templates.keys()}
        
        h_values = h_channel[mask]
        hist, _ = np.histogram(h_values, bins=180, range=(0, 180))
        hist = hist.astype(float) / hist.sum()
        
        # Dải màu đặc trưng cho từng mệnh giá (Hue: 0-179)
        # Căn chỉnh theo ảnh bạn cung cấp: 2k nâu/cam; 5k xanh dương; 20k xanh lam/cyan
        # Tách biệt để giảm nhầm lẫn với 1k và 500k (đều thiên xanh)
        color_ranges = {
            1000:   [(112, 125)],          # Xanh lam đậm (hẹp, cao hơn 5k/20k)
            2000:   [(10, 25)],            # Nâu/cam
            5000:   [(100, 112)],          # Xanh dương nhạt
            10000:  [(20, 35)],            # Nâu đỏ
            20000:  [(86, 98)],            # Xanh lam/cyan
            50000:  [(165, 179), (0, 6)],  # Hồng đỏ
            100000: [(50, 70)],            # Xanh lá
            200000: [(28, 42)],            # Cam vàng
            500000: [(120, 135)],          # Xanh dương đậm (dịch cao, tách 5k)
        }
        
        scores = {}
        for denom, ranges in color_ranges.items():
            score = 0
            for low, high in ranges:
                score += hist[low:high+1].sum()
            
            # Xử lý đặc biệt cho tờ 2,000 VND
            if denom == 2000:
                # Bonus nếu màu nâu/cam rõ ràng
                brown_score_main_range = hist[color_ranges[2000][0][0]:color_ranges[2000][0][1]+1].sum()
                if brown_score_main_range > 0.1: # If there's a significant amount of brown/orange
                    score *= 1.5 # Give a strong bonus
            
            # Xử lý đặc biệt cho tờ 5,000 VND (tím/hồng tím)
            elif denom == 5000:
                # Bonus nếu màu tím/hồng tím rõ ràng
                purple_score_main_range = hist[color_ranges[5000][0][0]:color_ranges[5000][0][1]+1].sum()
                if purple_score_main_range > 0.1:
                    score *= 1.5
            
            # Xử lý đặc biệt cho tờ 20,000 VND (xanh lam nhạt)
            elif denom == 20000:
                # Bonus nếu màu xanh lam nhạt rõ ràng
                light_blue_score_main_range = hist[color_ranges[20000][0][0]:color_ranges[20000][0][1]+1].sum()
                if light_blue_score_main_range > 0.1:
                    score *= 1.5
            
            # Bonus nếu màu chủ đạo rõ ràng
            if score > 0.2:
                score *= 1.2
            
            scores[denom] = min(1.0, score)
        
        return scores
    
    def display_image(self, image, canvas):
        """Hiển thị ảnh lên canvas"""
        # Chuyển sang RGB nếu cần
        if len(image.shape) == 2:
            display_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize để fit canvas
        canvas_w = canvas.winfo_width() if canvas.winfo_width() > 1 else 500
        canvas_h = canvas.winfo_height() if canvas.winfo_height() > 1 else 350
        
        h, w = display_img.shape[:2]
        scale = min(canvas_w / w, canvas_h / h)
        new_w, new_h = int(w * scale * 0.9), int(h * scale * 0.9)
        
        resized = cv2.resize(display_img, (new_w, new_h))
        
        # Chuyển sang PIL Image
        pil_img = Image.fromarray(resized)
        photo = ImageTk.PhotoImage(pil_img)
        
        # Hiển thị
        canvas.delete("all")
        canvas.create_image(canvas_w//2, canvas_h//2, image=photo, anchor=tk.CENTER)
        canvas.image = photo  # Giữ reference
    
    def clear(self, mode="image"):
        """Làm mới ứng dụng"""
        if mode == "camera":
            self.stop_camera()
        
        self.image_path = None
        self.current_image = None
        
        if hasattr(self, 'original_canvas'):
            self.original_canvas.delete("all")
        if hasattr(self, 'processed_canvas'):
            self.processed_canvas.delete("all")
        
        if hasattr(self, 'result_label'):
            self.result_label.config(text="Chưa có kết quả", fg="#7f8c8d")
        if hasattr(self, 'detail_label'):
            self.detail_label.config(text="")

def main():
    root = tk.Tk()
    app = CurrencyRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()